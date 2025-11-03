#!/usr/bin/env python3
"""
Flask API Autograder - Modular testing for different API versions.

This script tests Flask API endpoints and validates responses.
It assumes the Flask server is already running (typically via part_X_build_run.sh).

Usage:
    python flask_autograder.py --api v1 --key YOUR_KEY
    python flask_autograder.py --api v1 --api v2 --url http://localhost:5000
"""

import argparse
import logging
import os
import sys
import time
import warnings

import requests
from jsonschema import Draft7Validator

# Suppress urllib3 header parsing warnings (they're noisy and we handle the responses fine)
warnings.filterwarnings('ignore', message='.*Failed to parse headers.*')
warnings.filterwarnings('ignore', module='urllib3')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Suppress urllib3 connection/response warnings - they log header issues as WARNING
logging.getLogger("urllib3.connection").setLevel(logging.ERROR)
logging.getLogger("urllib3.connectionpool").setLevel(logging.ERROR)

# Track if we've seen header issues (to report once per test run)
_header_issues_detected = False

# Schema Definitions
API_SCHEMAS = {
    # Part 2 / v1 schemas
    "row_count": {
        "type": "object",
        "required": ["row_count"],
        "properties": {"row_count": {"type": "integer", "minimum": 0}},
        "additionalProperties": False,
    },
    "unique_nyse_stock_count": {
        "type": "object",
        "required": ["unique_nyse_stock_count"],
        "properties": {"unique_nyse_stock_count": {"type": "integer", "minimum": 0}},
        "additionalProperties": False,
    },
    "unique_nasdaq_stock_count": {
        "type": "object",
        "required": ["unique_nasdaq_stock_count"],
        "properties": {
            "unique_nasdaq_stock_count": {"type": "integer", "minimum": 0}
        },
        "additionalProperties": False,
    },
    # Part 3 / v2 schemas
    "v2_year_count": {
        "type": "object",
        "required": ["year", "count"],
        "properties": {
            "year": {"type": "integer", "minimum": 2010, "maximum": 2020},
            "count": {"type": "integer", "minimum": 0}
        },
        "additionalProperties": False,
    },
    "v2_open_price_info": {
        "type": "object",
        "required": ["symbol", "price_info"],
        "properties": {
            "symbol": {"type": "string", "minLength": 1},
            "price_info": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["date", "open"],
                    "properties": {
                        "date": {
                            "type": "string",
                            "pattern": r"^\d{4}-\d{2}-\d{2}$"
                        },
                        "open": {"type": "number"}
                    },
                    "additionalProperties": False
                }
            }
        },
        "additionalProperties": False,
    },
    "v2_close_price_info": {
        "type": "object",
        "required": ["symbol", "price_info"],
        "properties": {
            "symbol": {"type": "string", "minLength": 1},
            "price_info": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["date", "close"],
                    "properties": {
                        "date": {
                            "type": "string",
                            "pattern": r"^\d{4}-\d{2}-\d{2}$"
                        },
                        "close": {"type": "number"}
                    },
                    "additionalProperties": False
                }
            }
        },
        "additionalProperties": False,
    },
    "v2_high_price_info": {
        "type": "object",
        "required": ["symbol", "price_info"],
        "properties": {
            "symbol": {"type": "string", "minLength": 1},
            "price_info": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["date", "high"],
                    "properties": {
                        "date": {
                            "type": "string",
                            "pattern": r"^\d{4}-\d{2}-\d{2}$"
                        },
                        "high": {"type": "number"}
                    },
                    "additionalProperties": False
                }
            }
        },
        "additionalProperties": False,
    },
    "v2_low_price_info": {
        "type": "object",
        "required": ["symbol", "price_info"],
        "properties": {
            "symbol": {"type": "string", "minLength": 1},
            "price_info": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["date", "low"],
                    "properties": {
                        "date": {
                            "type": "string",
                            "pattern": r"^\d{4}-\d{2}-\d{2}$"
                        },
                        "low": {"type": "number"}
                    },
                    "additionalProperties": False
                }
            }
        },
        "additionalProperties": False,
    },
    "v2_high_low_price_info": {
        "type": "object",
        "required": ["symbol", "price_info"],
        "properties": {
            "symbol": {"type": "string", "minLength": 1},
            "price_info": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["date", "high_low"],
                    "properties": {
                        "date": {
                            "type": "string",
                            "pattern": r"^\d{4}-\d{2}-\d{2}$"
                        },
                        "high_low": {"type": "number"}
                    },
                    "additionalProperties": False
                }
            }
        },
        "additionalProperties": False,
    },
}


class FlaskAPITester:
    """Test harness for Flask API endpoints."""

    def __init__(
        self,
        base_url: str = "http://localhost:4000",
        api_key: str | None = None,
        json_output: bool = False,
    ):
        """
        Initialize the tester.

        Args:
            base_url: Base URL for the Flask application
            api_key: API key for authentication
            json_output: If True, output results as JSON instead of logs
        """
        self.base_url = base_url
        self.api_key = api_key
        self.json_output = json_output
        self.test_results = {"passed": 0, "failed": 0, "total": 0}
        self.endpoint_data = {}  # Store actual data returned from endpoints

    def make_request(
        self,
        endpoint: str,
        method: str = "GET",
        use_api_key: bool = True,
        custom_api_key: str | None = None,
        expected_status_codes: list[int] | None = None,
    ) -> tuple[dict | None, int, float]:
        """
        Make an HTTP request to the specified endpoint.

        Args:
            endpoint: API endpoint to call
            method: HTTP method (default: GET)
            use_api_key: Whether to include the API key in headers
            custom_api_key: Custom API key to use (overrides default)
            expected_status_codes: List of expected status codes

        Returns:
            Tuple of (response_data, status_code, elapsed_time_ms)
        """
        if expected_status_codes is None:
            expected_status_codes = [200]

        headers = {"Content-Type": "application/json"}

        if use_api_key:
            key = custom_api_key if custom_api_key else self.api_key
            if key:
                headers["DATA-241-API-KEY"] = key

        url = f"{self.base_url}{endpoint}"

        try:
            start_time = time.time()
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            else:
                logger.error(f"Unsupported HTTP method: {method}")
                return None, 500, 0.0
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds

            # Check for malformed headers (silently track for summary)
            global _header_issues_detected
            if not _header_issues_detected and hasattr(response, 'raw') and hasattr(response.raw, '_original_response'):
                raw_response = response.raw._original_response
                if hasattr(raw_response, 'msg') and hasattr(raw_response.msg, 'defects'):
                    if raw_response.msg.defects:
                        _header_issues_detected = True

            # Try to parse JSON response for successful requests
            if response.status_code in [200, 201]:
                try:
                    return response.json(), response.status_code, elapsed_time
                except ValueError:
                    logger.debug(f"Response is not valid JSON: {response.text[:100]}")
                    return None, response.status_code, elapsed_time

            return None, response.status_code, elapsed_time

        except requests.exceptions.ConnectionError:
            logger.error(
                f"Connection error: Could not connect to {self.base_url}. "
                "Is the Flask server running?"
            )
            return None, 503, 0.0
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout for {url}")
            return None, 504, 0.0
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None, 500, 0.0

    def validate_response(
        self, data: dict, schema: dict
    ) -> tuple[bool, list[str]]:
        """
        Validate response data against a JSON schema.

        Args:
            data: Response data to validate
            schema: JSON schema to validate against

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        validator = Draft7Validator(schema)
        errors = list(validator.iter_errors(data))

        if not errors:
            return True, []

        # Collect unique error messages
        unique_errors = set()
        for error in errors:
            # Create path string for context
            path_parts = [str(p) for p in error.path if not str(p).isdigit()]
            base_path = ".".join(path_parts) if path_parts else "root"
            error_msg = f"{base_path}: {error.message}"
            unique_errors.add(error_msg)

        # Limit to 5 errors for readability
        error_list = sorted(unique_errors)
        if len(error_list) > 5:
            error_list = error_list[:5]
            error_list.append("... (additional errors omitted)")

        return False, error_list

    def test_endpoint(
        self,
        endpoint: str,
        schema: dict | None = None,
        use_api_key: bool = True,
        custom_api_key: str | None = None,
        expected_status_codes: list[int] | None = None,
        test_name: str = "",
        endpoint_key: str | None = None,
    ) -> tuple[bool, dict | None]:
        """
        Test a single endpoint.

        Args:
            endpoint: API endpoint to test
            schema: JSON schema for validation (optional)
            use_api_key: Whether to include API key
            custom_api_key: Custom API key for testing
            expected_status_codes: Expected HTTP status codes
            test_name: Name/description of the test
            endpoint_key: Key to store endpoint data under (for summary reporting)

        Returns:
            Tuple of (success, response_data)
        """
        if expected_status_codes is None:
            expected_status_codes = [200]

        self.test_results["total"] += 1
        display_name = test_name or f"GET {endpoint}"

        if not self.json_output:
            logger.info(f"Testing: {display_name}")

        data, status_code, elapsed_time = self.make_request(
            endpoint,
            use_api_key=use_api_key,
            custom_api_key=custom_api_key,
            expected_status_codes=expected_status_codes,
        )

        # Check status code
        if status_code not in expected_status_codes:
            if not self.json_output:
                logger.error(
                    f"✗ FAILED: {display_name} - "
                    f"Expected status {expected_status_codes}, got {status_code} ({elapsed_time:.0f}ms)"
                )
            self.test_results["failed"] += 1
            return False, data

        # If we only care about status code, return success
        if status_code != 200 or schema is None:
            if not self.json_output:
                logger.info(
                    f"✓ PASSED: {display_name} - Status {status_code} ({elapsed_time:.0f}ms)"
                )
            self.test_results["passed"] += 1
            return True, data

        # Validate response schema
        if data is None:
            if not self.json_output:
                logger.error(f"✗ FAILED: {display_name} - No response data received ({elapsed_time:.0f}ms)")
            self.test_results["failed"] += 1
            return False, None

        is_valid, errors = self.validate_response(data, schema)

        if not is_valid:
            if not self.json_output:
                logger.error(f"✗ FAILED: {display_name} - Schema validation errors ({elapsed_time:.0f}ms):")
                for error in errors:
                    logger.error(f"  - {error}")
            self.test_results["failed"] += 1
            return False, data

        # Success! Store data if endpoint_key provided
        if endpoint_key and data:
            self.endpoint_data[endpoint_key] = data

        if not self.json_output:
            # Truncate long responses to first 60 characters
            data_str = str(data)
            if len(data_str) > 60:
                data_str = data_str[:60] + "..."
            logger.info(f"✓ PASSED: {display_name} - {data_str} ({elapsed_time:.0f}ms)")
        self.test_results["passed"] += 1
        return True, data

    def run_v1_tests(self) -> bool:
        """
        Run v1 API endpoint tests (Part 2).

        Tests:
        - /api/v1/row_count (with valid API key)
        - /api/v1/unique_nyse_stock_count (with valid API key)
        - /api/v1/unique_nasdaq_stock_count (with valid API key)
        - Authentication on row_count (401 for missing/invalid keys)
        - Authentication on NYSE endpoint (401 for missing key)
        - Authentication on NASDAQ endpoint (401 for missing key)

        Returns:
            True if all tests passed, False otherwise
        """
        if not self.json_output:
            logger.info("=" * 70)
            logger.info("RUNNING V1 API TESTS (Part 2)")
            logger.info("=" * 70)

        all_passed = True

        # Test 1: row_count endpoint
        if not self.json_output:
            logger.info("\n--- Testing /api/v1/row_count ---")
        success, _ = self.test_endpoint(
            "/api/v1/row_count",
            schema=API_SCHEMAS["row_count"],
            test_name="Row count with valid API key",
            endpoint_key="row_count",
        )
        all_passed = all_passed and success

        # Test 2: unique_nyse_stock_count endpoint
        if not self.json_output:
            logger.info("\n--- Testing /api/v1/unique_nyse_stock_count ---")
        success, _ = self.test_endpoint(
            "/api/v1/unique_nyse_stock_count",
            schema=API_SCHEMAS["unique_nyse_stock_count"],
            test_name="NYSE unique stock count with valid API key",
            endpoint_key="unique_nyse_stock_count",
        )
        all_passed = all_passed and success

        # Test 3: unique_nasdaq_stock_count endpoint
        if not self.json_output:
            logger.info("\n--- Testing /api/v1/unique_nasdaq_stock_count ---")
        success, _ = self.test_endpoint(
            "/api/v1/unique_nasdaq_stock_count",
            schema=API_SCHEMAS["unique_nasdaq_stock_count"],
            test_name="NASDAQ unique stock count with valid API key",
            endpoint_key="unique_nasdaq_stock_count",
        )
        all_passed = all_passed and success

        # Test 4: Authentication - missing API key on row_count
        if not self.json_output:
            logger.info("\n--- Testing authentication (missing API key) ---")
        success, _ = self.test_endpoint(
            "/api/v1/row_count",
            use_api_key=False,
            expected_status_codes=[401],
            test_name="Row count without API key (should return 401)",
        )
        all_passed = all_passed and success

        # Test 5: Authentication - invalid API key on row_count
        if not self.json_output:
            logger.info("\n--- Testing authentication (invalid API key) ---")
        success, _ = self.test_endpoint(
            "/api/v1/row_count",
            custom_api_key="INVALID_KEY_12345",
            expected_status_codes=[401],
            test_name="Row count with invalid API key (should return 401)",
        )
        all_passed = all_passed and success

        # Test 6: Authentication - missing API key on NYSE endpoint
        success, _ = self.test_endpoint(
            "/api/v1/unique_nyse_stock_count",
            use_api_key=False,
            expected_status_codes=[401],
            test_name="NYSE count without API key (should return 401)",
        )
        all_passed = all_passed and success

        # Test 7: Authentication - missing API key on NASDAQ endpoint
        success, _ = self.test_endpoint(
            "/api/v1/unique_nasdaq_stock_count",
            use_api_key=False,
            expected_status_codes=[401],
            test_name="NASDAQ count without API key (should return 401)",
        )
        all_passed = all_passed and success

        return all_passed

    def run_v2_tests(self) -> bool:
        """
        Run v2 API endpoint tests (Part 3).

        Tests:
        - /api/v2/{YEAR} for multiple valid years (2010, 2015, 2019, 2020)
        - /api/v2/{YEAR} for multiple invalid years (2009, 2021, 1980, 2025)
        - /api/v2/open/{SYMBOL} with valid symbol
        - /api/v2/close/{SYMBOL} with valid symbol
        - /api/v2/high/{SYMBOL} with valid symbol
        - /api/v2/low/{SYMBOL} with valid symbol
        - /api/v2/high_low/{SYMBOL} with valid symbol
        - Invalid symbol tests (404)
        - Authentication tests (401 for missing/invalid keys)

        Returns:
            True if all tests passed, False otherwise
        """
        if not self.json_output:
            logger.info("=" * 70)
            logger.info("RUNNING V2 API TESTS (Part 3)")
            logger.info("=" * 70)

        all_passed = True
        
        # Valid years to test (2010-2020)
        valid_years = [2010, 2015, 2019, 2020]  # Start, middle, recent, end
        # Invalid years to test
        invalid_years = [2009, 2021, 1980, 2025]  # Before range, after range, far before, far after
        
        # Test symbols - try common ones that should exist in the data
        test_symbols = ["AAPL", "IBM", "MSFT"]  # Common stocks likely in data
        
        # Test 1-4: /api/v2/{YEAR} with multiple valid years
        if not self.json_output:
            logger.info("\n--- Testing /api/v2/{YEAR} with valid years ---")
        for year in valid_years:
            success, data = self.test_endpoint(
                f"/api/v2/{year}",
                schema=API_SCHEMAS["v2_year_count"],
                test_name=f"Year count for {year} with valid API key",
                endpoint_key=f"v2_year_{year}",
            )
            all_passed = all_passed and success
            
            # Verify year matches what was requested
            if success and data and data.get("year") != year:
                if not self.json_output:
                    logger.error(
                        f"✗ FAILED: Year mismatch for /api/v2/{year} - "
                        f"expected {year}, got {data.get('year')}"
                    )
                all_passed = False
        
        # Test 5-8: /api/v2/{YEAR} with multiple invalid years (should return 404)
        if not self.json_output:
            logger.info("\n--- Testing /api/v2/{YEAR} with invalid years ---")
        for year in invalid_years:
            success, _ = self.test_endpoint(
                f"/api/v2/{year}",
                expected_status_codes=[404],
                test_name=f"Year count for invalid year {year} (should return 404)",
            )
            all_passed = all_passed and success
        
        # Test 9-13: Price endpoints for valid symbols
        price_endpoints = [
            ("open", "v2_open_price_info", "Open prices"),
            ("close", "v2_close_price_info", "Close prices"),
            ("high", "v2_high_price_info", "High prices"),
            ("low", "v2_low_price_info", "Low prices"),
            ("high_low", "v2_high_low_price_info", "High-Low difference"),
        ]
        
        if not self.json_output:
            logger.info("\n--- Testing /api/v2/{TYPE}/{SYMBOL} endpoints ---")
        
        for price_type, schema_key, description in price_endpoints:
            # Try each test symbol until one works
            symbol_tested = None
            for symbol in test_symbols:
                if not self.json_output:
                    logger.info(f"  Testing /api/v2/{price_type}/{symbol}...")
                
                success, data = self.test_endpoint(
                    f"/api/v2/{price_type}/{symbol}",
                    schema=API_SCHEMAS[schema_key],
                    test_name=f"{description} for {symbol} with valid API key",
                    endpoint_key=f"v2_{price_type}_{symbol}",
                )
                
                if success:
                    symbol_tested = symbol
                    # Verify symbol matches and price_info is non-empty
                    if data:
                        if data.get("symbol") != symbol:
                            if not self.json_output:
                                logger.error(
                                    f"✗ FAILED: Symbol mismatch for /api/v2/{price_type}/{symbol} - "
                                    f"expected {symbol}, got {data.get('symbol')}"
                                )
                            all_passed = False
                        elif not data.get("price_info") or len(data.get("price_info", [])) == 0:
                            if not self.json_output:
                                logger.warning(
                                    f"⚠ WARNING: Empty price_info for /api/v2/{price_type}/{symbol}"
                                )
                    break  # Found a working symbol, move to next endpoint type
            
            if symbol_tested:
                all_passed = all_passed and True
            else:
                # None of the test symbols worked - this is a failure
                if not self.json_output:
                    logger.error(
                        f"✗ FAILED: None of the test symbols ({test_symbols}) "
                        f"worked for /api/v2/{price_type}/ endpoint"
                    )
                all_passed = False
        
        # Test 14: Invalid symbol (should return 404)
        if not self.json_output:
            logger.info("\n--- Testing /api/v2/open/{SYMBOL} with invalid symbol ---")
        success, _ = self.test_endpoint(
            "/api/v2/open/INVALID_SYMBOL_XYZ123",
            expected_status_codes=[404],
            test_name="Open prices for invalid symbol (should return 404)",
        )
        all_passed = all_passed and success
        
        # Test 15: Authentication - missing API key on /api/v2/{YEAR}
        if not self.json_output:
            logger.info("\n--- Testing v2 authentication (missing API key) ---")
        success, _ = self.test_endpoint(
            f"/api/v2/{valid_years[0]}",
            use_api_key=False,
            expected_status_codes=[401],
            test_name="Year count without API key (should return 401)",
        )
        all_passed = all_passed and success
        
        # Test 16: Authentication - invalid API key on /api/v2/{YEAR}
        success, _ = self.test_endpoint(
            f"/api/v2/{valid_years[0]}",
            custom_api_key="INVALID_KEY_12345",
            expected_status_codes=[401],
            test_name="Year count with invalid API key (should return 401)",
        )
        all_passed = all_passed and success
        
        # Test 17: Authentication - missing API key on price endpoint
        # Use the first symbol that worked, or just use the first test symbol
        test_symbol = test_symbols[0]
        success, _ = self.test_endpoint(
            f"/api/v2/open/{test_symbol}",
            use_api_key=False,
            expected_status_codes=[401],
            test_name="Open prices without API key (should return 401)",
        )
        all_passed = all_passed and success
        
        # Test 18: Authentication - invalid API key on price endpoint
        success, _ = self.test_endpoint(
            f"/api/v2/open/{test_symbol}",
            custom_api_key="INVALID_KEY_12345",
            expected_status_codes=[401],
            test_name="Open prices with invalid API key (should return 401)",
        )
        all_passed = all_passed and success

        return all_passed

    def run_v3_tests(self) -> bool:
        """
        Run v3 API endpoint tests.

        Placeholder for future implementation.

        Returns:
            True (placeholder)
        """
        logger.info("=" * 70)
        logger.info("RUNNING V3 API TESTS")
        logger.info("=" * 70)
        logger.warning("V3 tests not yet implemented")
        return True

    def run_tests(self, apis_to_test: list[str]) -> bool:
        """
        Run selected API tests.

        Args:
            apis_to_test: List of API versions to test (e.g., ['v1', 'v2'])

        Returns:
            True if all tests passed, False otherwise
        """
        if not self.json_output:
            logger.info(f"Testing APIs: {', '.join(apis_to_test)}")
            logger.info(f"Base URL: {self.base_url}")
            logger.info(f"API Key: {'Set' if self.api_key else 'Not Set'}\n")

        all_passed = True

        if "v1" in apis_to_test:
            all_passed = self.run_v1_tests() and all_passed

        if "v2" in apis_to_test:
            all_passed = self.run_v2_tests() and all_passed

        if "v3" in apis_to_test:
            all_passed = self.run_v3_tests() and all_passed

        # Print summary
        self.print_summary()

        return all_passed

    def print_summary(self) -> None:
        """Print a summary of test results."""
        global _header_issues_detected
        
        total = self.test_results["total"]
        passed = self.test_results["passed"]
        failed = self.test_results["failed"]

        if self.json_output:
            # Output JSON format for parsing by other scripts
            import json
            result = {
                "total_tests": total,
                "passed": passed,
                "failed": failed,
                "all_passed": failed == 0 and total > 0,
                "header_issues": _header_issues_detected,
                "endpoint_data": self.endpoint_data,
            }
            print(json.dumps(result, indent=2))
            return

        logger.info("\n" + "=" * 70)
        logger.info("TEST SUMMARY")
        logger.info("=" * 70)
        logger.info(f"Total tests: {total}")
        logger.info(f"Passed: {passed}")
        logger.info(f"Failed: {failed}")
        
        # Report header issues if detected
        if _header_issues_detected:
            logger.info("\n⚠ CODE QUALITY ISSUE:")
            logger.info("  HTTP response headers are malformed (likely 'Content Type' instead of 'Content-Type')")
            logger.info("  This violates HTTP standards but responses were processed successfully")

        if failed == 0 and total > 0:
            logger.info("\n✓ ALL TESTS PASSED!")
        elif total > 0:
            logger.warning(f"\n✗ {failed} TEST(S) FAILED")
        else:
            logger.info("\nNo tests were run")


def main():
    """Main entry point for the autograder."""
    parser = argparse.ArgumentParser(
        description="Flask API Autograder - Test Flask endpoints",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test v1 endpoints (Part 2)
  python flask_autograder.py --api v1

  # Test multiple API versions
  python flask_autograder.py --api v1 --api v2

  # Use custom URL and API key
  python flask_autograder.py --api v1 --url http://localhost:5000 --key my_key

  # Enable debug logging
  python flask_autograder.py --api v1 --debug
        """,
    )

    parser.add_argument(
        "--url",
        default="http://localhost:4000",
        help="Base URL for the Flask application (default: http://localhost:4000)",
    )

    parser.add_argument(
        "--key",
        default=None,
        help="API key for authentication (default: read from DATA_241_API_KEY env var)",
    )

    parser.add_argument(
        "--api",
        action="append",
        choices=["v1", "v2", "v3"],
        help="Specify which API version to test (can be used multiple times). "
        "Default: v1",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format (for script parsing)",
    )

    args = parser.parse_args()

    # Configure logging level
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)
    
    # If JSON output is requested, suppress all logging
    if args.json:
        logging.getLogger().setLevel(logging.CRITICAL)

    # Get API key
    api_key = args.key or os.environ.get("DATA_241_API_KEY")

    if not api_key:
        logger.error(
            "Error: API key not provided. Set DATA_241_API_KEY environment "
            "variable or use --key option"
        )
        sys.exit(1)

    # Determine which APIs to test
    test_apis = args.api if args.api else ["v1"]

    # Create tester and run tests
    tester = FlaskAPITester(base_url=args.url, api_key=api_key, json_output=args.json)

    try:
        all_passed = tester.run_tests(test_apis)

        # Exit with appropriate code
        sys.exit(0 if all_passed else 1)

    except KeyboardInterrupt:
        logger.warning("\nTests interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.exception(f"Unexpected error during testing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

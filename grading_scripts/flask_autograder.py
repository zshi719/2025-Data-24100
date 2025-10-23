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
    ) -> tuple[dict | None, int]:
        """
        Make an HTTP request to the specified endpoint.

        Args:
            endpoint: API endpoint to call
            method: HTTP method (default: GET)
            use_api_key: Whether to include the API key in headers
            custom_api_key: Custom API key to use (overrides default)
            expected_status_codes: List of expected status codes

        Returns:
            Tuple of (response_data, status_code)
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
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            else:
                logger.error(f"Unsupported HTTP method: {method}")
                return None, 500

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
                    return response.json(), response.status_code
                except ValueError:
                    logger.debug(f"Response is not valid JSON: {response.text[:100]}")
                    return None, response.status_code

            return None, response.status_code

        except requests.exceptions.ConnectionError:
            logger.error(
                f"Connection error: Could not connect to {self.base_url}. "
                "Is the Flask server running?"
            )
            return None, 503
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout for {url}")
            return None, 504
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None, 500

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

        data, status_code = self.make_request(
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
                    f"Expected status {expected_status_codes}, got {status_code}"
                )
            self.test_results["failed"] += 1
            return False, data

        # If we only care about status code, return success
        if status_code != 200 or schema is None:
            if not self.json_output:
                logger.info(
                    f"✓ PASSED: {display_name} - Status {status_code}"
                )
            self.test_results["passed"] += 1
            return True, data

        # Validate response schema
        if data is None:
            if not self.json_output:
                logger.error(f"✗ FAILED: {display_name} - No response data received")
            self.test_results["failed"] += 1
            return False, None

        is_valid, errors = self.validate_response(data, schema)

        if not is_valid:
            if not self.json_output:
                logger.error(f"✗ FAILED: {display_name} - Schema validation errors:")
                for error in errors:
                    logger.error(f"  - {error}")
            self.test_results["failed"] += 1
            return False, data

        # Success! Store data if endpoint_key provided
        if endpoint_key and data:
            self.endpoint_data[endpoint_key] = data
            
        if not self.json_output:
            logger.info(f"✓ PASSED: {display_name} - {data}")
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
        Run v2 API endpoint tests.

        Placeholder for future implementation.

        Returns:
            True (placeholder)
        """
        logger.info("=" * 70)
        logger.info("RUNNING V2 API TESTS")
        logger.info("=" * 70)
        logger.warning("V2 tests not yet implemented")
        return True

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

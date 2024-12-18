# ruff: noqa: D101 D100 D107
import os
import sys

import requests
from jsonschema import Draft7Validator

# Schema Definitions
API_SCHEMAS = {
    # v1 schemas
    "row_count": {
        "type": "object",
        "required": ["row_count"],
        "properties": {"row_count": {"type": "integer", "minimum": 0}},
        "additionalProperties": False,
    },
    "unique_stock_count": {
        "type": "object",
        "required": ["unique_stock_count"],
        "properties": {"unique_stock_count": {"type": "integer", "minimum": 0}},
        "additionalProperties": False,
    },
    "row_by_market_count": {
        "type": "object",
        "required": ["NASDAQ", "NYSE"],
        "properties": {
            "NASDAQ": {"type": "integer", "minimum": 0},
            "NYSE": {"type": "integer", "minimum": 0},
        },
        "additionalProperties": False,
    },
    # v3 schemas
    "account_creation": {
        "type": "object",
        "required": ["account_id"],
        "properties": {"account_id": {"type": "integer", "minimum": 1}},
        "additionalProperties": False,
    },
    "account_holdings": {
        "type": "object",
        "required": ["account_id", "name", "stock_holdings"],
        "properties": {
            "account_id": {"type": "integer", "minimum": 1},
            "name": {"type": "string"},
            "stock_holdings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "symbol",
                        "purchase_date",
                        "sale_date",
                        "number_of_shares",
                    ],
                    "properties": {
                        "symbol": {"type": "string"},
                        "purchase_date": {"type": "string", "format": "date"},
                        "sale_date": {"type": "string", "format": "date"},
                        "number_of_shares": {"type": "integer", "minimum": 1},
                    },
                },
            },
        },
    },
    "stock_list": {
        "type": "object",
        "required": ["symbol", "holdings"],
        "properties": {
            "symbol": {"type": "string"},
            "holdings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": [
                        "account_id",
                        "purchase_date",
                        "sale_date",
                        "number_of_shares",
                    ],
                    "properties": {
                        "account_id": {"type": "integer", "minimum": 1},
                        "purchase_date": {"type": "string", "format": "date"},
                        "sale_date": {"type": "string", "format": "date"},
                        "number_of_shares": {"type": "integer", "minimum": 1},
                    },
                },
            },
        },
    },
    "account_return": {
        "type": "object",
        "required": ["account_id", "return"],
        "properties": {
            "account_id": {"type": "integer", "minimum": 1},
            "return": {"type": "number"},
        },
    },
    "accounts_list": {
        "type": "array",
        "items": {
            "type": "object",
            "required": ["account_id", "name"],
            "properties": {
                "account_id": {"type": "integer", "minimum": 1},
                "name": {"type": "string"},
            },
        },
    },
    "back_test_response": {
        "type": "object",
        "required": ["return", "num_observations"],
        "properties": {
            "return": {"type": "number"},
            "num_observations": {"type": "integer", "minimum": 0},
        },
        "additionalProperties": False,
    },
}

YEAR_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["year", "count"],
    "properties": {
        "year": {"type": "integer", "minimum": 1900, "maximum": 2100},
        "count": {"type": "integer", "minimum": 0},
    },
    "additionalProperties": False,
}


def short_output(data):
    """Print only the first few characters of a JSON object"""
    data_str = str(data)
    return data_str[:150]


def create_price_schema(price_type: str) -> dict:
    """Create a schema for price-related endpoints."""
    return {
        "type": "object",
        "required": ["symbol", "price_info"],
        "properties": {
            "symbol": {"type": "string"},
            "price_info": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["date", price_type],
                    "properties": {
                        "date": {"type": "string", "format": "date"},
                        price_type: {"type": "number"},
                    },
                    "additionalProperties": False,
                },
            },
        },
        "additionalProperties": False,
    }


PRICE_SCHEMAS = {
    "open": create_price_schema("open"),
    "close": create_price_schema("close"),
    "high": create_price_schema("high"),
    "low": create_price_schema("low"),
}


class APITester:
    def __init__(
        self,
        base_url: str = "http://localhost:4000",
        api_key: str | None = None,
    ):
        self.base_url = base_url
        self.api_key = api_key

    def make_request(
        self,
        endpoint: str,
        method: str = "GET",
        data: dict | None = None,
        expected_status_codes: list[int] = [200],
    ) -> tuple[dict | None, int]:
        """Make an HTTP request to the specified endpoint."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["DATA-241-API-KEY"] = self.api_key

        try:
            # Make the request
            if method == "GET":
                response = requests.get(f"{self.base_url}{endpoint}", headers=headers)
            elif method == "POST":
                response = requests.post(
                    f"{self.base_url}{endpoint}", headers=headers, json=data
                )
            elif method == "DELETE":
                response = requests.delete(
                    f"{self.base_url}{endpoint}", headers=headers, json=data
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            print(f"Response status code: {response.status_code}")

            # Handle response
            if response.status_code in expected_status_codes:
                if response.status_code in [200, 201]:
                    try:
                        return (response.json(), response.status_code)
                    except ValueError as e:  # noqa 841
                        print(
                            "Warning: Response is not JSON decodable: "
                            f" {response.text}"
                        )
                        return (None, response.status_code)
                return (None, response.status_code)

            return (None, response.status_code)

        except requests.exceptions.RequestException as e:
            status_code = getattr(e.response, "status_code", 500)
            return (None, status_code)

    def validate_response(self, data: dict, schema: dict) -> tuple[bool, list[str]]:
        """Validate response data and collect unique errors."""
        validator = Draft7Validator(schema)
        errors = list(validator.iter_errors(data))

        if not errors:
            return True, []

        # Create a set to store unique error messages
        unique_errors = set()

        for error in errors:
            # Strip the array index from the path to identify similar errors
            path_parts = [p for p in error.path if not str(p).isdigit()]
            base_path = ".".join(str(p) for p in path_parts) if path_parts else ""

            # Create a unique error identifier combining the path and message
            if base_path:
                error_msg = f"{base_path}: {error.message}"
            else:
                error_msg = error.message

            unique_errors.add(error_msg)

        # Convert to list and limit to 5 errors
        error_list = sorted(unique_errors)
        if len(error_list) > 5:  # noqa PLR2004
            error_list = error_list[:5]
            error_list.append("... more errors found")

        return False, error_list

    def test_endpoint(
        self,
        endpoint: str,
        schema: dict | None = None,
        method: str = "GET",
        data: dict | None = None,
        expected_status_codes: list[int] = [200],
    ) -> tuple[dict | None, int]:
        """Generic endpoint testing method."""
        print(f"\nTesting {method} {endpoint}")
        data_response, status_code = self.make_request(
            endpoint,
            method=method,
            data=data,
            expected_status_codes=expected_status_codes,
        )

        if status_code not in expected_status_codes:
            print(f"✗ {method} {endpoint}: " f"Unexpected status code {status_code}")
            return

        if status_code in [200, 201] and schema:
            valid, errors = self.validate_response(data_response, schema)

            if errors:
                short_response = short_output(data_response)
                error_message = "; ".join(errors)
                print(f"✗ {method} {endpoint}: " f"{error_message}: {short_response}")
            else:
                short_response = short_output(data_response)
                print(f"✓ {method} {endpoint}: Success: {short_response}")
        else:
            print(f"✓ {method} {endpoint}: Status code {status_code}" " as expected")

        return data_response

    def run_tests(self, apis_to_test=["v1", "v2", "v3"]):
        """Run all API tests."""
        print("\nRunning comprehensive API tests...")
        if "v1" in apis_to_test:
            self.run_v1_tests()
        if "v2" in apis_to_test:
            self.run_v2_tests()
        if "v3" in apis_to_test:
            self.run_v3_tests()
        if "v4" in apis_to_test:
            self.run_v4_tests()
        if "iv" in apis_to_test:
            self.run_iv_api_tests()
        if "test_backtest_perfect_values" in apis_to_test:
            self.test_backtest_perfect_values()

    def run_v1_tests(self):
        """Run v1 API tests"""
        print("Running tests on api/v1")
        v1_endpoints = {
            "/api/v1/row_by_market_count": API_SCHEMAS["row_by_market_count"],
            "/api/v1/row_count": API_SCHEMAS["row_count"],
            "/api/v1/unique_stock_count": API_SCHEMAS["unique_stock_count"],
        }

        for endpoint, schema in v1_endpoints.items():
            self.test_endpoint(endpoint, schema)

        # TODO -- add tests to make sure that the data-241-apk-key is working
        # TODO -- add tests to verify returns correct error if not present

    def run_v2_tests(self):
        """Run v2 API tests"""
        print("Running tests on api/v2")
        # Test invalid API key
        print("Testing invalid key")
        invalid_key_tester = APITester(self.base_url, "INVALID_KEY")
        invalid_key_tester.test_endpoint("/api/v2/2019", expected_status_codes=[401])

        valid_years = [2019, 2011, 2015]
        for year in valid_years:
            self.test_endpoint(f"/api/v2/{year}", YEAR_RESPONSE_SCHEMA)

        invalid_years = [1800, 1900]
        for year in invalid_years:
            self.test_endpoint(f"/api/v2/{year}", expected_status_codes=[404])

        # Test price endpoints
        valid_test_cases = [
            ("open", "AAPL"),
            ("close", "GOOG"),
            ("high", "MSFT"),
            ("low", "AMZN"),
        ]
        for price_type, symbol in valid_test_cases:
            endpoint = f"/api/v2/{price_type}/{symbol}"
            self.test_endpoint(endpoint, PRICE_SCHEMAS[price_type])

        invalid_test_cases = [
            ("open", "INVALID1"),
            ("close", "INVALID2"),
            ("high", "XYZ"),
            ("low", "ABC"),
        ]
        for price_type, symbol in invalid_test_cases:
            endpoint = f"/api/v2/{price_type}/{symbol}"
            self.test_endpoint(endpoint, expected_status_codes=[404])

    def run_v3_tests(self):
        """Run v3 API tests"""
        print("\nRunning tests on api/v3")

        # Test 1: Create first account
        print("\nTesting first account creation")
        create_account_data = {"name": "Test Account 1"}
        account1_info = self.test_endpoint(
            "/api/v3/accounts",
            schema=API_SCHEMAS["account_creation"],
            method="POST",
            data=create_account_data,
            expected_status_codes=[201],
        )

        account1_id = account1_info["account_id"]

        # Test 2: Create second account
        print("\nTesting second account creation")
        create_account_data = {"name": "Test Account 2"}
        account2_info = self.test_endpoint(
            "/api/v3/accounts",
            schema=API_SCHEMAS["account_creation"],
            method="POST",
            data=create_account_data,
            expected_status_codes=[201],
        )
        account2_id = account2_info["account_id"]

        self.test_account_ids = [account1_id, account2_id]
        # Test 3: Add stock to first account
        print("\nTesting adding stock to first account")
        stock_data1 = {
            "account_id": account1_id,
            "symbol": "MSFT",
            "purchase_date": "2018-02-20",
            "sale_date": "2019-02-20",
            "number_of_shares": 100,
        }
        self.test_endpoint(
            "/api/v3/stocks",
            method="POST",
            data=stock_data1,
            expected_status_codes=[201],
        )

        # Test 4: Add stocks to second account
        print("\nTesting adding stocks to second account")
        stock_data2 = {
            "account_id": account2_id,
            "symbol": "AAPL",
            "purchase_date": "2016-10-19",
            "sale_date": "2016-10-27",
            "number_of_shares": 50,
        }
        self.test_endpoint(
            "/api/v3/stocks",
            method="POST",
            data=stock_data2,
            expected_status_codes=[201],
        )

        stock_data3 = {
            "account_id": account2_id,
            "symbol": "IBM",
            "purchase_date": "2016-09-08",
            "sale_date": "2016-09-14",
            "number_of_shares": 2,
        }
        self.test_endpoint(
            "/api/v3/stocks",
            method="POST",
            data=stock_data3,
            expected_status_codes=[201],
        )

        # Test 5: Verify account holdings
        print("\nTesting account holdings retrieval")
        self.test_endpoint(
            f"/api/v3/accounts/{account1_id}",
            schema=API_SCHEMAS["account_holdings"],
        )
        self.test_endpoint(
            f"/api/v3/accounts/{account2_id}",
            schema=API_SCHEMAS["account_holdings"],
        )

        # Run a test to verify that the values are correct.
        self.run_final_perfect_tests()

        # Test 6: Verify stocks across all accounts
        print("\nTesting stocks retrieval across accounts")
        self.test_endpoint("/api/v3/stocks/MSFT", schema=API_SCHEMAS["stock_list"])
        self.test_endpoint("/api/v3/stocks/AAPL", schema=API_SCHEMAS["stock_list"])
        self.test_endpoint("/api/v3/stocks/IBM", schema=API_SCHEMAS["stock_list"])

        # Test 7: Calculate returns for both accounts
        print("\nTesting returns calculation schema")
        self.test_endpoint(
            f"/api/v3/accounts/return/{account1_id}",
            schema=API_SCHEMAS["account_return"],
        )
        self.test_endpoint(
            f"/api/v3/accounts/return/{account2_id}",
            schema=API_SCHEMAS["account_return"],
        )

        # Test: List all accounts
        print("\nTesting accounts list retrieval")

        self.test_endpoint("/api/v3/accounts", schema=API_SCHEMAS["accounts_list"])

        # Test 8: Delete IBM stock from second account
        print("\nTesting stock deletion")
        self.test_endpoint(
            "/api/v3/stocks",
            method="DELETE",
            data=stock_data3,
            expected_status_codes=[204],
        )

        # Test 9: Verify updated account holdings after stock deletion
        print("\nVerifying account holdings after stock deletion")
        self.test_endpoint(
            f"/api/v3/accounts/{account2_id}",
            schema=API_SCHEMAS["account_holdings"],
        )
        # Test 10: Delete both accounts
        print("\nTesting account deletion")
        delete_account1_data = {"account_id": account1_id}
        self.test_endpoint(
            "/api/v3/accounts",
            method="DELETE",
            data=delete_account1_data,
            expected_status_codes=[204],
        )

        delete_account2_data = {"account_id": account2_id}
        self.test_endpoint(
            "/api/v3/accounts",
            method="DELETE",
            data=delete_account2_data,
            expected_status_codes=[204],
        )

    def run_v4_tests(self):
        """Run v4 API tests"""
        print("\nRunning tests on api/v4")

        # Test 1: Valid backtest request
        valid_backtest_data = {
            "value_1": "O1",
            "value_2": "C1",
            "operator": "LT",
            "purchase_type": "B",
            "start_date": "2020-01-03",
            "end_date": "2020-01-03",
        }
        self.test_endpoint(
            "/api/v4/back_test",
            schema=API_SCHEMAS["back_test_response"],
            method="POST",
            data=valid_backtest_data,
        )

        # Test 2: Invalid date (non-trading day)
        invalid_date_data = {
            "value_1": "O1",
            "value_2": "C1",
            "operator": "LT",
            "purchase_type": "B",
            "start_date": "1990-01-01",
            "end_date": "1990-01-02",
        }
        self.test_endpoint(
            "/api/v4/back_test",
            method="POST",
            data=invalid_date_data,
            expected_status_codes=[400],
        )

    def run_iv_api_tests(self):
        """Run v2 API tests"""
        print("Running tests on api/v2")
        # Test invalid API key
        print("Testing invalid key")
        invalid_key_tester = APITester(self.base_url, "INVALID_KEY")
        invalid_key_tester.test_endpoint("/api/v2/2019", expected_status_codes=[401])

    def run_final_perfect_tests(self):
        """Run final perfect tests to verify specific account returns."""
        print("\nRunning Perfect Tests on Accounts")

        if not hasattr(self, "test_account_ids"):
            print("Error: No account IDs available. Run v3 tests first.")
            return

        # Test first account return
        first_account_response = self.test_endpoint(
            f"/api/v3/accounts/return/{self.test_account_ids[0]}",
            schema=API_SCHEMAS["account_return"],
        )

        if first_account_response:
            actual_return = first_account_response["return"]
            expected_return = 1568.0
            tolerance = 0.05

            if abs(actual_return - expected_return) <= tolerance:
                print(
                    f"✓ First account (ID: {self.test_account_ids[0]}) "
                    "return test passed: {actual_return}"
                )
            else:
                print(
                    f"✗ First account (ID: {self.test_account_ids[0]}) "
                    f"return test failed: Expected {expected_return} ± "
                    f"{tolerance}, got {actual_return}"
                )

        # Test second account return
        second_account_response = self.test_endpoint(
            f"/api/v3/accounts/return/{self.test_account_ids[1]}",
            schema=API_SCHEMAS["account_return"],
        )

        if second_account_response:
            actual_return = second_account_response["return"]
            expected_return = -47.62
            tolerance = 0.05

            if abs(actual_return - expected_return) <= tolerance:
                print(
                    f"✓ Second account (ID: {self.test_account_ids[1]}) "
                    "return test passed: {actual_return}"
                )
            else:
                print(
                    f"✗ Second account (ID: {self.test_account_ids[1]}) "
                    "return test failed: Expected {expected_return} ± "
                    "{tolerance}, got {actual_return}"
                )

    def test_backtest_perfect_values(self):
        """Verify exact values from backtest endpoint with tolerance."""
        print("\nTesting exact backtest values")

        test_data = {
            "value_1": "O1",
            "value_2": "C1",
            "operator": "LT",
            "purchase_type": "B",
            "start_date": "2020-01-03",
            "end_date": "2020-01-03",
        }

        response = self.test_endpoint(
            "/api/v4/back_test",
            schema=API_SCHEMAS["back_test_response"],
            method="POST",
            data=test_data,
        )

        if not response:
            print("✗ Backtest value verification failed: No response received")
            return

        # Check number of observations
        expected_observations = 2033
        actual_observations = response["num_observations"]
        if actual_observations != expected_observations:
            print(
                f"✗ Observations test failed: Expected {expected_observations}, got {actual_observations}"
            )
        else:
            print(f"✓ Observations test passed: {actual_observations}")

        # Check return value with tolerance
        expected_return = 2188.4675
        actual_return = response["return"]
        tolerance = 0.05

        if abs(actual_return - expected_return) <= tolerance:
            print(f"✓ Return value test passed: {actual_return}")
        else:
            print(
                f"✗ Return value test failed: Expected {expected_return} ± {tolerance}, got {actual_return}"
            )


if __name__ == "__main__":
    api_key = os.environ.get("DATA_241_API_KEY")
    if not api_key:
        print("Error: DATA_241_API_KEY environment variable not set")
        sys.exit(1)

    tester = APITester(api_key=api_key)
    tester.run_tests(apis_to_test=["v1"])
    tester.run_tests(apis_to_test=["v2"])
    tester.run_tests(apis_to_test=["v3"])
    tester.run_tests(apis_to_test=["v4"])
    tester.run_tests(apis_to_test=["iv"])
    tester.run_tests(apis_to_test=["test_backtest_perfect_values"])

# Note that we accepted either 2059 or 2188 for the result

# 1 ✓ POST /api/v4/back_test: Success: {'num_observations': 2033, 'return': 2188.4675000000034}
# ✓ GET /api/v3/accounts/return/3: Success: {'account_id': 3, 'return': 1568.0000000000007}
# ✓ GET /api/v3/accounts/return/4: Success: {'account_id': 4, 'return': -47.62499999999995}

# Group 2
# ✓ GET /api/v3/accounts/return/1: Success: {'account_id': 1, 'return': 1568.0000000000007}
# ✓ GET /api/v3/accounts/return/2: Success: {'account_id': 2, 'return': -47.62499999999995}
# ✓ POST /api/v4/back_test: Success: {'num_observations': 2033, 'return': 2059.37}

# Group 3
# ✗ Return value test failed: Expected 2188.4675 ± 0.05, got 2059.365400000001

# Group 4
# ✗ Return value test failed: Expected 2188.4675 ± 0.05, got 2059.37

# Group 5
# ✗ Return value test failed: Expected 2188.4675 ± 0.05, got 2059.37

# Group 6
# ✗ Return value test failed: Expected 2188.4675 ± 0.05, got 2059.365400000001

# Group 7
# N/A

# Group 8
# ✓ POST /api/v4/back_test: Success: {'num_observations': 2918, 'return': 3051.61}
# ✗ Observations test failed: Expected 2033, got 2918
# ✗ Return value test failed: Expected 2188.4675 ± 0.05, got 3051.61


# db_truncate: build
# 	docker run $(COMMON_DOCKER_FLAGS) $(IMAGE_NAME) \
# 	sqlite3 $(DB_PATH) "DELETE FROM accounts; DELETE FROM stocks_owned;"

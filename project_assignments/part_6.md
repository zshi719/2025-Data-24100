# Project Part #6

This document outlines the requirements for the next part of our data serving API.

### Coding Standards

During the quarter, you will be expected to adhere to the coding standards found [here](https://github.com/dsi-clinic/the-clinic/blob/main/coding-standards/coding-standards.md) and we will frequently use [this rubric](https://github.com/dsi-clinic/the-clinic/blob/main/rubrics/final-technical-cleanup.md) as a checklist for your code.

### Branches

During this quarter we will be using branches and pull requests in order to submit code. **Any commits directly to the main branch will result in points being deducted.** The one exception to this is the initial commit in the repo.

### Grading

All grading will be done based off a specific commit hash off of the main branch. At the time that an assignment is due students must submit the commit hash associated with their commit to Canvas. You need to submit the _full_ commit hash which is a 40 digit long hash of letters and numbers. It will generally look something like this: `2a2a59af9feacbdd2cd772884b24641c3b75dff7`.

To find the commit hash, you can either use the command line or check GitHub’s commit history.

Note that any changes requested in the grading of the previous part need to be corrected.

## Part VI: Accounts and Returns

The goal of this assignment is to generate an account system for people to track their stock ownership over this time period. 

Specifically we will create endpoints which:
1. Add stocks to an account
2. Remove stocks from an account
3. Add accounts
4. Delete Accounts
5. Calculates the return of the stocks owned by a specific account.

**IMPORTANT NOTE:** Depending on the age of your group members computers you may struggle to load and use all the data. If this is the case for your group, you can create an environment variable called "DOWNSAMPLE" which when set equal to 1 will only load data from 2016 and 2017. This smaller subset of the data should be performant on everyone's computer. Using "DOWNSAMPLE" is optional, the environment variable is a flag for the grader to know what is testable.

Your code must conform to all the requirements of all previous parts, including [Part V](./part_5.md) 

### Specifications:

#### Updates to Make / Docker
- In addition to existing `make` commands your `db_create` command now needs to create an `accounts` and `stocks_owned` table with the data definition spelled out below. When you create these they should be empty.
- Implement these changes using the `db_manage.py` command.

#### Table definitions

- There will be two tables as defined below:

```
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
```

```
CREATE TABLE stocks_owned (
   account_id INTEGER,
   symbol TEXT NOT NULL,
   purchase_date DATE NOT NULL,
   sale_date DATE NOT NULL,
   number_of_shares INTEGER NOT NULL,
);
```

#### Updates to Flask

- None of the previous endpoints should change from the specification. We will be adding a `v3` set of endpoints.

- Given a base url of `/api/v3/` implement the following endpoints with the functionality below. Note that _all_ requests need to go through the same authentication as `v1` and `v2` (e.g. using the `DATA-241-API-KEY` environment variable). If the key is invalid or not present in the header, the request should return a status code of 401.

- Note on date formatting: In the database tables all dates are stored as `date` types. When they are sent in the request and when they are returned they should all be formatted as a string in ['Y-m-d'](https://strftime.org/) format.

| Endpoint name | Request Type | Request Info | Expected Response | Other Notes |
| --- | --- | --- | --- | --- | 
| `accounts` | GET |  This lists all accounts. | It should respond with a json formatted list of all the accounts. Each item in the list is of the form: `{ 'account_id' : INT, 'name' : str}` | If no accounts exists should return an empty list. Upon success the status code should be 200. |
| `accounts` | POST | This is to create an account. The request body should contain a JSON object `{ 'name' : str }` and it should add a row to the accounts table with that name. | The request should respond with a JSON object of the form `{ 'account_id' : INT}` which is the account ID for this newly created user. | It should return a status code of 201 if an account is created, 409 if the name already exists. |
| `accounts` | DELETE | This will delete an account. Request body should contain a JSON object `{ 'account_id' : INT }` | The request should respond with a JSON object of the form `{ 'account_id' : INT}` which is the account ID for this newly created user. | This should delete the account _and all stocks associated with the account_. If the account does not exist, then it should return a status code of 404. If the account does exist and is deleted it should return status code of 204. |
| `accounts/<INT>` | GET | This list all stocked owned by an account. The integer in the url should correspond to the account id | The response should contain, in the body, a JSON object of the form `{ 'account_id' : INT, 'name' : string, 'stock_holdings' = [{'symbol' : str, 'purchase_date' : str, 'sale_date' : str, 'number_of_shares': int}, ...]}`. Note the `stock_holdings` are a list of JSON objects. | If the account does not exist then it should return a 404. If the account does not hold any stocks the `stock_holdings` should be an empty list. |
| `stocks/<symbol>` | GET | The should list details of all stock holdings across _all_ accounts. | The response should be a JSON object of the form: `{ 'symbol': str, 'holdings': [{'account_id' : int, 'purchase_date' : str, 'sale_date' : str, 'number_of_shares': int }, ...]}` This is a dictionary which contains a list inside the `holdings` key. | If there are no holdings associated with the stock it should return an empty list. The status code should be 200. | 
| `stocks` | POST | Request body should contain a JSON object of the form `{ 'account_id' : int, 'symbol': str, 'purchase_date' : str, 'sale_date': str, 'number_of_shares': INT}` | This should return the appropriate status code and nothing more. | An account can own the same stock multiple times with the same or different dates. Account id and symbol are _not_ to be assumed unique. A 201 status code should be returned upon success. If the date is not a valid date (not a trading day), then return a 400. | 
| `stocks` | DELETE | Request body should contain a JSON object of the form `{ 'account_id' : int, 'symbol': str, 'purchase_date' : str, 'sale_date': str, 'number_of_shares': INT}` | This should return the appropriate status code and nothing else. | This should delete a single holding from an account. Note that if the full information (dates, account and symbol) does not match then a 404 should e returned. |
| `accounts/return/<int>` | GET | | This should return the nominal return (how much the account made) across all their holdings. The format should be `{'account_id' : int, 'return': float}`. More information on the calculation is below. | If the account id does not exist it should return status code 404, otherwise it should return 200. | 

#### Additional Details

- As mentioned in class I strongly advise you to add an index to the `stocks` table to make sure that your code is performant.
- All dates will be of the format ['Y-m-d'](https://strftime.org/), as in the previous parts.
- A trading day as defined as one that is in the dataset. If the date exists in the `stocks` table (e.g. in the original zip files) then you should consider it a trading day.
- No request should take more than a few seconds (say 5). If it does you should add an index to the table to make sure that the query is faster.
- To calculate the return you will take the `close` price for the stocks on the day that they were sold and subtract the `open` price for the day that they were bought. Multiply this by the number of shares that they owned. Since an account can have multiple stock holdings, the above calculation should be repeated for all stocks owned by the specific account. 

$$ \mathrm{return} = \sum_{\mathrm{holdings}} \mathrm{num\_shares} \left( \mathrm{close}_{\mathrm{sales\_date}} - \mathrm{open}_{\mathrm{purchase\_date}} \right) $$

- To determine a "valid" date when adding a stock to an account you should verify that the symbol-date combination exists in the data. If the combination does not exist then return a 400. This is important since if the date does not exist then calculating the return would not be possible.

### Additional Fixes

Please correct all of the feedback for Part IV. A portion of the grade will be set to making sure that your code continues to pass those standards.

## How will this be graded

- We will check out the code at the commit hash that you submit.
- All of the previous coding standards will be checked and the all of the previous APIs (`v1` and `v2`) will also be tested.
- Your code will also be read over to make sure that it conforms to the standards laid out in class. If you want to receive full credit make sure that your code has sound logic, is easy to read, maintains a good separation of concerns and does not violate the DRY principle.
- We will run the `make` commands outlined above and verify that they work according to the standards set out above. 
- We will run an autograder on the endpoints to make sure that they return the correct data and information.
- Finally, your code will also be read to make sure that all documentation is up to date and that the code has a consistent set of abstraction standards. 
- No errors or warning should occur in normal operations.
# Project Part #7

This document outlines the requirements for the next part of our data serving API.

### Coding Standards

During the quarter, you will be expected to adhere to the coding standards found [here](https://github.com/dsi-clinic/the-clinic/blob/main/coding-standards/coding-standards.md) and we will frequently use [this rubric](https://github.com/dsi-clinic/the-clinic/blob/main/rubrics/final-technical-cleanup.md) as a checklist for your code.

### Branches

During this quarter we will be using branches and pull requests in order to submit code. **Any commits directly to the main branch will result in points being deducted.** The one exception to this is the initial commit in the repo.

### Grading

All grading will be done based off a specific commit hash off of the main branch. At the time that an assignment is due students must submit the commit hash associated with their commit to Canvas. You need to submit the _full_ commit hash which is a 40 digit long hash of letters and numbers. It will generally look something like this: `2a2a59af9feacbdd2cd772884b24641c3b75dff7`.

To find the commit hash, you can either use the command line or check GitHub’s commit history.

Note that any changes requested in the grading of the previous part need to be corrected.

## Part VII: Logging and Back-Testing

- Your code must conform to all the requirements of all previous parts, including [Part VI](./part_6.md) 

### Logging

- Update all logs that use a custom logger. As in the demonstration in class the log format should be `log_format = "%(asctime)s | %(levelname)s | %(message)s"`.
- The log specification is as follows:

| System | Level | Description | 
| --- | --- | --- | 
| All `manage_db` commands | INFO | <ul><li>When a command starts and what command</li><li>When a command ends (and how long it took the management command took</li></ul> | 
| `manage_db` loading commands | DEBUG | <ul><li>As each _year_ and Market is loaded there should be a log with the time it took to load that year and market</li></ul> | 
| `manage_db` table creation commands | DEBUG | <ul><li>Notification that the table was created with its name</li></ul> | 
| All Routes | DEBUG | <ul><li>Time it took to respond to the route</li><li>The body, header and route</li><li>The response</li></ul> | 
| All Routes | INFO | <ul><li>All non-2xx responses (so 500, 404, etc.)</li></ul>| 
| All Routes | WARN | <ul><li>Any time the incorrect (or no) API key is provided</li></ul> | 

- All logs should contain specific and useful information regarding the process written in a professional manner. 
- No other `print` statements should exist. If there are additional things you want to have reported please use an appropriate log command.
- You do not need to override the Werkzeug library logging if you do not wish to. 

### Backtesting API

- In this section we will add a `v4` route which will back test a trading strategy based on our data. 
- Given a base url of `/api/v4/` implement the following endpoint with the functionality below. Note that _all_ requests need to go through the same authentication as `v1`, `v2` and `v3` (e.g. using the `DATA-241-API-KEY` environment variable). If the key is invalid or not present in the header, the request should return a status code of 401.

| Endpoint name | Request Type | Request Info | Expected Response | Other Notes |
| --- | --- | --- | --- | --- | 
| `back_test` | POST |  Returns the nominal value of a specific trading strategy.  | It should respond with a json object of the form: `{ 'return' : "float(2)" \| example: 123.45, 'num_observations': int }`. | More info about the request below.

- The POST request body should have the following schema:

```
{
    "value_1" : Price Target,
    "value_2" : Price Target,
    "operator" : LT or LTE,
    "purchase_type": B or S,
    "start_date": date ,
    "end_date": date
}
```

- The object of this exercise is that you will define a condition (based on `value_1`, `value_2` and the `operator`) and, if that condition is met between the dates specified then you will either buy or sell a share of the stock, depending on the `purchase_type`.

- The price target consists of two components: A price type (`O`, `C`, `L`, `H`) and a number (`1-10`) which represents n days in the past day. 

- The operator consists of either less than (`LT` which represents &lt;) or less than or equal (`LTE` which represents &le;).

- The way that we build our back testing is that for every day between the `start_date` and `end_date` (inclusive on both sides) we evaluate the metrics and decide to buy or sell that stock that day (by sell we mean short the stock -- selling a share to someone else) based on the if the condition is met.

- How to interpret the condition. To interpret the condition we take `value_` and `value_2` and then use the operator to compare. 

- Lets consider the example here:

```
{
    "value_1" : "O1",
    "value_2" : "C1",
    "operator" : "LT",
    "purchase_type": "B", 
    "start_date": "2020-01-03",
    "end_date": "2020-01-03"
}
```

- In this case we can read this as we will Buy (since the `B`) if `O1 LT C1` or if the previous trading day's open is less than (strictly) its close. We will do this on a single day.
  
- Lets consider the following example to help us understand how to do the calculation for a particular stock:


<table>
<caption>Microsoft Snippet</caption>
<tr>
<td><pre>
Symbol  Date         Open     Close   High     Low
------  -----------  -------  ------  -------  --------
MSFT    01-Jan-2020  157.7    157.7   157.7    157.7
MSFT    02-Jan-2020  158.78   160.62  160.73   158.33
MSFT    03-Jan-2020  158.32   158.62  159.945  158.06
MSFT    06-Jan-2020  157.08   159.03  159.1    156.51
MSFT    07-Jan-2020  159.32   157.58  159.67   157.32
MSFT    08-Jan-2020  158.93   160.09  160.8    157.9491
MSFT    09-Jan-2020  161.835  162.09  162.215  161.03
MSFT    10-Jan-2020  162.82   161.34  163.22   161.18
MSFT    13-Jan-2020  161.76   163.28  163.31   161.26
MSFT    14-Jan-2020  163.39   162.13  163.6    161.72
MSFT    15-Jan-2020  162.62   163.18  163.94   162.57
</pre></td>
</tr>
</table>

- To calculate what to return we will need to go through every stock which has data on January 3rd (such as `MSFT`) see if the condition is met. In this case, the `O1` price is `158.78` and the `C1` price is `160.62`. In this case our condition is met `158.78 < 160.62` so Microsoft _will_ be included in our calculations.

- Since we are buying the stock, we will, as we did in the previous assignment "buy" the stock at the open and "sell" the stock at night of the 3rd which would be equal to a return of `158.62 - 158.32 = .30`

- This would be repeated over all stocks that exists on January 3rd and the total return would be added up and sent back as part of the response. 

- Lets do another one:

```
{
    "value_1" : "O1",
    "value_2" : "O2",
    "operator" : "LTE",
    "purchase_type": "S", 
    "start_date": "2020-01-13",
    "end_date": "2020-01-14"
}
```

- This strategy says: "Sell if yesterday's open price is less than or equal to the open price from two days ago."

| Date | Notes | 
| --- | --- | 
| January 13th | <ul><li>O1 (open from yesterday - Jan 10): 162.82</li><li>O2 (open from 2 days ago - Jan 9): 161.835</li><li>162.82 ≰ 161.835 (condition NOT met)</li></ul> |
| January 14th | <ul><li>O1 (open from yesterday - Jan 13): 161.76</li><li>O2 (open from 2 days ago - Jan 10): 162.82</li><li>161.76 ≤ 162.82 (condition MET)</li><li>Since this is a sell/short strategy:</li><li>Sell at open (163.39), buy back at close (162.13)</li><li>Return = 163.39 - 162.13 = 1.26</li></ul> |


- The other piece of the response is the `num_observations` piece of the response. This should count the number of stock-days that _met_ the criteria. So, continuing on the last example, Microsoft would add 1 to the number of observations reported because only 1 of the 2 days met the criteria and were counted.

### Specifications:

#### Updates to Make / Docker
- There are no required updates to the `make` and `docker` components.

#### Additional Details

- If either the start or end date is not a trading day, your route should return an error (status code 400).
- As mentioned in class I strongly advise you to add an index to the `stocks` table to make sure that your code is performant.
- All dates will be of the format ['Y-m-d'](https://strftime.org/), as in the previous parts.
- A trading day as defined as one that is in the dataset. If the date exists in the `stocks` table (e.g. in the original zip files) then you should consider it a trading day.
- No request should take more than a few seconds (say 5). If it does you should add an index to the table to make sure that the query is faster.
- You can assume that the back-testing window will never be more than 10 days. 
- You should not include any stock-date combination as an observation unless all of the required dates are there. For example, if `O3` is requested, but the stock was just created in the dataset (such as they just had an IPO) then than stock would _not_ be included as an observation. 
- Make sure that your code is performant (less than a few seconds per request) by adding appropriate indexes to the tables. You are also welcome to add additional columns to the `stocks` table if there is a clear path to making this site faster.
- Starting the flask server should _not_ pre load any data. Each request should be send an SQL statement. Do not use pandas `read_sql` to interface with the database. You are welcome to put data from SQL into a dataframe, but that action and code must be written by the group. This is similar to what we did in class).

### Additional Fixes

Please correct all of the feedback for Part VI. A portion of the grade will be set to making sure that your code continues to pass those standards.

## How will this be graded

- We will check out the code at the commit hash that you submit.
- All of the previous coding standards will be checked and the all of the previous APIs (`v1`, `v2` and `v3`) will also be tested.
- Your code will also be read over to make sure that it conforms to the standards laid out in class. If you want to receive full credit make sure that your code has sound logic, is easy to read, maintains a good separation of concerns and does not violate the DRY principle.
- We will run the `make` commands outlined above and verify that they work according to the standards set out above. 
- We will run an autograder on the endpoints to make sure that they return the correct data and information. This includes types and casing.
- Finally, your code will also be read to make sure that all documentation is up to date and that the code has a consistent set of abstraction standards. 
- No errors or warning should occur in normal operations.
- The database file itself should _NOT_ be committed to the repo.
# Quiz 6A - Answer Key

This quiz covers cumulative material from weeks 1-6, with emphasis on HTTP request components, Flask route handling, query parameters, and data manipulation with lists and tuples.

Common errors to watch for:

1. Confusing query parameters with URL parameters
2. Not understanding how `request.args` works (it's a dictionary-like object)
3. Not handling edge cases (missing parameters, empty lists, etc.)
4. Not extracting the correct elements from tuples (title vs score)
5. Including scores when only titles should be returned
6. Not returning immediately when finding the first match

---

## Quiz 6A Answers

**Question 1:** Identify where specific information would be located in an HTTP request

**Answer:**

| Information Type | Location in HTTP Request |
|-----------------|-------------------------|
| Search Terms from a google query | Query parameters (query string) |
| Information submitted for inserting data | Request body |
| Authentication token for API access | Request headers |

**Grading notes:**
- Each row is worth equal points
- Accept reasonable variations in terminology:
  - "query parameters" or "query string parameters" or "query string" are acceptable
  - "request headers" or "headers" or "HTTP headers" are acceptable
  - "request body" or "body" or "HTTP body" are acceptable
- Common mistakes:
  - Putting authentication token in body instead of headers
  - Putting search terms in body instead of query parameters
  - Confusing URL parameters (path parameters) with query parameters

---

**Question 2:** What would be printed to the console for the given GET request?

**Answer:**

```
12345
{'format': 'json', 'include_reviews': 'true'}
GET
```

**Explanation:**
- The first line prints the URL parameter `book_id` which is extracted from the route path `/api/books/<book_id>` and will be `12345`
- The second line prints the query parameters as a dictionary. The URL `?format=json&include_reviews=true` is parsed by `request.args.to_dict()` into `{'format': 'json', 'include_reviews': 'true'}`
- The third line prints the request method, which is `GET`
- Note: The code no longer includes descriptive labels, just the values themselves

**Common mistakes:**
- Including descriptive labels like "URL Parameter (book_id):" or "Query Parameters:" (these are no longer in the code)
- Including headers or body in the output (these are no longer printed by the code)
- Confusing query parameters with URL parameters
- Not understanding that `request.args.to_dict()` converts query parameters to a dictionary
- Including extra output or formatting that wasn't in the code
- Not matching the exact format of the print statements (just the values, one per line)

---

**Question 3:** Filter search results by relevance score

**Answer:**

```python
# INSERT ANSWER HERE
filtered_titles = [title for title, score in results if score > 0.5]
if len(filtered_titles) == 0:
    return jsonify({'results': []}), 200
return jsonify({'results': filtered_titles}), 200
```

**Alternative solution (using traditional loop):**

```python
# INSERT ANSWER HERE
filtered_titles = []
for title, score in results:
    if score > 0.5:
        filtered_titles.append(title)
if not filtered_titles:
    return jsonify({'results': []}), 200
return jsonify({'results': filtered_titles}), 200
```

**Alternative solution (returning empty list directly - also acceptable):**

```python
# INSERT ANSWER HERE
filtered_titles = [item[0] for item in results if item[1] > 0.5]
return jsonify({'results': filtered_titles}), 200
```

**Explanation:**
- Filter the results list to only include tuples where the relevance score (second element) is greater than 0.5
- Extract only the titles (first element of each tuple) into a new list
- Use list comprehension or a loop to filter and extract titles
- If no results meet the threshold, return `jsonify({'results': []})` with status code 200
- If there are filtered results, return `jsonify({'results': <list_of_titles>})` with status code 200
- The response format must be `{'results': <list_of_strings>}` where the list contains only book titles

**Common mistakes:**
- Not filtering correctly (checking wrong element of tuple)
- Including the scores in the returned list instead of just titles
- Not extracting just the title from each tuple
- Not returning the exact format `{'results': []}` when empty
- Returning tuples directly instead of a list of strings
- Forgetting to return the response
- Using wrong comparison operator (e.g., `>=` instead of `>`)
- Not understanding tuple unpacking in the list comprehension
- Using wrong status code (must be 200 for both cases)

---

**Question 4:** Find first result with relevance score above 1.0 (title only)

**Answer:**

```python
results = get_search_results(search_term)
for title, score in results:
    if score > 1.0:
        return jsonify({'book': title}), 200
return jsonify({'error': 'No results found'}), 404
```

**Alternative solution (using next with generator):**

```python
results = get_search_results(search_term)
result = next((item for item in results if item[1] > 1.0), None)
if result:
    return jsonify({'book': result[0]}), 200
return jsonify({'error': 'No results found'}), 404
```

**Explanation:**
- First call `get_search_results(search_term)` to get the results list
- Iterate through the results list
- Check if the relevance score (second element of tuple) is greater than 1.0
- Return the first match found immediately with format `{'book': <title>}` and status code 200
- Only return the title, not the relevance score
- If no match is found, return `{'error': 'No results found'}` with status code 404
- The response formats are specified: success uses `{'book': <title>}` with 200, failure uses `{'error': 'No results found'}` with 404

**Common mistakes:**
- Not checking the correct element of the tuple (score is second element, index 1)
- Not returning immediately when first match is found (would continue searching)
- Including the relevance score in the response (should only return the title)
- Using wrong status code (must be 404 for not found, 200 for success)
- Not using the exact format `{'error': 'No results found'}` when no result found
- Not using the exact format `{'book': <title>}` when result found
- Using wrong comparison operator or threshold
- Not formatting the result properly for jsonify
- Returning the tuple directly instead of formatting as a dictionary


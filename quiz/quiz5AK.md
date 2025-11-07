# Quiz 5A - Answer Key

## Question 1: Flask Route with Data Reshaping

**Solution:**

```python
@app.route('/api/movies/top_movies', methods=['GET'])
def top_movies():
    movies = get_top_movies()
    rankings = {}
    total = 0
    for i, (name, tickets, rating) in enumerate(movies, 1):
        rankings[i] = name
        total += tickets
    return jsonify({'rankings': rankings, 'total_tickets': total}), 200
```

**Alternative solution using dictionary comprehension:**

```python
@app.route('/api/movies/top_movies', methods=['GET'])
def top_movies():
    movies = get_top_movies()
    rankings = {i: movie[0] for i, movie in enumerate(movies, 1)}
    total = sum(movie[1] for movie in movies)
    return jsonify({'rankings': rankings, 'total_tickets': total}), 200
```


## Question 2: Function with *args for Sequential Discounts

**Solution:**

```python
def apply_discounts(price, *discounts):
    for discount in discounts:
        price = price - (price * discount / 100)
    return price
```

**Alternative solution:**

```python
def apply_discounts(price, *discounts):
    for discount in discounts:
        price *= (1 - discount / 100)
    return price
```


## Question 3: Filter and Transform Data

**Solution:**

```python
def get_popular_showtimes(showtimes):
    return [{'movie': movie, 'time': time} 
            for movie, time, tickets, theater in showtimes 
            if tickets >= 20]
```

**Alternative solution using traditional loop:**

```python
def get_popular_showtimes(showtimes):
    result = []
    for movie, time, tickets, theater in showtimes:
        if tickets >= 20:
            result.append({'movie': movie, 'time': time})
    return result
```


## Question 4: DRY Refactoring

**Solution:**

Lots of possible solutions -- two below. The key was to extract some or all of the cursor logic to a helper function.

**Helper function:**
```python
def get_movie_data(table_name, column_name, movie_title, result_key):
    cursor = conn.cursor()
    cursor.execute(f"SELECT date, {column_name} FROM {table_name} WHERE movie = '{movie_title}'")
    results = cursor.fetchall()
    # Convert to thousands
    formatted_results = [(date, value / 1000) for date, value in results]
    return jsonify({'movie': movie_title, result_key: formatted_results}), 200
```

**Rewritten movie_sales route:**
```python
@app.route('/api/movies/sales/<movie_title>', methods=['GET'])
def movie_sales(movie_title):
    return get_movie_data('sales', 'tickets_sold', movie_title, 'sales')
```

**Alternative solution (simpler helper):**
```python
def query_and_format(table, column, movie_title, key):
    cursor = conn.cursor()
    cursor.execute(f"SELECT date, {column} FROM {table} WHERE movie = '{movie_title}'")
    results = cursor.fetchall()
    formatted_results = [(date, val / 1000) for date, val in results]
    return jsonify({'movie': movie_title, key: formatted_results}), 200

@app.route('/api/movies/sales/<movie_title>', methods=['GET'])
def movie_sales(movie_title):
    return query_and_format('sales', 'tickets_sold', movie_title, 'sales')
```

**How the other routes would be rewritten (not required but for reference):**
```python
@app.route('/api/movies/revenue/<movie_title>', methods=['GET'])
def movie_revenue(movie_title):
    return get_movie_data('revenue', 'revenue', movie_title, 'revenue')

@app.route('/api/movies/concessions/<movie_title>', methods=['GET'])
def movie_concessions(movie_title):
    return get_movie_data('concessions', 'concession_revenue', movie_title, 'concessions')
```


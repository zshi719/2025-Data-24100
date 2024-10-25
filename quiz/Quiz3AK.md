## Quiz 3 AK

Two questions with multiple parts.


1A. 

```
make last_10_errors
    cat /logs/flask.log | grep FLASKERROR | tail
```

1B.

```
make total_errors
    cat /logs/flask.log | grep FLASKERROR | wc
```

2.

```
@app.route('/api/v1/status', methods=['GET'])
def api_status():
    status_code = api_status_code()

    if status_code == 0:
        return Response(status=500)
    elif status_code == 1:
        return Response(status=200)
    elif status_code == 2:
        return Response(status=503)

    return None
```


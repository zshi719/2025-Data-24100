## Quiz 6 AK

1. Taken from Notes. For update, put or patch or both were accepted.

2. Answers were `{ 'result': 8}` and `{ 'result': 16}` both with status code 200

2. Full route below:

```
@app.route('/api/question3/count/<string:text_input>', methods=['GET'])
def count_characters(text_input):
    return jsonify({'length' : len(text_input)}), 200
```
## Quiz 5 AK

1. One answer can be found below, though there were a few different methods of creating the resulting dictionary.

```
@app.route('/api/v1/top_3_users', methods=['GET'])
def return_location_info():
    top_users = api_high_score_interface()
    result = {i+1: name for i, name in enumerate(top_users)}
    return jsonify(result), 200

```

2. DRY stands for "Don't Repeat Yourself" and is the principle that code that you write should not be duplicated.

3. There were a few different ways of answering the question. To get rid of the DRY violations we needed to remove the two lines that were copy-pasted (the one that calculated `time\_in\_sections` and the one that scaled the score). Below was one method of doing that.

```
@app.route('/api/v1/score/<user>', methods=['GET'])
def user_score(user):

    final_result = {}
    level_1_dict, level_2_dict = api_score_user_info(user)  

    for level_dict in [level_1_dict, level_2_dict]:
        level_dict['time_in_seconds'] = (
            level_dict['end_time'] - level_dict['start_time']
        )
        level_dict['score'] = int(level_dict['score']/100)
    
    final_result['user'] = user
    final_result['max'] = max(level_1_dict['score'],
        level_2_dict['score'] )
        
    final_result['total_time'] = (
        level_1_dict['time_in_seconds'] + 
            level_2_dict['time_in_seconds'] )

    return jsonify(final_result), 200
```
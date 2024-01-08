import json
import requests
from flask import Flask, request, jsonify
from textblob import TextBlob
import datetime
app = Flask(__name__)

def analyze_sentiment(comment):
    analysis = TextBlob(comment)
    polarity = analysis.sentiment.polarity
    classification = 'positive' if polarity > 0 else 'negative' if polarity < 0 else 'neutral'
    return polarity, classification


@app.get("/hello")
def say_hello():
    return {"Message": "Welcome to the sentiment analysis API"}
    

@app.route('/get_comments', methods=['GET'])
def get_comments():
    try:
        subfeddit_id = request.args.get('subfeddit')
        start_time = request.args.get('start_time', None)
        end_time = request.args.get('end_time', None)
        sort_by = request.args.get('sort_by', None)
        
        apil_url = "http://feddit:8080/api/v1/subfeddit?subfeddit_id="
        input_subfeddit_id = subfeddit_id
        complete_url = apil_url+input_subfeddit_id
        get_subfeddits = requests.get(complete_url)
    
        get_subfeddits_comm = json.loads(get_subfeddits.text)
        subfeddit_data = filter_subfeddits(get_subfeddits_comm, start_time, end_time, sort_by, subfeddit_id)
        return subfeddit_data
    except Exception as e:
        return {"Error": str(e)}
    
    
def change_datetime(data, start_time, end_time):
    # print(data)
    filter_data_list = []
    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')
    end_time = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%SZ')
    for val in data['comments']:
        timestamp = datetime.datetime.fromtimestamp(val['created_at'])
        if timestamp >= start_time and timestamp <= end_time:
            timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
            val['created_at'] = timestamp
            filter_data_list.append(val)
    return filter_data_list        

def produce_sentiments(data):
    all_comments = []
    comments_list = []
    for i in data:
        comment_dict = {}
        comment_dict["comment_id"] = i["id"]
        comment_dict["created_at"] = i["created_at"]
        comment_dict["text"] = i["text"]
        comments_list.append(comment_dict)
        for i in comments_list:
            polarity, classification = analyze_sentiment(i['text'])
            i['polarity']=polarity
            i['classification']=classification
    return comments_list
        
    
def filter_subfeddits(data, start_time, end_time, sort_by, subfeddit_id):

    if data.get("comments",None)!=None:
        if start_time!= None and end_time!=None:
            filtered_data = change_datetime(data, start_time, end_time)
            
            if len(filtered_data) > 0:
                senti_out = produce_sentiments(filtered_data)
                if sort_by == 'polarity':
                    # Sort comments by polarity if requested
                    senti_out.sort(key=lambda x: x['polarity'], reverse=True)
                    return jsonify({"comment": [f"returning details for subfeddit_id: {subfeddit_id}"], "comments_list": senti_out})
                    # return senti_out
                else:
                    return jsonify({"comment": [f"returning detai   ls for subfeddit_id: {subfeddit_id}"], "comments_list": senti_out})
                    # return senti_out
            else:   
                 return "No data found in given time range!"
        else:
            # unfiltered_data = change_datetime(data)
            if len(data['comments']) > 0:
                senti_out = produce_sentiments(data['comments'])
                if sort_by == 'polarity':
                # Sort comments by polarity if requested
                    senti_out.sort(key=lambda x: x['polarity'], reverse = True)
                    return jsonify({"comment": [f"returning details for subfeddit_id: {subfeddit_id}"], "comments_list": senti_out})
                    
                else:
                    return jsonify({"comment": [f"returning detai   ls for subfeddit_id: {subfeddit_id}"], "comments_list": senti_out})
                    
            else:
                return  "No comments found!"
                
        

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


# feddit-sentiment-model-serving 

As part of this challenge I have developed a web API that identifies if comments on a given
subfeddit or category are positive or negative.

For this challenge, we serve sentiment segmentation model - TextBlob using Flask API and feddit api for data.

Docker compose orchestrates the feddit and code running Text blob and allows communication between them.

To run the example in a machine running Docker and docker compose, run:


docker build -t sentiment_image .

docker-compose up

To use this model, we can send request the Flask API, we can send the request:

http://localhost:5000/get_comments?subfeddit=1

To sort the output based on polarity:

http://localhost:5000/get_comments?subfeddit=1&sort_by=polarity

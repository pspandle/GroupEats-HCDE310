from flask import Flask, render_template, request
import requests
from textblob import TextBlob
from config import YELP_API_KEY

app = Flask(__name__)

headers = {
    "Authorization": f"Bearer {YELP_API_KEY}"
}


def get_review_sentiment(rating):

    if rating >= 4.5:
        text = "absolutely excellent and amazing food, highly recommend"
    elif rating >= 4.0:
        text = "very good food, really enjoyable experience"
    elif rating >= 3.5:
        text = "decent food, fairly good experience"
    elif rating >= 3.0:
        text = "okay food, nothing special"
    else:
        text = "poor food, disappointing experience"

    blob = TextBlob(text)
    return blob.sentiment.polarity


def score_restaurant(restaurant, cuisines, prices):

    score = 0

    restaurant_cuisines = [c["alias"].lower() for c in restaurant["categories"]]

    for cuisine in cuisines:
        if cuisine in restaurant_cuisines:
            score += 13

    if "price" in restaurant:
        match = False
        for price in prices:
            if restaurant["price"] == price:
                score += 10
                match = True
        if not match:
            score -= 5

    score += restaurant["rating"]

    return score


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/results", methods=["POST"])
def results():

    location = request.form["location"]

    cuisines = request.form.getlist("cuisine")
    prices = request.form.getlist("price")

    url = "https://api.yelp.com/v3/businesses/search"

    params = {
        "location": location,
        "term": "restaurants",
        "limit": 10,
        "categories": ",".join(set(cuisines)),
        "price": ",".join(
            str(["$", "$$", "$$$", "$$$$"].index(p) + 1) for p in set(prices)
        )
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    restaurants = []

    for r in data["businesses"]:

        score = score_restaurant(r, cuisines, prices)

        restaurants.append({
            "id": r["id"],
            "name": r["name"],
            "rating": r["rating"],
            "price": r.get("price", "N/A"),
            "address": r["location"]["address1"],
            "url": r["url"],
            "image_url": r.get("image_url", ""),
            "score": score
        })

    restaurants.sort(key=lambda x: x["score"], reverse=True)

    for r in restaurants[:3]:
        sentiment = get_review_sentiment(r["rating"])
        r["sentiment"] = round(sentiment, 2)
        r["score"] = round(r["score"] + sentiment * 5, 2)

    for r in restaurants[3:]:
        r["sentiment"] = "N/A"
        r["score"] = round(r["score"], 2)

    restaurants.sort(key=lambda x: x["score"], reverse=True)

    return render_template("results.html", restaurants=restaurants)


if __name__ == "__main__":
    app.run(debug=True)
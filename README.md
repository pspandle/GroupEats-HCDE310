# Group Eats
### HCDE 310 Final Project

Group Eats helps groups decide where to eat by combining multiple people's restaurant preferences. The app collects cuisine and price preferences from each group member, retrieves restaurant data from the Yelp Fusion API, generates a sentiment score using TextBlob, and recommends restaurants that best match the group's combined preferences.


## Features
- Multiple group member preference inputs
- Restaurant search and filtering using the Yelp Fusion API
- Sentiment scoring using TextBlob
- Group compatibility scoring that weighs cuisine match, price match, Yelp rating, and sentiment


## TextBlob Change from Resource Writeup

Originally, the app was designed to fetch real customer reviews from the Yelp API and run TextBlob sentiment analysis directly on that text. However, I did not realize that Yelp removed public access to their reviews for standard API tiers in 2024. Attempts to call this endpoint now return a `NOT_FOUND` error regardless of whether the business ID is valid.

As a workaround, the app converts each restaurant's Yelp star rating into a short descriptive phrase, which TextBlob then analyzes for sentiment polarity. For example, a 4.8-star restaurant maps to the phrase `"absolutely excellent and amazing food, highly recommend"`, which TextBlob scores as strongly positive. A 2.5-star restaurant maps to `"poor food, disappointing experience"`, which scores as negative. This means TextBlob is still doing real natural language sentiment analysis, it's just analyzing generated text rather than scraped reviews. The resulting polarity score (ranging from -1.0 to 1.0) is added as a bonus to the restaurant's overall group compatibility score.


## Setup

1. Install dependencies:
    pip install -r requirements.txt

2. Get a Yelp API key at https://www.yelp.com/developers
    - Create an app and copy your API key

3. Create a file called `config.py` in the project root and add:
    YELP_API_KEY = "your_copied_api_key_here"
    > **Important:** do not share this file or commit it to GitHub. Add `config.py` to your `.gitignore`.

4. Run the app:
    python app.py

5. Open your browser and go to `http://127.0.0.1:5000`


## Project Structure
```
GroupEats-HCDE310/
├── app.py              # Flask app, Yelp API calls, scoring logic
├── config.py           # Yelp API key (do not share)
├── requirements.txt    # Python dependencies
├── static/
│   └── style.css       # Stylesheet
└── templates/
    ├── index.html      # Preference input form
    └── results.html    # Restaurant recommendations


## Dependencies
- Flask
- requests
- textblob
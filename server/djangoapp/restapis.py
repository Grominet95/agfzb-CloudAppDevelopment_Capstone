import requests
import json
from .models import CarDealer
from .models import DealerReview
from requests.auth import HTTPBasicAuth


import requests
from requests.auth import HTTPBasicAuth
import json

def get_request(url, api_key=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    headers = {'Content-Type': 'application/json'}
    params = kwargs.get("params", None)  # Extract params from kwargs if present

    try:
        if api_key:
            # If an API key is provided, use it for HTTP Basic Auth
            response = requests.get(url, headers=headers, params=params, auth=HTTPBasicAuth('apikey', api_key))
        else:
            # If no API key is provided, make a regular GET request
            response = requests.get(url, headers=headers, params=params)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except Exception as e:
        print("Network exception occurred", str(e))
        return {"error": "Network exception occurred"}


def post_request(url, json_payload, **kwargs):
    print("POST to {} with payload: {}".format(url, json_payload))
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, json=json_payload)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data
    except Exception as e:
        print("Network exception occurred", str(e))
        return {"error": "Network exception occurred"}


def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, **kwargs)
    if json_result:
        # Assuming json_result is directly a list of dealers
        for dealer_doc in json_result:  # Iterate directly over the list
            # Create a CarDealer object with values in `dealer_doc`
            dealer_obj = CarDealer(
                address=dealer_doc["address"], 
                city=dealer_doc["city"], 
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"], 
                lat=dealer_doc["lat"], 
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"], 
                zip=dealer_doc["zip"]
            )
            results.append(dealer_obj)
    return results


def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Assuming your get_request function is properly set to handle parameters and API keys
    json_result = get_request(url, params={"dealerId": dealerId})

    if json_result:
        reviews = json_result.get("reviews", [])
        for review_doc in reviews:
            # Construct a DealerReview object for each review
            review_obj = DealerReview(
                dealership=review_doc.get("dealership"),
                name=review_doc.get("name"),
                purchase=review_doc.get("purchase"),
                review=review_doc.get("review"),
                purchase_date=review_doc.get("purchase_date"),
                car_make=review_doc.get("car_make"),
                car_model=review_doc.get("car_model"),
                car_year=review_doc.get("car_year"),
                sentiment="",  # This will be filled by Watson NLU
                id=review_doc.get("id")
            )

            # Call Watson NLU to analyze the sentiment of the review's text
            sentiment = analyze_review_sentiments(review_obj.review)
            review_obj.sentiment = sentiment

            results.append(review_obj)

    return results



def analyze_review_sentiments(dealerreview):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/YOUR_INSTANCE_ID/v1/analyze"
    params = {
        "text": dealerreview,
        "version": "2021-08-01",
        "features": "sentiment",
        "return_analyzed_text": False
    }
    response = get_request(url, api_key=api_key, params=params)
    sentiment_result = response.get("sentiment", {}).get("document", {}).get("label", "")
    return sentiment_result



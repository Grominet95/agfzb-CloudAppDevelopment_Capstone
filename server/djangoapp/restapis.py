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
    # Check if 'json_result' is a dictionary and contains a specific key for dealers
    if json_result and isinstance(json_result, dict) and 'dealers' in json_result:
        dealers = json_result['dealers']  # Adjust 'dealers' to the actual key if it's different
        for dealer_doc in dealers:
            # Assuming 'dealer_doc' is a dictionary with dealer information
            dealer_obj = CarDealer(
                address=dealer_doc.get("address", ""), 
                city=dealer_doc.get("city", ""), 
                full_name=dealer_doc.get("full_name", ""),
                id=dealer_doc.get("id", 0),  # Assuming 'id' is always present; adjust if necessary
                lat=dealer_doc.get("lat", 0.0), 
                long=dealer_doc.get("long", 0.0),
                short_name=dealer_doc.get("short_name", ""),
                st=dealer_doc.get("st", ""), 
                zip=dealer_doc.get("zip", "")
            )
            results.append(dealer_obj)
    elif json_result and isinstance(json_result, list):
        # If 'json_result' is directly a list of dealers
        for dealer_doc in json_result:
            dealer_obj = CarDealer(
                address=dealer_doc.get("address", ""), 
                city=dealer_doc.get("city", ""), 
                full_name=dealer_doc.get("full_name", ""),
                id=dealer_doc.get("id", 0),
                lat=dealer_doc.get("lat", 0.0), 
                long=dealer_doc.get("long", 0.0),
                short_name=dealer_doc.get("short_name", ""),
                st=dealer_doc.get("st", ""), 
                zip=dealer_doc.get("zip", "")
            )
            results.append(dealer_obj)
    else:
        print("Unexpected JSON structure:", json_result)
    return results


def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, params={"dealerId": dealerId})
    
    if isinstance(json_result, list):
        for review_doc in json_result:
            if isinstance(review_doc, dict):
                # Use get method to handle missing keys
                review_obj = DealerReview(
                    dealership=review_doc.get("dealership"),
                    name=review_doc.get("name"),
                    purchase=review_doc.get("purchase"),
                    review=review_doc.get("review"),
                    purchase_date=review_doc.get("purchase_date", None),  # Provide default value if key is missing
                    car_make=review_doc.get("car_make"),
                    car_model=review_doc.get("car_model"),
                    car_year=review_doc.get("car_year"),
                    sentiment="",  # Initialize sentiment to empty string, to be filled later
                    id=review_doc.get("id")
                )
               
                review_obj.sentiment = analyze_review_sentiments(review_obj.review)
                results.append(review_obj)
    else:
        print("Unexpected JSON structure:", json_result)

    return results




def analyze_review_sentiments(dealerreview):
    api_key = 'Lbnu0BJSeiVgOZ1nZd72B9k8xWfHj4CPgmGcVCZYJl2M'  # Replace with your actual API key
    url = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/63c00a62-4546-4dd8-8ca7-17978673d108/v1/analyze"  # Replace with your actual endpoint
    
    params = {
        "text": dealerreview,
        "version": "2021-08-01",
        "features": "sentiment",
        "return_analyzed_text": False
    }

    response = get_request(url, api_key=api_key, params=params)
    if 'sentiment' in response and 'document' in response['sentiment']:
        return response['sentiment']['document']['label']
    else:
        # Log this case and return a default sentiment
        print("Sentiment not found in the Watson NLU response:", response)
        return "neutral"



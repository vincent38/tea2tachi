import requests
import os

def putScoresFile(scores_json, api_key):
    TACHI_API_URL = os.getenv('TACHI_API_URL')
    if TACHI_API_URL is None:
        raise Exception("Fatal - Missing Tachi API URL")
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'X-User-Intent': 'true'
    }

    response = requests.post(TACHI_API_URL, headers=headers, json=scores_json)
    return response
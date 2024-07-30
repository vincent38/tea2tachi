import requests
import os

def getDataFromTea(api_key):
    TEA_API_URL = os.getenv('TEA_API_URL')
    if TEA_API_URL is None:
        raise Exception("Fatal - Missing Tea API URL")
    
    headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }
    response = requests.request('GET', TEA_API_URL, headers=headers)
    return response.json()
import requests
import json

# set up the request parameters
params = {
  'api_key': '902001EE928446608F1DFDA760750BFC',
  'q': 'the distance between earch and moon is about 239,000 miles (384,400 kilometers)'
}

# make the http GET request to Scale SERP
api_result = requests.get('https://api.scaleserp.com/search', params)

# print the JSON response from Scale SERP
print(json.dumps(api_result.json()))
import json
import requests
from nltk.tokenize import sent_tokenize
scaleserp_api_key='902001EE928446608F1DFDA760750BFC',

input_text = 'According to the National Aeronautics and Space Administration (NASA), \
the average distance between the Earth and the Moon is about 238,855 miles (384,400 kilometers).'

def add_citation(text):
    sentences = sent_tokenize(text)
    links = []
    for sentence in sentences:
        params = {
            'api_key': scaleserp_api_key,
            'q': sentence,
        }
        api_result = requests.get('https://api.scaleserp.com/search', params)
        link = api_result.json()['organic_results'][0]['link']
        links.append(link)
    # print(sentences, links)
    return sentences, links


add_citation(input_text)
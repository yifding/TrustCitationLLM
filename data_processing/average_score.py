import os
import jsonlines
from collections import defaultdict

input_file = '/var/www/html/trust/trust/result.jsonl'
num_citation2num = dict()
num_citation2total_score = dict()
with jsonlines.open(input_file) as reader:
    records = [record for record in reader]

for record in records:
    num_citations = record['num_citations']
    ratings = record['ratings']
    for (num_citation, rating) in zip(num_citations, ratings):
        if num_citation not in num_citation2num:
            num_citation2num[num_citation] = 0
            num_citation2total_score[num_citation] = 0
        num_citation2num[num_citation] += 1
        num_citation2total_score[num_citation] += rating

for num_citation in [0, 1, 4, 7, 10]:
    print(f'num_citation: {num_citation}; number_qa: {num_citation2num[num_citation]};average_scores: {num_citation2total_score[num_citation] / num_citation2num[num_citation]}')
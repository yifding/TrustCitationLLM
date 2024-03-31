import os
import scipy
import numpy as np
import jsonlines
from collections import defaultdict

input_file = '/Users/yding4/Desktop/flask_chatgpt_response/third_batch.jsonl'
output_file = '/Users/yding4/Desktop/flask_chatgpt_response/data_processing/third_batch/third_batch.jsonl'
num_citation2num = defaultdict(list)
records = []
with jsonlines.open(input_file) as reader:
    for record in reader:
        # only keep the records after 3/13/2024 1:34
        # 1710308055.0
        if record['start_time'][0] >= 1710308055.0:
            records.append(record)

with jsonlines.open(output_file, 'w') as writer:
    writer.write_all(records)


for record in records:
    num_citations = record['num_citations']
    ratings = record['ratings']
    random_citations = record['random_citations']
    for (num_citation, random_citation, rating) in zip(num_citations, random_citations, ratings):
        num_citation2num[(num_citation, random_citation)].append(rating)

# print(num_citation2num)
for random_citation in [0, 1]:
    for num_citation in [0, 1, 5]:
        if (num_citation, random_citation) not in num_citation2num:
            continue
        print(
            f' num_citation: {num_citation}; ' \
            f' random_citation: {random_citation}; ' \
            f' number_qa: {len(num_citation2num[(num_citation, random_citation)])};' \
            f' average_scores: {scipy.stats.tmean(num_citation2num[(num_citation, random_citation)])}'
            f' standard deviation: {scipy.stats.tstd(num_citation2num[(num_citation, random_citation)])}'
            f' median: {np.median(num_citation2num[(num_citation, random_citation)])}'
        )
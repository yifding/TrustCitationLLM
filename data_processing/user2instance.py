import pandas as pd

input_file = '/Users/yding4/Desktop/flask_chatgpt_response/data_processing/first_batch/result_clean.csv'
# output_file = '/Users/yding4/Desktop/flask_chatgpt_response/data_processing/first_batch/result_clean_instance.jsonl'
output_file = '/Users/yding4/Desktop/flask_chatgpt_response/data_processing/first_batch/result_clean_instance.csv'

df = pd.read_csv(input_file)

new_instances = []
for index in range(len(df)):
    record = df.loc[index]
    for (
        question, 
        answer, 
        rating,
        num_citation,
        citations,
    ) in zip(
        eval(record['questions']),
        eval(record['answers']),
        eval(record['ratings']),
        eval(record['num_citations']),
        eval(record['citations_list']),
    ):
        if num_citation in [0, 1, 4, 7, 10]:
            new_instance = {
                'user_id': record['user_id'],
                'question': question,
                'answer': answer,
                'rating':rating,
                'num_citation': num_citation,
                'citations': citations,
                
                'random_citations': 1 if 'random_citations' in record and record['random_citations'] == 1 else 0,
                'age': record['age'],
                'chatgpt_heard': record['chatgpt_heard'],
                'education': record['education'],
                'gender': record['gender'],
                'political_orientation': record['political_orientation'],
                'race': record['race'],
                'residence': record['residence'],
                
            }
            new_instances.append(new_instance)

df_2 = pd.DataFrame(new_instances)
df_2.to_csv(output_file, encoding='utf-8')

# with jsonlines.open(output_file, 'w') as writer:
    # writer.write_all(new_instances)
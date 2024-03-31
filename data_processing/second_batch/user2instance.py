import pandas as pd

input_file = '/Users/yding4/Desktop/flask_chatgpt_response/data_processing/second_batch/second_batch.jsonl'
# output_file = '/Users/yding4/Desktop/flask_chatgpt_response/data_processing/first_batch/result_clean_instance.jsonl'
output_file = '/Users/yding4/Desktop/flask_chatgpt_response/data_processing/second_batch/second_batch_clean_instance.csv'

df = pd.read_json(input_file, lines=True)

new_instances = []
for index in range(len(df)):
    record = df.loc[index]
    for (
        question, 
        answer, 
        rating,
        num_citation,
        citations,
        random_citation,
        hook_over,
    ) in zip(
        record['questions'],
        record['answers'],
        record['ratings'],
        record['num_citations'],
        record['citations_list'],
        record['random_citations'],
        record['hook_overs'],
    ):
        if num_citation in [0, 1, 5]:
            new_instance = {
                'user_id': record['user_id'],
                'question': question,
                'answer': answer,
                'rating':rating,
                'num_citation': num_citation,
                'random_citation': random_citation,
                'hook_over': hook_over,
                'citations': citations,
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
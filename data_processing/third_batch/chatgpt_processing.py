import pandas as pd
from tqdm import tqdm
import openai

openai.api_key = "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"


def open_response(prompt):
    tmp_n = 0
    while tmp_n <= 10:
        try:
            response = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",  # You can choose a different engine
                prompt=prompt,
                max_tokens=150,
            )
            response = response.choices[0].text.strip()
            break
        except:
            tmp_n += 1
    if tmp_n == 10:
        return -1

    if 'yes' in response.lower():
        return 1
    elif 'no' in response.lower():
        return 0
    else:
        -1

def yes_more(prompt, loop=5):
    ans = []
    for i in range(loop):
        ans.append(open_response(prompt))
    if any(r==1 for r in ans):
        return 1
    else:
        return 0

input_file = '/nfs/yding4/flask_chatgpt_response/data_processing/third_batch/third_batch_clean_instance.csv'
output_file = '/nfs/yding4/flask_chatgpt_response/data_processing/third_batch/third_batch_clean_instance_classifier.csv'
df = pd.read_csv(input_file)
df.insert(16, "Factual", 0, True)
df.insert(17, "Political", 0, True)
df.insert(18, "Advise", 0, True)


for i in tqdm(range((len(df)))):
# for i in tqdm(range(10)):
    question = df['question'][i]

    factual_prompt = "please answer yes or no to the following question\n" + question + "\nIs mentioned question a factual question?"
    factual_response = yes_more(factual_prompt)
    df['Factual'][i] = factual_response

    political_prompt = "please answer yes or no to the following question\n" + question + "\nIs mentioned question political?"
    political_response = yes_more(political_prompt)
    df['Political'][i] = political_response

    advise_prompt = question + "\n please answer yes or no to the following question.\n Is mentioned question asking for advice?"
    advise_response = yes_more(advise_prompt)
    df['Advise'][i] = advise_response

    print(question, factual_response, political_response, advise_response)

df.to_csv(output_file)



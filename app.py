from flask import Flask, render_template, request, redirect, url_for
import json
import openai
import requests
from nltk.tokenize import sent_tokenize

from form import AskForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
openai.api_key = "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"
scaleserp_api_key='902001EE928446608F1DFDA760750BFC',


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
    
    # 1. insert citation inside the symbols (,".?!;)
    s = ''
    for index, sentence in enumerate(sentences):
        if sentence[-1] in ',".?!;':
            s += sentence[:-1] + f' [{str(index + 1)}]' + sentence[-1]
        else:
            s += sentence + f' [{str(index + 1)}] '
    instances = []
    for index, _ in enumerate(sentences):
        instances.append(f'[{str(index + 1)}]' + ' ' + links[index])
    return s, instances


@app.route('/', methods=['GET', 'POST'])
@app.route('/ask', methods=['GET', 'POST'])
def ask():
    ask_form = AskForm() 
    chatgpt_reply = ''
    # if request.method == 'POST' and ask_form.validate_on_submit():
    if request.method == 'POST':
        user_input = ask_form.user_input.data
        # You can customize the prompt or instructions based on your use case
        prompt = f"User: {user_input}\nChatGPT:"

        # Make a request to the OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can choose a different engine
            prompt=prompt,
            max_tokens=150,
        )

        # Extract the model's reply from the API response
        chatgpt_reply = response.choices[0].text.strip()

        # Add citations.
        chatgpt_reply, instances = add_citation(chatgpt_reply)

        return render_template('index.html', form=ask_form, chatgpt_reply=chatgpt_reply, instances=instances)
        # return redirect(url_for('ask', form=ask_form, chatgpt_reply=chatgpt_reply))
    else:
        return render_template('index.html', form=ask_form, chatgpt_reply=chatgpt_reply)


if __name__ == '__main__':
    app.run(debug=True)
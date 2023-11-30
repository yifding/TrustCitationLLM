from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

import sys
import json
import uuid
import random
import openai
import requests
from nltk.tokenize import sent_tokenize
from flask_login import current_user
from form import AskForm, CollectForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

openai.api_key = "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"
scaleserp_api_key='902001EE928446608F1DFDA760750BFC',

MAX_QUESTION_NUM = 10
RATING = -1
"""
class User(db.Model):
"""

class QuestionAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20))
    user_score = db.Column(db.Integer)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    qa_number = db.Column(db.Integer)
    num_citations = db.Column(db.Integer)
    start_time = db.Column(db.Integer)
    gpt_time_elapsed = db.Column(db.Integer)
    user_time_elapsed = db.Column(db.Integer)
    citations = db.relationship('Citation', backref='qa', lazy=True)


class Citation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hyperlink = db.Column(db.Text, nullable=False)
    qa_id = db.Column(db.Integer, db.ForeignKey('question_answer.id'), nullable=False)


def add_citation(text):
    sentences = sent_tokenize(text)
    # keep the first five sentences

    sentences = sentences[:5]
    chuncks = [0, 1, 4, 7, 10]
    # roll the dice first time. random.randint includes both sides
    chunck_index = random.randint(0, 4)
    chunck = chuncks[chunck_index]
    # roll the dice second time, to grasp the total number.
    chunck_list = []
    remain_num = chunck
    for index in range(len(sentences) - 1):
        cur_num = random.randint(0, min(5, remain_num))
        chunck_list.append(cur_num)
        remain_num -= cur_num
    
    chunck_list.append(min(5, remain_num))

    links_list = []
    tmp_link_index = 1
    for sentence, chunck in zip(sentences, chunck_list):
        links = []
        params = {
            'api_key': scaleserp_api_key,
            'q': sentence,
        }
        api_result = requests.get('https://api.scaleserp.com/search', params)
        for link_index in range(chunck):
            if 'organic_results' in api_result.json():
                link = api_result.json()['organic_results'][link_index]['link']
                links.append([tmp_link_index, link])
                tmp_link_index += 1
        links_list.append(links)

    return chunck_list, sentences, links_list


@app.route('/', methods=['GET', 'POST'])
def ask():
    ask_form = AskForm() 
    chatgpt_reply = ''
    # if request.method == 'POST' and ask_form.validate_on_submit():
    if request.method == 'POST' and ask_form.user_input.data:
        user_input = ask_form.user_input.data
        # You can customize the prompt or instructions based on your use case
        prompt = f"User: {user_input}\nChatGPT:"

        # Make a request to the OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can choose a different engine
            prompt=prompt,
            max_tokens=150,
        )
        # test rating
        # rating = ask_form.rating.data
        # print(f'MMP rating: {rating}')

        # Extract the model's reply from the API response
        chatgpt_reply = response.choices[0].text.strip()

        # Add citations.
        chunck_list, sentences, links_list = add_citation(chatgpt_reply)
        # chatgpt_reply = zip(sentences, links_list)

        # return render_template('index.html', form=ask_form, chatgpt_reply=chatgpt_reply, links_list=links_list)
        # print(f'sentences: {sentences}')
        # print(f'links_list: {links_list}')
        return redirect(url_for('collect', user_input=user_input, sentences=sentences, links_list=links_list))
    else:
        # check user_id existing in the session variables
        
        user_id = session.get('user_id', '')
        if user_id == '':
            session['user_id'] = uuid.uuid4()
            session['question_num'] = 1
            print(f"session['question_num']: {session['question_num']}")

        else:
            session['question_num'] += 1
            rating = request.args.get('rating', -1)
            # TODO: store the data in db
            print(f"session['question_num']: {session['question_num']}")
            print(f"session['rating']: {rating}")

        print(f"RATING: {RATING}")
        print(f"session['question_num']: {session['question_num']}")
        return render_template('index.html', form=ask_form, chatgpt_reply=chatgpt_reply)


@app.route('/collect', methods=['GET', 'POST'])
def collect():
    user_input = request.args.get('user_input')
    sentences = request.args.getlist('sentences')
    links_list = request.args.getlist('links_list')
    new_links_list = []
    # list of list has some problems
    for links in links_list:
        new_links_list.append(eval(links))
    links_list = new_links_list
    if len(sentences) == 1:
        links_list = [links_list]
    # print(f'user_input: {user_input}')
    # print(f'sentences: {sentences}')
    # print(f'links_list: {links_list}')
    # function to collect user response on question_answer.
    collect_form = CollectForm()
    # if request.method == 'POST' and collect_form.rating.data:
    if request.method == 'POST':
        rating = collect_form.rating.data
        RATING = rating
        # TODO: db to store data
        # session['rating'] = rating
        # print(f'rating: {rating}', file=sys.stdout)
        # print(f"rating: {session['question_num']}", file=sys.stdout)
        # return redirect(url_for('ask'))'
        flash('Your post has been deleted!', 'success')
        return render_template('collect.html')
    else:
        chatgpt_reply=zip(sentences, links_list)
        # flash('chatgpt response make up !', 'info')
        return render_template('collect.html', form=collect_form, user_input=user_input, chatgpt_reply=chatgpt_reply, links_list=links_list)

if __name__ == '__main__':
    app.run(debug=True)
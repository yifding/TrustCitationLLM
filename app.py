from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

import sys
import json
import uuid
import time
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
"""
class User(db.Model):
"""

class QuestionAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20))
    rating = db.Column(db.Integer)
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
    sentence_index = db.Column(db.Integer, nullable=False)
    hyperlink = db.Column(db.Text, nullable=False)
    qa_id = db.Column(db.Integer, db.ForeignKey('question_answer.id'), nullable=False)

db.create_all()


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

    return tmp_link_index, chunck_list, sentences, links_list


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route("/consent", methods=['GET', 'POST'])
def consent():
    return render_template('consent.html')

# @app.route("/", methods=['GET', 'POST'])
@app.route('/ask', methods=['GET', 'POST'])
def ask():
    print('a')
    ask_form = AskForm() 
    print(ask_form)
    print(request.method)
    # if request.method == 'POST' and ask_form.validate_on_submit():
    if request.method == 'POST' and ask_form.validate_on_submit() and ask_form.rating.data:
        print('b')
        session['user_time'] = time.time()
        # TODO: db to collect all the data.
        # stats the citation number.

        question_answer = QuestionAnswer(
            user_id=str(session['user_id']),
            rating=ask_form.rating.data,
            question=session['user_input'],
            answer=' '.join(session['sentences']),
            qa_number=session['question_num'],
            num_citations=session['num_citations'],
            start_time=session['start_time'],
            gpt_time_elapsed=session['chatgpt_time'] - session['start_time'],
            user_time_elapsed=session['user_time'] - session['chatgpt_time'],
        )

        db.session.add(question_answer)
        db.session.commit()

        for sentence_index, (_, links) in enumerate(zip(session['sentences'], session['links_list'])):
            for link in links:
                citation = Citation(
                    sentence_index=sentence_index,
                    hyperlink=link[1],
                    qa=question_answer,
                )
                db.session.add(citation)
                db.session.commit()
        flash('Your response has been collected!', 'success')
        return redirect(url_for('ask'))

    elif request.method == 'POST' and ask_form.validate_on_submit() and ask_form.user_input.data:
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
        num_citations, chunck_list, sentences, links_list = add_citation(chatgpt_reply)

        session['chatgpt_time'] = time.time()
        # chatgpt_reply = zip(sentences, links_list)
        chatgpt_reply=zip(sentences, links_list)

        # store intermediate variables as session variables
        session['num_citations'] = num_citations - 1
        session['user_input'] = user_input
        session['sentences'] = sentences
        session['links_list'] = links_list

        # return render_template('collect.html', user_input=user_input, sentences=sentences, links_list=links_list)
        return render_template('collect.html', form=ask_form, user_input=user_input, chatgpt_reply=chatgpt_reply, links_list=links_list)

    else:
        # check user_id existing in the session variables
        user_id = session.get('user_id', '')
        if user_id == '':
            session['user_id'] = uuid.uuid4()
            session['question_num'] = 1
        else:
            session['question_num'] += 1

        session['start_time'] = time.time()
        return render_template('index.html', form=ask_form)


if __name__ == '__main__':
    app.run(debug=True)
import jsonlines
from app import QuestionAnswer, GeoGraphic, Citation

records = []
for geo_graphic in GeoGraphic.query.all():
    user_id = geo_graphic.user_id
    age = geo_graphic.age
    chatgpt_heard = geo_graphic.chatgpt_heard
    education = geo_graphic.education
    gender = geo_graphic.gender
    political_orientation = geo_graphic.political_orientation
    race = geo_graphic.race
    residence = geo_graphic.residence

    question_answers = QuestionAnswer.query.filter_by(user_id=user_id).all()
    questions = []
    answers = []
    citations_list = []
    num_citations = []
    ratings = []
    random_citations = []
    hook_overs = []
    start_time = []
    for question_answer in question_answers:
        questions.append(question_answer.question)
        answers.append(question_answer.answer)
        ratings.append(question_answer.rating)
        # num_citations.append(question_answer.num_citations)
        random_citations.append(question_answer.random_citations)
        hook_overs.append(question_answer.hook_overs)
        start_time.append(question_answer.start_time)
        tmp_citations = []
        for tmp_citation in question_answer.citations:
            tmp_citations.append(tmp_citation.hyperlink)
        citations_list.append(tmp_citations)

        # for tmp_citations in citations_list:
        #     tmp_num_citation = len(tmp_citations)
        #     tmp_num_citations.append(tmp_num_citation)
        num_citations.append(len(tmp_citations))
        
    record = {
        'user_id': user_id,
        'age': age,
        'chatgpt_heard': chatgpt_heard,
        'education': education,
        'gender': gender,
        'political_orientation': political_orientation,
        'race': race,
        'residence': residence,
        'questions': questions,
        'answers': answers,
        'ratings': ratings,
        'num_citations': num_citations,
        'random_citations': random_citations,
        'hook_overs': hook_overs,
        'start_time': start_time,
        'citations_list': citations_list,
    }

    records.append(record)

with jsonlines.open('third_batch.jsonl', 'w') as writer:
    writer.write_all(records)

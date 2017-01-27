from flask import Flask, url_for, render_template, request
from app import app
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)

@app.route('/')
def index():
    # Gets all keys in database 
    # question = r.keys(pattern='*')
    # Placeholder questions
    question = ['In what year did the Titanic sink?', 'What capital city lies on the Potomac River?', 'What year was the first Super Bowl played?', 'The companies HP, Microsoft and Apple were all started in a what?']
    return render_template('index.html', question=question)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('CreateQuestion.html')
    elif request.method == 'POST':
		# Read form data and save it
        title = request.form['title']
        question = request.form['question']
        answer = request.form['answer']
		# Store data in the database
        r.set(title + ':question', question)
        r.set(title + ':answer', answer)
		# Show question that user created
        return render_template('CreatedQuestion.html', question=question)
    else:
        return '<h2>Invalid Request</h2>'

@app.route('/question/<title>', methods=['GET', 'POST'])
def question(title):
    if request.method == 'GET':
		# Send user the form

		# Read question for the database
        question = r.get(title + ':question')

        return render_template('AnswerQuestion.html', question=question)
    elif request.method == 'POST':
		# Check if submitted answer is correct
        submittedAnswer = request.form['submittedAnswer']

		# Read answer from database
        answer = r.get(title + ':answer')

        if submittedAnswer == answer:
            return render_template('Correct.html')
        else:
            return render_template('Incorrect.html', submittedAnswer=submittedAnswer, answer=answer)
    else:
        return '<h2>Invalid request</h2>'
from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.debug = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

question = 0

@app.route('/')
def show_home():
    survey_title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title=survey_title, instructions=instructions)

@app.route('/questions/<question>')
def show_question(question):
    q_num = int(question)
    question_obj = satisfaction_survey.questions[q_num]
    question_title = question_obj.question
    choices = question_obj.choices
    if (responses is None):
        return redirect("/")
    elif (len(responses) != q_num):
        return redirect(f'/questions/{len(responses)}')
    elif (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/thank-you')
    else:
        return render_template('questions.html', q_num=q_num, question=question_title, choices=choices)

@app.route('/answer', methods=["POST"])
def add_answer():    
    answer = request.form.get('answer')
    responses.append(answer)

    q_num = request.args['q_num']
    question = int(q_num) + 1

    if question < len(satisfaction_survey.questions):
        return redirect(f'/questions/{question}')
    else:
        return redirect('/thank-you')
    
@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html', responses=responses)
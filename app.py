from flask import Flask, request, render_template, redirect, flash, session
from random import randint, choice, sample
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey
#help with mentor in Git
app = Flask(__name__)

app.config["SECRET_KEY"] = "dancingmonkey2019"
debug = DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

RESPONSES = "responses"

@app.route("/")
def basePage():
    """Landing Page for selecting survey"""
    return render_template("index.html", survey=survey)

@app.route("/0", methods=["POST"])
def start_survey():
    """Question 0"""
    session[RESPONSES] = []
    return redirect("/questions/0")

@app.route("/responses", methods=["POST"])
def responses():
    """Handle all responses"""
    choice = request.form["answer"]
    responses = session[RESPONSES]
    responses.append(choice)
    session[RESPONSES] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")

    #return render_template("responses.html", responses=RESPONSES)

@app.route("/questions/<int:id>")
def show_question(id):
    responses = session.get(RESPONSES)

    if (responses is None):
        return redirect("/")
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    if (len(responses) != id):
        flash(f"Invalid Question id: {id}.")
        return redirect("/questions/{len(responses)}")

    question = survey.questions[id]
    return render_template("question.html", question_num=id, question=question)    

@app.route("/complete")
def complete():
    return render_template("responses.html")

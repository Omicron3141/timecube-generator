from Generator import sentenceGenerator

from flask import Flask
from flask import render_template

from flask_bootstrap import Bootstrap

def create_app():
  a = Flask(__name__)
  Bootstrap(a)
  return a


app = create_app()


@app.before_first_request
def load_data():
	print("Loading initial data")
	sentenceGenerator.load("Generator/model.npz")

@app.route('/')
def main_page():
    initial_sentence = sentenceGenerator.create_sentence()
    return render_template('main.html', sentence=initial_sentence)

@app.route('/new')
def load_new_sentence():
    sentence = sentenceGenerator.create_sentence()
    return sentence



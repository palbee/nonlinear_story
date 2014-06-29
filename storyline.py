#!/usr/bin/env python
"""Silly application for generating colloborative prose and poetry."""

from flask import Flask, render_template, request, redirect
from models import db
from models import User, Word

app = Flask(__name__)

db.create_all()

@app.route('/')
def show_a_story():
    number_of_words = db.session.query(Word).count()
    try:
        corpus = db.session.query(Word).get(number_of_words).corpus()
    except Exception as e:
        corpus = redirect("/contribute")
    return corpus

@app.route('/contribute',methods=['POST', 'GET'])
def append_2_story():
    # Handle posts
    if request.method == 'POST':
        # Retrieve and clean the submittors contribution
        contrib = request.form.get('contribution','')
        contrib = contrib.strip()
        if len(contrib) != 0:
            # Prepare link to old contribution
            last_word_id = request.form.get('last_word',None)
            if last_word_id is not None:
                try:
                    last_word_id = int(last_word_id)
                except:
                    last_word = None
                else:
                    last_word = db.session.query(Word).get(last_word_id)
                    last_word.terminal = False
            else:
                last_word = None
            last_word = Word(contrib, last_word ,None)
            db.session.add(last_word)
            db.session.commit()
    last_words = db.session.query(Word).filter_by(terminal=True).all()
    return render_template('contribute.html', last_words = last_words)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Word(db.Model):
    """Models a user contributed word."""
    __tablename__ = 'word'
    id = db.Column(db.Integer, primary_key=True) # Unique entruy id
    prev_id = db.Column(db.Integer, db.ForeignKey('word.id')) # The predecessor
    word = db.Column(db.String(80), unique=False) # The word being added
    terminal = db.Column(db.Boolean, default=False) # Is this a terminal word?
    prev_word = db.relationship("Word", remote_side=[id],
        backref=db.backref('next_words', lazy='dynamic'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User',
        backref=db.backref('words', lazy='dynamic'))
  
    def corpus(self):
        """Returns the corpus of the text generated thus far."""
        if self.prev_word is None:
            return self.word
        else:
            curr_text = self.word;
            predecessor = self.prev_word
            while predecessor is not None:
                curr_text = "%s %s" % (predecessor.word, curr_text)
                predecessor = predecessor.prev_word
            return curr_text
            
    def __init__(self, word, prev_word, user):
        self.word = word
        self.prev_word = prev_word
        self.user = user
        self.terminal = True

    def __repr__(self):
        return '<Word %r>' % (self.word,)

class User(db.Model):
    """Model for a user. Not used yet."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r, %r>' % (self.username, self.email)

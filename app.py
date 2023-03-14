from flask import Flask, render_template, send_from_directory, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_cors import CORS, cross_origin
import os
import re
import openai
import IPython

app = Flask(__name__, static_folder='client/build', static_url_path='')
if os.environ.get('ENV') == 'prod':
    uri = os.getenv("DATABASE_URL")  # or other relevant config var
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    openai.api_key = os.environ.get('OPENAI_KEY')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/ai-book-chat-local'
    openai.api_key = os.environ.get('OPENAI_KEY')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
cors = CORS(app)
model_id = "gpt-3.5-turbo"


def get_initial_message(character, book):
    return [
        {"role": "system", "content": "Answer the following question as if you are " + character + " from " + book + ". How would " + character +
            " answer the question? If the answer cannot be found in the book " + book + ", say you don\'t know the answer to that question. If the question is inappropriate for a 10 year old, say that you are not going to dignify that question with an answer. Answer as " + character + "."}
    ]


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String(120), nullable=False)
    characters = db.Column(db.String(200), nullable=False)
    handle = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return f'Book: {self.book}'

    def __init__(self, book, characters, handle):
        self.book = book
        self.characters = characters
        self.handle = handle


def format_book(book):
    return {
        'book': book.book,
        'characters': book.characters,
        'handle': book.handle,
        'id': book.id,
        'created_at': book.created_at
    }


@app.route('/',  defaults={'path': ''})
@app.errorhandler(404)
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api')
@cross_origin()
def Welcome():
    return 'Welcome to the AI Chat API'


@app.route('/api/books', methods=['POST'])
def create_book():
    book = request.json['book']
    characters = request.json['characters']
    handle = request.json['handle']
    newBook = Book(book, characters, handle)
    db.session.add(newBook)
    db.session.commit()
    return format_book(newBook)

# get all books


@app.route('/api/books', methods=['GET'])
def get_books():
    books = Book.query.order_by(Book.id.desc()).all()
    book_list = []
    for book in books:
        book_list.append(format_book(book))
    return {'book': book_list}

# get a single book


@app.route('/api/books/<handle>', methods=['GET'])
def get_book(handle):
    book = Book.query.filter_by(handle=handle).first()
    formatted_book = format_book(book)
    formatted_book['characters'] = formatted_book['characters'].split(',')
    character = formatted_book['characters'][0]
    messages = get_initial_message(
        character, formatted_book['book'])
    messages.append({"role": "assistant", "content": "Hi, I'm " + character +
                    " from " + formatted_book['book'] + ". Ask me a question."})
    return {'book': format_book(book), 'messages': messages, 'character': character}


@app.route('/api/conversation', methods=['POST'])
def continue_conversation():
    messages = request.json['messages']
    question = request.json["question"]
    # messages.append({"role": "user", "content": question})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    return messages


@app.route('/api/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.filter_by(id=id).first()
    db.session.delete(book)
    db.session.commit()
    return f'Book (id: {id}) deleted'

# update an book


@app.route('/api/books/<id>', methods=['PUT'])
def update_book(id):
    book = Book.query.filter_by(id=id).first()
    book.book = request.json['book']
    book.characters = request.json['characters']
    db.session.commit()
    return format_book(book)


if __name__ == '__main__':
    db.create_all()
    app.run()

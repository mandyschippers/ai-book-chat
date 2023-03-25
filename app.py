# from flask import Flask, render_template, send_from_directory, request, jsonify, make_response
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from datetime import datetime
# from flask_cors import CORS, cross_origin
# import os
# import re
# import openai
# import IPython

# app = Flask(__name__, static_folder='client/build', static_url_path='')
# if os.environ.get('ENV') == 'prod':
#     uri = os.getenv("DATABASE_URL")  # or other relevant config var
#     if uri and uri.startswith("postgres://"):
#         uri = uri.replace("postgres://", "postgresql://", 1)
#     app.config['SQLALCHEMY_DATABASE_URI'] = uri
#     openai.api_key = os.environ.get('OPENAI_KEY')
# else:
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/ai-book-chat-local'
#     openai.api_key = os.environ.get('OPENAI_KEY')
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# cors = CORS(app)
# model_id = os.environ.get('MODEL')


# def get_initial_message(character, book):
#     return [
#         {"role": "system", "content": "You are " + character + " from the book " + book +
#             ". Answer the questions from the user only if you can know the answer, based on the book. If the answer cannot be found in the book, say you don't know the answer to that question. Don't reply in any way that is inappropriate for a child. Don't ever admit that you are anything other than " + character + ". Keep it brief."}
#     ]


# def get_initial_personality_message(name, books):
#     return [
#         {"role": "system", "content": "You are " + name + ", author of works including " + books +
#             ". Answer questions from the user only if you can know the answer, based on your situation. Otherwise, say you don't know the answer to that question. Analyse " + name + "'s writing style and answer as " + name + " would. Every third time you respond, ask a follow-up question as if you are curious about the person asking the question and you want to know more about them and how they experience life. You are talking to a close friend."}]


# def get_initial_hogwarts_library_message():
#     return [
#         {"role": "system", "content": "You are a Magical book in the Hogwarts Library that knows everything that happens in the world described in the Harry Potter books. Answer the user's questions about Harry Potter, but don't answer anything that's inappropriate for children. Respond in a magical writing style that belongs in the world of Harry Potter. Answer the question only if it can be known based on the Harry Potter Book series."}]


# def get_initial_gpt4_message():
#     return []


# class Book(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     book = db.Column(db.String(120), nullable=False)
#     characters = db.Column(db.String(200), nullable=False)
#     handle = db.Column(db.String(120), nullable=True)
#     created_at = db.Column(db.DateTime, nullable=False,
#                            default=datetime.utcnow)

#     def __repr__(self):
#         return f'Book: {self.book}'

#     def __init__(self, book, characters, handle):
#         self.book = book
#         self.characters = characters
#         self.handle = handle


# def format_book(book):
#     return {
#         'book': book.book,
#         'characters': book.characters,
#         'handle': book.handle,
#         'id': book.id,
#         'created_at': book.created_at
#     }


# class Personality(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120), nullable=False)
#     books = db.Column(db.String(2000), nullable=False)
#     handle = db.Column(db.String(120), nullable=True)
#     created_at = db.Column(db.DateTime, nullable=False,
#                            default=datetime.utcnow)

#     def __repr__(self):
#         return f'Presonality: {self.name}'

#     def __init__(self, name, books, handle):
#         self.name = name
#         self.books = books
#         self.handle = handle


# def format_personality(personality):
#     print(personality)
#     return {
#         'name': personality.name,
#         'books': personality.books,
#         'handle': personality.handle,
#         'id': personality.id,
#         'created_at': personality.created_at
#     }


# @app.route('/',  defaults={'path': ''})
# @app.errorhandler(404)
# def serve(path):
#     return send_from_directory(app.static_folder, 'index.html')


# @app.route('/api')
# @cross_origin()
# def Welcome():
#     return 'Welcome to the AI Chat API'

# # do a route /api/personalities/add to add a personality


# @app.route('/api/personalities/add', methods=['POST'])
# def create_personality():
#     name = request.json['name']
#     books = request.json['books']
#     handle = request.json['handle']
#     newPersonality = Personality(name, books, handle)
#     db.session.add(newPersonality)
#     db.session.commit()
#     return format_personality(newPersonality)

# # a route /api/personality/<handle> to get a personality


# @app.route('/api/personalities/<handle>', methods=['GET'])
# def get_personality(handle):
#     personality = Personality.query.filter_by(handle=handle).first()
#     print(personality)
#     formatted_personality = format_personality(personality)
#     books = formatted_personality['books']
#     messages = get_initial_personality_message(
#         formatted_personality['name'], books)
#     messages.append({"role": "assistant", "content": "Hi, I'm " + formatted_personality['name'] +
#                     ". What would you like to talk about?"})
#     return {'personality': formatted_personality, 'messages': messages, 'name': formatted_personality['name'], 'model': model_id}


# @app.route('/api/books', methods=['POST'])
# def create_book():
#     book = request.json['book']
#     characters = request.json['characters']
#     handle = request.json['handle']
#     newBook = Book(book, characters, handle)
#     db.session.add(newBook)
#     db.session.commit()
#     return format_book(newBook)

# # get all books


# @app.route('/api/books', methods=['GET'])
# def get_books():
#     books = Book.query.order_by(Book.id.desc()).all()
#     book_list = []
#     for book in books:
#         book_list.append(format_book(book))
#     return {'book': book_list}

# # get a single book


# @app.route('/api/books/<handle>', methods=['GET'])
# def get_book(handle):
#     book = Book.query.filter_by(handle=handle).first()
#     formatted_book = format_book(book)
#     formatted_book['characters'] = formatted_book['characters'].split(',')
#     character = formatted_book['characters'][0]
#     messages = get_initial_message(
#         character, formatted_book['book'])
#     messages.append({"role": "assistant", "content": "Hi, I'm " +
#                     character + ". Ask me a question."})
#     return {'book': format_book(book), 'messages': messages, 'character': character}


# @app.route('/api/conversation', methods=['POST'])
# def continue_conversation():
#     messages = request.json['messages']
#     question = request.json["question"]
#     max_length = request.json["max_length"]
#     model = request.json["model"]
#     response = openai.ChatCompletion.create(
#         model=model if model else model_id,
#         messages=messages,
#         temperature=0.7,
#         max_tokens=max_length,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )
#     reply = response.choices[0].message.content
#     messages.append({"role": "assistant", "content": reply})
#     return messages


# @app.route('/api/books/<id>', methods=['DELETE'])
# def delete_book(id):
#     book = Book.query.filter_by(id=id).first()
#     db.session.delete(book)
#     db.session.commit()
#     return f'Book (id: {id}) deleted'

# # update an book


# @app.route('/api/books/<id>', methods=['PUT'])
# def update_book(id):
#     book = Book.query.filter_by(id=id).first()
#     book.book = request.json['book']
#     book.characters = request.json['characters']
#     db.session.commit()
#     return format_book(book)


# @app.route('/api/hogwarts-library', methods=['GET'])
# def get_hogwarts_library():
#     messages = get_initial_hogwarts_library_message()
#     messages.append({"role": "assistant", "content": "Welcome to the Hogwarts Library! Here you will find everything you ever wanted to know about the Wizarding world... do you have a question for me?"})
#     return {'book': 'the Hogwarts Library', 'messages': messages, 'character': 'the Magical Book'}


# @app.route('/api/secret-oracle', methods=['GET'])
# def get_secret_oracle():
#     messages = get_initial_gpt4_message()
#     messages.append({"role": "assistant", "content": "Welcome to the Secret Oracle! Here you will find everything you ever wanted to know about anything... do you have a question for me?"})
#     return {'book': None, 'messages': messages, 'character': 'the Secret Oracle'}


# if __name__ == '__main__':
#     db.create_all()
#     app.run()

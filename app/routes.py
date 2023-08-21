# from app import routes
from flask_cors import CORS, cross_origin
from flask import render_template, send_from_directory, request, jsonify, make_response
from app.services import (get_initial_message, get_initial_personality_message,
                          get_initial_hogwarts_library_message,
                          get_initial_llm_message, get_initial_gpt4_message,
                          format_book, format_personality,
                          format_llm_personality)
from app.models import Book, Personality, LlmPersonality
from app import app, db
import openai

openai.api_key = app.config['OPENAI_KEY']


@app.route('/', defaults={'path': ''})
@app.errorhandler(404)
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api')
@cross_origin()
def Welcome():
    return 'Welcome to the AI Chat API'


# do a route /api/personalities/add to add a personality


@app.route('/api/personalities/add', methods=['POST'])
@cross_origin()
def create_personality():
    name = request.json['name']
    books = request.json['books']
    handle = request.json['handle']
    newPersonality = Personality(name, books, handle)
    db.session.add(newPersonality)
    db.session.commit()
    return format_personality(newPersonality)


# route to add an llm personality


@app.route('/api/add-personality', methods=['POST'])
@cross_origin()
def add_llm_personality():
    name = request.json['name']
    description = request.json['description']
    llm_personality = request.json['llm_personality']
    handle = request.json['handle']
    newLlmPersonality = LlmPersonality(name, description, llm_personality,
                                       handle)
    db.session.add(newLlmPersonality)
    db.session.commit()
    return format_llm_personality(newLlmPersonality)


# a route /api/personality/<handle> to get a personality


@app.route('/api/personalities/<handle>', methods=['GET'])
def get_personality(handle):
    personality = Personality.query.filter_by(handle=handle).first()
    formatted_personality = format_personality(personality)
    books = formatted_personality['books']
    messages = get_initial_personality_message(formatted_personality['name'],
                                               books)
    messages.append({
        "role":
        "assistant",
        "content":
        "Hi, I'm " + formatted_personality['name'] +
        ". What would you like to talk about?"
    })
    return {
        'personality': formatted_personality,
        'messages': messages,
        'name': formatted_personality['name'],
        'model': app.config.get('MODEL')
    }


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
    messages = get_initial_message(character, formatted_book['book'])
    messages.append({
        "role": "assistant",
        "content": "Hi, I'm " + character + ". Ask me a question."
    })
    return {
        'book': format_book(book),
        'messages': messages,
        'character': character
    }


# get a single llm personality


@app.route('/api/chat/<handle>', methods=['GET'])
def get_llm_personality(handle):
    llm_personality = LlmPersonality.query.filter_by(handle=handle).first()
    formatted_llm_personality = format_llm_personality(llm_personality)
    messages = get_initial_llm_message(
        formatted_llm_personality['llm_personality'])
    messages.append({
        "role":
        "assistant",
        "content":
        "Hi, I'm " + formatted_llm_personality['name'] + ". I am " +
        formatted_llm_personality['description'] + ". Ask me a question."
    })
    return {
        'personality': formatted_llm_personality,
        'messages': messages,
        'name': formatted_llm_personality['name']
    }


@app.route('/api/conversation', methods=['POST'])
@cross_origin()
def continue_conversation():
    messages = request.json['messages']
    max_length = request.json["max_length"]
    model = request.json["model"]
    response = openai.ChatCompletion.create(
        model=model if model else app.config.get('MODEL'),
        messages=messages,
        temperature=0.7,
        max_tokens=max_length,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
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


@app.route('/api/hogwarts-library', methods=['GET'])
def get_hogwarts_library():
    messages = get_initial_hogwarts_library_message()
    messages.append({
        "role":
        "assistant",
        "content":
        "Welcome to the Hogwarts Library! Here you will find everything you ever wanted to know about the Wizarding world... do you have a question for me?"
    })
    return {
        'book': 'the Hogwarts Library',
        'messages': messages,
        'character': 'the Magical Book'
    }


@app.route('/api/secret-oracle', methods=['GET'])
def get_secret_oracle():
    messages = get_initial_gpt4_message()
    messages.append({
        "role":
        "assistant",
        "content":
        "Welcome to the Secret Oracle! Here you will find everything you ever wanted to know about anything... do you have a question for me?"
    })
    return {
        'book': None,
        'messages': messages,
        'character': 'the Secret Oracle'
    }

from app import db
from datetime import datetime


class LlmPersonality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    llm_personality = db.Column(db.String(10000), nullable=False)
    handle = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Personality: {self.name}, {self.description}'

    def __init__(self, name, description, llm_personality, handle):
        self.name = name
        self.description = description
        self.llm_personality = llm_personality
        self.handle = handle


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String(120), nullable=False)
    characters = db.Column(db.String(200), nullable=False)
    handle = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return f'Book: {self.book}'

    def __init__(self, book, characters, handle):
        self.book = book
        self.characters = characters
        self.handle = handle


class Personality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    books = db.Column(db.String(2000), nullable=False)
    handle = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return f'Personality: {self.name}'

    def __init__(self, name, books, handle):
        self.name = name
        self.books = books
        self.handle = handle

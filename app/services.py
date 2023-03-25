import os
import re
import openai
import IPython

model_id = os.environ.get('MODEL')


def get_initial_message(character, book):
    return [
        {"role": "system", "content": "You are " + character + " from the book " + book +
            ". Answer the questions from the user only if you can know the answer, based on the book. If the answer cannot be found in the book, say you don't know the answer to that question. Don't reply in any way that is inappropriate for a child. Don't ever admit that you are anything other than " + character + ". Keep it brief."}
    ]


def get_initial_personality_message(name, books):
    return [
        {"role": "system", "content": "You are " + name + ", author of works including " + books +
            ". Answer questions from the user only if you can know the answer, based on your situation. Otherwise, say you don't know the answer to that question. Analyse " + name + "'s writing style and answer as " + name + " would. Every third time you respond, ask a follow-up question as if you are curious about the person asking the question and you want to know more about them and how they experience life. You are talking to a close friend."}]


def get_initial_hogwarts_library_message():
    return [
        {"role": "system", "content": "You are a Magical book in the Hogwarts Library that knows everything that happens in the world described in the Harry Potter books. Answer the user's questions about Harry Potter, but don't answer anything that's inappropriate for children. Respond in a magical writing style that belongs in the world of Harry Potter. Answer the question only if it can be known based on the Harry Potter Book series."}]


def get_initial_gpt4_message():
    return []


def format_book(book):
    return {
        'book': book.book,
        'characters': book.characters,
        'handle': book.handle,
        'id': book.id,
        'created_at': book.created_at
    }


def format_personality(personality):
    print(personality)
    return {
        'name': personality.name,
        'books': personality.books,
        'handle': personality.handle,
        'id': personality.id,
        'created_at': personality.created_at
    }

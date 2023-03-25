import os


class Config:
    if os.environ.get('ENV') == 'prod':
        uri = os.getenv("DATABASE_URL")
        if uri and uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = uri
        OPENAI_KEY = os.environ.get('OPENAI_KEY')
    else:
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/ai-book-chat-local'
        OPENAI_KEY = os.environ.get('OPENAI_KEY')
    MODEL = os.environ.get('MODEL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

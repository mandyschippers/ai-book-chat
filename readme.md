deployment

install/update: heroku cli

Deploy w heroku ($7/month)
heroku add -a [heroku app name]

Add postgres ($5/month)
heroku addons:create heroku-postgresql:mini

env variables:
ENV (prod)
OPENAI_KEY (from openai)
MODEL (openai llm model name)
DATABASE_URL (from postgres)

db migrations https://flask-migrate.readthedocs.io:

(first time)

- flask db init

(every time there are changes to models.py including the first time)

- flask db migrate -m "message"
- flask db upgrade

Front end

- make sure that the url in constants.js matches the heroku url of the app
- Deployment: run npm run build from the client folder first

- running locally
  Backend: in main folder (not app folder) run: flask --app app run
  Frontend: in client folder run: npm start

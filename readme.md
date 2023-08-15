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

Database migration
heroku ps:exec --app=[app name]
in command line: alembic init alembic

Front end

- make sure that the url in constants.js matches the heroku url of the app

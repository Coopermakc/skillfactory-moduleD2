"""
При разворачивании задания на Хероку необходимо добавить переменную "APP_LOCATION" со значением "heroku"
Например, так
 $ heroku config:set APP_LOCATION=heroku
"""

import sentry_sdk
from bottle import route, HTTPResponse, run
from sentry_sdk.integrations.bottle import BottleIntegration

import os

sentry_sdk.init(
    dsn="https://<key>.ingest.sentry.io/<project>",  #вместо <key>  и <project>  укажите ваши данные из sentry
    integrations=[BottleIntegration()]
    )


@route("/success")
def success():
    html = """
        <!doctype html>
        <html lang="en">
        <head>
            <title>Check logs</title>
        </head>
        <body>
            <div class="container">
            <h1>Success page!</h1>
            <p class="small">Эта страница не возвращает ошибок</p>
            </div>
        </body>
        </html>
        """
    return HTTPResponse(status=200, body=html)

@route('/')
def index():
    return "Для проверки задания добавьте в адресной строке /success  для успешной страницы, а /fail для страницы с ошибкой"


@route("/fail")
def fail():
    raise RuntimeError('This is run time error')
    return HTTPResponse(status=500, body='Here error with code 500')


if os.environ.get("APP_LOCATION") == "heroku":
    run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        server="gunicorn",
        workers=3,
    )
else:
    run(host="localhost", port=8080, debug=True)
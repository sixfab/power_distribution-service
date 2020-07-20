from .urls import urls
import os
import time
from flask import Flask, session, send_file, request
from .helpers.exceptions import RetryLimitError
from . import app

SECRET_KEY = "sixfab"
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)

for methods, rule, endpoint in urls:
    app.add_url_rule(rule, endpoint.__name__, endpoint, methods=methods)


@app.before_request
def before_request_handler():
    is_service_locked = app.config.get("locked", False)

    if is_service_locked:
      if time.time() < is_service_locked:
        is_service_locked = True
      else:
        is_service_locked = False

    if is_service_locked and "/locker/release" not in request.path:
      return {"err": "Service  unavailable, locked."}, 503


@app.after_request
def after_request_handler(response):
    return response


@app.errorhandler(RetryLimitError)
def handle_retry_limit_exceed(e):
    return {"err": "retry limit"}, 503


@app.route("/docs")
def redoc():
    return """
    <!DOCTYPE html>
        <html>
          <head>
            <title>HAT API Documentation</title>
            <!-- needed for adaptive design -->
            <meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">

            <!--
            ReDoc doesn't change outer page styles
            -->
            <style>
              body {
                margin: 0;
                padding: 0;
              }
            </style>
          </head>
          <body>
            <redoc spec-url='./openapi'></redoc>
            <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"> </script>
          </body>
        </html>
    """


@app.route("/openapi")
def return_openapi():
    return send_file(os.path.dirname(os.path.realpath(__file__)) + "/openapi.yaml")

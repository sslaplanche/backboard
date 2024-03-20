import os
import json
from datetime import datetime, timedelta

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

from scripts.daily import fetch_data

from celery import Celery

app = Flask(__name__)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

## TASKS
@celery.task(bind=True)
def fetch_daily_summary(self):
    daily_summary = fetch_data()
    return daily_summary


## FRONTEND ROUTES
@app.route('/')
def index():
    return render_template('index.html')
    # return 'The time is ' + str(datetime.now())

@app.route('/daily')
def daily():
    try:
        daily_summary = fetch_daily_summary()
        return render_template('daily.html', context={'todays_players': daily_summary})
    except Exception as e:
        return render_template('error.html', context={'error': e})

## API ROUTES
@app.route('/api/daily')
def daily_api():
    daily_summary = fetch_daily_summary()
    return jsonify(daily_summary)

if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5050,
    )
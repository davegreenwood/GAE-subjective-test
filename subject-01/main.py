from google.appengine.ext import ndb
import logging
import os
import datetime
from subutils import get_media_path, get_media, buttons
from subutils import get_shuffled_idx, n_items, question_prog

from flask import Flask, render_template, request, session


app = Flask(__name__)
app.secret_key = os.urandom(24)
logger = logging.getLogger(__name__)


class Tester(ndb.Model):
    """ The ndb entity"""
    answers = ndb.JsonProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)

    def add_answer(self, media_key, answer_value):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.debug('adding answer: {}, time: {}'.format(answer_value, now))
        self.answers[media_key] = dict(answer=answer_value, time=now)
        self.put()


def set_cookie():
    if 'items' not in session:
        logger.debug('New session created.')
        items = get_shuffled_idx()
        tester = Tester(answers=dict())
        session['key'] = tester.put().urlsafe()
        session['items'] = items
        session['idx'] = 0
        session['vid'] = get_media_path(items[0])
        session['msg'] = question_prog(0)
        return
    if session['idx'] == n_items:
        logger.debug('Idx: {} equals items: {}.'.format(
            session['idx'], n_items))
        session.pop('items', None)
        session.pop('total', None)
        session.pop('idx', None)
        session['msg'] = 'Testing is complete. Thank you!!'
        session['vid'] = 'static/media/thank.mp4'
        return
    logger.debug('Index: {}'.format(session['idx']))
    session['vid'] = get_media_path(session['idx'])
    session['msg'] = question_prog(session['idx'])
    return


def put_data():
    urlsafe_key = session.get('key', None)
    items = session.get('items', None)
    idx = session.get('idx', None)
    if items is None or idx is None or urlsafe_key is None:
        return
    # collect and put data
    value = request.form['action']
    media_key = get_media(items[idx - 1])
    key = ndb.Key(urlsafe=urlsafe_key)
    tester = key.get()
    tester.add_answer(media_key, value)
    return


def increment():
    # increment session data
    put_data()
    if session.get('idx', None) is None:
        return
    session['idx'] += 1
    return


@app.route('/')
def index():
    # here we will render the main content
    set_cookie()
    return render_template('index.html',
                           title='Home',
                           b0=buttons[0],
                           b1=buttons[1],
                           vid=session['vid'],
                           msg=session['msg'])


@app.route('/submitted', methods=['POST'])
def submitted_form():
    # here we put the data to the store and go back to the index.
    increment()
    return index()


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

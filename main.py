from nltk.tokenize import sent_tokenize
from classification.ChatGPTClassifier import ChatGPTClassifier

import dbInit

from flask import Flask, request, jsonify
from flask_cors import CORS

from sqlalchemy.orm import scoped_session
from database import SessionLocal

from decorators.postData import data_required

from config import currentConfig

from models import Selector

DEFAULT_CONTENT = ''

def createApp(config):
    app = Flask(__name__)

    CORS(app, resources={r'/api/*': {'origins': '*'}})

    app.session = scoped_session(SessionLocal)
    app.config['JSON_AS_ASCII'] = config.JSON_AS_ASCII

    return app

app = createApp(currentConfig)
dbInit.initializeDb(app.session)

@app.route('/api/v0/selectors/', methods=['GET'])
def getSelectors():
    selectors = [{'url': selector.url, 'selector': selector.selector}
                 for selector in app.session.query(Selector).all()]

    return jsonify(selectors), 200

@app.route('/api/v0/selectors/', methods=['POST'])
@data_required(['url', 'selector'])
def addSelector():
    json = request.get_json(force=True)

    selector = Selector(
        url=json['url'],
        selector=json['selector'])

    app.session.add(selector)
    app.session.commit()

    return DEFAULT_CONTENT, 200

@app.route('/api/v0/classify/', methods=['POST'])
@data_required(['newsText'])
def classifyNewsText():
    json = request.get_json(force=True)

    newsSentences = sent_tokenize(json['newsText'])

    classifier = ChatGPTClassifier()
    classifications = classifier.classifySentences(newsSentences)

    result = [{'sentenceLength': len(sentence),
               'opinionLevel': classification}
              for sentence, classification
              in zip(newsSentences, classifications)]

    return jsonify(list(result)), 200


@app.teardown_appcontext
def removeSession(*args, **kwargs):
    app.session.remove()

if __name__ == '__main__':
    app.run(debug=True)
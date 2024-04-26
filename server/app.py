#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    for article in Article.query.all():
        article_dict = article.to_dict()
        return make_response(article_dict, 200)

max_pageviews = 3
@app.route('/articles/<int:id>')
def show_article(id):
    if 'page_views' not in session:
        session['page_views'] = 0

    session['page_views'] += 1
    article = Article.query.filter(Article.id == id).first()

    if article == None:
        return make_response({
            "error": f"Article {id} not found"
        }, 404)

    if session['page_views'] <= max_pageviews:
        article_dict = article.to_dict()
        response = make_response(article_dict, 200)
        return response
    else:
        return make_response({
            "message": "Maximum pageview limit reached"
        }, 401)




if __name__ == '__main__':
    app.run(port=5555)

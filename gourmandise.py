from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from waitress import serve

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://gourmand:GourmandPassword@db.aws.gop.onl/gourmand'
db = SQLAlchemy(app)

class Gourmand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    vote = db.Column(db.Float, default=0.0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api', methods=['GET'])
def hello_world():
    posts = ['get 2 random gourmandises', "https://gourmandise.gopnik.net/api/get_random_posts", 'post vote', "https://gourmandise.gopnik.net/api/increment_vote", 'post gourmandise', "https://gourmandise.gopnik.net/api/increment_vote"]
    return jsonify(posts)

@app.route('/api/add_post', methods=['POST'])
def add_post():
    content = request.json.get('content')
    new_post = Gourmand(content=content)
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post added successfully'})

@app.route('/api/increment_vote', methods=['POST'])
def increment_vote():
    post_id = request.json.get('id')
    post = Gourmand.query.filter_by(id=post_id).first()
    if post:
        post.vote += 1
        db.session.commit()
        return jsonify({'message': 'Vote incremented successfully'})
    else:
        return jsonify({'error': 'Post not found'})

@app.route('/api/get_random_posts', methods=['GET'])
def get_random_posts():
    random_posts = Gourmand.query.order_by(func.rand()).limit(2).all()
    posts = [{'id': post.id, 'content': post.content, 'vote': post.vote} for post in random_posts]
    return jsonify(posts)

if __name__ == '__main__':
    app.run(debug=True)
    #serve(app, host='0.0.0.0', port=5000)

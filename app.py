from flask import Flask, jsonify, request, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder = basedir + '/public/')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + \
    os.path.join(basedir, 'DB.db')
app.config['SQLALCHEMY_ DATABASE_URI'] = False
db = SQLAlchemy(app)


class Confessions(db.Model):
    """
    Takes two parameters:
    @name: String
    @message: String
    """
    __tablename__ = 'confessions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    message = db.Column(db.String(256))

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/<path:path>')
def send_file(path):
    return send_from_directory(basedir+'/public/', path)

@app.route('/api/get', methods=['GET'])
def get_confession():
    messages = Confessions.query.all()
    messages_tuple = tuple(map(lambda confession: {
        'name': confession.name,
        'title': confession.message
    }, messages))
    return jsonify(messages_tuple), 200


@app.route('/api/post', methods=['POST'])
def post_confession():
    name = request.json.get('name')
    message = request.json.get('message')
    if name is None or message is None:
        return jsonify({"status": "Name or message cannot be blank"}), 400
    confess = Confessions(name=name, message=message)
    db.session.add(confess)
    db.session.commit()
    return jsonify({"status": "Confession added successfully!"}), 201


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

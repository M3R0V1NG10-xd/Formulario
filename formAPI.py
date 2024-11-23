import os
import pymysql
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://root:66HyCUgAA37X0KjCKMPVhBBD0Fiz4Bx0@dpg-csvcenbtq21c73empopg-a.oregon-postgres.render.com/formdb_6ik0'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        try:
            new_user = User(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User login saved successfully"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    return render_template('login.html')

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id, 
        'email': user.email, 
        'created_at': user.created_at
    } for user in users]), 200

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/redirect')
def redirect():
    return render_template('redirect.html')

@app.route('/redirect2')
def redirect2():
    return render_template('redirect2.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/redirect3')
def redirect3():
    return render_template('redirect3.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
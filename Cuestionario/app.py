from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/db_name'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())

class Pregunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.Enum('Activo', 'Reflexivo', 'Teórico', 'Pragmático'), nullable=False)

class OpcionRespuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Integer, nullable=False)

class Respuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_pregunta = db.Column(db.Integer, db.ForeignKey('pregunta.id'), nullable=False)
    id_opcion = db.Column(db.Integer, db.ForeignKey('opcion_respuesta.id'), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        # Save responses to database
        pass
    preguntas = Pregunta.query.all()
    return render_template('survey.html', preguntas=preguntas)

@app.route('/results')
def results():
    # Calculate learning style and generate spider chart
    return render_template('results.html', plot_url=generate_spider_chart())

def generate_spider_chart():
    # Calculate results and create spider chart
    return plot_url

if __name__ == '__main__':
    app.run(debug=True)

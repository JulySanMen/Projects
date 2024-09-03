from flask import Flask, render_template, request, redirect, url_for
import pymysql
import matplotlib.pyplot as plt
import numpy as np


app = Flask (__name__)

# Configuración de la base de datos
def obtener_conexion():
    return pymysql.connect(host='localhost', user='root', password='', db='cuestionario')     

# Página de inicio que muestra el cuestionario
@app.route('/')
def index():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM preguntas")
    preguntas = cursor.fetchall()
    conn.close()
    return render_template('index.html', preguntas=preguntas)

# Guardar respuestas en la base de datos
@app.route('/guardar_respuestas', methods=['POST'])
def guardar_respuestas():
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    
    cursor.execute("INSERT INTO participantes (nombre, correo) VALUES (%s, %s)", (nombre, correo))
    participante_id = cursor.lastrowid
    
    for key, value in request.form.items():
        if key.startswith('respuesta'):
            pregunta_id = int(key.split('_')[1])
            respuesta = int(value)
            cursor.execute("INSERT INTO respuestas (participante_id, pregunta_id, respuesta) VALUES (%s, %s, %s)",
                           (participante_id, pregunta_id, respuesta))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('graficar', participante_id=participante_id))

# Graficar resultados en gráfico de araña
@app.route('/graficar/<int:participante_id>')
def graficar(participante_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT preguntas.estilo, AVG(respuestas.respuesta) AS promedio
    FROM respuestas
    JOIN preguntas ON respuestas.pregunta_id = preguntas.id
    WHERE respuestas.participante_id = %s
    GROUP BY preguntas.estilo
    """, (participante_id,))
    
    resultados = cursor.fetchall()
    conn.close()

    estilos = [fila[0] for fila in resultados]
    valores = [fila[1] for fila in resultados]

    etiquetas = ['Activo', 'Reflexivo', 'Teórico', 'Pragmático']
    valores_completos = [valores[estilos.index(etiqueta)] if etiqueta in estilos else 0 for etiqueta in etiquetas]
    valores_completos += valores_completos[:1]
    angulos = np.linspace(0, 2 * np.pi, len(etiquetas), endpoint=False).tolist()
    angulos += angulos[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angulos, valores_completos, color='blue', alpha=0.25)
    ax.plot(angulos, valores_completos, color='blue', linewidth=2)
    ax.set_yticklabels([])
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(etiquetas)

    plt.savefig('static/resultado.png')
    plt.close()

    return render_template('graficar.html', imagen='resultado.png')

if __name__ == '__main__':
    app.run(debug=True)

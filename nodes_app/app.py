from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def home():
    role = "admin"
    notes = ["Note 1", "Note 2", "Note 3"]
    return render_template('home.html', role=role, notes=notes)

@app.route('/acerca-de')
def about():
    return "This is a simple Flask application."

@app.route('/contacto', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        return "Formulario enviado correctamente.", 201
    return "Contact us at"

@app.route('/api/info')
def api_info():
    data = {
        "name": "FlaskApp",
        "version": "1.0",
        "description": "A simple Flask application"
    }
    return jsonify(data), 200

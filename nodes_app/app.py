from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

import os
from flask_sqlalchemy import SQLAlchemy

DB_FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    'notes.sqlite')

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_FILE_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Note {self.id}: {self.title}>"
    

# app.config["SQLALCHEMY_ECHO"] = True
# print("DB_FILE_PATH ->", DB_FILE_PATH)


# @app.before_first_request
# def create_tables():
#     db.create_all()


# @app.route('/')
# def home():
#     notes = [
#         {
#             "title": "Titulo de prueba",
#             "content": "Contenido de prueba"
#         }
#     ]
#     return render_template('home.html', notes=notes)

@app.route('/')
def home():
    notes = Note.query.order_by(Note.id.desc()).all()
    return render_template('home.html', notes=notes)



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

@app.route('/confirmation')
def confirmation():
    return "Formulario enviado correctamente."

@app.route('/api/notes', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        title = request.form.get('title', '')
        content = request.form.get('content', '')

        note_db = Note(title=title, content=content)

        db.session.add(note_db)
        db.session.commit()


        # print(f"Nota recibida: {note_db}")
        return redirect(url_for('home'))
    return render_template('note_form.html', note=None)

@app.route('/editar-nota/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    note = Note.query.get_or_404(id)
    if request.method == 'POST':
        title = request.form.get('title', '')
        content = request.form.get('content', '')

        note.title = title
        note.content = content

        db.session.commit()

        return redirect(url_for('home'))

    return render_template('edit_note.html', note=note)

@app.route('/eliminar-nota/<int:id>', methods=['POST'])
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('home'))
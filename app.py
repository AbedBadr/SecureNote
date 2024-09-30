from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///note.db'
db = SQLAlchemy(app)

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<Task %r' % self.id

@app.route("/", methods=['POST', 'GET'])
#@app.route("/index", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        note_title = request.form['title']
        note_content = request.form['content']
        new_note = Notes(title=note_title, content=note_content)

        try:
            db.session.add(new_note)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your note'

    else:
        notes = Notes.query.order_by(Notes.date_created).all()
        return render_template('index.html', notes=notes)

if __name__ == "__main__":
    app.run(debug=True)
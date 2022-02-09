from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases/contacts.db'
db = SQLAlchemy(app)

class Contact(db.Model):
    id_contact = db.Column(db.INT(), primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(200), nullable=False)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)


@app.route('/add_contact', methods=['POST', 'GET'])
def add_contact():
    new_contact = Contact(
        name = request.form['name-contact'],
        email = request.form['email-contact'])
    try:
        db.session.add(new_contact)
        db.session.commit()
        return redirect('/')
    except:
        return 'DB Error for creating'


@app.route('/delete/<int:id>')
def delete(id):
    try:
        Contact.query.filter_by(id_contact=id).delete()
        db.session.commit()
        return redirect('/')
    except:
        return 'DB Error for delete'
    
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    edit_contact = Contact.query.filter_by(id_contact=id).first()

    if request.method == 'POST':
        try:
            edit_contact.name = request.form['name-contact']
            edit_contact.email = request.form['email-contact']
            db.session.commit()
            return redirect('/')
        except:
            return 'DB Error for creating'
    else:
        return render_template('update.html', contact=edit_contact)


if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(120), unique=True, nullable=False)
    author = db.Column(db.String(40))
    publisher = db.Column(db.String(40))

    def __repr__(self):
        return f"{self.book_name} by {self.author}"


@app.route('/')
def index():
    return 'My API homepage!'

@app.route('/books')
def get_books():
    books = Book.query.all()

    output = []
    for book in books:
        book_data = {'Title': book.book_name, 'Author': book.author, 'Publisher': book.publisher}

        output.append(book_data)

    return {"Books": output}

@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {'Title': book.book_name, 'Author': book.author, 'Publisher': book.publisher}

@app.route('/books', methods=['POST'])
def add_book():
    book = Book(book_name=request.json['Title'], author=request.json['Author'], publisher=request.json['Publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}

@app.route('/books/<id>')
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"Book": "Not found"}
    db.session.delete(book)
    db.session.commit()
    return {"Book": "Deleted"}
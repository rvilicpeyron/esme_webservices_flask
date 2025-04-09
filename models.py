from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class StudentBook(db.Model):
    __tablename__ = 'student_book'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime)

    # Relationships back to Student and Book
    student = db.relationship("Student", back_populates="student_books")
    book = db.relationship("Book", back_populates="student_books")


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_at = db.Column(db.DateTime)

    # Relationship to StudentBook
    student_books = db.relationship("StudentBook", back_populates="book")

    # Convenient access to borrowers (viewonly to avoid conflict)
    borrowers = db.relationship("Student", secondary="student_book", viewonly=True)


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    birth_date = db.Column(db.DateTime)

    # Relationship to StudentBook
    student_books = db.relationship("StudentBook", back_populates="student")

    # Convenient access to books
    borrowed_books = db.relationship("Book", secondary="student_book", viewonly=True)


    
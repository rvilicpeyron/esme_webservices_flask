from flask import Blueprint, request, jsonify
from models import db, Student, Book
from datetime import datetime

students_bp = Blueprint('students', __name__)

# Ajouter un étudiant
@students_bp.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    new_student = Student(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        birth_date=datetime.strptime(data['birth_date'], '%Y-%m-%d')
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student added", "id": new_student.id}), 201

# Récupérer tous les étudiants
@students_bp.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{
        'id': s.id, 'first_name': s.first_name, 'last_name': s.last_name,
        'email': s.email, 'birth_date': s.birth_date.strftime('%Y-%m-%d'),
        'books': [{'id': b.id, 'title': b.title} for b in s.books]
    } for s in students])

# Récupérer un étudiant par ID
@students_bp.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify({
        'id': student.id, 'first_name': student.first_name, 'last_name': student.last_name,
        'email': student.email, 'birth_date': student.birth_date.strftime('%Y-%m-%d'),
        'books': [{'id': b.id, 'title': b.title} for b in student.books]
    })

# Modifier un étudiant
@students_bp.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.get_json()

    student.first_name = data.get('first_name', student.first_name)
    student.last_name = data.get('last_name', student.last_name)
    student.email = data.get('email', student.email)
    if 'birth_date' in data:
        student.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d')

    db.session.commit()
    return jsonify({"message": "Student updated"})

# Supprimer un étudiant
@students_bp.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted"})

# Associer un livre à un étudiant
@students_bp.route('/students/<int:student_id>/borrow/<int:book_id>', methods=['POST'])
def borrow_book(student_id, book_id):
    student = Student.query.get_or_404(student_id)
    book = Book.query.get_or_404(book_id)

    student.books.append(book)
    db.session.commit()
    return jsonify({"message": f"Book {book.title} borrowed by {student.first_name}"})

# Désassocier un livre d’un étudiant
@students_bp.route('/students/<int:student_id>/return/<int:book_id>', methods=['POST'])
def return_book(student_id, book_id):
    student = Student.query.get_or_404(student_id)
    book = Book.query.get_or_404(book_id)

    if book in student.books:
        student.books.remove(book)
        db.session.commit()
        return jsonify({"message": f"Book {book.title} returned by {student.first_name}"})
    return jsonify({"error": "Book not borrowed"}), 400


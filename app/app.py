from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin123@localhost/student_management4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Student model
class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    course = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Student('{self.name}', '{self.age}', '{self.course}')"

# Route for the home page to display the list of students
@app.route('/')
def home():
    students = Students.query.all()  # Fetch all student records
    return render_template('index.html', students=students)

# Route to add a new student
@app.route('/add', methods=['POST'])
def add():
    forName = request.form['name']
    forAge = request.form['age']
    forCourse = request.form['course']

    # Create a new Student record
    newStudent = Students(name=forName, age=forAge, course=forCourse)
    db.session.add(newStudent)
    db.session.commit()
    return redirect(url_for('home'))

# Route to edit an existing student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    std = Students.query.get_or_404(id)
    if request.method == 'POST':
        std.name = request.form['name']
        std.age = request.form['age']
        std.course = request.form['course']
        db.session.commit()
        return redirect(url_for('home'))
    
    return render_template('edit.html', student=std)

# Route to delete a student
@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    std = Students.query.get_or_404(id)
    db.session.delete(std)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

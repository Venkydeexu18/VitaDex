from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from flask_sqlalchemy import SQLAlchemy
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from itertools import product
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

instance_path = os.path.join(app.root_path, 'instance')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_path, "database.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if not os.path.exists(instance_path):
    os.makedirs(instance_path)

db = SQLAlchemy(app)

class User(db.Model):
    email = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(20))
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(10))
    blood_group = db.Column(db.String(10))
    date_of_birth = db.Column(db.String(20))

class Health(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thalach = db.Column(db.Float)
    trestbps = db.Column(db.Float)
    chol = db.Column(db.Float)
    email = db.Column(db.String(50), db.ForeignKey('user.email'))

with app.app_context():
    db.create_all()
    
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

questions = [
        {
            'question': "Enter Your Age",
            'field_name': 'age',
            'input_type': 'number',
            'options': []
        },
        {
            'question': "Select Gender",
            'field_name': 'sex',
            'input_type': 'select',
            'options': [
                {'value': '', 'label': 'Select Gender'},
                {'value': '1', 'label': 'Male'},
                {'value': '0', 'label': 'Female'}
            ]
        },
        {
            'question': "Select Chest Pain Type (cp)",
            'field_name': 'cp',
            'input_type': 'select',
            'options': [
                {'value': '', 'label': 'Select Chest Pain Type (cp)'},
                {'value': '0', 'label': 'Typical Angina (No pain)'},
                {'value': '1', 'label': 'Atypical Angina'},
                {'value': '2', 'label': 'Non Anginal Pain'},
                {'value': '3', 'label': 'Asymptomatic'}
            ]
        },
        {
            'question': "Enter Resting Blood Pressure (mm Hg)(trestbps)",
            'field_name': 'trestbps',
            'input_type': 'number',
            'options': []
        },
        {
            'question': "Enter Serum Cholestoral (mg/dl)(chol)",
            'field_name': 'chol',
            'input_type': 'number',
            'options': []
        },
        {
            'question': "Fasting Blood Sugar > 120 (mg/dl)(fbs)",
            'field_name': 'fbs',
            'input_type': 'select',
            'options': [
                {'value': '', 'label': 'Fasting Blood Sugar > 120 (mg/dl)(fbs)'},
                {'value': '1', 'label': 'Yes'},
                {'value': '0', 'label': 'No'}
            ]
        },
        {
            'question': "Resting Electrocardiographic Results (restecg)",
            'field_name': 'restecg',
            'input_type': 'select',
            'options': [
                {'value': '', 'label': 'Resting Electrocardiographic Results (restecg)'},
                {'value': '0', 'label': 'Normal'},
                {'value': '1', 'label': 'Abnormal'},
                {'value': '2', 'label': 'Probable'}
            ]
        },
        {
            'question': "Enter Maximum Heart Rate Achieved (thalach)",
            'field_name': 'thalach',
            'input_type': 'number',
            'options': []
        },
        {
            'question': "Select Exercise Induced Angina (exang)",
            'field_name': 'exang',
            'input_type': 'select',
            'options': [
                {'value': '', 'label': 'Select Exercise Induced Angina (exang)'},
                {'value': '1', 'label': 'Yes'},
                {'value': '0', 'label': 'No'}
            ]
        },
        {
            'question': "Enter Your Oldpeak (oldpeak)",
            'field_name': 'oldpeak',
            'input_type': 'text',
            'options': []
        },
        {
            'question': "Select Peak Exercise ST Segment (Slope)",
            'field_name': 'slope',
            'input_type': 'select',
            'options': [
                {'value': '', 'label': 'Select Peak Exercise ST Segment (Slope)'},
                {'value': '0', 'label': 'Upsloping'},
                {'value': '1', 'label': 'Flat'},
                {'value': '2', 'label': 'Downsloping'}
            ]
        },
        {
            'question': "Number of Major Vessels (ca)",
            'field_name': 'ca',
            'input_type': 'select',
            'options': [
                {'value': '', 'label': 'Number of Major Vessels (ca)'},
                {'value': '0', 'label': 'Zero'},
                {'value': '1', 'label': 'One'},
                {'value': '2', 'label': 'Two'},
                {'value': '3', 'label': 'Three'},
                {'value': '4', 'label': 'Four'}
            ]
        },
        {
            'question': "Select Thal Type (thal)",
            'field_name': 'thal',
            'input_type': 'select',
            'options': [
                {'value': '', 'label': 'Select Thal Type (thal)'},
                {'value': '0', 'label': 'Normal'},
                {'value': '1', 'label': 'Fixed'},
                {'value': '2', 'label': 'Defect'},
                {'value': '3', 'label': 'Reversible'}
            ]
        },
    ]

dquestions = [
    {
        'question': "Number of Pregnancies:",
        'field_name': 'pregnancies',
        'input_type': 'number',
        'options': []
    },
    {
        'question': "Glucose Level:",
        'field_name': 'glucose',
        'input_type': 'number',
        'options': []
    },
    {
        'question': "Blood Pressure:",
        'field_name': 'blood_pressure',
        'input_type': 'number',
        'options': []
    },
    {
        'question': "Skin Thickness:",
        'field_name': 'skin_thickness',
        'input_type': 'number',
        'options': []
    },
    {
        'question': "Insulin Level:",
        'field_name': 'insulin',
        'input_type': 'number',
        'options': []
    },
    {
        'question': "BMI (Body Mass Index):",
        'field_name': 'bmi',
        'input_type': 'number',
        'options': []
    },
    {
        'question': "Diabetes Pedigree Function:",
        'field_name': 'diabetes_pedigree',
        'input_type': 'number',
        'options': []
    },
    {
        'question': "Age:",
        'field_name': 'age',
        'input_type': 'number',
        'options': []
    }
]
squestions = [
    {
        'question': "Do you have a cough?",
        'field_name': 'cough',
        'input_type': 'select',
        'options': [
            {'value': '1', 'label': 'Yes'},
            {'value': '0', 'label': 'No'}
        ]
    },
    {
        'question': "Do you have a fever?",
        'field_name': 'fever',
        'input_type':  'select',
        'options': [
            {'value': '1', 'label': 'Yes'},
            {'value': '0', 'label': 'No'}
        ]
    },
    {
        'question': "Do you have a sore throat?",
        'field_name': 'sore_throat',
        'input_type': 'select',
        'options': [
            {'value': '1', 'label': 'Yes'},
            {'value': '0', 'label': 'No'}
        ]
    },
    {
        'question': "Do you have difficulty breathing?",
        'field_name': 'difficulty_breathing',
        'input_type':  'select',
        'options': [
            {'value': '1', 'label': 'Yes'},
            {'value': '0', 'label': 'No'}
        ]
    },
    {
        'question': "Do you have fatigue?",
        'field_name': 'fatigue',
        'input_type':  'select',
        'options': [
            {'value': '1', 'label': 'Yes'},
            {'value': '0', 'label': 'No'}
        ]
    },
    {
        'question': "Do you have body aches?",
        'field_name': 'body_aches',
        'input_type':  'select',
        'options': [
            {'value': '1', 'label': 'Yes'},
            {'value': '0', 'label': 'No'}
        ]
    },
    {
        'question': "Do you have loss of taste/smell?",
        'field_name': 'loss_of_taste_smell',
        'input_type': 'select',
        'options': [
            {'value': '1', 'label': 'Yes'},
            {'value': '0', 'label': 'No'}
        ]
    },
    {
        'question': "Do you have a headache?",
        'field_name': 'headache',
        'input_type':  'select',
        'options': [
            {'value': '1', 'label': 'Yes'},
            {'value': '0', 'label': 'No'}
        ]
    },
    {
        'question': "Do you have diarrhea?",
        'field_name': 'diarrhea',
        'input_type':  'select',
        'options': [
            {'value': '1', 'label': 'Yes'},
            {'value': '0', 'label': 'No'}
        ]
    }
]

current_question_index = 0
user_answers = {} 


@app.route('/')
def home():
    user = None
    if 'email' in session:
        email = session['email']
        user = User.query.filter_by(email=email).first()
    if user:
        name = user.name
        return render_template('base.html', name=name)
    return render_template('base.html')
@app.route('/diseases', methods=['GET', 'POST'])
def all():
    return render_template('diagnose.html')


@app.route('/heart_disease', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        current_question = int(request.form.get('current_question', 0))
        if current_question < len(questions):
            field_name = questions[current_question]['field_name']
            answer = request.form.get(field_name)
            user_answers[field_name] = answer
            current_question += 1

        if current_question >= len(questions):
            user = User()
            df = pd.read_csv('heart.csv')
            features = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach',
                        'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']
            df = df[features]
            X = df.iloc[:, :-1].values
            y = df.iloc[:, -1].values
            scaler = StandardScaler()
            X = scaler.fit_transform(X)
            knn = KNeighborsClassifier(n_neighbors=5)
            knn.fit(X, y)
            user_data = [float(user_answers[question['field_name']]) for question in questions]
            email = session['email']
            health_data = Health.query.filter_by(email=email).first()
            if health_data:
                health_data.thalach = user_data[7]
                health_data.trestbps = user_data[3]
                health_data.chol = user_data[4]
            else:
                health_data = Health(email=email, thalach=user_data[7], trestbps=user_data[3], chol=user_data[4])

            db.session.add(health_data)
            db.session.commit()
            pred_args = scaler.transform([user_data])
            proba = knn.predict_proba(pred_args)
            if y[proba.argmax()] == 1 and proba.max() >= 0.7:
                blast = 0
                res = "You already have heart disease."
            elif proba.max() >= 0.7:
                blast = 0
                res = "You'll likely develop heart disease in the future."
            else:
                blast = 1
                res = "You don't have heart disease."
            return render_template('index.html', data="Heart Disease", res=res, blast = blast)

        return render_template('heart_disease.html', question=questions[current_question], current_question=current_question)
    
    return render_template('heart_disease.html', question=questions[0], current_question=0)

@app.route('/diabetes', methods=['GET', 'POST'])
@login_required
def diabetes():
    if request.method == 'POST':
        current_question = int(request.form.get('current_question', 0))
        if current_question < len(dquestions):
            field_name = dquestions[current_question]['field_name']
            answer = request.form.get(field_name)
            user_answers[field_name] = answer
            current_question += 1

        if current_question >= len(dquestions):
            df = pd.read_csv('diabetes.csv')
            X = df.iloc[:, :-1].values
            y = df.iloc[:, -1].values
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            knn = KNeighborsClassifier(n_neighbors=3)
            knn.fit(X_train, y_train)
            user_data = [float(user_answers[question['field_name']]) for question in dquestions]
            email = session['email']

            health_data = Health.query.filter_by(email=email).first()
            if health_data:
                health_data.thalach = user_data[0]
                health_data.trestbps = user_data[1]
                health_data.chol = user_data[2]
            else:
                health_data = Health(email=email, thalach=user_data[0], trestbps=user_data[1], chol=user_data[2])
            db.session.add(health_data)
            db.session.commit()
            X_new = [user_data]
            prediction = knn.predict(X_new)
            if prediction[0] == 1:
                blast = 0
                res = "You may have diabetes."
            else:
                blast = 1
                res = "You don't have diabetes."
            return render_template('index.html', data="Diabetes", res=res, blast = blast)

        return render_template('diabetes.html', question=dquestions[current_question], current_question=current_question)
    
    return render_template('diabetes.html', question=dquestions[0], current_question=0)

@app.route('/covid', methods=['GET', 'POST'])
@login_required
def covid():
    if request.method == 'POST':
        current_question = int(request.form.get('current_question', 0))
        if current_question < len(squestions):
            field_name = squestions[current_question]['field_name']
            answer = request.form.get(field_name)
            user_answers[field_name] = answer
            current_question += 1

        if current_question >= len(squestions):
            symptoms = [
                'Cough',
                'Fever',
                'Sore throat',
                'Difficulty breathing',
                'Fatigue',
                'Body aches',
                'Loss of taste/smell',
                'Headache',
                'Diarrhea'
            ]

            all_combinations = list(product([0, 1], repeat=len(symptoms)))
            X_train = [list(combination) for combination in all_combinations]
            y_train = ['COVID-19' if sum(combination) >= 4 else 'No COVID-19' for combination in all_combinations]
            knn = KNeighborsClassifier(n_neighbors=3)
            knn.fit(X_train, y_train)
            user_data = [float(user_answers[question['field_name']]) for question in squestions]
            X_new = [user_data]
            prediction = knn.predict(X_new)
            if prediction[0] == 'COVID-19':
                blast = 0
                res = "You've COVID-19 or may have it in the future."
            else:
                blast = 1
                res = "You don't have COVID-19 or are at a low risk."
            print(blast)
            return render_template('index.html', data="Covid-19", res=res, blast=blast)

        return render_template('covid.html', question=squestions[current_question], current_question=current_question)
    
    return render_template('covid.html', question=squestions[0], current_question=0)


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def edit_profile():
    email = session.get('email')
    user = User.query.filter_by(email=email).first()

    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.gender = request.form['gender']
        user.phone = request.form['phone']
        user.blood_group = request.form['blood_group']
        user.age = request.form['age']
        user.date_of_birth = request.form['date_of_birth']
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit_profile.html', user=user)

@app.route('/dashboard')
@login_required
def dashboard():
    email = session.get('email')
    user = User.query.filter_by(email=email).first()
    health_data = Health.query.filter_by(email=email).all()
    return render_template('dashboard.html', user=user, health_data=health_data)

@app.route('/support')
@login_required
def support():
    return render_template('contact.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            error = 'Email already exists. Please choose a different email.'
            return render_template('login.html', error=error)

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        session['email'] = email
        session['name'] = name
        session['password'] = password
        return redirect(url_for('home'))

    return render_template('login.html')

def authenticate_user(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return user.name 
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user:
            if user.password == password:
                session['email'] = email
                name = authenticate_user(email)
                if name is not None:
                    session['name'] = name
                return redirect(url_for('home'))
            else:
                error = "Invalid password. Please try again."
        else:
            error = "Email is not registered with us. Please try again."

    return render_template('login.html', error=error)
@app.route('/forgot')
def forgot():
    return render_template('startup.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            error = "Passwords do not match. Please try again."
            return render_template('forgot_password.html', error=error)

        user = User.query.filter_by(email=email).first()

        if user:
            user.password = password
            db.session.commit()
            return redirect(url_for('login'))
        else:
            error = "User not found. Please try again."
            return render_template('forgot_password.html', error=error)

    return render_template('forgot_password.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

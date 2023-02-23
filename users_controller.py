from flask import render_template, redirect, request, session, flash
from flask_app import app

#Importamos Modelo
from flask_app.models.users import User
from flask_app.models.citas import Cita

#Importación de BCrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    #Validamos la info que recibimos
    if not User.valida_usuario(request.form):
        return redirect('/')
    
    #Guardar registro
    pwd = bcrypt.generate_password_hash(request.form['password']) 

    #Creamos un diccionario con todos los datos del request.form

    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }

    id = User.save(formulario)

    session['user_id'] = id

    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    #Verificamos que el email exista en la Base de datos
    user = User.get_by_email(request.form) 

    if not user:
        flash('E-mail no encontrado', 'inicio_sesion')
        return redirect('/')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password incorrecto', 'inicio_sesion')
        return redirect('/')

    session['user_id'] = user.id 
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario)

    citas = Cita.get_all()

    return render_template('dashboard.html', user=user, citas=citas)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
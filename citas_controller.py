from flask import render_template, redirect, session, request, flash
from flask_app import app

#Importación de modelos
from flask_app.models.users import User
from flask_app.models.citas import Cita

@app.route('/new/cita')
def new_cita():
    #se comprueba si el usuario inició sesión

    if 'user_id' not in session:
        return redirect('/')

    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario)

    return render_template('new_cita.html', user=user)

@app.route('/create/cita', methods=['POST'])
def create_cita():
    if 'user_id' not in session:
        return redirect('/')
    
    #Validación de Cita
    if not Cita.valida_cita(request.form):
        return redirect('/new/cita')
    
    #Guardar cita
    Cita.save(request.form)

    return redirect('/dashboard')

@app.route('/edit/cita/<int:id>')
def edit_cita(id):
    if 'user_id' not in session:
        return redirect('/')

    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario)

    formulario_calificacion = {"id": id}
    cita = Cita.get_by_id(formulario_calificacion)

    return render_template('edit_cita.html', user=user, cita=cita)

@app.route('/update/cita', methods=['POST'])
def update_cita():
    if 'user_id' not in session:
        return redirect('/')
    
    #Validación de Cita
    if not Cita.valida_cita(request.form):
        return redirect('/edit/cita/'+request.form['id']) 
    
    Cita.update(request.form)

    return redirect('/dashboard')

@app.route('/delete/cita/<int:id>')
def delete_cita(id):
    if 'user_id' not in session:
        return redirect('/')

    formulario = {"id": id}
    Cita.delete(formulario)

    return redirect('/dashboard')
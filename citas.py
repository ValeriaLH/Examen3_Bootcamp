from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 

from datetime import datetime  #Manipular fechas

class Cita:

    def __init__(self, data):
        self.id = data['id']
        self.task = data['task']
        self.date = data['date']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @staticmethod
    def valida_cita(formulario):
        es_valido = True

        if formulario['task'] == '':
            flash('Cita no puede ser vacío', 'citas')
            es_valido = False
        
        if formulario['date'] == '':
            flash('Ingrese una fecha', 'citas')
            es_valido = False
        else:
            fecha_obj = datetime.strptime(formulario['date'], '%Y-%m-%d') 
            hoy = datetime.now() #Me da la fecha de hoy
            if fecha_obj < hoy:
                flash('La fecha debe ser en futuro', 'citas')
                es_valido = False
        
        if formulario['status'] == '':
            flash('Status no puede ser vacío', 'citas')
            es_valido = False
        
        return es_valido
    

    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO citas (task, date, status, user_id) VALUES (%(task)s, %(date)s, %(status)s, %(user_id)s)"
        result = connectToMySQL('citas').query_db(query, formulario)
        return result
    

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM citas"
        results = connectToMySQL('citas').query_db(query) 
        citas = []

        for cita in results:
            citas.append(cls(cita)) 
        
        return citas

    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT * FROM citas WHERE id = %(id)s"
        result = connectToMySQL('citas').query_db(query, formulario)
        cita = cls(result[0])
        return cita
    
    @classmethod
    def update(cls, formulario):
        query = "UPDATE citas SET task=%(task)s, date=%(date)s, status=%(status)s, user_id=%(user_id)s WHERE id=%(id)s"
        result = connectToMySQL('citas').query_db(query, formulario)
        return result
    

    @classmethod
    def delete(cls, formulario):
        query = "DELETE FROM citas WHERE id = %(id)s"
        result = connectToMySQL('citas').query_db(query, formulario)
        return result
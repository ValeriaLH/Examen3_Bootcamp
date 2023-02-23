#importar flask
from flask import Flask

#Inicializar app
app = Flask(__name__)

#Declarar llave secreta - se utilza cuando existe una sesión
app.secret_key = "LLave secreta"
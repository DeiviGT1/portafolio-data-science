from flask import Flask, render_template, request, redirect, url_for
from webscrapping import WebScrapping
from analysis import marcadores
import pandas as pd
import jsonpickle
import time
import json
import operator

app = Flask(__name__, template_folder='./templates', static_folder='./static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

lista_equipos = json.loads(open('./info/teams.json', encoding="utf8").read())


@app.route('/')
def index():
  
  data = json.loads(open('./info/json_resultados_historicos.json').read())["json_resultados_historicos"]
  partidos = marcadores(data, lista_equipos)
  version_number = int(time.time())
  resultados = {"resultados"  : partidos}


  return render_template('index.html', resultados=resultados, version = version_number)

@app.route('/resultados/<team>', methods=['GET'])
def historial(team):
  
  data = json.loads(open('./info/json_resultados_historicos.json').read())["json_resultados_historicos"]
  try:
    data = [x for x in data if x["id"] == team]
  except:
    return "Equipo no valido"
  
  version_number = int(time.time())
  return render_template('historico.html', data=data, version = version_number)


if __name__ == '__main__':
  app.run(host='localhost', port=5000, debug=True, use_reloader=True)
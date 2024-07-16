import pandas as pd
import numpy as np
import json

def resultados_inicial(ganador):
    if ganador == "Independiente Medellín":
        return {"partidos_ganados": 0,
                "partidos_perdidos": 1,
                "partidos_empatados": 0}
    elif ganador == "Empate":
        return {"partidos_ganados": 0,
                "partidos_perdidos": 0,
                "partidos_empatados": 1}
    else:
        return {"partidos_ganados": 1,
                "partidos_perdidos": 0,
                "partidos_empatados": 0}

def marcadores(data, lista_equipos):
  data = json.loads(open('./info/json_resultados_historicos.json').read())["json_resultados_historicos"]
  partidos ={}
  dict_=[]
  for i in data:
    ganador = i["ganador"]
    rival = i["rival"]
    escudo = lista_equipos[rival]
    if rival not in partidos:
      partidos[rival] = {"escudo":escudo,
                         "resultados" : resultados_inicial(ganador),
                         "partidos_totales": sum(resultados_inicial(ganador).values())}
    else:
      partidos[rival]["resultados"]["partidos_ganados"] += resultados_inicial(ganador)["partidos_ganados"]
      partidos[rival]["resultados"]["partidos_perdidos"] += resultados_inicial(ganador)["partidos_perdidos"]
      partidos[rival]["resultados"]["partidos_empatados"] += resultados_inicial(ganador)["partidos_empatados"]
      partidos[rival]["partidos_totales"] += sum(resultados_inicial(ganador).values())
    
  return partidos
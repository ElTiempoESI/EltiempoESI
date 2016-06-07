#!/usr/bin/env python

#Incluir los archivos de cabecera
import twitter
import urllib2
import io
import json
import time
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt

#Iniciar sesion
#Boot es variable global de la aplicacion
#postcondicion: creacion de un objeto boot de la API de Twitter

CONSUMER_KEY = '1ltYgYB7IkET9aR6JxklqBG7D'
CONSUMER_SECRET = 'JyLPQWLggNcRbZZc3zzlAXrPyTeXAeDgXSkfB2IaaYu7T7vVIU'
OAUTH_TOKEN = '739172777077448711-TnwwmloLvrrj99FYN3jP6pQiaBsS90m'
OAUTH_TOKEN_SECRET = 'CIMzUezyJOtIER5KSBUnNb1nnWbUtFNiLviHurCki7oyH'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,CONSUMER_KEY, CONSUMER_SECRET)
boot = twitter.Twitter(auth = auth)

"""
Funcion: readMention
Precondicion: exista un objeto de tipo Twitter
Postcondicion: devuelve el contenido de la mencion
"""

def readMention():
	return boot.statuses.mentions_timeline(count = 1)

"""
Funcion: saveJson
Precondicion: recibe el nombre del archivo junto con su objeto
Postcondicion: guarda el Json
"""

def saveJson(name, data):
	with io.open('{0}.json'.format(name), 'w', encoding='utf-8') as f:
		f.write(unicode(json.dumps(data, ensure_ascii = False)))

"""
Funcion: readJson
Precondicion: recibe el nombre del archivo
Postcondicion: devuelve lo leido de dicho archivo
"""

def readJson(name):
	return json.loads(open(name).read())

"""
Funcion: formatingCity
Precondicion: recibe una cadena con la lectura de la mencion en twitter
Postcondicion: sustituye espacios por guiones bajos y devuelve la cadena
"""

def formatingCity(mencion):
	return mencion.replace(' ', '_')

"""
Funcion: formatingUrl
Precondicion: recibe una cadena con la ciudad origen
Postcondicion: sustituye espacion por + y devuelve la cadena
"""

def formatingUrl(mencion):
	return mencion.replace(' ', '+')


"""
Funcion: peticionApiWeather
Precondicion: recibe una cadena con la ciudad a consultar el tiempo
Postcondicion: devuelve la respuesta de la API
"""

def peticionApiWeather(name):
	web = urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+name+',ES&APPID=f07ee5db0071179675cb7ea6d4cfa6f3')
	data = json.load(web)
	return data

"""
Funcion: createtweet
Precondicion: Recibe la respuesta de la web del tiempo en formato JSON
Postcondicion: se crean unas cadenas que se almacenan en un diccionario
"""

def createTweet(web, user, destino):
	for webi in web['weather']:
		estado = webi['main']
	temperatura = web['main']['temp'] - 273.15 #La web del tiempo nos devuelve la temperatura en GRADOS KELVIN
	viento = web['wind']['speed']
	nombre = web['name']
	cadena = user+"\nCiudad: "+nombre+"\nEstado: "+estado+"\nTemperatura: "+str(temperatura)+" grados"+"\nViento: "+str(viento)+" Km/h"
	postingTweet(cadena)
        if(destino != 'None'):
                cadena2 = 'https://www.google.es/maps/dir/'+nombre+'/'+destino+'/'
                postingTweet(cadena2)

"""
Funcion: postingTweet
Precondicion: recibe ristra de campos que se publicaran en el tweet junto con el usuario al que se le enviara
Postcondicion: publica el tweet
"""

def postingTweet(cadena):
	boot.statuses.update(status = cadena)
	print "Publicado con exito"

"""
Funcion: printGraph
Precondicion: recibe un diccionario con los usuarios que han twiteado
Postcondicion: crea un grafico de quesitos con los usuarios del diccionario
"""

def  printGraph(twiteros):
        usuarios = twiteros.keys()
        clave = twiteros.values()

        plt.pie(clave, labels = usuarios)  # Dibuja un grafico de quesitos
        plt.title(u'Porcentaje de menciones por usuario')
        plt.show()


def inicioRec(palabra_antigua, usuario_antiguo):
	mencion = readMention()
	saveJson('tweet_json', mencion)
	tweet_json = readJson('tweet_json.json')

	for tweety in tweet_json:
		palabra = tweety[ 'text' ]
		user = tweety[ 'user' ]['screen_name']

	palabra = palabra[14:]
	user = "@"+user

        palabra = formatingCity(palabra)

	if(palabra_antigua != palabra or usuario_antiguo != user):
		print "El antiguo fue: "+usuario_antiguo+" y pidio: "+palabra_antigua
                print "El usuario: "+user+" hace la siguiente peticion: "+palabra
        else:
                time.sleep(10)
                inicioRec(palabra,user)

def inicio():
	mencion = readMention()
	saveJson('tweet_json', mencion)
	tweet_json = readJson('tweet_json.json')

	for tweety in tweet_json:
		palabra = tweety[ 'text' ]
		user = tweety[ 'user' ]['screen_name']
                destino = tweety[ 'place' ][ 'name' ]
	palabra = palabra[14:]
	user = "@"+user

        if(twiteros.has_key(user)):
                twiteros[user] += 1
        else:
                twiteros[user] = 1

	palabra1 = formatingCity(palabra)
        palabra2 = formatingUrl(palabra)
        destino = formatingUrl(destino)
	web_json = peticionApiWeather(palabra1)
	createTweet(web_json,user,destino)
	inicioRec(palabra,user)


twiteros = {}
cont = 0

while True:
	inicio()
        cont += 1
        if(cont%2 == 0):
                printGraph(twiteros)

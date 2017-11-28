# -*-coding:utf-8-*-

from flask import Flask,url_for,render_template, request,Response
from apscheduler.schedulers.background import BackgroundScheduler

from bs4 import BeautifulSoup
import time, urllib2, re, pymongo
from pymongo import MongoClient
from beebotte import *
from flask_sse import sse



_hostname   = 'api.beebotte.com'
_token      = '1510354696907_Eyiro6Dnp75b5381'
url='http://www.numeroalazar.com.ar/'
bbt = BBT(token = _token, hostname = _hostname)

def gethtml(url):
    try:
        req = urllib2.Request(url)
        return urllib2.urlopen(req).read()
    except Exception, e:
        time.sleep(2)
        return ''



def getnum(web):
    soup = BeautifulSoup(web, 'html.parser')
    #print soup
    busca =soup.find(id="numeros_generados").text
    num= re.findall(r"[0-9]+.[0-9]{2}",busca)
    
    #print num
    return num[0]





def insertBBT(fecha,hora,numero):
 
    bbt.write("datosweb", "fecha", fecha)
    bbt.write("datosweb", "hora", hora)
    bbt.write("datosweb", "numaleatorio", float(numero))

    


def insertMongo(num_1,fecha,hora):
    #conexion
    con = MongoClient('localhost',27017)
    db = con.datosweb
    datos = db.datos

    #insertar datos
    datonum1 ={"numero":num_1 , "fecha":fecha, "hora":hora}
    
    try:
        datos.insert(datonum1)
       
    except Exception as e:
        print "Unexpected error:", type(e), e
    return datos




def getMongo():
    #obtener un dato
    datosmongo = datos.find_one()
    return datosmongo
  


def updateMongo(datosmongo):
    #actualizar dato en una colección
    datos.update(datosmongo, {"$set":{"numero":num_1,"fecha":fecha}})




app = Flask(__name__)


def update_media():	
    	   
    media = media_value
    vmedio = {"tipo":"media", "valor":media}
    data_json = json.dumps(vmedio)
    yield 'data: %s\n\n' % str(data_json)
    if (alert ==1):
        #print 'dentro de alert'
	alerta = {"tipo":"alerta", "valor":numero}
	data_al_json = json.dumps(alerta)
  	yield 'data: %s\n\n' % str(data_al_json)
    
	
	
			 
@app.route('/')
def routindex():
    return render_template('contact.html',lista = listanum, fecha=listafecha, hora=listahora)
	


@app.route('/result.html')
def index():
    return render_template('result.html')
	



@app.route('/update_media')
def sse_request():	  
	return Response(update_media(), mimetype='text/event-stream')

	  


@app.route('/contact.html')
def resultcontact():
    return render_template('contact.html', lista= listanum, fecha=listafecha, hora=listahora, listaum= listaumnum, fechaum=listaumfecha, horaum=listaumhora)




@app.route('/', methods=['POST'])
def my_template():
    global umbralinf
    global umbralsup
    global media
    global umbralrun
    umbrun=0
    cursor = datos.find()
    listaumnum = []
    listaumfecha= []
    listaumhora= []
    cursor = datos.find()
    
    if request.method == 'POST':
        print '1'
       
        if (request.form['my-form']=="Enviar Umbral Runtime"):
            print '2'
            umbralrun = request.form['umbralrun']
            
            if umbralrun.isdigit():	 
	        return render_template('contact.html',lista = listanum, media=media,fecha=listafecha, hora=listahora, listaum = listaumnum, fechaum=listaumfecha, horaum=listaumhora, umbralrun=umbralrun) 
	    else:
		return render_template('contact.html',lista = listanum, media=media,fecha=listafecha, hora=listahora, listaum = listaumnum, fechaum=listaumfecha, horaum=listaumhora, umbralrun=umbralrun) 
            
        
        elif (request.form['my-form']=="Enviar Umbral Inf"):
            umbralinf = request.form['umbral-i']
	    if umbralinf.isdigit():
	        print 'superior',umbralsup
            	for dat in cursor:
                    num1= float(dat['numero']) 
                    if num1 > float(umbralinf) and num1<float(umbralsup):	       
	            	num= dat['numero'] 
		    	fech= dat['fecha']
		        hor= dat['hora']
		    	listaumnum.append(num)
		    	listaumfecha.append(fech)
		    	listaumhora.append(hor)	  
            if len(listaumnum) > 0:
                return render_template('contact.html',umbralinf=umbralinf,umbralsup=umbralsup,lista = listanum, media=media,fecha=listafecha, hora=listahora, listaum = listaumnum, fechaum=listaumfecha, horaum=listaumhora )
            else:
                return render_template('contact.html',umbralsup=umbralsup,lista = listanum, media=media,fecha=listafecha, hora=listahora, listaum = listaumnum, fechaum=listaumfecha, horaum=listaumhora, umbralinf='introduce valor numerico 1')
  
       
 	elif (request.form['my-form']=="Enviar Umbral Sup"):
            print 'dentro 1'
            umbralsup = request.form['umbral-s']
            print 'kk',umbralsup
	    if umbralsup.isdigit():
            	for dat in cursor:
                    num1= float(dat['numero']) 
                    if num1 < float(umbralsup) and num1 > float(umbralinf): 		       
	            	num= dat['numero'] 
		    	fech= dat['fecha']
		    	hor= dat['hora']
		    	listaumnum.append(num)
		    	listaumfecha.append(fech)
		    	listaumhora.append(hor)	  
            if len(listaumnum) > 0:
                return render_template('contact.html',umbralsup=umbralsup,umbralinf=umbralinf, lista = listanum, media=media,fecha=listafecha, hora=listahora, listaum = listaumnum, fechaum=listaumfecha, horaum=listaumhora )
            else:
                return render_template('contact.html',umbralinf=umbralinf,lista = listanum, media=media,fecha=listafecha, hora=listahora, listaum = listaumnum, fechaum=listaumfecha, horaum=listaumhora, umbralsup='introduce valor numerico 2')    
       
    else:
        return render_template('contact.html', media=media,lista = listanum, fecha=listafecha, hora=listahora)
   


				  
	

      


#funcion que comprueba la media
def comp_media(cursor):
    total=0
    valor=0
    listanum = []
    listafecha= []
    listahora= []
    for dat in cursor:    
	total=total+1 
	num= dat['numero']
	fech= dat['fecha']
	hor= dat['hora']
	valor=float(valor) + float(num)
	listanum.append(num)
	listafecha.append(fech)
	listahora.append(hor)
    media=valor/total
    return media
    
def saveMongo():
    global numero
    global datos
    global cursor
    global umbralrun
    global media_value
    global alert
    global umbrun
    alert =0;
    
    web=gethtml(url)
    fecha = time.strftime("%d/%m/%y")
    hora =  time.strftime("%X")
    numero= getnum(web)
    #print hora
    insertBBT(fecha,hora,numero)
    datos=insertMongo(numero,fecha,hora)
    cursor = datos.find()
    #print 'umbral puesto', umbralrun
    media_value=comp_media(cursor)
    print media_value

    if umbralrun > 0:
        if numero > umbralrun:
            print 'Umbral superado!'
            alert=1
    #print 'Leo y Guardo en Mongo:'
    #print numero
    return datos,numero



if __name__ == "__main__":
   
    scheduler = BackgroundScheduler()
    scheduler.add_job(saveMongo,'interval',seconds=10)
    scheduler.start()
 

    global fecha
    global web
    global dat
    global media
    global umbralrun
   
    umbralrun=0
    umbralsup=100
    umbralinf=0
    
    umbrun=0;
    datos,numero=saveMongo()  
    #datosmongo = datos.find()
    total=0
    valor=0
    listanum = []
    listafecha= []
    listahora= []
    media=comp_media(datos.find())
    for dat in datos.find():    
	num= dat['numero']
	fech= dat['fecha']
	hor= dat['hora']
	valor=float(valor) + float(num)
	listanum.append(num)
	listafecha.append(fech)
	listahora.append(hor)
 
   
    app.run(host ='0.0.0.0')
    

  





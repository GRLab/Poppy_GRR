#!/usr/bin/python
import os
import socket
import BaseHTTPServer
from urlparse import urlparse
import fonctions 
import json
import time
from collections import OrderedDict
import logging
from logging.handlers import RotatingFileHandler

#Gestion des requetes
class RequestHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    
    def send_data(self, jsonfile, BDD = "false"):
		jsondata = fonctions.loadData(jsonfile, BDD)
		print jsondata
		return jsondata
    
    def read_data(self, moveName, previsu = False):
		moveconfig = self.rfile.read(int(self.headers['Content-Length']))
		succeed = fonctions.readConfig(moveconfig, moveName)
		if previsu == True :
			print " bien en previsu mode"
			fonctions.GoMove(moveName)
			fonctions.RemoveMove(moveName)
			succeed = 'moved'
		if "created" in succeed or "moved" in succeed:
			self.send_headers(201)
		else :
			self.send_headers()
		return succeed
    
    def send_headers(self, code=200):
	#accuse que la communication s'est effectuee
		try:
			self.send_response(code)
			self.send_header("Content-type", "text/html/json/")
			self.send_header("Access-Control-Allow-Origin","*")
			self.end_headers()
		except socket.error, e:
			if e[0] == 32:
				print "broken pipe!!!!!!!!!!!!"
				logger.error("client disconnected ! ***** BROKEN PIPE *****")
				pass
			else:
				logger.exception("***** socket error *****")
			
	
    def do_POST(self):
	#print self.path	#pour voir ce qui a ete recu avant traitement
	parsed_path = urlparse(self.path) #recupere l'url de la requete
	try :
		params = dict([p.split('=') for p in parsed_path[4].split('&')])
		IPclient = self.client_address[0]
	except:
		params={}
	
	text=""
	#request verification and application
        
	if 'Submit' in params.keys() and "set+robot+compliant" == params['Submit']:
	    poppyParts=[]
	    logger.info(IPclient+" REQUEST - setting the robot compliant")
	    if params['poppyParts']!="":
			poppyParts = params['poppyParts'].split(",")
			fonctions.Compliant(poppyParts)
	    else:
			fonctions.Compliant()
	    self.send_headers()
	    text="Poppy is compliant now"
	    logger.info(IPclient+" RESPONSE - "+text)
 
	if 'Submit' in params.keys() and "set+robot+non-compliant" == params['Submit']:
	    poppyParts=[]
	    logger.info(IPclient+" REQUEST - setting the robot non-compliant")  
	    if params['poppyParts']!="":
			poppyParts = params['poppyParts'].split(",")
			fonctions.NonCompliant(poppyParts, notMoving = True)
	    else:
			fonctions.NonCompliant()
	    self.send_headers()
	    text="Poppy is non-compliant now"
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "set+robot+semi-compliant" == params['Submit']:
	    poppyParts=[]
	    if params['poppyParts']!="":
			poppyParts = params['poppyParts'].split(",")
	    logger.info(IPclient+" REQUEST - setting the robot semi-compliant")  
	    fonctions.semiCompliant(poppyParts)
	    self.send_headers()
	    text="Poppy is semi-compliant now"
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "set+robot+initial+position" == params['Submit']:
	    self.send_headers()
	    logger.info(IPclient+" REQUEST - setting the robot in initial position")
	    fonctions.PosInit()
	    text="Poppy is in his initial position"
	    logger.info(IPclient+" RESPONSE - "+text)
            
	if 'Submit' in params.keys() and "save+init+pos" == params['Submit']:
	    posName=""
	    if params['posName']!="":
		    posName = params['posName']
	    logger.info(IPclient+" REQUEST - saving initial position "+posName)
	    fonctions.SavePosInit(posName)
	    text = 'initial position saved'
	    self.send_headers(201)
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "go+init+pos" == params['Submit']:
	    posName=""
	    if params['posName']!="":
		    posName = params['posName']
	    logger.info(IPclient+" REQUEST - going to initial position")
	    fonctions.GoPosInit(posName)
	    text = 'Poppy in initial position'
	    self.send_headers(201)
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "save+part+move" == params['Submit']:
	    moveName="dataMove.json"
	    if params['moveName']!="":
		    moveName = params['moveName']
	    semiMou=''
	    if params['semiMou']!="":
		    semiMou = params['semiMou']
	    playedMove=''
	    if params['playedMove']!="":
		    playedMove = params['playedMove']
	    poppyParts=[]
	    if params['poppyParts']!="":
			poppyParts = params['poppyParts'].split(",")
	    logger.info(IPclient+" REQUEST - saving ss mov : "+moveName+", "+poppyParts)
	    text = fonctions.SaveMovePart(poppyParts, moveName, semiMou, playedMove)
	    if text == 'move part saved':
		    self.send_headers(201)
	    else:
		    self.send_headers()
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "create+move" == params['Submit']:
	    moveName=""
	    if params['moveName']!="":
			moveName = params['moveName']
	    previsual= False
	    if params['previsu']=="True":
		    print "previsu mode"
		    previsual = True
	    logger.info(IPclient+" REQUEST - creating move : "+moveName)
	    exist = fonctions.directory(moveName)
	    if exist == '':
			text = self.read_data(moveName, previsu = previsual)
	    else:
		    self.send_headers()
		    text="move already exists"
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "create+exo" == params['Submit']:
	    exoName="dataPos.json"
	    if params['exoName']!="":
			exoName = params['exoName']
	    logger.info(IPclient+" REQUEST - creating exo or seance : "+exoName)
	    exist = fonctions.directory(exoName)
	    if exist == '':
			text = self.read_data(exoName)
	    else:
			self.send_headers()
			text="move already exists"
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "rename" == params['Submit']:
	    previousName = params['previousName']
	    newName = params['newName']
	    logger.info(IPclient+" REQUEST - renaming : "+previousName+" -> "+newName)
	    text = fonctions.rename(previousName, newName)
	    if 'exist' in text:
			self.send_headers()
	    else:
			self.send_headers(201)
	    logger.info(IPclient+" RESPONSE - "+text)
	
	if 'Submit' in params.keys() and "symetry" == params['Submit']:
	    moveName="dataPos.json"
	    if params['moveName']!="":
			moveName = params['moveName']
	    logger.info(IPclient+" REQUEST - symetry of : "+moveName)
	    text = fonctions.symetry(moveName)
	    if 'exist' in text:
			self.send_headers()
	    else:
			self.send_headers(201)
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "reverse" == params['Submit']:
	    moveName="dataPos.json"
	    if params['moveName']!="":
			moveName = params['moveName']
	    logger.info(IPclient+" REQUEST - reverse of : "+moveName)
	    text = fonctions.reverse(moveName)
	    if 'exist' in text:
			self.send_headers()
	    else:
			self.send_headers(201)
	    logger.info(IPclient+" RESPONSE - "+text)
		    
	if 'Submit' in params.keys() and "remove+move" == params['Submit']:
	    moveName=""
	    if params['moveName']!="":
			moveName = params['moveName']
	    logger.info(IPclient+" REQUEST - removing : "+moveName)
	    remove = fonctions.RemoveMove(moveName)
	    if remove == True:
			self.send_headers(201)
			text="file removed"
	    else:
			self.send_headers(200)
			text="file does not exist"
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "go+move" == params['Submit']:
	    moveName=""
	    if params['moveName']!="":
		    moveName = params['moveName']
	    speed=2
	    if params['speed']!="":
		    speed = params['speed']
	    poppyParts=[]
	    if params['poppyParts']!="":
			poppyParts = params['poppyParts'].split(",")
	    logger.info(IPclient+" REQUEST - playing move : "+moveName+", speed : "+speed)
	    text = fonctions.GoMove(moveName, speed, poppyParts = poppyParts)
	    if text == 'Poppy moved':
		    self.send_headers(201)
	    else:
		    self.send_headers()
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "go+reverse" == params['Submit']:
	    moveName=""
	    if params['moveName']!="":
		    moveName = params['moveName']
	    speed=2
	    if params['speed']!="":
		    speed = params['speed']
	    logger.info(IPclient+" REQUEST - playing reverse move : "+moveName+", speed : "+speed)
	    text = fonctions.GoMove(moveName, speed, rev=True)
	    if text == 'Poppy moved':
		    self.send_headers(201)
	    else:
		    self.send_headers()
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "go+exo" == params['Submit']:
	    exoName=""
	    if params['exoName']!="":
		    exoName = params['exoName']
	    logger.info(IPclient+" REQUEST - playing exo : "+exoName)
	    text = fonctions.GoExo(exoName)
	    if text == 'Exercice has started':
		    exoCompo = self.send_data(exoName)
		    self.send_headers(201)
		    try:
				self.wfile.write(exoCompo)
		    except socket.error, e:
				if e[0] == errno.EPIPE:
					logger.error(IPclient+" disconnected ! ***** BROKEN PIPE *****")
				else:
					logger.exception(IPclient+" ***** socket error *****")
	    else:
		    self.send_headers()
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "go" == params['Submit']:
	    time.sleep(0.8) 	#le temps que le stop se fasse
	    exoName=""
	    if params['exoName']!="":
			exoName = params['exoName']
	    logger.info(IPclient+" REQUEST - playing : "+exoName)
	    dir = fonctions.directory(exoName)
	    if dir == 'exo' or dir == 'seance':
			text = fonctions.GoExo(exoName)
			if text == 'Exercice has started':
				exoCompo = self.send_data(exoName)
				text = ''
				self.send_headers(201)
				try:
					self.wfile.write(exoCompo)
				except socket.error, e:
					if e[0] == errno.EPIPE:
						logger.error(IPclient+" disconnected ! ***** BROKEN PIPE *****")
					else:
						logger.exception(IPclient+" ***** socket error *****")
			else:
				self.send_headers()
	    else :
			text = fonctions.GoMove(exoName)
			if text == 'Move has started':
				self.send_headers(202)
			else:
				self.send_headers()
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "stop+exo" == params['Submit']:
	    logger.info(IPclient+" REQUEST - stop !")
	    text = fonctions.StopExo()
	    if  'stopped' in text:
		    self.send_headers(201)
	    else:
		    self.send_headers()
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "pause+exo" == params['Submit']:
	    logger.info(IPclient+" REQUEST - pause !")
	    text = fonctions.PauseExo()
	    if text == 'move paused':
		    self.send_headers(201)
	    else:
		    self.send_headers()
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "resume+exo" == params['Submit']:
	    logger.info(IPclient+" REQUEST - resume !")
	    text = fonctions.ResumeExo()
	    if 'resumed' in text:
		    self.send_headers(201)
	    else:
		    self.send_headers()
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "verif+fin+exo" == params['Submit']:
	    verif = fonctions.verifFinExo()
	    if verif["info"] == 'end':
			self.send_headers(201)
			logger.info(IPclient+" RESPONSE - exo finished")
	    else:
		    self.send_headers()
	    try:
			self.wfile.write(verif)
	    except socket.error, e:
			if e[0] == errno.EPIPE:
				logger.error(IPclient+" disconnected ! ***** BROKEN PIPE *****")
			else:
				logger.exception(IPclient+" ***** socket error ***** ")
	    
	if 'Submit' in params.keys() and "verif+fin+mov" == params['Submit']:
	    verif = fonctions.verifFinMov()
	    if verif == 'end':
			self.send_headers(201)
			logger.info(IPclient+" RESPONSE - move finished")
	    else:
		    self.send_headers()

	if 'Submit' in params.keys() and "senddata" == params['Submit']:
		jsonfile="dataPos.json"
		if params['jsonfile']!="":
			jsonfile = params['jsonfile']
		self.read_data(jsonfile, 200)
		text="data ok !"
		print ('data ok !')

	if 'Submit' in params.keys() and "add+move" == params['Submit']:
		if params['moveName']!="":
			moveName = params['moveName']
		if params['type']!="":
			moveType = params['type']
		logger.info(IPclient+" REQUEST - adding "+moveType+" in Poppy : "+moveName)
		moveFile = self.rfile.read(int(self.headers['Content-Length']))
		text=fonctions.addMove(moveName, moveType, moveFile)
		if text == "added":
			self.send_headers(201)
		else:
			self.send_headers()
		logger.info(IPclient+" RESPONSE - "+text)
	try:
		self.wfile.write(text)
	except socket.error, e:
		if e[0] == errno.EPIPE:
			logger.error(IPclient+" disconnected ! ***** BROKEN PIPE *****")
		else:
			logger.exception(IPclient+" ***** socket error ***** ")

    def do_GET(self):
	#print self.path	#pour voir ce qui a ete recu avant traitement
	parsed_path = urlparse(self.path) #recupere l'url de la requete
	try :
		params = dict([p.split('=') for p in parsed_path[4].split('&')])
		IPclient = self.client_address[0]
	except:
		params={}
	
	text=""
        #request verification and application
	
	if 'Submit' in params.keys() and "receivedata" == params['Submit']:
	    jsonfile=""
	    if params['jsonfile']!="":
		    jsonfile = params['jsonfile']
	    BDD = ""
	    if params['BDD']!="":
		    BDD = params['BDD']
	    logger.info(IPclient+" GET REQUEST - receiving data")
	    jsondata = self.send_data(jsonfile, BDD)
	    jsondata = json.dumps(jsondata)
	    if jsondata == 'does not exist':
			self.send_headers(200)
			text = "file does not exist"
	    else:
			self.send_headers(201)
			try:
				self.wfile.write(jsondata)
			except socket.error, e:
				if e[0] == errno.EPIPE:
					logger.error(IPclient+" disconnected ! ***** BROKEN PIPE *****")
				else:
					logger.exception(IPclient+" ***** socket error ***** ")
			text = "file "+jsonfile+" has been sent"
	    logger.info(IPclient+" RESPONSE - "+text)
	    
	if 'Submit' in params.keys() and "getMesure" == params['Submit']:
		results = fonctions.scanResults()
		results = json.dumps(results)
		self.send_headers(200)
		try:
			self.wfile.write(results)
		except socket.error, e:
			if e[0] == errno.EPIPE:
				logger.error(IPclient+" disconnected ! ***** BROKEN PIPE *****")
			else:
				logger.exception(IPclient+" ***** socket error ***** ")

	if 'Submit' in params.keys() and "getIP" == params['Submit']:
		logger.info(IPclient+" REQUEST - sending Poppy IP")
		IPAddress = fonctions.giveIP()
		self.send_headers(200)
		try:
			self.wfile.write(IPAddress)
		except socket.error, e:
			if e[0] == errno.EPIPE:
				logger.error(IPclient+" disconnected ! ***** BROKEN PIPE *****")
			else:
				logger.exception(IPclient+" ***** socket error ***** ")
		logger.info(IPclient+" RESPONSE - "+IPAddress)

	if 'Submit' in params.keys() and "getLogs" == params['Submit']:
	    logger.info(IPclient+" REQUEST - get logs")
	    logs = fonctions.send_logs()
	    self.send_response(200)
	    self.send_header('Content-Type', 'application/gzip')
	    self.send_header("Access-Control-Allow-Origin","*")
	    self.send_header('Content-Disposition', 'attachment;''filename=logs_'+str(year)+'-'+str(month)+'.tar.gz')
	    self.end_headers()
	    try:
			self.wfile.write(logs)
	    except socket.error, e:
			if e[0] == errno.EPIPE:
				logger.error(IPclient+" disconnected ! ***** BROKEN PIPE *****")
			else:
				logger.exception(IPclient+" ***** socket error ***** ")
	    logger.info(IPclient+" RESPONSE - logs sent")

	if 'Submit' in params.keys() and "getPreviousLogs" == params['Submit']:
	    logger.info(IPclient+" REQUEST - get previous logs")
	    logs = fonctions.send_logs(previous = True)
	    self.send_response(200)
	    self.send_header('Content-Type', 'application/gzip')
	    self.send_header("Access-Control-Allow-Origin","*")
	    if month ==1:
			self.send_header('Content-Disposition', 'attachment;''filename=logs_'+str(year-1)+'-'+str(12)+'.tar.gz')
	    else:
			self.send_header('Content-Disposition', 'attachment;''filename=logs_'+str(year)+'-'+str(month-1)+'.tar.gz')
	    self.end_headers()
	    try:
			self.wfile.write(logs)
	    except socket.error, e:
			if e[0] == errno.EPIPE:
				logger.error(IPclient+" disconnected ! ***** BROKEN PIPE *****")
			else:
				logger.exception(IPclient+" ***** socket error ***** ")
	    logger.info(IPclient+" RESPONSE - logs sent")

#Configuration logs
year = int(time.strftime('%Y', time.localtime()))		#annee en cours
month = int(time.strftime('%m', time.localtime()))		#mois en cours
logger = logging.getLogger('PoppyGRR_log')
logger.setLevel(logging.DEBUG)
if ("logs_"+str(year)+"-"+str(month)) not in os.listdir('log/'):
	os.mkdir("log/logs_"+str(year)+"-"+str(month))
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%d/%m/%Y %I:%M:%S %p")
handler = logging.handlers.RotatingFileHandler("./log/logs_"+str(year)+"-"+str(month)+"/serverlog.log", mode="a", maxBytes= 100000000000, backupCount= 1, encoding="utf-8")
handler.setFormatter(formatter)
logger.addHandler(handler)
#CREATION du serveur web
PORT = 4567
poppyName = "poppygr"
server_address = (poppyName+".local", PORT) #changer l'IP en fonction
server = BaseHTTPServer.HTTPServer
handler = RequestHandler
print "Serveur actif sur le port :", PORT
fonctions.mesure()	#start scanning the motors
fonctions.compress_log()	#compresse les logs anterieurs
logger.info('initializing poppy server')
httpd = server(server_address, handler)
httpd.serve_forever()


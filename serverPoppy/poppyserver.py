#!/usr/bin/env python
import os
import json
import socket
import BaseHTTPServer
from urlparse import urlparse
import json
import time
from collections import OrderedDict
import logging
from logging.handlers import RotatingFileHandler
from threading import Thread
from eyes.eyes import *
from sound.sound import Sound
from fonctions import *

#importation des configurations
with open('./CONFIG.json', 'r') as f:
	config = json.load(f)
	poppyName = config["poppyName"]["value"]
	kinectName = config["kinectName"]["value"]
	screenOn = True if config["screenOn"]["value"] == "True" else False
	fullScreen = True if config["fullScreen"]["value"] == "True" else False
	Volume = config["Volume"]["value"]
	internet = True if config["internet"]["value"] == "True" else False
	wrists = True if config["wrists"]["value"] == "True" else False
	creature = config["creature"]["value"]
	seuil_bien = config["seuil_bien"]["value"]
	seuil_nul = config["seuil_nul"]["value"]
	nb_demo = config["nb_demo"]["value"]

#arret http server
class stopServer(Thread):
	def __init__(self, httpd):
		Thread.__init__(self)
		self.httpd = httpd

	def run(self):
		self.httpd.shutdown()
		self.httpd.socket.close()

#Gestion des requetes
class RequestHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    
    def send_data(self, jsonfile, BDD = "false"):
		try:
			jsondata = poppy.loadData(jsonfile, BDD)
		except:
			logger.exception("***** load data error *****")
		print jsondata
		return jsondata
    
    def read_data(self, moveName, previsu = False):
		moveconfig = self.rfile.read(int(self.headers['Content-Length']))
		try:
			succeed = poppy.readConfig(moveconfig, moveName)
		except:
			logger.exception("***** read config error *****")
		if previsu == True :
			print " bien en previsu mode"
			try:
				poppy.GoMove(moveName)
			except:
				logger.exception("***** GoMove error *****")
			try:
				poppy.RemoveMove(moveName)
			except:
				logger.exception("***** RemoveMove error *****")
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
			try:
				poppy.Compliant(poppyParts)
			except:
				logger.exception("***** Part Compliant error *****")
	    else:
			try:
				poppy.Compliant()
			except:
				logger.exception("***** Compliant error *****")
	    self.send_headers()
	    text="Poppy is compliant now"
	    logger.info(IPclient+" RESPONSE - "+text)
 
	if 'Submit' in params.keys() and "set+robot+non-compliant" == params['Submit']:
	    poppyParts=[]
	    logger.info(IPclient+" REQUEST - setting the robot non-compliant")  
	    if params['poppyParts']!="":
			poppyParts = params['poppyParts'].split(",")
			try:
				poppy.NonCompliant(poppyParts, notMoving = True)
			except:
				logger.exception("***** Part NonCompliant error *****")
	    else:
			try:
				poppy.NonCompliant()
			except:
				logger.exception("***** NonCompliant error *****")
	    self.send_headers()
	    text="Poppy is non-compliant now"
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "set+robot+semi-compliant" == params['Submit']:
	    poppyParts=[]
	    if params['poppyParts']!="":
			poppyParts = params['poppyParts'].split(",")
	    logger.info(IPclient+" REQUEST - setting the robot semi-compliant")  
	    try:
			poppy.semiCompliant(poppyParts)
	    except:
			logger.exception("***** semiCompliant error *****")
	    self.send_headers()
	    text="Poppy is semi-compliant now"
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "set+robot+initial+position" == params['Submit']:
	    self.send_headers()
	    logger.info(IPclient+" REQUEST - setting the robot in initial position")
	    try:
			poppy.PosInit()
	    except:
			logger.exception("***** PosInit error *****")
	    text="Poppy is in his initial position"
	    logger.info(IPclient+" RESPONSE - "+text)
            
	if 'Submit' in params.keys() and "save+init+pos" == params['Submit']:
	    posName=""
	    if params['posName']!="":
		    posName = params['posName']
	    logger.info(IPclient+" REQUEST - saving initial position "+posName)
	    try:
			poppy.SavePosInit(posName)
	    except:
			logger.exception("***** SavePosInit error *****")
	    text = 'initial position saved'
	    self.send_headers(201)
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "go+init+pos" == params['Submit']:
	    posName=""
	    if params['posName']!="":
		    posName = params['posName']
	    logger.info(IPclient+" REQUEST - going to initial position : "+posName)
	    try:
			poppy.GoPosInit(posName)
	    except:
			logger.exception("***** GoPosInit error *****")
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
	    logger.info(IPclient+" REQUEST - saving ss mov : "+moveName+", "+str(poppyParts))
	    try:
			text = poppy.SaveMovePart(poppyParts, moveName, semiMou, playedMove)
	    except:
			logger.exception("***** saveMovePart error *****")
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
	    try:
			exist = poppy.directory(moveName)
	    except:
			logger.exception("***** directory error *****")
	    if exist == '':
			text = self.read_data(moveName, previsu = previsual)
	    else:
		    self.send_headers()
		    voice.play("./sound/sounds/existedeja.mp3")
		    text="move already exists"
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "create+exo" == params['Submit']:
	    exoName="dataPos.json"
	    if params['exoName']!="":
			exoName = params['exoName']
	    logger.info(IPclient+" REQUEST - creating exo or seance : "+exoName)
	    try:
			exist = poppy.directory(exoName)
	    except:
			logger.exception("***** directory error *****")
	    if exist == '':
			text = self.read_data(exoName)
	    else:
			self.send_headers()
			voice.play("./sound/sounds/existedeja.mp3")
			text="move already exists"
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "rename" == params['Submit']:
	    previousName = params['previousName']
	    newName = params['newName']
	    logger.info(IPclient+" REQUEST - renaming : "+previousName+" -> "+newName)
	    try:
			text = poppy.rename(previousName, newName)
	    except:
			logger.exception("***** rename error *****")
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
	    try:
			text = poppy.symetry(moveName)
	    except:
			logger.exception("***** symetry error *****")
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
	    try:
			text = poppy.reverse(moveName)
	    except:
			logger.exception("***** reverse error *****")
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
	    try:
			remove = poppy.RemoveMove(moveName)
	    except:
			logger.exception("***** RemoveMove error *****")
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
	    try:
			text = poppy.GoMove(moveName, speed, poppyParts = poppyParts)
	    except:
			logger.exception("***** GoMove error *****")
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
	    try:
			text = poppy.GoMove(moveName, speed, rev=True)
	    except:
			logger.exception("***** reverse GoMove error *****")
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
	    try:
			text = poppy.GoExo(exoName)
	    except:
			logger.exception("***** GoExo error *****")
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
	    text = poppy.waitVoice()
	    time.sleep(1) 	#le temps que le stop se fasse
	    exoName=""
	    if params['exoName']!="":
			exoName = params['exoName']
	    logger.info(IPclient+" REQUEST - playing : "+exoName)
	    try:
			dir = poppy.directory(exoName)
	    except:
			logger.exception("***** directory error *****")
	    if dir == 'exo' or dir == 'seance':
			try:
				text = poppy.GoExo(exoName)
			except:
				logger.exception("***** GoExo error *****")
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
			try:
				text = poppy.GoMove(exoName)
			except:
				logger.exception("***** GoMove error *****")
			if text == 'Move has started':
				self.send_headers(202)
			else:
				self.send_headers()
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "stop+exo" == params['Submit']:
	    logger.info(IPclient+" REQUEST - stop !")
	    try:
			text = poppy.StopExo()
	    except:
			logger.exception("***** StopExo error *****")
	    if  'stopped' in text:
		    self.send_headers(201)
	    else:
		    self.send_headers()
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "pause+exo" == params['Submit']:
	    logger.info(IPclient+" REQUEST - pause !")
	    try:
			text = poppy.PauseExo()
	    except:
			logger.exception("***** PauseExo error *****")
	    if text == 'move paused':
		    self.send_headers(201)
	    else:
		    self.send_headers()
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "resume+exo" == params['Submit']:
	    logger.info(IPclient+" REQUEST - resume !")
	    try:
			text = poppy.ResumeExo()
	    except:
			logger.exception("***** ResumeExo error *****")
	    if 'resumed' in text:
		    self.send_headers(201)
	    else:
		    self.send_headers()
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "verif+fin+exo" == params['Submit']:
	    try:
			verif = poppy.verifFinExo()
	    except:
			logger.exception("***** verifFinExo error *****")
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
	    try:
			verif = poppy.verifFinMov()
	    except:
			logger.exception("***** verifFinMov error *****")
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
		try:
			text=poppy.addMove(moveName, moveType, moveFile)
		except:
			logger.exception("***** addMove error *****")
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

	if 'Submit' in params.keys() and "set+volume" == params['Submit']:
		if params['volume']!="":
			volume=params['volume']
		logger.info(IPclient+" REQUEST - set volume "+str(volume))
		try:
			text=poppy.setVolume(volume)
		except:
			logger.exception("***** setVolume error *****")
		self.send_headers()
		logger.info(IPclient+" RESPONSE - "+text)
		print (text)

	if 'Submit' in params.keys() and "kinect+feedback" == params['Submit']:
	    logger.info(IPclient+" REQUEST - kinect feedback !")
	    feedback = self.rfile.read(int(self.headers['Content-Length']))
	    feedback=json.loads(feedback)
	    print feedback
	    try:
			text = poppy.kinectFeedback(feedback)
	    except:
			logger.exception("***** kinect Feedback error *****")
	    if 'ok' in text:
		    self.send_headers(201)
	    else:
		    self.send_headers()
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "end+kinect+observation" == params['Submit']:
	    logger.info(IPclient+" REQUEST - kinect end observation !")
	    try:
			text = poppy.sayEndKinectObserv()
	    except:
			logger.exception("***** sayEndDinectObserv error *****")
	    if 'ended' in text:
		    self.send_headers(201)
	    else:
		    self.send_headers()
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "say" == params['Submit']:
	    logger.info(IPclient+" REQUEST - say")
	    sentence = self.rfile.read(int(self.headers['Content-Length']))
	    print sentence
	    try:
			text = poppy.say(sentence)
	    except:
			logger.exception("***** say error *****")
	    if 'ok' in text:
		    self.send_headers(201)
	    else:
		    self.send_headers()
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "create+voice" == params['Submit']:
	    logger.info(IPclient+" REQUEST - create voice")
	    filename=''
	    voicetext=''
	    if params['title']!="":
	    	filename = params['title']
	    if params['voice']!="":
	    	voicetext = params['voice']
	    try:
	    	text = poppy.createVoice('instructions',filename,voicetext)
	    except:
	    	logger.exception("***** create voice error *****")
	    if 'ok' in text:
		    self.send_headers(201)
	    else:
		    self.send_headers()
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "setFaceState" == params['Submit']:
	    logger.info(IPclient+" REQUEST - setFaceState")
	    faceState = self.rfile.read(int(self.headers['Content-Length']))
	    print faceState
	    try:
			text = poppy.setFaceState(faceState)
	    except:
			logger.exception("***** setFaceState error *****")
	    if 'ok' in text:
		    self.send_headers(201)
	    else:
		    self.send_headers()
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "setEyeDirection" == params['Submit']:
	    logger.info(IPclient+" REQUEST - setEyeDirection")
	    eyeDirection = self.rfile.read(int(self.headers['Content-Length']))
	    print eyeDirection
	    try:
			text = poppy.setRestEyeDirection(eyeDirection)
	    except:
			logger.exception("***** setEyeDirection error *****")
	    if 'ok' in text:
		    self.send_headers(201)
	    else:
		    self.send_headers()
	    logger.info(IPclient+" RESPONSE - "+text)

	if 'Submit' in params.keys() and "setMotorPosition" == params['Submit']:
	    logger.info(IPclient+" REQUEST - setMotorPosition")
	    motorPosition = self.rfile.read(int(self.headers['Content-Length']))
	    print motorPosition
	    try:
			poppy.setMotorPosition(motorPosition)
	    except:
			logger.exception("***** setMotorPosition error *****")
	    self.send_headers(201)
	    logger.info(IPclient+" RESPONSE - "+text)

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
		try:
			results = poppy.scanResults()
		except:
			logger.exception("***** scanResults error *****")
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
		try:
			IPAddress = poppy.giveIP()
		except:
			logger.exception("***** giveIP error *****")
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
	    try:
			logs = poppy.send_logs()
	    except:
			logger.exception("***** send_logs error *****")
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
	    try:
			logs = poppy.send_logs(previous = True)
	    except:
			logger.exception("***** previous send_logs error *****")
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

	if 'Submit' in params.keys() and "stopServer" == params['Submit']:
	    logger.info(IPclient+" REQUEST - stopServer")
	    print "stop server"
	    voice.play("./sound/sounds/aurevoir.mp3")
	    if face!='none':
			face.update('asleep')
	    self.send_headers(200)
	    self.wfile.write('')
	    time.sleep(1)
	    stopThread = stopServer(httpd)
	    stopThread.start()
	    if face!='none':
			face.stopAnimation()
	    pygame.quit()
	    poppy.stopAll()

#Configuration logs
year = int(time.strftime('%Y', time.localtime()))		#annee en cours
month = int(time.strftime('%m', time.localtime()))		#mois en cours
logger = logging.getLogger('PoppyGRR_log')
logger.setLevel(logging.DEBUG)
if ("logs_"+str(year)+"-"+str(month)) not in os.listdir('./log/'):
	os.mkdir("./log/logs_"+str(year)+"-"+str(month))
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%d/%m/%Y %I:%M:%S %p")
handler = logging.handlers.RotatingFileHandler("./log/logs_"+str(year)+"-"+str(month)+"/serverlog.log", mode="a", maxBytes= 100000000000, backupCount= 1, encoding="utf-8")
handler.setFormatter(formatter)
logger.addHandler(handler)
#CREATION du serveur web
PORT = 4567
server_address = (poppyName+".local", PORT) #changer l'IP en fonction
server = BaseHTTPServer.HTTPServer
handler = RequestHandler
print "Serveur actif sur le port :", PORT
logger.info('initializing poppy server')
#initialisation de l ecran
time.sleep(2)
if screenOn:
	face = Face(datapath="./eyes/", bgcolor=[180,180,225], fullscreen=fullScreen)
	print "ecran initialise"
else:
	face = 'none'
#initialisation du son
voice = Sound(frequence=29400,volume=Volume)
voice.play("./sound/sounds/init.mp3")
#attente avant initialisation, pour demarrage au boot RPi
time.sleep(8)
voice.play("./sound/sounds/motorInit.mp3")
moteursInitialise = False
moteursInitEssai = 0
while not moteursInitialise:
	logger.info("essai initialisation moteur "+str(moteursInitEssai))
	try:
		time.sleep(2)
		poppy=PoppyGRR(face, voice, kinectName, internet, creature, wrists, seuil_bien, seuil_nul, nb_demo)
		moteursInitialise = True
		logger.info("----- moteurs initialises -----")
	except:
		logger.exception("***** motor init error *****")
		moteursInitEssai +=1
		if moteursInitEssai ==3:
			voice.play("./sound/sounds/errorMotorInit.mp3")
			time.sleep(3)
			break

if moteursInitialise:
	if face!='none':
		face.update('happy', 'center')
	try:
		poppy.mesure()	#start scanning the motors
	except:
		logger.exception("***** mesure error *****")
	try:
		poppy.compress_log()	#compresse les logs anterieurs
	except:
		logger.exception("***** compress_log error *****")
	time.sleep(0.5)

	httpd = server(server_address, handler)
	voice.play("./sound/sounds/pret.mp3")
	time.sleep(0.8)
	if internet:
		voice.say("Au faite, mon nom est "+poppyName)
	#poppy.setFaceState('angry')
	#poppy.setRestEyeDirection('bottomleft')
	httpd.serve_forever()
elif face!='none':
	face.stop()

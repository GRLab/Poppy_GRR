#!/usr/bin/python

import BaseHTTPServer
from urlparse import urlparse
import fonctions 
import json
import time
from collections import OrderedDict

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
        self.send_response(code)
	self.send_header("Content-type", "text/html/json")
        self.send_header("Access-Control-Allow-Origin","*")
	self.end_headers()    
	
    def do_POST(self):

	print self.path	#pour voir ce qui a ete recu avant traitement
        parsed_path = urlparse(self.path) #recupere l'url de la requete
	try :
            params = dict([p.split('=') for p in parsed_path[4].split('&')])
        except:
            params={}
	
	text=""
        #request verification and application
        
        if 'Submit' in params.keys() and "set+robot+compliant" == params['Submit']:
	    poppyParts=[]
	    print("setting the robot compliant")
	    if params['poppyParts']!="":
		poppyParts = params['poppyParts'].split(",")
		fonctions.Compliant(poppyParts)
	    else:
		fonctions.Compliant()
            self.send_headers()
	    text="Poppy is compliant now"
            print ('Maniable')
            
	if 'Submit' in params.keys() and "set+robot+non-compliant" == params['Submit']:
	    poppyParts=[]
	    print("setting the robot non-compliant")  
            if params['poppyParts']!="":
		poppyParts = params['poppyParts'].split(",")
		fonctions.NonCompliant(poppyParts, notMoving = True)
            else:
		fonctions.NonCompliant()
	    self.send_headers()
	    text="Poppy is non-compliant now"
	    print ('Non-compliant')

	if 'Submit' in params.keys() and "set+robot+semi-compliant" == params['Submit']:
	    poppyParts=[]
	    if params['poppyParts']!="":
	   	 poppyParts = params['poppyParts'].split(",")
	    print("setting the robot semi-compliant")  
            fonctions.semiCompliant(poppyParts)
            self.send_headers()
	    text="Poppy is semi-compliant now"
	    print ('semi-compliant')

        if 'Submit' in params.keys() and "set+robot+initial+position" == params['Submit']:
            self.send_headers()
	    print("setting the robot in initial position")
            fonctions.PosInit()
	    text="Poppy is in his initial position"
            print ('Initial Position')
            
	if 'Submit' in params.keys() and "save+init+pos" == params['Submit']:
            posName=""
	    if params['posName']!="":
		    posName = params['posName']
	    fonctions.SavePosInit(posName)
	    text = 'initial position saved'
	    self.send_headers(201)
	    print(text)

	if 'Submit' in params.keys() and "go+init+pos" == params['Submit']:
            posName=""
	    if params['posName']!="":
		    posName = params['posName']
	    fonctions.GoPosInit(posName)
	    text = 'Poppy in initial position'
	    self.send_headers(201)
	    print(text)

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
	    text = fonctions.SaveMovePart(poppyParts, moveName, semiMou, playedMove)
	    if text == 'move part saved':
		    self.send_headers(201)
	    else:
		    self.send_headers()
	    print(text)

	if 'Submit' in params.keys() and "create+move" == params['Submit']:
	    moveName=""
	    if params['moveName']!="":
		    moveName = params['moveName']
	    previsual= False
	    if params['previsu']=="True":
		    print "previsu mode"
		    previsual = True
	    exist = fonctions.directory(moveName)
	    if exist == '':
	    	    text = self.read_data(moveName, previsu = previsual)
		    print (text)
	    else:
		    self.send_headers()
		    text="move already exists"
		    print('move already exists')

	if 'Submit' in params.keys() and "create+exo" == params['Submit']:
	    exoName="dataPos.json"
	    if params['exoName']!="":
		    exoName = params['exoName']
	    exist = fonctions.directory(exoName)
	    if exist == '':
	    	    text = self.read_data(exoName)
		    print (text)
	    else:
		    self.send_headers()
		    text="move already exists"
		    print('move already exists')
	
	if 'Submit' in params.keys() and "symetry" == params['Submit']:
	    moveName="dataPos.json"
	    if params['moveName']!="":
		    moveName = params['moveName']
	    text = fonctions.symetry(moveName)
	    if 'exist' in text:
	    	    self.send_headers()
	    else:
		    self.send_headers(201)
	    print ("symetry file "+moveName+"Sym created")

	if 'Submit' in params.keys() and "reverse" == params['Submit']:
	    moveName="dataPos.json"
	    if params['moveName']!="":
		    moveName = params['moveName']
	    text = fonctions.reverse(moveName)
	    if 'exist' in text:
	    	    self.send_headers()
	    else:
		    self.send_headers(201)
	    print ("reverse file "+moveName+"Rev created")
		    
        if 'Submit' in params.keys() and "remove+move" == params['Submit']:
	    moveName=""
	    if params['moveName']!="":
		    moveName = params['moveName']
	    remove = fonctions.RemoveMove(moveName)
            if remove == True:
		self.send_headers(201)
		text="file removed"
            	print ('file removed')
            else:
		self.send_headers(200)
		text="file does not exist"
            	print ('file does not exist')

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
	    text = fonctions.GoMove(moveName, speed, poppyParts = poppyParts)
            if text == 'Poppy moved':
		self.send_headers(201)
            else:
		self.send_headers()
	    print (text)

        if 'Submit' in params.keys() and "go+reverse" == params['Submit']:
	    moveName=""
	    if params['moveName']!="":
		    moveName = params['moveName']
	    speed=2
	    if params['speed']!="":
		    speed = params['speed']
	    text = fonctions.GoMove(moveName, speed, rev=True)
            if text == 'Poppy moved':
		self.send_headers(201)
            else:
		self.send_headers()
	    print (text)

	if 'Submit' in params.keys() and "go+exo" == params['Submit']:
	    exoName=""
	    if params['exoName']!="":
		exoName = params['exoName']
	    text = fonctions.GoExo(exoName)
            if text == 'Exercice has started':
		exoCompo = self.send_data(exoName)
		text = ''
		self.send_headers(201)
		self.wfile.write(exoCompo)
            else:
		self.send_headers()
	    print (text)

	if 'Submit' in params.keys() and "go" == params['Submit']:
	    time.sleep(0.8) 	#le temps que le stop se fasse
	    exoName=""
	    if params['exoName']!="":
		exoName = params['exoName']
	    dir = fonctions.directory(exoName)
	    if dir == 'exo' or dir == 'seance':
		text = fonctions.GoExo(exoName)
		if text == 'Exercice has started':
			exoCompo = self.send_data(exoName)
			text = ''
			self.send_headers(201)
			self.wfile.write(exoCompo)
		else:
			self.send_headers()
	    else :
		text = fonctions.GoMove(exoName)
		if text == 'Move has started':
			self.send_headers(202)
		else:
			self.send_headers()
	    print (text)

	if 'Submit' in params.keys() and "stop+exo" == params['Submit']:
	    text = fonctions.StopExo()
            if  'stopped' in text:
		self.send_headers(201)
            else:
		self.send_headers()
	    print (text)

	if 'Submit' in params.keys() and "pause+exo" == params['Submit']:
	    text = fonctions.PauseExo()
            if text == 'move paused':
		self.send_headers(201)
            else:
		self.send_headers()
	    print (text)

	if 'Submit' in params.keys() and "resume+exo" == params['Submit']:
	    text = fonctions.ResumeExo()
            if 'resumed' in text:
		self.send_headers(201)
            else:
		self.send_headers()
	    print (text)

	if 'Submit' in params.keys() and "verif+fin+exo" == params['Submit']:
	    verif = fonctions.verifFinExo()
            if verif["info"] == 'end':
		self.send_headers(201)
            else:
		self.send_headers()
		self.wfile.write(verif)
	    
	if 'Submit' in params.keys() and "verif+fin+mov" == params['Submit']:
	    verif = fonctions.verifFinMov()
            if verif == 'end':
		self.send_headers(201)
            else:
		self.send_headers()

	if 'Submit' in params.keys() and "senddata" == params['Submit']:
		jsonfile="dataPos.json"
		if params['jsonfile']!="":
			jsonfile = params['jsonfile']
		self.read_data(jsonfile, 200)
		text="data ok !"
		print ('data ok !')

	self.wfile.write(text)

    def do_GET(self):
	print self.path	#pour voir ce qui a ete recu avant traitement
	parsed_path = urlparse(self.path) #recupere l'url de la requete
	try :
            params = dict([p.split('=') for p in parsed_path[4].split('&')])
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
	    jsondata = self.send_data(jsonfile, BDD)
	    jsondata = json.dumps(jsondata)
	    if jsondata == 'does not exist':
		self.send_headers(200)
		print ('does not exist!')
	    else:
		self.send_headers(201)
		self.wfile.write(jsondata)
		print ('data send!')
	    
	if 'Submit' in params.keys() and "getMesure" == params['Submit']:
		results = fonctions.scanResults()
		results = json.dumps(results)
		self.send_headers(200)
		self.wfile.write(results)

	print

        
#CREATION du serveur web
PORT = 4567
server_address = ("poppygr.local", PORT) #changer l'IP en fonction
server = BaseHTTPServer.HTTPServer
handler = RequestHandler
print "Serveur actif sur le port :", PORT
fonctions.mesure()	#start scanning the motors
httpd = server(server_address, handler)
httpd.serve_forever()

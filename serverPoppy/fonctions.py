from poppy_humanoid import PoppyHumanoid
import time
import os
import pypot.primitive
from pypot.dynamixel.io.abstract_io import AbstractDxlIO
from pypot.dynamixel.__init__ import get_available_ports
import json
import numpy
import socket
import csv
from collections import OrderedDict
#Creation de l'objet robot
Poppyboid = PoppyHumanoid() 

#variables moteurs
idmoteur=[m.id for m in Poppyboid.motors]	#variable ID
nbmoteurs=len(idmoteur)				#nombre de moteurs
temps=0						#variable temps
position=range(nbmoteurs)			#variable present position
voltage=range(nbmoteurs)			#variable inumpyut voltage
temperature=range(nbmoteurs)			#variable temperature
couple=range(nbmoteurs)				#variable pourcentage of couple
poppyPart_alert = {}			# dict contenant les parties du robot en surchauffe
SEUIL_TEMP = 53					# seuil de temperature pour alerter
SEUIL_TEMP_ARRET = 56			# seuil de temperature pour arreter le moteur
SecurityStop = False
#Ivalue=0					#variable intensite
TIME_LIMIT = 10
SEUIL_ANGLE = 5						# angle min de detection enregistrement et pour bouger
SEUIL_ANGLE_MAX = 20				# angle max a l'initialisation de la pos avant mvt
LIMITE_ANGLE = 40					# amplitude de mouvement : angle max de deplacement
SEMI_MOU = list()					# liste des parties Poppy en mode semi-mou
PLAYING_MOVE = False				# mouvement ou partie de mouvement en cours
MOVING_ENABLE = False				# autorisation mouvement (False = stop mouvement)
PLAYING_EXO = False				# exercice en cours ou non
EXO_ENABLE = False					# autorise exercice (False = stop exercice)
EXO_SLEEP = False					# pause exercice
PAUSE = False						# pause inter mouvement ou inter exercice
EXO_TEMPS = 0					# compteur de temps pendant exercice ou seance
EXO_TEMPS_LIMITE = 0				# valeur max de temps d'un exercice ou seance
NUM_EXO = 0						# numero de l'exercice en cours
NUM_MOV = 0						# numero du mouvement en cours
SCANNING = 0					# en train de scanner les positions moteurs ou non

t0 = time.time()

#ser=serial.Serial('/dev/ttyACM1', 9600)		#ouverture du port seriel pour mesure I
time.sleep(2)

#PRIMITIVES
#primitive enregistrement partie de sous-mouvement
class movePartPrimitive(pypot.primitive.Primitive):
	def __init__(self, robot, poppyParts, moveName):
		self.robot=robot
		self.poppyParts=poppyParts
		self.moveName=moveName
		pypot.primitive.Primitive.__init__(self, robot)	

	def run(self):
		global SEUIL_ANGLE
    		print 'scanning Poppy...'
		position= OrderedDict() #creation d'un dictionnaire avec maintien de l'ordre
		position["speed"]={}
		if "jambe_gauche" in self.poppyParts:
			position["speed"]["jambe_gauche"] = 0.2
		if "jambe_droite" in self.poppyParts:
			position["speed"]["jambe_droite"] = 0.2
		if "tete" in self.poppyParts:
			position["speed"]["tete"] = 0.2
		if "colonne" in self.poppyParts:
			position["speed"]["colonne"] = 0.2
		if "bras_gauche" in self.poppyParts:
			position["speed"]["bras_gauche"] = 0.2
		if "bras_droit" in self.poppyParts:
			position["speed"]["bras_droit"] = 0.2
		is_moving = True
		not_moving = False
		not_moving_counter = 0
		position_counter = 1
		
		while(not_moving == False): 
			print 'position '+str(position_counter)
			position[position_counter]={}
			if position_counter>10: 	# 2 secondes pour commencer le mouvement
				is_moving = False	#initialisation de la verification du mouvement
			#partie jambe gauche
			if "jambe_gauche" in self.poppyParts:
				position[position_counter]["11"]= Poppyboid.l_hip_x.present_position
				position[position_counter]["12"]= Poppyboid.l_hip_z.present_position
				position[position_counter]["13"]= Poppyboid.l_hip_y.present_position
				position[position_counter]["14"]= Poppyboid.l_knee_y.present_position
				position[position_counter]["15"]= Poppyboid.l_ankle_y.present_position
				if position_counter!=1 and is_moving == False:
					if abs(position[position_counter]["11"]-position[position_counter-1]["11"])>SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["12"]-position[position_counter-1]["12"])>SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["13"]-position[position_counter-1]["13"])>SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["14"]-position[position_counter-1]["14"])>SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["15"]-position[position_counter-1]["15"])>SEUIL_ANGLE:
						is_moving = True
			#partie jambe droite
			if "jambe_droite" in self.poppyParts:
				position[position_counter]["21"]= Poppyboid.r_hip_x.present_position
				position[position_counter]["22"]= Poppyboid.r_hip_z.present_position
				position[position_counter]["23"]= Poppyboid.r_hip_y.present_position
				#print "position m23 "+str(position_counter)+" : "+str(position[position_counter]["23"])
				position[position_counter]["24"]= Poppyboid.r_knee_y.present_position
				position[position_counter]["25"]= Poppyboid.r_ankle_y.present_position
				if position_counter!=1 and is_moving == False:
					if abs(position[position_counter]["21"]-position[position_counter-1]["21"])>SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["22"]-position[position_counter-1]["22"])>SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["23"]-position[position_counter-1]["23"])>SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["24"]-position[position_counter-1]["24"])>SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["25"]-position[position_counter-1]["25"])>SEUIL_ANGLE:
						is_moving = True
			#partie colonne
			if "colonne" in self.poppyParts:
				position[position_counter]["31"]= Poppyboid.abs_y.present_position
				position[position_counter]["32"]= Poppyboid.abs_x.present_position
				position[position_counter]["33"]= Poppyboid.abs_z.present_position
				position[position_counter]["34"]= Poppyboid.bust_y.present_position
				position[position_counter]["35"]= Poppyboid.bust_x.present_position
				if position_counter!=1 and is_moving == False:
					if abs(position[position_counter]["31"]-position[position_counter-1]["31"])>SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["32"]-position[position_counter-1]["32"])>SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["33"]-position[position_counter-1]["33"])>SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["34"]-position[position_counter-1]["34"])>SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["35"]-position[position_counter-1]["35"])>SEUIL_ANGLE:
						is_moving = True
			#partie tete
			if "tete" in self.poppyParts:
				position[position_counter]["36"]= Poppyboid.head_z.present_position
				position[position_counter]["37"]= Poppyboid.head_y.present_position
				if position_counter!=1 and is_moving == False:
					if abs(position[position_counter]["36"]-position[position_counter-1]["36"])>SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["37"]-position[position_counter-1]["37"])>SEUIL_ANGLE:
						is_moving = True
			#partie bras gauche
			if "bras_gauche" in self.poppyParts:
				position[position_counter]["41"]= Poppyboid.l_shoulder_y.present_position
				position[position_counter]["42"]= Poppyboid.l_shoulder_x.present_position
				position[position_counter]["43"]= Poppyboid.l_arm_z.present_position
				position[position_counter]["44"]= Poppyboid.l_elbow_y.present_position
				if position_counter!=1 and is_moving == False:
					if abs(position[position_counter]["41"]-position[position_counter-1]["41"])>SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["42"]-position[position_counter-1]["42"])>SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["43"]-position[position_counter-1]["43"])>SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["44"]-position[position_counter-1]["44"])>SEUIL_ANGLE:
						is_moving = True
			#partie bras droit
			if "bras_droit" in self.poppyParts:
				position[position_counter]["51"]= Poppyboid.r_shoulder_y.present_position
				position[position_counter]["52"]= Poppyboid.r_shoulder_x.present_position
				position[position_counter]["53"]= Poppyboid.r_arm_z.present_position
				position[position_counter]["54"]= Poppyboid.r_elbow_y.present_position
				if position_counter!=1 and is_moving == False:
					if abs(position[position_counter]["51"]-position[position_counter-1]["51"])>SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["52"]-position[position_counter-1]["52"])>SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["53"]-position[position_counter-1]["53"])>SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["54"]-position[position_counter-1]["54"])>SEUIL_ANGLE:
						is_moving = True
		
			time.sleep(0.2) #frequence d'enregistrement
			if is_moving == False:			# si ca a pas bouge ce tour ci
				not_moving_counter += 1 	# on compte combien de tours de suite
				if not_moving_counter == TIME_LIMIT: # si on a atteint la limite
					#supprime les increments immobiles
					if TIME_LIMIT>2 :
						position["nb_temps"]=position_counter-(TIME_LIMIT-2)
						for i in range(TIME_LIMIT-2):
							del position[position_counter-i]
					else:
						position["nb_temps"]=position_counter
					not_moving = True	# on sort de la boucle et on arrete
			else:
				not_moving_counter = 0		# sinon on recommence a compter
			position_counter += 1
		
		#export into a Json file ----------- Change file name if necessary
		with open('./move/mov/'+self.moveName+'.json', 'w') as f:
			json.dump(position, f, indent=4)
		time.sleep(0.2)
		print 'move saving done'


#primitive enregistrement position
class positionPrimitive(pypot.primitive.Primitive):
	def __init__(self, robot, posName='currentPos'):
		self.robot=robot
		self.posName=posName
		pypot.primitive.Primitive.__init__(self, robot)	

	def run(self):
		#print 'scanning Poppy...'
		global SCANNING
		SCANNING = 1
		position= OrderedDict() #creation d'un dictionnaire avec maintien de l'ordre
		#partie jambes
		position["11"]= Poppyboid.l_hip_x.present_position
		position["12"]= Poppyboid.l_hip_z.present_position
		position["13"]= Poppyboid.l_hip_y.present_position
		position["14"]= Poppyboid.l_knee_y.present_position
		position["15"]= Poppyboid.l_ankle_y.present_position
		position["21"]= Poppyboid.r_hip_x.present_position
		position["22"]= Poppyboid.r_hip_z.present_position
		position["23"]= Poppyboid.r_hip_y.present_position
		position["24"]= Poppyboid.r_knee_y.present_position
		position["25"]= Poppyboid.r_ankle_y.present_position
		position["31"]= Poppyboid.abs_y.present_position
		position["32"]= Poppyboid.abs_x.present_position
		#partie torso
		position["33"]= Poppyboid.abs_z.present_position
		position["34"]= Poppyboid.bust_y.present_position
		position["35"]= Poppyboid.bust_x.present_position
		position["36"]= Poppyboid.head_z.present_position
		position["37"]= Poppyboid.head_y.present_position
		position["41"]= Poppyboid.l_shoulder_y.present_position
		position["42"]= Poppyboid.l_shoulder_x.present_position
		position["43"]= Poppyboid.l_arm_z.present_position
		position["44"]= Poppyboid.l_elbow_y.present_position
		position["51"]= Poppyboid.r_shoulder_y.present_position
		position["52"]= Poppyboid.r_shoulder_x.present_position
		position["53"]= Poppyboid.r_arm_z.present_position
		position["54"]= Poppyboid.r_elbow_y.present_position
		#export into a Json file ----------- Change file name if necessary
		with open('./position/'+self.posName+'.json', 'w') as f:
			json.dump(position, f, indent=4)
		#print 'scanning done'
		SCANNING = 0
#attacher une primitive au robot : rend la primitive reutilisable dans d'autres primitives
Poppyboid.attach_primitive(positionPrimitive(Poppyboid), 'scanPosition')
Poppyboid.attach_primitive(positionPrimitive(Poppyboid, 'debout'), 'initDebout')
Poppyboid.attach_primitive(positionPrimitive(Poppyboid, 'assis'), 'initAssis')
		
#primitive mise en position
class miseEnPosPrimitive(pypot.primitive.Primitive):
	def __init__(self, robot, position, speed):
		self.robot=robot
		self.position=position
		self.speed=speed
		pypot.primitive.Primitive.__init__(self, robot)	

	def run(self):
		global SCANNING
		global SEUIL_ANGLE
		global LIMITE_ANGLE
		timeMultiplier = 2
		self.robot.scanPosition.start()
		time.sleep(0.1)
		while SCANNING == 1:
			time.sleep(0.05)
		positionActu={} #Position de depart
		positionFin={} #Position a atteindre
		#charge un fichier Json - position courante
		with open('./position/currentPos.json', 'r') as f:
		    positionActu = json.load(f)
	
		positionFin = self.position
		#print self.speed.keys()	
		if "jambe_gauche" in self.speed.keys() and "11" in positionFin:
			if abs(positionFin["11"]-positionActu["11"])>SEUIL_ANGLE :
				if abs(positionFin["11"]-positionActu["11"])>LIMITE_ANGLE:
					if positionFin["11"]-positionActu["11"]>0:
						positionFin["11"]=positionActu["11"]+LIMITE_ANGLE
					else:
						positionFin["11"]=positionActu["11"]-LIMITE_ANGLE
				self.robot.goto_position({'l_hip_x':positionFin["11"]}, timeMultiplier*self.speed["jambe_gauche"], wait=False)
			if abs(positionFin["12"]-positionActu["12"])>SEUIL_ANGLE :
				if abs(positionFin["12"]-positionActu["12"])>LIMITE_ANGLE:
					if positionFin["12"]-positionActu["12"]>0:
						positionFin["12"]=positionActu["12"]+LIMITE_ANGLE
					else:
						positionFin["12"]=positionActu["12"]-LIMITE_ANGLE
				self.robot.goto_position({'l_hip_z':positionFin["12"]}, timeMultiplier*self.speed["jambe_gauche"], wait=False)
			if abs(positionFin["13"]-positionActu["13"])>SEUIL_ANGLE :
				if abs(positionFin["13"]-positionActu["13"])>LIMITE_ANGLE:
					if positionFin["13"]-positionActu["13"]>0:
						positionFin["13"]=positionActu["13"]+LIMITE_ANGLE
					else:
						positionFin["13"]=positionActu["13"]-LIMITE_ANGLE
				self.robot.goto_position({'l_hip_y':positionFin["13"]}, timeMultiplier*self.speed["jambe_gauche"], wait=False)
			if abs(positionFin["14"]-positionActu["14"])>SEUIL_ANGLE :
				if abs(positionFin["14"]-positionActu["14"])>LIMITE_ANGLE:
					if positionFin["14"]-positionActu["14"]>0:
						positionFin["14"]=positionActu["14"]+LIMITE_ANGLE
					else:
						positionFin["14"]=positionActu["14"]-LIMITE_ANGLE
				self.robot.goto_position({'l_knee_y': positionFin["14"]}, timeMultiplier*self.speed["jambe_gauche"], wait=False)
			if abs(positionFin["15"]-positionActu["15"])>SEUIL_ANGLE :
				if abs(positionFin["15"]-positionActu["15"])>LIMITE_ANGLE:
					if positionFin["15"]-positionActu["15"]>0:
						positionFin["15"]=positionActu["15"]+LIMITE_ANGLE
					else:
						positionFin["15"]=positionActu["15"]-LIMITE_ANGLE
				self.robot.goto_position({'l_ankle_y':positionFin["15"]}, timeMultiplier*self.speed["jambe_gauche"], wait=False)
		if "jambe_droite" in self.speed.keys() and "21" in positionFin:
			if abs(positionFin["21"]-positionActu["21"])>SEUIL_ANGLE :
				if abs(positionFin["21"]-positionActu["21"])>LIMITE_ANGLE:
					if positionFin["21"]-positionActu["21"]>0:
						positionFin["21"]=positionActu["21"]+LIMITE_ANGLE
					else:
						positionFin["21"]=positionActu["21"]-LIMITE_ANGLE
				self.robot.goto_position({'r_hip_x':positionFin["21"]}, timeMultiplier*self.speed["jambe_droite"], wait=False)
			if abs(positionFin["22"]-positionActu["22"])>SEUIL_ANGLE :
				if abs(positionFin["22"]-positionActu["22"])>LIMITE_ANGLE:
					if positionFin["22"]-positionActu["22"]>0:
						positionFin["22"]=positionActu["22"]+LIMITE_ANGLE
					else:
						positionFin["22"]=positionActu["22"]-LIMITE_ANGLE
				self.robot.goto_position({'r_hip_z':positionFin["22"]}, timeMultiplier*self.speed["jambe_droite"], wait=False)
			if abs(positionFin["23"]-positionActu["23"])>SEUIL_ANGLE :
				if abs(positionFin["23"]-positionActu["23"])>LIMITE_ANGLE:
					if positionFin["23"]-positionActu["23"]>0:
						positionFin["23"]=positionActu["23"]+LIMITE_ANGLE
					else:
						positionFin["23"]=positionActu["23"]-LIMITE_ANGLE
				self.robot.goto_position({'r_hip_y': positionFin["23"]}, timeMultiplier*self.speed["jambe_droite"], wait=False)
			if abs(positionFin["24"]-positionActu["24"])>SEUIL_ANGLE :
				if abs(positionFin["24"]-positionActu["24"])>LIMITE_ANGLE:
					if positionFin["24"]-positionActu["24"]>0:
						positionFin["24"]=positionActu["24"]+LIMITE_ANGLE
					else:
						positionFin["24"]=positionActu["24"]-LIMITE_ANGLE
				self.robot.goto_position({'r_knee_y':positionFin["24"]}, timeMultiplier*self.speed["jambe_droite"], wait=False)
			if abs(positionFin["25"]-positionActu["25"])>SEUIL_ANGLE :
				if abs(positionFin["25"]-positionActu["25"])>LIMITE_ANGLE:
					if positionFin["25"]-positionActu["25"]>0:
						positionFin["25"]=positionActu["25"]+LIMITE_ANGLE
					else:
						positionFin["25"]=positionActu["25"]-LIMITE_ANGLE
				self.robot.goto_position({'r_ankle_y':positionFin["25"]}, timeMultiplier*self.speed["jambe_droite"], wait=False)
		if "colonne" in self.speed.keys() and "31" in positionFin:
			if abs(positionFin["31"]-positionActu["31"])>SEUIL_ANGLE :
				if abs(positionFin["31"]-positionActu["31"])>LIMITE_ANGLE:
					if positionFin["31"]-positionActu["31"]>0:
						positionFin["31"]=positionActu["31"]+LIMITE_ANGLE
					else:
						positionFin["31"]=positionActu["31"]-LIMITE_ANGLE
				self.robot.goto_position({'abs_y':positionFin["31"]}, timeMultiplier*self.speed["colonne"], wait=False)
			if abs(positionFin["32"]-positionActu["32"])>SEUIL_ANGLE :
				if abs(positionFin["32"]-positionActu["32"])>LIMITE_ANGLE:
					if positionFin["32"]-positionActu["32"]>0:
						positionFin["32"]=positionActu["32"]+LIMITE_ANGLE
					else:
						positionFin["32"]=positionActu["32"]-LIMITE_ANGLE
				self.robot.goto_position({'abs_x':positionFin["32"]}, timeMultiplier*self.speed["colonne"], wait=False)
			if abs(positionFin["33"]-positionActu["33"])>SEUIL_ANGLE :
				if abs(positionFin["33"]-positionActu["33"])>LIMITE_ANGLE:
					if positionFin["33"]-positionActu["33"]>0:
						positionFin["33"]=positionActu["33"]+LIMITE_ANGLE
					else:
						positionFin["33"]=positionActu["33"]-LIMITE_ANGLE
				self.robot.goto_position({'abs_z':positionFin["33"]}, timeMultiplier*self.speed["colonne"], wait=False)
			if abs(positionFin["34"]-positionActu["34"])>SEUIL_ANGLE :
				if abs(positionFin["34"]-positionActu["34"])>LIMITE_ANGLE:
					if positionFin["34"]-positionActu["34"]>0:
						positionFin["34"]=positionActu["34"]+LIMITE_ANGLE
					else:
						positionFin["34"]=positionActu["34"]-LIMITE_ANGLE
				self.robot.goto_position({'bust_y':positionFin["34"]}, timeMultiplier*self.speed["colonne"], wait=False)
			if abs(positionFin["35"]-positionActu["35"])>SEUIL_ANGLE :
				if abs(positionFin["35"]-positionActu["35"])>LIMITE_ANGLE:
					if positionFin["35"]-positionActu["35"]>0:
						positionFin["35"]=positionActu["35"]+LIMITE_ANGLE
					else:
						positionFin["35"]=positionActu["35"]-LIMITE_ANGLE
				self.robot.goto_position({'bust_x':positionFin["35"]}, timeMultiplier*self.speed["colonne"], wait=False)
		if "bras_droit" in self.speed.keys() and "51" in positionFin:
			if abs(positionFin["51"]-positionActu["51"])>SEUIL_ANGLE :
				if abs(positionFin["51"]-positionActu["51"])>LIMITE_ANGLE:
					if positionFin["51"]-positionActu["51"]>0:
						positionFin["51"]=positionActu["51"]+LIMITE_ANGLE
					else:
						positionFin["51"]=positionActu["51"]-LIMITE_ANGLE
				self.robot.goto_position({'r_shoulder_y':positionFin["51"]}, timeMultiplier*self.speed["bras_droit"], wait=False)
			if abs(positionFin["52"]-positionActu["52"])>SEUIL_ANGLE :
				if abs(positionFin["52"]-positionActu["52"])>LIMITE_ANGLE:
					if positionFin["52"]-positionActu["52"]>0:
						positionFin["52"]=positionActu["52"]+LIMITE_ANGLE
					else:
						positionFin["52"]=positionActu["52"]-LIMITE_ANGLE
				self.robot.goto_position({'r_shoulder_x':positionFin["52"]}, timeMultiplier*self.speed["bras_droit"], wait=False)
			if abs(positionFin["53"]-positionActu["53"])>SEUIL_ANGLE :
				if abs(positionFin["53"]-positionActu["53"])>LIMITE_ANGLE:
					if positionFin["53"]-positionActu["53"]>0:
						positionFin["53"]=positionActu["53"]+LIMITE_ANGLE
					else:
						positionFin["53"]=positionActu["53"]-LIMITE_ANGLE
				self.robot.goto_position({'r_arm_z':positionFin["53"]}, timeMultiplier*self.speed["bras_droit"], wait=False)
			if abs(positionFin["54"]-positionActu["54"])>SEUIL_ANGLE :
				if abs(positionFin["54"]-positionActu["54"])>LIMITE_ANGLE:
					if positionFin["54"]-positionActu["54"]>0:
						positionFin["54"]=positionActu["54"]+LIMITE_ANGLE
					else:
						positionFin["54"]=positionActu["54"]-LIMITE_ANGLE
				self.robot.goto_position({'r_elbow_y': positionFin["54"]}, timeMultiplier*self.speed["bras_droit"], wait=False)
		if "bras_gauche" in self.speed.keys() and "41" in positionFin:
			if abs(positionFin["41"]-positionActu["41"])>SEUIL_ANGLE :
				if abs(positionFin["41"]-positionActu["41"])>LIMITE_ANGLE:
					if positionFin["41"]-positionActu["41"]>0:
						positionFin["41"]=positionActu["41"]+LIMITE_ANGLE
					else:
						positionFin["41"]=positionActu["41"]-LIMITE_ANGLE
				Poppyboid.goto_position({'l_shoulder_y':positionFin["41"]},timeMultiplier*self.speed["bras_gauche"], wait=False)
			if abs(positionFin["42"]-positionActu["42"])>SEUIL_ANGLE:
				if abs(positionFin["42"]-positionActu["42"])>LIMITE_ANGLE:
					if positionFin["42"]-positionActu["42"]>0:
						positionFin["42"]=positionActu["42"]+LIMITE_ANGLE
					else:
						positionFin["42"]=positionActu["42"]-LIMITE_ANGLE
				self.robot.goto_position({'l_shoulder_x':positionFin["42"]}, timeMultiplier*self.speed["bras_gauche"], wait=False)
			if abs(positionFin["43"]-positionActu["43"])>SEUIL_ANGLE :
				if abs(positionFin["43"]-positionActu["43"])>LIMITE_ANGLE:
					if positionFin["43"]-positionActu["43"]>0:
						positionFin["43"]=positionActu["43"]+LIMITE_ANGLE
					else:
						positionFin["43"]=positionActu["43"]-LIMITE_ANGLE
				self.robot.goto_position({'l_arm_z':positionFin["43"]}, timeMultiplier*self.speed["bras_gauche"], wait=False)
			if abs(positionFin["44"]-positionActu["44"])>SEUIL_ANGLE :
				if abs(positionFin["44"]-positionActu["44"])>LIMITE_ANGLE:
					if positionFin["44"]-positionActu["44"]>0:
						positionFin["44"]=positionActu["44"]+LIMITE_ANGLE
					else:
						positionFin["44"]=positionActu["44"]-LIMITE_ANGLE
				self.robot.goto_position({'l_elbow_y': positionFin["44"]}, timeMultiplier*self.speed["bras_gauche"], wait=False)
		if "tete" in self.speed.keys() and "36" in positionFin:
			if abs(positionFin["36"]-positionActu["36"])>SEUIL_ANGLE :
				if abs(positionFin["36"]-positionActu["36"])>LIMITE_ANGLE:
					if positionFin["36"]-positionActu["36"]>0:
						positionFin["36"]=positionActu["36"]+LIMITE_ANGLE
					else:
						positionFin["36"]=positionActu["36"]-LIMITE_ANGLE
				self.robot.goto_position({'head_z':positionFin["36"]}, timeMultiplier*self.speed["tete"], wait=False)
			if abs(positionFin["37"]-positionActu["37"])>SEUIL_ANGLE :
				if abs(positionFin["37"]-positionActu["37"])>LIMITE_ANGLE:
					if positionFin["37"]-positionActu["37"]>0:
						positionFin["37"]=positionActu["37"]+LIMITE_ANGLE
					else:
						positionFin["37"]=positionActu["37"]-LIMITE_ANGLE
				self.robot.goto_position({'head_y':positionFin["37"]}, timeMultiplier*self.speed["tete"], wait=False)
		#Pour laisser le temps au robot d'effectuer le mouvement : t_sleep>t_mouvement
		#time.sleep(1)     

class goMovePrimitive(pypot.primitive.Primitive):
	def __init__(self, robot, rev, moveType, moveName, speedDict, tempsboucle, startTime, endTime):
		self.robot=robot
		self.rev=rev
		self.moveType=moveType
		self.moveName=moveName
		self.speedDict=speedDict
		self.tempsboucle=tempsboucle
		self.startTime=startTime
		self.endTime=endTime
		pypot.primitive.Primitive.__init__(self, robot)
		
	def run(self):
		global EXO_TEMPS
		global EXO_SLEEP
		global EXO_ENABLE
		global MOVING_ENABLE
		global PLAYING_MOVE

		while PLAYING_MOVE:	# attente que la partie du mouvement precedent se termine
			time.sleep(0.1)
		PLAYING_MOVE = True
		#time.sleep(0.5)		#attente le temps que mov precedent se termine
		print "startTime : "+str(self.startTime)+", endTime : "+str(self.endTime)
		with open('./move/'+self.moveType+'/'+self.moveName+'.json', 'r') as f:
			moveFile = json.load(f)
		if self.rev == False:
			for temps in range(self.startTime, self.endTime):
				while EXO_SLEEP == True and MOVING_ENABLE == True:
					time.sleep(0.1)
				if MOVING_ENABLE == False:
					PLAYING_MOVE = False
					print "---stop moving primitive 1---"
					return
				if temps+1 == 1:
					goFirstPos(moveFile[str(temps+1)], moveFile["speed"])
				else:
					if str(temps+1) in moveFile:
						miseEnPosPrimitive(Poppyboid,moveFile[str(temps+1)], self.speedDict).start()
					if MOVING_ENABLE == False:
						PLAYING_MOVE = False
						print "---stop moving primitive 2---"
						return
					time.sleep(self.tempsboucle)
				EXO_TEMPS += 1
		else:
			return	#TODO : lecture a l'envers non geree !!!
			for temps in range(moveFile["nb_temps"]):
				while EXO_SLEEP == True and MOVING_ENABLE == True:
					time.sleep(0.2)
				if MOVING_ENABLE == False:
					PLAYING_MOVE = False
					print "---stop moving primitive 1---"
					return
				if temps+1 == 1:
					goFirstPos(moveFile[str(moveFile["nb_temps"]-temps)], moveFile["speed"])
				else:
					if str(moveFile["nb_temps"]-temps) in moveFile:
						miseEnPosPrimitive(Poppyboid,moveFile[str(moveFile["nb_temps"]-temps)], self.speedDict).start()
					if MOVING_ENABLE == False:
						PLAYING_MOVE = False
						print "---stop moving primitive 2---"
						return
					time.sleep(self.tempsboucle)
				EXO_TEMPS += 1
		PLAYING_MOVE = False
		if self.endTime == moveFile["nb_temps"]:	#si on est a la derniere partie
			MOVING_ENABLE = False

#primitive jouer un exo ou une seance
class goExoPrimitive(pypot.primitive.Primitive):
	def __init__(self, robot, exoName, exoType):
		self.robot=robot
		self.exoName=exoName
		self.exoType=exoType
		pypot.primitive.Primitive.__init__(self, robot)	

	def run(self):
		global PLAYING_EXO
		global EXO_ENABLE
		global EXO_SLEEP
		global EXO_TEMPS
		global EXO_TEMPS_LIMITE
		global TIME_LIMIT
		global NUM_EXO
		global NUM_MOV
		global PAUSE
		NUM_MOV = 0
		with open('./move/'+self.exoType+'/'+self.exoName+'.json', 'r') as f:
			moveConfig= json.load(f)

		for i in range(moveConfig["nb_fichiers"]):		#verifie les parametres du fichier config
			while EXO_SLEEP == True and EXO_ENABLE == True:				#tant que l'exercice est en pause
				time.sleep(0.05)
			if EXO_ENABLE == False:					#si ordre d'arreter la primitive
				break
			namefile = moveConfig["fichier"+str(i+1)]["namefile"]
			#Si c'est un exercice
			if directory(namefile) == "exo":
				time.sleep(1.5)
				while (PLAYING_EXO == True):	#on attend que pas d'exo en cours
					time.sleep(0.2)
				if EXO_ENABLE == False:			#si ordre d'arreter la primitive
					print "---stop seance 1---"
					return
				NUM_EXO +=1
				NUM_MOV = 0
				if i==0:
					time.sleep(1)
				elif moveConfig["fichier"+str(i)]["pause"] == 0:
					time.sleep(1)
				else:
					PAUSE = True
					time.sleep(moveConfig["fichier"+str(i)]["pause"])
					PAUSE = False
					EXO_TEMPS += int(moveConfig["fichier"+str(i)]["pause"])
				if EXO_ENABLE == False:			#si ordre d'arreter la primitive
					print "---stop seance 2---"
					return
				goExoPrimitive(self.robot,namefile, "exo").start()
				time.sleep(1)
			#si c'est un mouvement
			else: 
				PLAYING_EXO = True
				speed = moveConfig["fichier"+str(i+1)]["vitesse"]
			#JOUE LE MOUVEMENT i+1
				NUM_MOV +=1
				move = GoMove(namefile, speed)
				if move == "stop":
					print "---stop exo via stop move---"
					PLAYING_EXO = False
					return
				if EXO_ENABLE == False:			#si ordre d'arreter la primitive
					print "---stop exo 1---"
					PLAYING_EXO = False
					return
				PAUSE = True
				if moveConfig["fichier"+str(i+1)]["pause"]!=0:
					time.sleep(moveConfig["fichier"+str(i+1)]["pause"])
				PAUSE = False
				EXO_TEMPS += moveConfig["fichier"+str(i+1)]["pause"]
				PLAYING_EXO = False
				if EXO_ENABLE == False:			#si ordre d'arreter la primitive
					print "---stop exo 2---"
					PLAYING_EXO = False
					return
		#		if move != "Poppy moved":
		#			return move
		if EXO_TEMPS>=EXO_TEMPS_LIMITE:
			EXO_ENABLE = False
		#return "played"

#primitive mode semi-mou
class semiCompliantPrimitive(pypot.primitive.Primitive):
	def run(self):
		t = 0.01
		global SEMI_MOU
		while len(SEMI_MOU) != 0:
			if "jambe_gauche" in SEMI_MOU :
				self.robot.goto_position({'l_hip_x':self.robot.l_hip_x.present_position}, t, wait=False)
				self.robot.goto_position({'l_hip_z':self.robot.l_hip_z.present_position}, t, wait=False)
				self.robot.goto_position({'l_hip_y':self.robot.l_hip_y.present_position}, t, wait=False)
				self.robot.goto_position({'l_knee_y': self.robot.l_knee_y.present_position}, t, wait=False)
				self.robot.goto_position({'l_ankle_y':self.robot.l_ankle_y.present_position}, t, wait=False)
			if "jambe_droite" in SEMI_MOU :
				self.robot.goto_position({'r_hip_x':self.robot.r_hip_x.present_position}, t, wait=False)
				self.robot.goto_position({'r_hip_z':self.robot.r_hip_z.present_position}, t, wait=False)
				self.robot.goto_position({'r_hip_y': self.robot.r_hip_y.present_position}, t, wait=False)
				self.robot.goto_position({'r_knee_y':self.robot.r_knee_y.present_position}, t, wait=False)
				self.robot.goto_position({'r_ankle_y':self.robot.r_ankle_y.present_position}, t, wait=False)
			if "colonne" in SEMI_MOU :
				self.robot.goto_position({'abs_y':self.robot.abs_y.present_position}, t, wait=False)
				self.robot.goto_position({'abs_x':self.robot.abs_x.present_position}, t, wait=False)
				self.robot.goto_position({'abs_z':self.robot.abs_z.present_position}, t, wait=False)
				self.robot.goto_position({'bust_y':self.robot.bust_y.present_position}, t, wait=False)
				self.robot.goto_position({'bust_x':self.robot.bust_x.present_position}, t, wait=False)
			if "bras_droit" in SEMI_MOU :
				self.robot.goto_position({'r_shoulder_y':self.robot.r_shoulder_y.present_position}, t, wait=False)
				self.robot.goto_position({'r_shoulder_x':self.robot.r_shoulder_x.present_position}, t, wait=False)
				self.robot.goto_position({'r_arm_z':self.robot.r_arm_z.present_position}, t, wait=False)
				self.robot.goto_position({'r_elbow_y': self.robot.r_elbow_y.present_position}, t, wait=False)
			if "bras_gauche" in SEMI_MOU :
				self.robot.goto_position({'l_shoulder_y':self.robot.l_shoulder_y.present_position},t, wait=False)
				self.robot.goto_position({'l_shoulder_x':self.robot.l_shoulder_x.present_position}, t, wait=False)
				self.robot.goto_position({'l_arm_z':self.robot.l_arm_z.present_position}, t, wait=False)
				self.robot.goto_position({'l_elbow_y': self.robot.l_elbow_y.present_position}, t, wait=False)
			if "tete" in SEMI_MOU :
				self.robot.goto_position({'head_z':self.robot.head_z.present_position}, t, wait=False)
				self.robot.goto_position({'head_y':self.robot.head_y.present_position}, t, wait=False)
			time.sleep(t/2.0)

def setSecurityMode():
	global SecurityStop
	SecurityStop = True

#mesure de l'etat des moteurs
def scanMotors(idmoteur, t0):
	global position
	global violtage
	global temperature
	global couple
	global poppyPart_alert
	global SEUIL_TEMP
	global SEUIL_TEMP_ARRET
	global SecurityStop
	stop = False
	temps = time.time()-t0
	#mesures
	imoteur=0
	poppyPart_alert['JG'] = 'ok'
	poppyPart_alert['JD'] = 'ok'
	poppyPart_alert['T'] = 'ok'
	poppyPart_alert['Col'] = 'ok'
	poppyPart_alert['BG'] = 'ok'
	poppyPart_alert['BD'] = 'ok'

	for m in Poppyboid.motors:
		position[imoteur] = m.present_position
		voltage[imoteur] = m.present_voltage
		temperature[imoteur] = m.present_temperature
		couple[imoteur] = m.present_load
		if round(temperature[imoteur], 1)>=SEUIL_TEMP:
			if idmoteur[imoteur]>=11 and idmoteur[imoteur]<=19:
				poppyPart = "JG"
			if idmoteur[imoteur]>=21 and idmoteur[imoteur]<=29:
				poppyPart = "JD"
			if idmoteur[imoteur]>=31 and idmoteur[imoteur]<=35:
				poppyPart = "Col"
			if idmoteur[imoteur]>=36 and idmoteur[imoteur]<=37:
				poppyPart = "T"
				Compliant("tete")	#desactive la tete car chauffe vite
			if idmoteur[imoteur]>=41 and idmoteur[imoteur]<=49:
				poppyPart = "BG"
			if idmoteur[imoteur]>=51 and idmoteur[imoteur]<=59:
				poppyPart = "BD"
			if poppyPart not in poppyPart_alert:
				poppyPart_alert[poppyPart]=""
			if poppyPart_alert[poppyPart]!="stop" and round(temperature[imoteur],1)<SEUIL_TEMP_ARRET:
				poppyPart_alert[poppyPart]="warning"
			elif round(temperature[imoteur],1)>=SEUIL_TEMP_ARRET:
				poppyPart_alert[poppyPart]="stop"
				stop = True
		imoteur=imoteur+1
	if stop == True and SecurityStop == False:
		if not poppyCompliant():
			print "set security mode"
			setSecurityMode()
			time.sleep(10)
			print "security mode : stop exo"
			StopExo()
			time.sleep(5)
			print "security mode : semi compliant"
			semiCompliant()
			time.sleep(20)
			print "security mode : compliant"
			Compliant()
			time.sleep(5)
			print "security mode OFF"
			SecurityStop = False


#primitive scan moteurs regulier
class scanMotorsLoop(pypot.primitive.Primitive):
	def __init__(self, Poppyboid, idmoteur, t0):
		pypot.primitive.Primitive.__init__(self, Poppyboid)
		self.Poppyboid=Poppyboid
		self.idmoteur=idmoteur
		self.t0=t0

	def run(self):
		while True:
			scanMotors(self.idmoteur, self.t0)
			time.sleep(5)

Poppyboid.attach_primitive(scanMotorsLoop(Poppyboid, idmoteur, t0), 'scan')

def scanResults():
	global position
	global voltage
	global temperature
	global couple
	global poppyPart_alert
	results = {}
	results["position"]={}
	results["voltage"]={}
	results["temperature"]={}
	results["couple"]={}
	results["temperature"]["max"]=0
	for imoteur in range(nbmoteurs):		
		#print"ID : ", idmoteur[imoteur], "\t", round(temps, 2), "s\tposition : ", position[imoteur], "\tvoltage : ", round(voltage[imoteur], 1), "\ttemperature : ", temperature[imoteur], "\tcouple : ", couple[imoteur]
		results["position"][idmoteur[imoteur]] = position[imoteur]
		results["voltage"][idmoteur[imoteur]] = round(voltage[imoteur], 1)
		results["temperature"][idmoteur[imoteur]] = round(temperature[imoteur], 1)
		results["couple"][idmoteur[imoteur]] = couple[imoteur]
		if round(temperature[imoteur], 1)>results["temperature"]["max"]:
			results["temperature"]["max"]=round(temperature[imoteur], 1)
	if "poppyPart_alert" in results:
		del results["poppyPart_alert"]
	results["poppyPart_alert"]=poppyPart_alert

	results[u'compliant'] = poppyCompliant()
	results[u'compliant'] = "u'"+str(results[u'compliant'] )+"'"
	results[u'compliantBG'] = "u'"+str(Poppyboid.l_arm_z.compliant)+"'"
	results[u'compliantBD'] = "u'"+str(Poppyboid.r_arm_z.compliant)+"'"
	results[u'compliantT'] = "u'"+str(Poppyboid.head_z.compliant)+"'"
	results[u'compliantJG'] = "u'"+str(Poppyboid.l_hip_z.compliant)+"'"
	results[u'compliantJD'] = "u'"+str(Poppyboid.r_hip_z.compliant)+"'"
	results[u'compliantCol'] = "u'"+str(Poppyboid.abs_z.compliant)+"'"
	return results

#FONCTIONS
def Compliant(poppyParts='all'): 
	global SEMI_MOU
	print ('Poppy gets compliant')
	if poppyParts == 'all':
		while len(SEMI_MOU)>0:
			del SEMI_MOU[0]
		for m in Poppyboid.motors: 
			m.compliant = True 
	else :
		if 'jambe_gauche' in poppyParts:
			if 'jambe_gauche' in SEMI_MOU:
				SEMI_MOU.remove("jambe_gauche")
			Poppyboid.l_hip_x.compliant = True
			Poppyboid.l_hip_z.compliant = True
			Poppyboid.l_hip_y.compliant = True
			Poppyboid.l_knee_y.compliant = True
			Poppyboid.l_ankle_y.compliant = True
		if 'jambe_droite' in poppyParts:
			if 'jambe_droite' in SEMI_MOU:
				SEMI_MOU.remove("jambe_droite")
			Poppyboid.r_hip_x.compliant = True
			Poppyboid.r_hip_z.compliant = True
			Poppyboid.r_hip_y.compliant = True
			Poppyboid.r_knee_y.compliant = True
			Poppyboid.r_ankle_y.compliant = True
		if 'bras_gauche' in poppyParts:
			if 'bras_gauche' in SEMI_MOU:
				SEMI_MOU.remove("bras_gauche")
			Poppyboid.l_shoulder_y.compliant = True
			Poppyboid.l_shoulder_x.compliant = True
			Poppyboid.l_arm_z.compliant = True
			Poppyboid.l_elbow_y.compliant = True
		if 'bras_droit' in poppyParts:
			if 'bras_droit' in SEMI_MOU:
				SEMI_MOU.remove("bras_droit")
			Poppyboid.r_shoulder_y.compliant = True
			Poppyboid.r_shoulder_x.compliant = True
			Poppyboid.r_arm_z.compliant = True
			Poppyboid.r_elbow_y.compliant = True
		if 'colonne' in poppyParts:
			if 'colonne' in SEMI_MOU:
				SEMI_MOU.remove("colonne")
			Poppyboid.abs_y.compliant = True
			Poppyboid.abs_x.compliant = True
			Poppyboid.abs_z.compliant = True
			Poppyboid.bust_y.compliant = True
			Poppyboid.bust_x.compliant = True
		if 'tete' in poppyParts:
			if 'tete' in SEMI_MOU:
				SEMI_MOU.remove("tete")
			Poppyboid.head_z.compliant = True
			Poppyboid.head_y.compliant = True

def NonCompliant(poppyParts='all', torqueLimit = 100, notMoving = False): 
	print ('Poppy gets non-compliant')
	sleep = 0
	if poppyParts == 'all':
		while len(SEMI_MOU)>0:
			del SEMI_MOU[0]
			sleep = 1
		for m in Poppyboid.motors: 
			m.torque_limit = torqueLimit
			m.compliant = False 
	else:
		poppyPartsCompliant = list()
		if 'jambe_gauche' in poppyParts:
			if 'jambe_gauche' in SEMI_MOU and torqueLimit==100:
				SEMI_MOU.remove("jambe_gauche")
				sleep=1
			Poppyboid.l_hip_x.torque_limit = torqueLimit
			Poppyboid.l_hip_x.compliant = False
			Poppyboid.l_hip_z.torque_limit = torqueLimit
			Poppyboid.l_hip_z.compliant = False
			Poppyboid.l_hip_y.torque_limit = torqueLimit
			Poppyboid.l_hip_y.compliant = False
			Poppyboid.l_knee_y.torque_limit = torqueLimit
			Poppyboid.l_knee_y.compliant = False
			Poppyboid.l_ankle_y.torque_limit = torqueLimit
			Poppyboid.l_ankle_y.compliant = False
		elif 'jambe_gauche' not in SEMI_MOU:
			poppyPartsCompliant.append('jambe_gauche')
		if 'jambe_droite' in poppyParts:
			if 'jambe_droite' in SEMI_MOU and torqueLimit==100:
				SEMI_MOU.remove("jambe_droite")
				sleep=1
			Poppyboid.r_hip_x.torque_limit = torqueLimit
			Poppyboid.r_hip_x.compliant = False
			Poppyboid.r_hip_z.torque_limit = torqueLimit
			Poppyboid.r_hip_z.compliant = False
			Poppyboid.r_hip_y.torque_limit = torqueLimit
			Poppyboid.r_hip_y.compliant = False
			Poppyboid.r_knee_y.torque_limit = torqueLimit
			Poppyboid.r_knee_y.compliant = False
			Poppyboid.r_ankle_y.torque_limit = torqueLimit
			Poppyboid.r_ankle_y.compliant = False
		elif 'jambe_droite' not in SEMI_MOU:
			poppyPartsCompliant.append('jambe_droite')
		if 'bras_gauche' in poppyParts:
			if 'bras_gauche' in SEMI_MOU and torqueLimit==100:
				SEMI_MOU.remove("bras_gauche")
				sleep=1
			Poppyboid.l_shoulder_y.torque_limit = torqueLimit
			Poppyboid.l_shoulder_y.compliant = False
			Poppyboid.l_shoulder_x.torque_limit = torqueLimit
			Poppyboid.l_shoulder_x.compliant = False
			Poppyboid.l_arm_z.torque_limit = torqueLimit
			Poppyboid.l_arm_z.compliant = False
			Poppyboid.l_elbow_y.torque_limit = torqueLimit
			Poppyboid.l_elbow_y.compliant = False
		elif 'bras_gauche' not in SEMI_MOU:
			poppyPartsCompliant.append('bras_gauche')
		if 'bras_droit' in poppyParts:
			if 'bras_droit' in SEMI_MOU and torqueLimit==100:
				SEMI_MOU.remove("bras_droit")
				sleep=1
			Poppyboid.r_shoulder_y.torque_limit = torqueLimit
			Poppyboid.r_shoulder_y.compliant = False
			Poppyboid.r_shoulder_x.torque_limit = torqueLimit
			Poppyboid.r_shoulder_x.compliant = False
			Poppyboid.r_arm_z.torque_limit = torqueLimit
			Poppyboid.r_arm_z.compliant = False
			Poppyboid.r_elbow_y.torque_limit = torqueLimit
			Poppyboid.r_elbow_y.compliant = False
		elif 'bras_droit' not in SEMI_MOU:
			poppyPartsCompliant.append('bras_droit')
		if 'colonne' in poppyParts:
			if 'colonne' in SEMI_MOU and torqueLimit==100:
				SEMI_MOU.remove("colonne")
				sleep=1
			Poppyboid.abs_y.torque_limit = torqueLimit
			Poppyboid.abs_y.compliant = False
			Poppyboid.abs_x.torque_limit = torqueLimit
			Poppyboid.abs_x.compliant = False
			Poppyboid.abs_z.torque_limit = torqueLimit
			Poppyboid.abs_z.compliant = False
			Poppyboid.bust_y.torque_limit = torqueLimit
			Poppyboid.bust_y.compliant = False
			Poppyboid.bust_x.torque_limit = torqueLimit
			Poppyboid.bust_x.compliant = False
		elif 'colonne' not in SEMI_MOU:
			poppyPartsCompliant.append('colonne')
		if 'tete' in poppyParts:
			if 'tete' in SEMI_MOU and torqueLimit==100:
				SEMI_MOU.remove("tete")
				sleep=1
			Poppyboid.head_z.torque_limit = torqueLimit
			Poppyboid.head_z.compliant = False
			Poppyboid.head_y.torque_limit = torqueLimit
			Poppyboid.head_y.compliant = False
		elif 'tete' not in SEMI_MOU:
			poppyPartsCompliant.append('tete')
		if notMoving == True:
			Compliant(poppyPartsCompliant)
	time.sleep(sleep)

def semiCompliant(poppyParts='all'): 
	global SEMI_MOU
	print ('Poppy gets semi-compliant')
	if len(SEMI_MOU)>0:
		NonCompliant(SEMI_MOU)
	while len(SEMI_MOU)>0:
		NonCompliant(SEMI_MOU)
		del SEMI_MOU[0]
	time.sleep(1)
	for i in range(len(poppyParts)):
		SEMI_MOU.append(poppyParts[i]) 
	print SEMI_MOU
	NonCompliant(poppyParts, torqueLimit = 1)
	semiCompliantPrimitive(Poppyboid).start()

def SavePosInit(namePos):
	print('save init position')
	#positionPrimitive(Poppyboid, namePos).start
	if namePos == 'debout':
		Poppyboid.initDebout.start()
	elif namePos == 'assis':
		Poppyboid.initAssis.start()
	time.sleep(1.5)
	
def GoPosInit(namePos):
	print ('going to initial position')
	speed = {}
	speed["tete"] = 0.1
	speed["colonne"] = 0.1
	speed["bras_gauche"] = 0.1
	speed["bras_droit"] = 0.1
	speed["jambe_gauche"] = 0.1
	speed["jambe_droite"] = 0.1
	with open('./position/'+namePos+'.json', 'r') as f:
		    position = json.load(f)
	NonCompliant()
	time.sleep(0.5)
	goFirstPos(position, speed, 'True')
	time.sleep(0.5)

def SaveMovePart(poppyParts, moveName, semiMou, playedMove = ''):
	print ('going to save move part')
	NonCompliant(poppyParts)
	time.sleep(0.5)
	#TODO : Rajouter un bruit sonore
	if semiMou == 'True':
		semiCompliant(poppyParts)
	else:
		Compliant(poppyParts)
	if directory(moveName) != '':
		return 'move already exists'
	#Verification, si on joue mov en meme temps (playedMove), que pas de doublons PoppyParts
	if playedMove!= '':
		dir = directory(playedMove)
		if dir == '':
			return 'move to play '+playedMove+' does not exist'
		elif dir == 'exo' or dir == 'seance':
			return 'move to play '+playedMove+' is not a move'
		with open('./move/'+dir+'/'+playedMove+'.json', 'r') as f:
			moveToPlay = json.load(f)
		for i in range(len(poppyParts)):
			if poppyParts[i] in moveToPlay["speed"].keys():
				return poppyParts[i]+' is already in the move to play' 
	saveMovePart = movePartPrimitive(Poppyboid, poppyParts, moveName)
	saveMovePart.start()
	if playedMove != '' :
		GoMove(playedMove, save = True)
	saveMovePart.join()
	NonCompliant(poppyParts)
	majMoveList('mov', moveName, poppyParts)
	time.sleep(0.2)
	Compliant(poppyParts)
	#TODO : Rajouter un bruit sonore
	return 'move part saved'
	
	#mise a jour de la liste des fichiers mouvements
def majMoveList(moveDir, moveName, poppyParts):
	with open('./move/movelist.json','r') as f:
		jsondata = json.load(f)
	print moveDir+" saved"
	if moveName not in jsondata["list_"+moveDir]:
		jsondata["nb_"+moveDir] += 1
	jsondata["list_"+moveDir][moveName] = poppyParts
	with open('./move/movelist.json','w') as f:
		json.dump(jsondata, f, indent=4)

def symetry(moveName):
	dir = directory(moveName)
	if dir == '':
		return 'move file does not exist'
	if dir != 'mov':
		return 'not a move'
	moveFile = './move/'+dir+'/'+moveName+'.json'
	symName = moveName+'Sym'
	symFile = './move/'+dir+'/'+symName+'.json'
	if directory(symName) != '':
		return 'symetry '+symName+' already exists'
	with open(moveFile, 'r') as f:
		moveData = json.load(f)
	symData = {}
	symData["nb_temps"] = moveData["nb_temps"]
	for nb_temps in range(moveData["nb_temps"]):
		if str(nb_temps+1) in moveData :
			symData[str(nb_temps+1)] = {}
		if '41' in moveData[str(nb_temps+1)] : 	#bras gauche en bras droit
			symData[str(nb_temps+1)]["51"] = moveData[str(nb_temps+1)]["41"]
			symData[str(nb_temps+1)]["52"] = - moveData[str(nb_temps+1)]["42"]
			symData[str(nb_temps+1)]["53"] = - moveData[str(nb_temps+1)]["43"]
			symData[str(nb_temps+1)]["54"] = moveData[str(nb_temps+1)]["44"]
		if '51' in moveData[str(nb_temps+1)] : 	#bras droit en bras gauche
			symData[str(nb_temps+1)]["41"] = moveData[str(nb_temps+1)]["51"]
			symData[str(nb_temps+1)]["42"] = - moveData[str(nb_temps+1)]["52"]
			symData[str(nb_temps+1)]["43"] = - moveData[str(nb_temps+1)]["53"]
			symData[str(nb_temps+1)]["44"] = moveData[str(nb_temps+1)]["54"]
		if '11' in moveData[str(nb_temps+1)] : 	#jambe gauche en jambe droite
			symData[str(nb_temps+1)]["21"] = - moveData[str(nb_temps+1)]["11"]
			symData[str(nb_temps+1)]["22"] = - moveData[str(nb_temps+1)]["12"]
			symData[str(nb_temps+1)]["23"] = moveData[str(nb_temps+1)]["13"]
			symData[str(nb_temps+1)]["24"] = moveData[str(nb_temps+1)]["14"]
			symData[str(nb_temps+1)]["25"] = moveData[str(nb_temps+1)]["15"]
		if '21' in moveData[str(nb_temps+1)] : 	#jambe droite en jambe gauche
			symData[str(nb_temps+1)]["11"] = - moveData[str(nb_temps+1)]["21"]
			symData[str(nb_temps+1)]["12"] = - moveData[str(nb_temps+1)]["22"]
			symData[str(nb_temps+1)]["13"] = moveData[str(nb_temps+1)]["23"]
			symData[str(nb_temps+1)]["14"] = moveData[str(nb_temps+1)]["24"]
			symData[str(nb_temps+1)]["15"] = moveData[str(nb_temps+1)]["25"]
		if '31' in moveData[str(nb_temps+1)] : 	#colonne
			symData[str(nb_temps+1)]["31"] = moveData[str(nb_temps+1)]["31"]
			symData[str(nb_temps+1)]["32"] = - moveData[str(nb_temps+1)]["32"]
			symData[str(nb_temps+1)]["33"] = - moveData[str(nb_temps+1)]["33"]
			symData[str(nb_temps+1)]["34"] = moveData[str(nb_temps+1)]["34"]
			symData[str(nb_temps+1)]["35"] = - moveData[str(nb_temps+1)]["35"]
		if '36' in moveData[str(nb_temps+1)] : 	#tete
			symData[str(nb_temps+1)]["36"] = - moveData[str(nb_temps+1)]["36"]
			symData[str(nb_temps+1)]["37"] = moveData[str(nb_temps+1)]["37"]
	symData["speed"] = {}
	poppyParts = list()
	if 'bras_gauche' in moveData["speed"]:
		symData["speed"]["bras_droit"] = moveData["speed"]["bras_gauche"]
		poppyParts.append("bras_droit")
	if 'bras_droit' in moveData["speed"]:
		symData["speed"]["bras_gauche"] = moveData["speed"]["bras_droit"]
		poppyParts.append("bras_gauche")
	if 'jambe_gauche' in moveData["speed"]:
		symData["speed"]["jambe_droite"] = moveData["speed"]["jambe_gauche"]
		poppyParts.append("jambe_droite")
	if 'jambe_droite' in moveData["speed"]:
		symData["speed"]["jambe_gauche"] = moveData["speed"]["jambe_droite"]
		poppyParts.append("jambe_gauche")
	if 'colonne' in moveData["speed"]:
		symData["speed"]["colonne"] = moveData["speed"]["colonne"]
		poppyParts.append("colonne")
	if 'tete' in moveData["speed"]:
		symData["speed"]["tete"] = moveData["speed"]["tete"]
		poppyParts.append("tete")
	with open(symFile,'w') as f:
		json.dump(symData, f, indent=4)
	majMoveList(dir, symName, poppyParts)
	return dir
	
def reverse(moveName):
	dir = directory(moveName)
	if dir == '':
		return 'move file does not exist'
	moveFile = './move/'+dir+'/'+moveName+'.json'
	revName = moveName+'Rev'
	revFile = './move/'+dir+'/'+revName+'.json'
	if directory(revName) != '':
		return 'reverse '+revName+' already exists'
	with open(moveFile, 'r') as f:
		moveData = json.load(f)
	revData = {}
	revData["nb_temps"] = moveData["nb_temps"]
	nb_tps_max = moveData["nb_temps"]
	for nb_temps in range(moveData["nb_temps"]):
		if str(nb_temps+1) in moveData :
			revData[str(nb_tps_max-nb_temps)] = {}
		if '41' in moveData[str(nb_temps+1)] : 	#bras gauche en bras droit
			revData[str(nb_tps_max-nb_temps)]["41"] = moveData[str(nb_temps+1)]["41"]
			revData[str(nb_tps_max-nb_temps)]["42"] = moveData[str(nb_temps+1)]["42"]
			revData[str(nb_tps_max-nb_temps)]["43"] = moveData[str(nb_temps+1)]["43"]
			revData[str(nb_tps_max-nb_temps)]["44"] = moveData[str(nb_temps+1)]["44"]
		if '51' in moveData[str(nb_temps+1)] : 	#bras droit en bras gauche
			revData[str(nb_tps_max-nb_temps)]["51"] = moveData[str(nb_temps+1)]["51"]
			revData[str(nb_tps_max-nb_temps)]["52"] = moveData[str(nb_temps+1)]["52"]
			revData[str(nb_tps_max-nb_temps)]["53"] = moveData[str(nb_temps+1)]["53"]
			revData[str(nb_tps_max-nb_temps)]["54"] = moveData[str(nb_temps+1)]["54"]
		if '11' in moveData[str(nb_temps+1)] : 	#jambe gauche en jambe droite
			revData[str(nb_tps_max-nb_temps)]["11"] = moveData[str(nb_temps+1)]["11"]
			revData[str(nb_tps_max-nb_temps)]["12"] = moveData[str(nb_temps+1)]["12"]
			revData[str(nb_tps_max-nb_temps)]["13"] = moveData[str(nb_temps+1)]["13"]
			revData[str(nb_tps_max-nb_temps)]["14"] = moveData[str(nb_temps+1)]["14"]
			revData[str(nb_tps_max-nb_temps)]["15"] = moveData[str(nb_temps+1)]["15"]
		if '21' in moveData[str(nb_temps+1)] : 	#jambe droite en jambe gauche
			revData[str(nb_tps_max-nb_temps)]["21"] = moveData[str(nb_temps+1)]["21"]
			revData[str(nb_tps_max-nb_temps)]["22"] = moveData[str(nb_temps+1)]["22"]
			revData[str(nb_tps_max-nb_temps)]["23"] = moveData[str(nb_temps+1)]["23"]
			revData[str(nb_tps_max-nb_temps)]["24"] = moveData[str(nb_temps+1)]["24"]
			revData[str(nb_tps_max-nb_temps)]["25"] = moveData[str(nb_temps+1)]["25"]
		if '31' in moveData[str(nb_temps+1)] : 	#colonne
			revData[str(nb_tps_max-nb_temps)]["31"] = moveData[str(nb_temps+1)]["31"]
			revData[str(nb_tps_max-nb_temps)]["32"] = moveData[str(nb_temps+1)]["32"]
			revData[str(nb_tps_max-nb_temps)]["33"] = moveData[str(nb_temps+1)]["33"]
			revData[str(nb_tps_max-nb_temps)]["34"] = moveData[str(nb_temps+1)]["34"]
			revData[str(nb_tps_max-nb_temps)]["35"] = moveData[str(nb_temps+1)]["35"]
		if '36' in moveData[str(nb_temps+1)] : 	#tete
			revData[str(nb_tps_max-nb_temps)]["36"] = moveData[str(nb_temps+1)]["36"]
			revData[str(nb_tps_max-nb_temps)]["37"] = moveData[str(nb_temps+1)]["37"]
	revData["speed"] = {}
	poppyParts = list()
	if 'bras_droit' in moveData["speed"]:
		revData["speed"]["bras_droit"] = moveData["speed"]["bras_droit"]
		poppyParts.append("bras_droit")
	if 'bras_gauche' in moveData["speed"]:
		revData["speed"]["bras_gauche"] = moveData["speed"]["bras_gauche"]
		poppyParts.append("bras_gauche")
	if 'jambe_droite' in moveData["speed"]:
		revData["speed"]["jambe_droite"] = moveData["speed"]["jambe_droite"]
		poppyParts.append("jambe_droite")
	if 'jambe_gauche' in moveData["speed"]:
		revData["speed"]["jambe_gauche"] = moveData["speed"]["jambe_gauche"]
		poppyParts.append("jambe_gauche")
	if 'colonne' in moveData["speed"]:
		revData["speed"]["colonne"] = moveData["speed"]["colonne"]
		poppyParts.append("colonne")
	if 'tete' in moveData["speed"]:
		revData["speed"]["tete"] = moveData["speed"]["tete"]
		poppyParts.append("tete")
	with open(revFile,'w') as f:
		json.dump(revData, f, indent=4)
	majMoveList(dir, revName, poppyParts)
	return dir

def RemoveMove(moveName):
	print ('going to remove file')
	remove = False
	#mise a jour de la liste des fichiers mouvements
	dir = directory(moveName)	#recupere le type de mouvement
	if dir != '':
		with open('./move/movelist.json',  'r') as f:
			movelist = json.load(f)
		nbInDir = 'nb_'+dir
		movelist[nbInDir] -= 1
		os.remove('./move/'+dir+'/'+moveName+'.json')
		realDir = 'list_'+dir
		del movelist[realDir][moveName]
		remove = True
		if remove == True:
			with open('./move/movelist.json','w') as f:
				json.dump(movelist, f, indent=4)
	time.sleep(1)
	return remove

#fonction mise en premiere position du mouvement
def goFirstPos(position, speed, init = False):
		Poppyboid.scanPosition.start()
		time.sleep(0.1)
		if init == True:
			vitesse = 40
		else:
			vitesse = 80
		temps_attente = 0
		if init == 'True':
			seuil = 0
		else:
			seuil = SEUIL_ANGLE_MAX
		positionActu={} #Position de depart
		positionFin={} #Position a atteindre
		#charge un fichier Json - position courante
		with open('./position/currentPos.json', 'r') as f:
		    positionActu = json.load(f)
		
		positionFin = position
		print speed.keys()	
		print positionFin
		if "bras_droit" in speed.keys() and "51" in positionFin:
			if abs(positionFin["51"]-positionActu["51"])>seuil :
				v =  abs(positionFin["51"]-positionActu["51"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'r_shoulder_y':positionFin["51"]},v, wait=False)
			if abs(positionFin["52"]-positionActu["52"])>seuil :
				v = abs(positionFin["52"]-positionActu["52"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'r_shoulder_x':positionFin["52"]}, v, wait=False)
			if abs(positionFin["53"]-positionActu["53"])>seuil :
				v =abs(positionFin["53"]-positionActu["53"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'r_arm_z':positionFin["53"]}, v, wait=False)
			if abs(positionFin["54"]-positionActu["54"])>seuil :
				v = abs(positionFin["54"]-positionActu["54"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'r_elbow_y': positionFin["54"]}, v, wait=False)
		if "bras_gauche" in speed.keys() and "41" in positionFin:
			if abs(positionFin["41"]-positionActu["41"])>seuil :
				v = abs(positionFin["41"]-positionActu["41"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'l_shoulder_y':positionFin["41"]}, v, wait=False)
			if abs(positionFin["42"]-positionActu["42"])>seuil:
				v = abs(positionFin["42"]-positionActu["42"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'l_shoulder_x':positionFin["42"]}, v, wait=False)
			if abs(positionFin["43"]-positionActu["43"])>seuil :
				v = abs(positionFin["43"]-positionActu["43"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'l_arm_z':positionFin["43"]}, v, wait=False)
			if abs(positionFin["44"]-positionActu["44"])>seuil :
				v = abs(positionFin["44"]-positionActu["44"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'l_elbow_y': positionFin["44"]}, v, wait=False)
		if "colonne" in speed.keys() and "31" in positionFin:
			if abs(positionFin["31"]-positionActu["31"])>seuil :
				v = abs(positionFin["31"]-positionActu["31"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'abs_y':positionFin["31"]}, v, wait=False)
			if abs(positionFin["32"]-positionActu["32"])>seuil :
				v = abs(positionFin["32"]-positionActu["32"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'abs_x':positionFin["32"]}, v, wait=False)
			if abs(positionFin["33"]-positionActu["33"])>seuil :
				v = abs(positionFin["33"]-positionActu["33"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'abs_z':positionFin["33"]},v, wait=False)
			if abs(positionFin["34"]-positionActu["34"])>seuil :
				v = abs(positionFin["34"]-positionActu["34"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'bust_y':positionFin["34"]}, v, wait=False)
			if abs(positionFin["35"]-positionActu["35"])>seuil :
				v =  abs(positionFin["35"]-positionActu["35"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'bust_x':positionFin["35"]},v, wait=False)
		if "tete" in speed.keys() and "36" in positionFin:
			if abs(positionFin["36"]-positionActu["36"])>seuil :
				v = abs(positionFin["36"]-positionActu["36"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'head_z':positionFin["36"]},v , wait=False)
			if abs(positionFin["37"]-positionActu["37"])>seuil :
				v = abs(positionFin["37"]-positionActu["37"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'head_y':positionFin["37"]}, v, wait=False)
		time.sleep(temps_attente/4.0)
		if "jambe_gauche" in speed.keys() and "11" in positionFin:
			if abs(positionFin["11"]-positionActu["11"])>seuil :
				v = abs(positionFin["11"]-positionActu["11"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'l_hip_x':positionFin["11"]}, v, wait=False)
				print 'ok 11'
			if abs(positionFin["12"]-positionActu["12"])>seuil :
				v = abs(positionFin["12"]-positionActu["12"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'l_hip_z':positionFin["12"]}, v, wait=False)
			if abs(positionFin["13"]-positionActu["13"])>seuil :
				v = abs(positionFin["13"]-positionActu["13"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'l_hip_y':positionFin["13"]}, v, wait=False)
			if abs(positionFin["14"]-positionActu["14"])>seuil :
				v = abs(positionFin["14"]-positionActu["14"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'l_knee_y': positionFin["14"]}, v, wait=False)
			if abs(positionFin["15"]-positionActu["15"])>seuil :
				v = abs(positionFin["15"]-positionActu["15"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'l_ankle_y':positionFin["15"]}, v, wait=False)
		if "jambe_droite" in speed.keys() and "21" in positionFin:
			if abs(positionFin["21"]-positionActu["21"])>seuil :
				v = abs(positionFin["21"]-positionActu["21"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'r_hip_x':positionFin["21"]}, v, wait=False)
			if abs(positionFin["22"]-positionActu["22"])>seuil :
				v =  abs(positionFin["22"]-positionActu["22"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'r_hip_z':positionFin["22"]},v, wait=False)
			if abs(positionFin["23"]-positionActu["23"])>seuil :
				v = abs(positionFin["23"]-positionActu["23"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'r_hip_y': positionFin["23"]}, v, wait=False)
			if abs(positionFin["24"]-positionActu["24"])>seuil :
				v = abs(positionFin["24"]-positionActu["24"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'r_knee_y':positionFin["24"]}, v, wait=False)
			if abs(positionFin["25"]-positionActu["25"])>seuil :
				v = abs(positionFin["25"]-positionActu["25"])/vitesse
				if v > temps_attente:
					temps_attente = v
				Poppyboid.goto_position({'r_ankle_y':positionFin["25"]}, v, wait=False)
		print temps_attente
		time.sleep(temps_attente)

def GoMove(moveName, speed=5, rev=False, save=False, poppyParts=''):
	global SecurityStop
	if SecurityStop == True:
		return "Security mode"
	global EXO_TEMPS
	global EXO_SLEEP
	global EXO_ENABLE
	global MOVING_ENABLE
	global PLAYING_EXO
	global PLAYING_MOVE
	EXO_SLEEP = False
	MOVING_ENABLE = True
	if len(poppyParts) == 0:
		poppyParts = list()
		poppyParts.append("tete")
		poppyParts.append("bras_droit")
		poppyParts.append("bras_gauche")
		poppyParts.append("jambe_gauche")
		poppyParts.append("jambe_droite")
		poppyParts.append("colonne")
	moveType = directory(moveName)
	if int(speed)>10:
		speed=10
	elif int(speed) <1:
		speed = 1
	if moveType == '':
		return 'move file does not exist'
	elif moveType == 'exo' or moveType == 'seance':
		return 'not a move file !'
	print ('going to move')
	with open('./move/'+moveType+'/'+moveName+'.json', 'r') as f:
		moveFile = json.load(f)
# decompose en fonction du nombre de parties temporelles du mouvement
	if not "parties" in moveFile:	#initialisation pour les fichiers ancienne generation
		moveFile["parties"]={}
		moveFile["parties"]["nb_parts"]=1
		moveFile["parties"]["offsetPart1"]={}
		moveFile["parties"]["offsetPart1"]["min"]=0
	for part in range(1, moveFile["parties"]["nb_parts"]+1):
		print "part : "+str(part)
		startTime = moveFile["parties"]["offsetPart"+str(part)]["min"]
		if part == moveFile["parties"]["nb_parts"]:	# recuperation temps fin de chaque partie
			endTime = moveFile["nb_temps"]
		else:
			endTime = moveFile["parties"]["offsetPart"+str(part+1)]["min"]
		tempsboucle = 50
		if part == 1:	# initialise la liste des poppyParts pour la lecture du mouvement
			speedList = list()
			speedDict = {}
			nb_speed = ""
		else:
			nb_speed = part
		#print "poppyParts"
		#print poppyParts
		for key, value in moveFile["speed"+str(nb_speed)].iteritems():
			#print "key : "+key
			if key in poppyParts:
				speedList.append(key)
				#print "speed : "+str(speed)
				#print moveFile["speed"][key]
				value = value*(2.2/(float(speed)*0.2+1.0))
				moveFile["speed"+str(nb_speed)][key] = value
				print moveFile["speed"+str(nb_speed)][key]
				if value < tempsboucle:
					tempsboucle = value
				if tempsboucle>=0.5:
					tempsboucle = 0.5
				speedDict[key] = value
		tempsboucle = tempsboucle*1.2
		print "temps boucle : "+ str(tempsboucle)
		if save == True:
			NonCompliant(speedList, 25)
		else:
			NonCompliant(speedList)
		if PLAYING_EXO==False:		#juste un mouvement en lecture
			while PLAYING_MOVE:
				time.sleep(0.1)
			goMovePrimitive(Poppyboid, rev, moveType, moveName, speedDict, tempsboucle, startTime, endTime).start()
			time.sleep(0.05)
		else:
			goMoveFunction(rev, moveType, moveName, speedDict, tempsboucle, startTime, endTime)
			time.sleep(0.05)
	return 'Move has started'

def goMoveFunction(rev, moveType, moveName, speedDict, tempsboucle, startTime, endTime):
	global EXO_TEMPS
	global EXO_SLEEP
	global EXO_ENABLE
	global MOVING_ENABLE
	global PLAYING_MOVE

	print "verif si playing move"
	while PLAYING_MOVE:
		time.sleep(0.1)
	PLAYING_MOVE=True
	print "startTime : "+str(startTime)+", endTime : "+str(endTime)
	with open('./move/'+moveType+'/'+moveName+'.json', 'r') as f:
		moveFile = json.load(f)
	if rev == False:
		for temps in range(startTime, endTime):
			while EXO_SLEEP == True and MOVING_ENABLE == True:
				time.sleep(0.1)
			if MOVING_ENABLE == False:
				PLAYING_MOVE = False
				print "---stop move 1---"
				return "stop"
			if temps+1 == 1:
				goFirstPos(moveFile[str(temps+1)], moveFile["speed"])
			else:
				if str(temps+1) in moveFile:
					miseEnPosPrimitive(Poppyboid,moveFile[str(temps+1)], speedDict).start()
				if MOVING_ENABLE == False:
					PLAYING_MOVE = False
					print "---stop move 2---"
					return "stop"
				time.sleep(tempsboucle)
				if MOVING_ENABLE == False:
					PLAYING_MOVE = False
					print "---stop move 3---"
					return "stop"
			EXO_TEMPS += 1
	else:
		return "stop" 	#TODO : lecture non geree a l'envers !!!
		for temps in range(moveFile["nb_temps"]):
			while EXO_SLEEP == True and MOVING_ENABLE == True:
				time.sleep(0.5)
			if MOVING_ENABLE == False:
				PLAYING_MOVE = False
				return "stop"
			if temps+1 == 1:
				goFirstPos(moveFile[str(moveFile["nb_temps"]-temps)], moveFile["speed"])
			else:
				if str(moveFile["nb_temps"]-temps) in moveFile:
					miseEnPosPrimitive(Poppyboid,moveFile[str(moveFile["nb_temps"]-temps)], speedDict).start()
				if MOVING_ENABLE == False:
					PLAYING_MOVE = False
					return "stop"
				time.sleep(tempsboucle)
				if MOVING_ENABLE == False:
					PLAYING_MOVE = False
					print "---stop move 3---"
					return "stop"
			EXO_TEMPS += 1
	PLAYING_MOVE = False
	if endTime == moveFile["nb_temps"]:
		MOVING_ENABLE = False

def GoExo(exoName):
	global SecurityStop
	if SecurityStop == True:
		return "Security mode"
	#time.sleep(0.5)	#le temps que la seance precedente se finnisse si existante
	global PLAYING_EXO
	PLAYING_EXO = False
	global EXO_ENABLE 
	EXO_ENABLE = True
	global EXO_SLEEP
	EXO_SLEEP = False
	global EXO_TEMPS
	EXO_TEMPS = 0
	global NUM_EXO
	NUM_EXO = 0
	global NUM_MOV
	NUM_MOV = 0
	global EXO_TEMPS_LIMITE
	exoType = directory(exoName)
	if exoType == '':
		return exoName + ' does not exist'
	elif exoType == 'mov':
		return 'not an exercice or a seance !'
	print ('preparing the file')
	with open('./move/'+exoType+'/'+exoName+'.json', 'r') as f:
		moveFile = json.load(f)
	#tous les fichiers existent ?
	for i in range(moveFile['nb_fichiers']):
		if directory(moveFile['fichier'+str(i+1)]['namefile']) == '':
			return moveFile['fichier'+str(i+1)]['namefile'] + " is missing !"
		elif directory(moveFile['fichier'+str(i+1)]['namefile']) == 'exo':
			with open('./move/exo/'+moveFile['fichier'+str(i+1)]['namefile']+'.json', 'r') as f:
				exoFile = json.load(f)
			for j in range(exoFile['nb_fichiers']):
				if directory(exoFile['fichier'+str(j+1)]['namefile']) == '':
					return exoFile['fichier'+str(j+1)]['namefile'] + " in "+moveFile['fichier'+str(i+1)]['namefile'] +" is missing !"
	EXO_TEMPS_LIMITE = moveFile['nb_temps']
	goExoPrimitive(Poppyboid,exoName, exoType).start()
	time.sleep(1)
	return 'Exercice has started'

def StopExo():
	global EXO_ENABLE
	global MOVING_ENABLE
	global PAUSE
	while PAUSE == True:		#si on est en pause inter-exo ou inter-mouvements
		time.sleep(0.2)
	if EXO_ENABLE == True:
		EXO_ENABLE = False
		MOVING_ENABLE = False
		return 'exercice stopped'
	elif MOVING_ENABLE == True:
		EXO_ENABLE = False
		MOVING_ENABLE = False
		return 'movement stopped'
	else:
		EXO_ENABLE = False
		MOVING_ENABLE = False
		return 'no exercice or movement is running'

def PauseExo():
	global EXO_SLEEP
	if EXO_SLEEP == False:
		EXO_SLEEP = True
		return 'move paused'
	else:
		return 'no exercice is running'

def ResumeExo():
	global EXO_SLEEP
	global EXO_ENABLE
	global MOVING_ENABLE
	if EXO_SLEEP == True and EXO_ENABLE == True:
		EXO_SLEEP = False
		return 'exercice resumed'
	elif EXO_SLEEP == True and MOVING_ENABLE == True:
		EXO_SLEEP = False
		return 'move resumed'
	else:
		return 'no exercice or movement in pause'

def verifFinExo():
	global EXO_ENABLE
	global EXO_TEMPS
	global EXO_TEMPS_LIMITE
	global NUM_EXO
	global NUM_MOV
	verif = {}
	if EXO_ENABLE == False :
		verif["info"]= "end"
	else:
		verif["info"]= "moving " + str(EXO_TEMPS)+"/"+str(EXO_TEMPS_LIMITE)
	verif["num_exo"]=str(NUM_EXO)
	verif["num_mov"]=str(NUM_MOV)
	return verif

def verifFinMov():
	global MOVING_ENABLE
	if MOVING_ENABLE == False :
		return "end"
	else:
		return "moving"

def mesure():
	Poppyboid.scan.start()

def readConfig(moveConfig, movename=''):
	print type(moveConfig)
	if type(moveConfig)!=type({}):
		moveConfig=json.loads(moveConfig)
		print type(moveConfig)
	print moveConfig
	#for key, value in moveConfig.iteritems():
	#	print key, value
	moveDir = moveConfig["type"]
	moveName='./move/'+moveDir+'/'+movename+'.json'
	if moveDir != "exo" and moveDir != "seance":	# si on cree un mouvement (donc pas un exo ni seance)
		moveFile = OrderedDict()					# fichier final du mouvement
		moveFile["speed"] = {}
		moveFile["parties"] = {}				# parametres definition des parties temporelles du mouvement
		moveFile["parties"]["nb_parts"] = 1			# nombre de parties
		moveFile["parties"]["offsetPart1"]= {}			# premiere partie demarre au temps 1
		moveFile["parties"]["offsetPart1"]["min"]= 0		# premiere partie demarre au temps 1
		timeline={}						# dico pour regrouper la timeline de chaque poppypart
		timeline["tete"]={}
		timeline["colonne"]={}
		timeline["bras_gauche"]={}
		timeline["bras_droit"]={}
		timeline["jambe_gauche"]={}
		timeline["jambe_droite"]={}
	poppyParts = list()						# liste avec les parties concernees de poppy
	nb_temps_max = 0
	
	for i in range(moveConfig["nb_fichiers"]):		#verifie les parametres du fichier config
		if moveDir != "exo" and moveDir != "seance":	# si on cree un mouvement (donc pas un exo ni seance)
			offset = moveConfig["fichier"+str(i+1)]["offset"]
			period = 10 - moveConfig["fichier"+str(i+1)]["speed"]	#periode = inverse de vitesse
			t0min = -1						#offset minimum sur une partie
		shortnamefile = moveConfig["fichier"+str(i+1)]["namefile"]
		dir = directory(shortnamefile)
		if dir == '':						# chaque partie existe ?
			return shortnamefile+ ' does not exist'
		namefile = './move/'+dir+'/'+shortnamefile+'.json'
		with open(namefile,  'r') as f:
			movepart = json.load(f)			# movepart : fichier qui compose le move ou l'exo
		if moveDir != "seance":				# init des temps du fichier pour la timeline
			if moveDir == "mov":
				t0 = offset
				tf = t0 + period*movepart["nb_temps"]
			for key, value in movepart["speed"].iteritems():	# verifie si plusieurs fichiers avec meme poppypart
				print " "
				newPart = 0
				actualpart = key
				if key in poppyParts :
					print "condition ok : memes parties dans poppyparts"
					if moveDir != "exo" and moveDir != "seance":	# si on cree un mouvement (donc pas un exo ni seance)
						print "actualpart : "+actualpart
						print "juste avant la boucle !!!!!"
						#print timeline 
						for key, value2 in timeline[actualpart].iteritems():	#parcourt tous les fichiers avec la partie actualpart
							print "condition pour la cle : "+key
							print "t0 : "+str(t0)+" - tOref : "+str(timeline[actualpart][key]["t0"])+" - tf : "+str(tf)+" - tfref : "+str(timeline[actualpart][key]["tf"])
							if not ((t0<timeline[actualpart][key]["t0"] and tf<timeline[actualpart][key]["t0"]) or (t0>timeline[actualpart][key]["tf"] and tf>timeline[actualpart][key]["tf"])):
								print "error ! multiple files with the same part"
								return "error ! t0 : "+str(t0)+" - tf : "+str(tf)+" - tOref : "+str(timeline[actualpart][key]["t0"])+" - tfref : "+str(timeline[actualpart][key]["tf"])

							else:
								newPart=1
								if t0<timeline[actualpart][key]["t0"] and (timeline[actualpart][key]["t0"]<t0min or t0min==-1):
									t0min = timeline[actualpart][key]["t0"] #MAJ offset min

				else:
					poppyParts.append(key)			# met a jour la liste
#TODO

				if moveDir == "mov" and newPart:
					moveFile["parties"]["nb_parts"]+=1	#incremente nb parties tempo
					moveFile["parties"]["offsetPart"+str(moveFile["parties"]["nb_parts"])]={}
				if moveDir == "mov":				# gestion si mouvement
					timeline[actualpart]["fichier"+str(i+1)]={}		#MAJ du dico de la timeline
					timeline[actualpart]["fichier"+str(i+1)]["t0"]=t0
					timeline[actualpart]["fichier"+str(i+1)]["tf"]=tf
					print "t0min : "+str(t0min)
					print "nb_parts : "+ str(moveFile["parties"]["nb_parts"])

					if (t0min == -1 and newPart):				# si y a une autre partie sur autre PoppyPart qui commence apres le nouveau
						for offsetPart, offsetValue in moveFile["parties"].iteritems():
							if offsetPart != "nb_parts" and "min" in moveFile["parties"][offsetPart]:
								if moveFile["parties"][offsetPart]["min"]>t0:
									t0min = moveFile["parties"][offsetPart]["min"]		# MAJ t0min selon toutes les offsetParts
									print "correction t0min : "+str(t0min)
									break

					if (t0min == -1 and newPart) or not newPart: 		# si le movepart actuel a le plus grand offset OU si premier ajoute OU si nouveau poppyPart
						k=0		#compteur pour dictionnaire speed
						print "creating offsetPart"+str(moveFile["parties"]["nb_parts"])
						print moveFile["parties"]
						removeLast = False
						kcompteur=0
						for offsetPart, offsetValue in moveFile["parties"].iteritems():			# pour tous les offsetparts
							kcompteur +=1							#incremente compteur
							if offsetPart != "nb_parts" and "min" in moveFile["parties"][offsetPart]:
								if moveFile["parties"][offsetPart]["min"]==t0 and t0!=0 and newPart:
									moveFile["parties"]["nb_parts"]-=1	#en fait pas +1 au nb de parties
									removeLast = True
									print "supprime le fake nouveau offsetpart"
								elif newPart==0 and t0==moveFile["parties"][offsetPart]["min"]:	#si meme offset que partie existante
									t0min = 0
									print "ajoute "+str(t0)+" a : "+offsetPart
									moveFile["parties"][offsetPart][actualpart]=t0				#rajoute la nouvelle poppyPart
									k = kcompteur												#enregistre le compteur
									break
								elif newPart==0 and t0<moveFile["parties"][offsetPart]["min"]:	#si y a un offset existant plus grand
									t0min = moveFile["parties"][offsetPart]["min"]
									break
								previousOffsetPart = offsetPart
						if removeLast:
							del moveFile["parties"]["offsetPart"+str(moveFile["parties"]["nb_parts"]+1)]	#suppr le offsetPart cree
						if t0min == -1:							# TODO : si on ajoute le nouveau a la fin. Faire les differents cas
							realOffsetPart = "offsetPart"+str(moveFile["parties"]["nb_parts"])
						elif t0min != 0:
							realOffsetPart = previousOffsetPart
						if t0min !=0:
							print "ajoute "+str(t0)+" a "+realOffsetPart
							moveFile["parties"][realOffsetPart][actualpart]=t0	# ajoute la nouvelle partie a offsetpart

							if "min" in moveFile["parties"][realOffsetPart]:		#MAJ du min des offset de la partie
								if t0<moveFile["parties"][realOffsetPart]["min"]:
									moveFile["parties"][realOffsetPart]["min"]=t0
							else:
								moveFile["parties"][realOffsetPart]["min"]=t0
						# MAJ de speed
						if moveFile["parties"]["nb_parts"]==1:
							k=""
						elif k==0:
							k=moveFile["parties"]["nb_parts"]
						if "speed"+str(k) not in moveFile:
							print "creating speed"+str(k)
							moveFile["speed"+str(k)]={}
						if period == 0:
							moveFile["speed"+str(k)][actualpart] = value/2
							period = 1
						else:
							moveFile["speed"+str(k)][actualpart] = period*value
						print "speed"+str(k)+" completed"
						print moveFile["speed"+str(k)]

					else:
						for partNumber in range(1,moveFile["parties"]["nb_parts"]):	# parcourt toutes les parties offsetPart
							print "boucle dans parties nb_parts, iteration "+str(partNumber)
							print moveFile["parties"]
							print "offsetPart"+str(partNumber)+" : "+str(moveFile["parties"]["offsetPart"+str(partNumber)]["min"])
							if actualpart in moveFile["parties"]["offsetPart"+str(partNumber)]:
								if moveFile["parties"]["offsetPart"+str(partNumber)][actualpart]==t0min:	#arrive a offsetPart directement superieur
									print "condition egal a t0min : OK ("+str(t0min)+" = "+str(moveFile["parties"]["offsetPart"+str(partNumber)][actualpart])
									for j in range(moveFile["parties"]["nb_parts"],partNumber, -1):	#decale tout en +1
										print "boucle degressive: iteration "+str(j)+" ["+str(moveFile["parties"]["nb_parts"])+"; "+str(partNumber)+"]"
										print moveFile["parties"]
										del moveFile["parties"]["offsetPart"+str(j)]
										moveFile["parties"]["offsetPart"+str(j)]={}
										for partKey, partValue in moveFile["parties"]["offsetPart"+str(j-1)].iteritems():	#recopie offsetPart
											if j==2 and partKey==actualpart:
												moveFile["parties"]["offsetPart2"][partKey]=partValue
												moveFile["parties"]["offsetPart2"]["min"]=partValue
											elif j!=2:
												moveFile["parties"]["offsetPart"+str(j)][partKey]=partValue
											
									# partie speed
										if j!=moveFile["parties"]["nb_parts"]:
											del moveFile["speed"+str(j)]
										if (j-1)!=1:
											moveFile["speed"+str(j)]={}
											for speedKey, speedValue in moveFile["speed"+str(j-1)].iteritems():		#recopie speed
												moveFile["speed"+str(j)][speedKey]=speedValue
										else:
											moveFile["speed2"]={}
											moveFile["speed2"][actualpart]=moveFile["speed"][actualpart]
									print "ajout nouvelle valeur offsetPart"+str(partNumber)+" = "+str(t0)
									if partNumber!=1:
										del moveFile["parties"]["offsetPart"+str(partNumber)]
										moveFile["parties"]["offsetPart"+str(partNumber)]={}
									moveFile["parties"]["offsetPart"+str(partNumber)][actualpart]=t0
									moveFile["parties"]["offsetPart"+str(partNumber)]["min"]=t0
									print moveFile["parties"]

									if partNumber==1:
										partNumber=""
									else:
										del moveFile["speed"+str(partNumber)]
										moveFile["speed"+str(partNumber)]={}
									if period == 0:
										moveFile["speed"+str(partNumber)][actualpart] = value/2
										period = 1
									else:
										moveFile["speed"+str(partNumber)][actualpart] = period*value
									break

		else:	#si c'est une seance...
			with open("./move/movelist.json", 'r') as f:
				movelist = json.load(f)
			if dir=='mov':
				exoname = shortnamefile+"exo"		#creation d'un exo pour contenir le mouvement seul
				moveConfig2 = {}			#creation du fichier de config du nouvel exo
				moveConfig2["type"]="exo"
				moveConfig2["nb_fichiers"]=1
				moveConfig2["fichier1"]=moveConfig["fichier"+str(i+1)]
				succeed = readConfig(moveConfig2, exoname)
				if succeed == "exercice created":
					with open("./move/movelist.json", 'r') as f:
						movelist = json.load(f)
					for j in range(len(movelist['list_exo'][exoname])):
						if movelist['list_exo'][exoname][j] not in poppyParts:
							poppyParts.append(movelist['list_exo'][exoname][j])	#met a jour la liste des poppyparts
					moveConfig["fichier"+str(i+1)]["namefile"]=exoname
				else:
					return "error ! the exercice "+exoname+" can't be created to compose the seance"

			elif dir=='exo':
				for j in range(len(movelist['list_exo'][shortnamefile])):
					if movelist['list_exo'][shortnamefile][j] not in poppyParts:
						poppyParts.append(movelist['list_exo'][shortnamefile][j])	#met a jour la liste des poppyparts
			
	#CREATION DU MOUVEMENT
		if moveDir != "exo" and moveDir != "seance":	# si on cree un mouvement (donc pas un exo ni seance)
			first = True				# si premier mouvement pour initialisation
			actualpart = ""
			for key2, value in movepart["speed"].iteritems():	# verifie si premier a s'executer
				actualpart = key2
				for key3, value in timeline[actualpart].iteritems():	#parcourt tous les fichiers
					if int(t0)>int(timeline[actualpart][key3]["t0"]):
						first = False
						break
			periodtmp = period
			for nb_temps in range(movepart["nb_temps"]):
				for key, value in movepart[str(nb_temps+1)].iteritems():
					if nb_temps+1 == 1:
						if first:
							realOffset = 0
							period = 1
						else:
							realOffset = offset
					elif nb_temps+1 == 2:
						realOffset = offset
						period = periodtmp
					if str(period*(nb_temps+1)+realOffset) not in moveFile:
						moveFile[str(period*(nb_temps+1)+realOffset)] = {}
					moveFile[str(period*(nb_temps+1)+realOffset)][key] = value
			if nb_temps_max < period*movepart["nb_temps"]+realOffset:
				nb_temps_max = period*movepart["nb_temps"]+realOffset
			moveFile["nb_temps"] = nb_temps_max
		else:			# si on est dans le cas d'un exo ou d'une seance
			nb_temps_max += movepart["nb_temps"]
			nb_temps_max += moveConfig["fichier"+str(i+1)]["pause"]
			
	if moveDir == "exo" or moveDir == "seance":	# si on cree un exo ou une seance
		moveConfig["nb_temps"] = nb_temps_max
		with open(moveName, 'w') as f:
			json.dump(moveConfig, f, indent=4)	
	else:									# si pas exo ou seance
		moveFile["parties"]["offsetPart1"]["min"]=0			# premier offset = 0
		with open(moveName, 'w') as f:
			json.dump(moveFile, f, indent=4)
	
	majMoveList(moveDir, movename, poppyParts)
	if moveDir == 'exo':
		return "exercice created"
	elif moveDir == 'seance':
		return "seance created"
	else:
		return "move created"

def addMove(moveName, moveType, moveFile):
	moveFile = json.loads(moveFile)
	print type(moveFile)
	moveDir = directory(moveName)
	if moveDir != '':
		return "already exists"
	poppyParts = list()
	print moveFile
	if "tete" in moveFile["poppyParts"]:
		poppyParts.append("tete")
	if "bras_gauche" in moveFile["poppyParts"]:
		poppyParts.append("bras_gauche")
	if "bras_droit" in moveFile["poppyParts"]:
		poppyParts.append("bras_droit")
	if "colonne" in moveFile["poppyParts"]:
		poppyParts.append("colonne")
	if "jambe_gauche" in moveFile["poppyParts"]:
		poppyParts.append("jambe_gauche")
	if "jambe_droite" in moveFile["poppyParts"]:
		poppyParts.append("jambe_droite")
	del moveFile["poppyParts"]
	with open("./move/"+moveType+"/"+moveName+".json", 'w') as f:
		json.dump(moveFile, f, indent=4)
	majMoveList(moveType, moveName, poppyParts)
	
def directory(moveName):
	with open('./move/movelist.json', 'r') as f:
		movelist = json.load(f)
	if moveName in movelist["list_mov"]:
		return 'mov'
	elif moveName in movelist["list_exo"]:
		return 'exo'
	elif moveName in movelist["list_seance"]:
		return 'seance'
	else:
		return ''

def readExoCompo(exoName):
	exoDir = directory(exoName)
	exoCompo = {}
	exoCompo['nom'] = exoName
	with open('./move/'+exoDir+'/'+exoName+'.json', 'r') as f:
		exoConfig=json.load(f)
	exoCompo['nb_fichiers'] = exoConfig['nb_fichiers']
	for i in range(exoConfig["nb_fichiers"]):		#on deroule tous les fichiers de la liste
		if directory(exoConfig['fichier'+str(i+1)]['namefile']) == 'exo' : # si c'est un exo
			exoCompo[str(i+1)] = {}
			exoCompo[str(i+1)] = readExoCompo(exoConfig['fichier'+str(i+1)]['namefile'])
		else:								#si c'est un mouvement
			exoCompo[str(i+1)] = exoConfig['fichier'+str(i+1)]['namefile']
	return exoCompo
		
def loadData(moveName, BDD):
	dir = directory(moveName)
	jsondata={}
	if moveName == 'movelist':
		moveName = './move/'+moveName+'.json'
	elif dir == '':
		return 'does not exist'
	elif (dir == 'exo' or dir == 'seance') and BDD == "false":
		jsondata = readExoCompo(moveName)
		return jsondata
	else:
		moveName='./move/'+dir+'/'+moveName+'.json'
	
	with open(moveName, 'r') as f:
		jsondata=json.load(f)
	if moveName == './move/movelist.json':
		jsondata[u'compliant'] = poppyCompliant()
		jsondata[u'compliant'] = "u'"+str(jsondata[u'compliant'] )+"'"
		jsondata[u'compliantBG'] = "u'"+str(Poppyboid.l_arm_z.compliant)+"'"
		jsondata[u'compliantBD'] = "u'"+str(Poppyboid.r_arm_z.compliant)+"'"
		jsondata[u'compliantT'] = "u'"+str(Poppyboid.head_z.compliant)+"'"
		jsondata[u'compliantJG'] = "u'"+str(Poppyboid.l_hip_z.compliant)+"'"
		jsondata[u'compliantJD'] = "u'"+str(Poppyboid.r_hip_z.compliant)+"'"
		jsondata[u'compliantCol'] = "u'"+str(Poppyboid.abs_z.compliant)+"'"
	return jsondata

def poppyCompliant():
#	if len(Poppyboid.compliant) == 25:
#		return True
	if Poppyboid.l_arm_z.compliant == False:
		return False
	if Poppyboid.r_arm_z.compliant == False:
		return False
	if Poppyboid.head_z.compliant == False:
		return False
	if Poppyboid.l_hip_z.compliant == False:
		return False
	if Poppyboid.r_hip_z.compliant == False:
		return False
	if Poppyboid.abs_z.compliant == False:
		return False
	return True

def giveIP():
	IPaddress = ([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
	print IPaddress
	return IPaddress

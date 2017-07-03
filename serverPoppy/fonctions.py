from poppy_humanoid import PoppyHumanoid
from contextlib import closing
import sys
import time
import os
import shutil
import pypot.primitive
from pypot.dynamixel.io.abstract_io import AbstractDxlIO
from pypot.dynamixel.__init__ import get_available_ports
import json
import numpy
import socket
import csv
from collections import OrderedDict
import logging
from logging.handlers import RotatingFileHandler
import tarfile
from threading import Thread
import requests
from random import randint
import pygame

#PRIMITIVES
#primitive enregistrement partie de sous-mouvement
class movePartPrimitive(pypot.primitive.Primitive):
	def __init__(self, poppy, poppyParts, moveName):
		self.PoppyGRR=poppy
		self.poppyParts=poppyParts
		self.moveName=moveName
		pypot.primitive.Primitive.__init__(self, self.PoppyGRR.Poppyboid)	

	def run(self):
		self.PoppyGRR.SEUIL_ANGLE
    		print 'scanning Poppy...'
		position= OrderedDict() #creation d'un dictionnaire avec maintien de l'ordre
		position["speed"]={}
		if self.PoppyGRR.creature == "humanoid":
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
			if "jambe_gauche" in self.poppyParts and self.PoppyGRR.creature == "humanoid":
				position[position_counter]["11"]= self.PoppyGRR.Poppyboid.l_hip_x.present_position
				position[position_counter]["12"]= self.PoppyGRR.Poppyboid.l_hip_z.present_position
				position[position_counter]["13"]= self.PoppyGRR.Poppyboid.l_hip_y.present_position
				position[position_counter]["14"]= self.PoppyGRR.Poppyboid.l_knee_y.present_position
				position[position_counter]["15"]= self.PoppyGRR.Poppyboid.l_ankle_y.present_position
				if position_counter!=1 and is_moving == False:
					if abs(position[position_counter]["11"]-position[position_counter-1]["11"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["12"]-position[position_counter-1]["12"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["13"]-position[position_counter-1]["13"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["14"]-position[position_counter-1]["14"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["15"]-position[position_counter-1]["15"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
			#partie jambe droite
			if "jambe_droite" in self.poppyParts and self.PoppyGRR.creature == "humanoid":
				position[position_counter]["21"]= self.PoppyGRR.Poppyboid.r_hip_x.present_position
				position[position_counter]["22"]= self.PoppyGRR.Poppyboid.r_hip_z.present_position
				position[position_counter]["23"]= self.PoppyGRR.Poppyboid.r_hip_y.present_position
				#print "position m23 "+str(position_counter)+" : "+str(position[position_counter]["23"])
				position[position_counter]["24"]= self.PoppyGRR.Poppyboid.r_knee_y.present_position
				position[position_counter]["25"]= self.PoppyGRR.Poppyboid.r_ankle_y.present_position
				if position_counter!=1 and is_moving == False:
					if abs(position[position_counter]["21"]-position[position_counter-1]["21"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["22"]-position[position_counter-1]["22"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["23"]-position[position_counter-1]["23"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["24"]-position[position_counter-1]["24"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["25"]-position[position_counter-1]["25"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
			#partie colonne
			if "colonne" in self.poppyParts:
				position[position_counter]["31"]= self.PoppyGRR.Poppyboid.abs_y.present_position
				position[position_counter]["32"]= self.PoppyGRR.Poppyboid.abs_x.present_position
				position[position_counter]["33"]= self.PoppyGRR.Poppyboid.abs_z.present_position
				position[position_counter]["34"]= self.PoppyGRR.Poppyboid.bust_y.present_position
				position[position_counter]["35"]= self.PoppyGRR.Poppyboid.bust_x.present_position
				if position_counter!=1 and is_moving == False:
					if abs(position[position_counter]["31"]-position[position_counter-1]["31"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["32"]-position[position_counter-1]["32"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["33"]-position[position_counter-1]["33"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["34"]-position[position_counter-1]["34"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["35"]-position[position_counter-1]["35"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
			#partie tete
			if "tete" in self.poppyParts:
				position[position_counter]["36"]= self.PoppyGRR.Poppyboid.head_z.present_position
				position[position_counter]["37"]= self.PoppyGRR.Poppyboid.head_y.present_position
				if position_counter!=1 and is_moving == False:
					if abs(position[position_counter]["36"]-position[position_counter-1]["36"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["37"]-position[position_counter-1]["37"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
			#partie bras gauche
			if "bras_gauche" in self.poppyParts:
				position[position_counter]["41"]= self.PoppyGRR.Poppyboid.l_shoulder_y.present_position
				position[position_counter]["42"]= self.PoppyGRR.Poppyboid.l_shoulder_x.present_position
				position[position_counter]["43"]= self.PoppyGRR.Poppyboid.l_arm_z.present_position
				position[position_counter]["44"]= self.PoppyGRR.Poppyboid.l_elbow_y.present_position
				if self.PoppyGRR.wrists:
					position[position_counter]["45"]= self.PoppyGRR.Poppyboid.l_wrist_z.present_position
					position[position_counter]["46"]= self.PoppyGRR.Poppyboid.l_wrist_x.present_position
				if position_counter!=1 and is_moving == False:
					if abs(position[position_counter]["41"]-position[position_counter-1]["41"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["42"]-position[position_counter-1]["42"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["43"]-position[position_counter-1]["43"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["44"]-position[position_counter-1]["44"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
					if self.PoppyGRR.wrists:
						if abs(position[position_counter]["45"]-position[position_counter-1]["45"])>self.PoppyGRR.SEUIL_ANGLE:
							is_moving = True
						if abs(position[position_counter]["46"]-position[position_counter-1]["46"])>self.PoppyGRR.SEUIL_ANGLE:
							is_moving = True

			#partie bras droit
			if "bras_droit" in self.poppyParts:
				position[position_counter]["51"]= self.PoppyGRR.Poppyboid.r_shoulder_y.present_position
				position[position_counter]["52"]= self.PoppyGRR.Poppyboid.r_shoulder_x.present_position
				position[position_counter]["53"]= self.PoppyGRR.Poppyboid.r_arm_z.present_position
				position[position_counter]["54"]= self.PoppyGRR.Poppyboid.r_elbow_y.present_position
				if self.PoppyGRR.wrists:
					position[position_counter]["55"]= self.PoppyGRR.Poppyboid.r_wrist_z.present_position
					position[position_counter]["56"]= self.PoppyGRR.Poppyboid.r_wrist_x.present_position
				if position_counter!=1 and is_moving == False:
					if abs(position[position_counter]["51"]-position[position_counter-1]["51"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["52"]-position[position_counter-1]["52"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["53"]-position[position_counter-1]["53"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
					if abs(position[position_counter]["54"]-position[position_counter-1]["54"])>self.PoppyGRR.SEUIL_ANGLE:
						is_moving = True
					if self.PoppyGRR.wrists:
						if abs(position[position_counter]["55"]-position[position_counter-1]["55"])>self.PoppyGRR.SEUIL_ANGLE:
							is_moving = True
						if abs(position[position_counter]["56"]-position[position_counter-1]["56"])>self.PoppyGRR.SEUIL_ANGLE:
							is_moving = True
		
			time.sleep(0.2) #frequence d'enregistrement
			if is_moving == False:			# si ca a pas bouge ce tour ci
				not_moving_counter += 1 	# on compte combien de tours de suite
				if not_moving_counter == self.PoppyGRR.TIME_LIMIT: # si on a atteint la limite
					#supprime les increments immobiles
					if self.PoppyGRR.TIME_LIMIT>2 :
						position["nb_temps"]=position_counter-(self.PoppyGRR.TIME_LIMIT-2)
						for i in range(self.PoppyGRR.TIME_LIMIT-2):
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
	def __init__(self, poppy, posName='currentPos'):
		self.PoppyGRR=poppy
		self.posName=posName
		pypot.primitive.Primitive.__init__(self, self.PoppyGRR.Poppyboid)	

	def run(self):
		#print 'scanning Poppy...'
		self.PoppyGRR.SCANNING = 1
		position= OrderedDict() #creation d'un dictionnaire avec maintien de l'ordre
		#partie jambes
		if self.PoppyGRR.creature == "humanoid":
			position["11"]= self.PoppyGRR.Poppyboid.l_hip_x.present_position
			position["12"]= self.PoppyGRR.Poppyboid.l_hip_z.present_position
			position["13"]= self.PoppyGRR.Poppyboid.l_hip_y.present_position
			position["14"]= self.PoppyGRR.Poppyboid.l_knee_y.present_position
			position["15"]= self.PoppyGRR.Poppyboid.l_ankle_y.present_position
			position["21"]= self.PoppyGRR.Poppyboid.r_hip_x.present_position
			position["22"]= self.PoppyGRR.Poppyboid.r_hip_z.present_position
			position["23"]= self.PoppyGRR.Poppyboid.r_hip_y.present_position
			position["24"]= self.PoppyGRR.Poppyboid.r_knee_y.present_position
			position["25"]= self.PoppyGRR.Poppyboid.r_ankle_y.present_position
			position["31"]= self.PoppyGRR.Poppyboid.abs_y.present_position
			position["32"]= self.PoppyGRR.Poppyboid.abs_x.present_position
		#partie torso
		position["33"]= self.PoppyGRR.Poppyboid.abs_z.present_position
		position["34"]= self.PoppyGRR.Poppyboid.bust_y.present_position
		position["35"]= self.PoppyGRR.Poppyboid.bust_x.present_position
		position["36"]= self.PoppyGRR.Poppyboid.head_z.present_position
		position["37"]= self.PoppyGRR.Poppyboid.head_y.present_position
		position["41"]= self.PoppyGRR.Poppyboid.l_shoulder_y.present_position
		position["42"]= self.PoppyGRR.Poppyboid.l_shoulder_x.present_position
		position["43"]= self.PoppyGRR.Poppyboid.l_arm_z.present_position
		position["44"]= self.PoppyGRR.Poppyboid.l_elbow_y.present_position
		if self.PoppyGRR.wrists:
			position["45"]= self.PoppyGRR.Poppyboid.l_wrist_z.present_position
			position["46"]= self.PoppyGRR.Poppyboid.l_wrist_x.present_position
		position["51"]= self.PoppyGRR.Poppyboid.r_shoulder_y.present_position
		position["52"]= self.PoppyGRR.Poppyboid.r_shoulder_x.present_position
		position["53"]= self.PoppyGRR.Poppyboid.r_arm_z.present_position
		position["54"]= self.PoppyGRR.Poppyboid.r_elbow_y.present_position
		if self.PoppyGRR.wrists:
			position["55"]= self.PoppyGRR.Poppyboid.r_wrist_z.present_position
			position["56"]= self.PoppyGRR.Poppyboid.r_wrist_x.present_position
		#export into a Json file ----------- Change file name if necessary
		with open('./position/'+self.posName+'.json', 'w') as f:
			json.dump(position, f, indent=4)
		#print 'scanning done'
		self.PoppyGRR.SCANNING = 0
		
#primitive mise en position
class miseEnPosPrimitive(pypot.primitive.Primitive):
	def __init__(self, poppy, position, speed):
		self.PoppyGRR=poppy
		self.Poppyboid=self.PoppyGRR.Poppyboid
		self.position=position
		self.speed=speed
		pypot.primitive.Primitive.__init__(self, self.Poppyboid)	

	def run(self):
		timeMultiplier = 2
		self.Poppyboid.scanPosition.start()
		time.sleep(0.1)
		while self.PoppyGRR.SCANNING == 1:
			time.sleep(0.05)
		positionActu={} #Position de depart
		positionFin={} #Position a atteindre
		#charge un fichier Json - position courante
		with open('./position/currentPos.json', 'r') as f:
		    positionActu = json.load(f)
	
		positionFin = self.position
		#print self.speed.keys()	
		if "jambe_gauche" in self.speed.keys() and self.PoppyGRR.creature == "humanoid":
			if "11" in positionFin:
 				if abs(positionFin["11"]-positionActu["11"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["11"]-positionActu["11"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["11"]-positionActu["11"]>0:
							positionFin["11"]=positionActu["11"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["11"]=positionActu["11"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'l_hip_x':positionFin["11"]}, timeMultiplier*self.speed["jambe_gauche"], wait=False)
			if "12" in positionFin:
				if abs(positionFin["12"]-positionActu["12"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["12"]-positionActu["12"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["12"]-positionActu["12"]>0:
							positionFin["12"]=positionActu["12"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["12"]=positionActu["12"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'l_hip_z':positionFin["12"]}, timeMultiplier*self.speed["jambe_gauche"], wait=False)
			if "13" in positionFin:
				if abs(positionFin["13"]-positionActu["13"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["13"]-positionActu["13"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["13"]-positionActu["13"]>0:
							positionFin["13"]=positionActu["13"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["13"]=positionActu["13"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'l_hip_y':positionFin["13"]}, timeMultiplier*self.speed["jambe_gauche"], wait=False)
			if "14" in positionFin:
				if abs(positionFin["14"]-positionActu["14"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["14"]-positionActu["14"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["14"]-positionActu["14"]>0:
							positionFin["14"]=positionActu["14"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["14"]=positionActu["14"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'l_knee_y': positionFin["14"]}, timeMultiplier*self.speed["jambe_gauche"], wait=False)
			if "15" in positionFin:
				if abs(positionFin["15"]-positionActu["15"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["15"]-positionActu["15"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["15"]-positionActu["15"]>0:
							positionFin["15"]=positionActu["15"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["15"]=positionActu["15"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'l_ankle_y':positionFin["15"]}, timeMultiplier*self.speed["jambe_gauche"], wait=False)
		if "jambe_droite" in self.speed.keys() and self.PoppyGRR.creature == "humanoid":
			if "21" in positionFin:
				if abs(positionFin["21"]-positionActu["21"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["21"]-positionActu["21"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["21"]-positionActu["21"]>0:
							positionFin["21"]=positionActu["21"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["21"]=positionActu["21"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'r_hip_x':positionFin["21"]}, timeMultiplier*self.speed["jambe_droite"], wait=False)
			if "22" in positionFin:
				if abs(positionFin["22"]-positionActu["22"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["22"]-positionActu["22"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["22"]-positionActu["22"]>0:
							positionFin["22"]=positionActu["22"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["22"]=positionActu["22"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'r_hip_z':positionFin["22"]}, timeMultiplier*self.speed["jambe_droite"], wait=False)
			if "23" in positionFin:
				if abs(positionFin["23"]-positionActu["23"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["23"]-positionActu["23"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["23"]-positionActu["23"]>0:
							positionFin["23"]=positionActu["23"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["23"]=positionActu["23"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'r_hip_y': positionFin["23"]}, timeMultiplier*self.speed["jambe_droite"], wait=False)
			if "24" in positionFin:
				if abs(positionFin["24"]-positionActu["24"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["24"]-positionActu["24"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["24"]-positionActu["24"]>0:
							positionFin["24"]=positionActu["24"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["24"]=positionActu["24"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'r_knee_y':positionFin["24"]}, timeMultiplier*self.speed["jambe_droite"], wait=False)
			if "25" in positionFin:
				if abs(positionFin["25"]-positionActu["25"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["25"]-positionActu["25"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["25"]-positionActu["25"]>0:
							positionFin["25"]=positionActu["25"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["25"]=positionActu["25"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'r_ankle_y':positionFin["25"]}, timeMultiplier*self.speed["jambe_droite"], wait=False)
		if "colonne" in self.speed.keys():
			if "31" in positionFin:
				if abs(positionFin["31"]-positionActu["31"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["31"]-positionActu["31"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["31"]-positionActu["31"]>0:
							positionFin["31"]=positionActu["31"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["31"]=positionActu["31"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'abs_y':positionFin["31"]}, timeMultiplier*self.speed["colonne"], wait=False)
			if "32" in positionFin:
				if abs(positionFin["32"]-positionActu["32"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["32"]-positionActu["32"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["32"]-positionActu["32"]>0:
							positionFin["32"]=positionActu["32"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["32"]=positionActu["32"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'abs_x':positionFin["32"]}, timeMultiplier*self.speed["colonne"], wait=False)
			if "33" in positionFin:
				if abs(positionFin["33"]-positionActu["33"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["33"]-positionActu["33"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["33"]-positionActu["33"]>0:
							positionFin["33"]=positionActu["33"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["33"]=positionActu["33"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'abs_z':positionFin["33"]}, timeMultiplier*self.speed["colonne"], wait=False)
			if "34" in positionFin:
				if abs(positionFin["34"]-positionActu["34"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["34"]-positionActu["34"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["34"]-positionActu["34"]>0:
							positionFin["34"]=positionActu["34"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["34"]=positionActu["34"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'bust_y':positionFin["34"]}, timeMultiplier*self.speed["colonne"], wait=False)
			if "35" in positionFin:
				if abs(positionFin["35"]-positionActu["35"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["35"]-positionActu["35"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["35"]-positionActu["35"]>0:
							positionFin["35"]=positionActu["35"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["35"]=positionActu["35"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'bust_x':positionFin["35"]}, timeMultiplier*self.speed["colonne"], wait=False)
		if "bras_droit" in self.speed.keys():
			if "51" in positionFin:
				if abs(positionFin["51"]-positionActu["51"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["51"]-positionActu["51"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["51"]-positionActu["51"]>0:
							positionFin["51"]=positionActu["51"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["51"]=positionActu["51"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'r_shoulder_y':positionFin["51"]}, timeMultiplier*self.speed["bras_droit"], wait=False)
			if "52" in positionFin:
				if abs(positionFin["52"]-positionActu["52"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["52"]-positionActu["52"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["52"]-positionActu["52"]>0:
							positionFin["52"]=positionActu["52"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["52"]=positionActu["52"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'r_shoulder_x':positionFin["52"]}, timeMultiplier*self.speed["bras_droit"], wait=False)
			if "53" in positionFin:
				if abs(positionFin["53"]-positionActu["53"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["53"]-positionActu["53"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["53"]-positionActu["53"]>0:
							positionFin["53"]=positionActu["53"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["53"]=positionActu["53"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'r_arm_z':positionFin["53"]}, timeMultiplier*self.speed["bras_droit"], wait=False)
			if "54" in positionFin:
				if abs(positionFin["54"]-positionActu["54"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["54"]-positionActu["54"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["54"]-positionActu["54"]>0:
							positionFin["54"]=positionActu["54"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["54"]=positionActu["54"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'r_elbow_y': positionFin["54"]}, timeMultiplier*self.speed["bras_droit"], wait=False)
			if self.PoppyGRR.wrists:
				if "55" in positionFin:
					if abs(positionFin["55"]-positionActu["55"])>self.PoppyGRR.SEUIL_ANGLE :
						if abs(positionFin["55"]-positionActu["55"])>self.PoppyGRR.LIMITE_ANGLE:
							if positionFin["55"]-positionActu["55"]>0:
								positionFin["55"]=positionActu["55"]+self.PoppyGRR.LIMITE_ANGLE
							else:
								positionFin["55"]=positionActu["55"]-self.PoppyGRR.LIMITE_ANGLE
						self.Poppyboid.goto_position({'r_wrist_z': positionFin["55"]}, timeMultiplier*self.speed["bras_droit"], wait=False)
				if "56" in positionFin:
					if abs(positionFin["56"]-positionActu["56"])>self.PoppyGRR.SEUIL_ANGLE :
						if abs(positionFin["56"]-positionActu["56"])>self.PoppyGRR.LIMITE_ANGLE:
							if positionFin["56"]-positionActu["56"]>0:
								positionFin["56"]=positionActu["56"]+self.PoppyGRR.LIMITE_ANGLE
							else:
								positionFin["56"]=positionActu["56"]-self.PoppyGRR.LIMITE_ANGLE
						self.Poppyboid.goto_position({'r_wrist_x': positionFin["56"]}, timeMultiplier*self.speed["bras_droit"], wait=False)
		if "bras_gauche" in self.speed.keys():
			if "41" in positionFin:
				if abs(positionFin["41"]-positionActu["41"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["41"]-positionActu["41"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["41"]-positionActu["41"]>0:
							positionFin["41"]=positionActu["41"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["41"]=positionActu["41"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'l_shoulder_y':positionFin["41"]},timeMultiplier*self.speed["bras_gauche"], wait=False)
			if "42" in positionFin:
				if abs(positionFin["42"]-positionActu["42"])>self.PoppyGRR.SEUIL_ANGLE:
					if abs(positionFin["42"]-positionActu["42"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["42"]-positionActu["42"]>0:
							positionFin["42"]=positionActu["42"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["42"]=positionActu["42"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'l_shoulder_x':positionFin["42"]}, timeMultiplier*self.speed["bras_gauche"], wait=False)
			if "43" in positionFin:
				if abs(positionFin["43"]-positionActu["43"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["43"]-positionActu["43"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["43"]-positionActu["43"]>0:
							positionFin["43"]=positionActu["43"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["43"]=positionActu["43"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'l_arm_z':positionFin["43"]}, timeMultiplier*self.speed["bras_gauche"], wait=False)
			if "44" in positionFin:
				if abs(positionFin["44"]-positionActu["44"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["44"]-positionActu["44"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["44"]-positionActu["44"]>0:
							positionFin["44"]=positionActu["44"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["44"]=positionActu["44"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'l_elbow_y': positionFin["44"]}, timeMultiplier*self.speed["bras_gauche"], wait=False)
			if self.PoppyGRR.wrists:
				if "45" in positionFin:
					if abs(positionFin["45"]-positionActu["45"])>self.PoppyGRR.SEUIL_ANGLE :
						if abs(positionFin["45"]-positionActu["45"])>self.PoppyGRR.LIMITE_ANGLE:
							if positionFin["45"]-positionActu["45"]>0:
								positionFin["45"]=positionActu["45"]+self.PoppyGRR.LIMITE_ANGLE
							else:
								positionFin["45"]=positionActu["45"]-self.PoppyGRR.LIMITE_ANGLE
						self.Poppyboid.goto_position({'l_wrist_z': positionFin["45"]}, timeMultiplier*self.speed["bras_gauche"], wait=False)
				if "46" in positionFin:
					if abs(positionFin["46"]-positionActu["46"])>self.PoppyGRR.SEUIL_ANGLE :
						if abs(positionFin["46"]-positionActu["46"])>self.PoppyGRR.LIMITE_ANGLE:
							if positionFin["46"]-positionActu["46"]>0:
								positionFin["46"]=positionActu["46"]+self.PoppyGRR.LIMITE_ANGLE
							else:
								positionFin["46"]=positionActu["46"]-self.PoppyGRR.LIMITE_ANGLE
						self.Poppyboid.goto_position({'l_wrist_x': positionFin["46"]}, timeMultiplier*self.speed["bras_gauche"], wait=False)
		if "tete" in self.speed.keys():
			if "36" in positionFin:
				if abs(positionFin["36"]-positionActu["36"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["36"]-positionActu["36"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["36"]-positionActu["36"]>0:
							positionFin["36"]=positionActu["36"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["36"]=positionActu["36"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'head_z':positionFin["36"]}, timeMultiplier*self.speed["tete"], wait=False)
			if "37" in positionFin:
				if abs(positionFin["37"]-positionActu["37"])>self.PoppyGRR.SEUIL_ANGLE :
					if abs(positionFin["37"]-positionActu["37"])>self.PoppyGRR.LIMITE_ANGLE:
						if positionFin["37"]-positionActu["37"]>0:
							positionFin["37"]=positionActu["37"]+self.PoppyGRR.LIMITE_ANGLE
						else:
							positionFin["37"]=positionActu["37"]-self.PoppyGRR.LIMITE_ANGLE
					self.Poppyboid.goto_position({'head_y':positionFin["37"]}, timeMultiplier*self.speed["tete"], wait=False)
		#Pour laisser le temps au robot d'effectuer le mouvement : t_sleep>t_mouvement
		#time.sleep(1)     

class goMovePrimitive(pypot.primitive.Primitive):
	def __init__(self, poppy, rev, moveType, moveName, speedDict, tempsboucle, startTime, endTime):
		self.PoppyGRR=poppy
		self.rev=rev
		self.moveType=moveType
		self.moveName=moveName
		self.speedDict=speedDict
		self.tempsboucle=tempsboucle
		self.startTime=startTime
		self.endTime=endTime
		pypot.primitive.Primitive.__init__(self, self.PoppyGRR.Poppyboid)
		
	def run(self):
		while self.PoppyGRR.PLAYING_MOVE:	# attente que la partie du mouvement precedent se termine
			time.sleep(0.1)
		self.PoppyGRR.PLAYING_MOVE = True
		self.PoppyGRR.directionPoppypart = self.speedDict
		if self.PoppyGRR.FACE_MANAGING_ENABLE and not self.PoppyGRR.DIRECTION_MANAGING_ON:
			self.PoppyGRR.DIRECTION_MANAGING_ON = True
			self.PoppyGRR.directionTh = Thread(target=self.PoppyGRR.setDirectionEyes)
			self.PoppyGRR.directionTh.start()
		#time.sleep(0.5)		#attente le temps que mov precedent se termine
		print "startTime : "+str(self.startTime)+", endTime : "+str(self.endTime)
		with open('./move/'+self.moveType+'/'+self.moveName+'.json', 'r') as f:
			moveFile = json.load(f)
		if self.rev == False:
			for temps in range(self.startTime, self.endTime):
				while self.PoppyGRR.EXO_SLEEP == True and self.PoppyGRR.MOVING_ENABLE == True:
					time.sleep(0.1)
				if self.PoppyGRR.MOVING_ENABLE == False:
					self.PoppyGRR.PLAYING_MOVE = False
					print "---stop moving primitive 1---"
					return
				if temps+1 == 1:
					self.PoppyGRR.goFirstPos(moveFile[str(temps+1)], moveFile["speed"])
				else:
					if str(temps+1) in moveFile:
						miseEnPosPrimitive(self.PoppyGRR,moveFile[str(temps+1)], self.speedDict).start()
					if self.PoppyGRR.MOVING_ENABLE == False:
						self.PoppyGRR.PLAYING_MOVE = False
						print "---stop moving primitive 2---"
						return
					time.sleep(self.tempsboucle)
				self.PoppyGRR.EXO_TEMPS += 1
		else:
			return	#TODO : lecture a l'envers non geree !!!
			for temps in range(moveFile["nb_temps"]):
				while self.PoppyGRR.EXO_SLEEP == True and self.PoppyGRR.MOVING_ENABLE == True:
					time.sleep(0.2)
				if self.PoppyGRR.MOVING_ENABLE == False:
					self.PoppyGRR.PLAYING_MOVE = False
					print "---stop moving primitive 1---"
					return
				if temps+1 == 1:
					self.PoppyGRR.goFirstPos(moveFile[str(moveFile["nb_temps"]-temps)], moveFile["speed"])
				else:
					if str(moveFile["nb_temps"]-temps) in moveFile:
						self.PoppyGRR.miseEnPosPrimitive(self.PoppyGRR,moveFile[str(moveFile["nb_temps"]-temps)], self.speedDict).start()
					if self.PoppyGRR.MOVING_ENABLE == False:
						self.PoppyGRR.PLAYING_MOVE = False
						print "---stop moving primitive 2---"
						return
					time.sleep(self.tempsboucle)
				self.PoppyGRR.EXO_TEMPS += 1
		self.PoppyGRR.PLAYING_MOVE = False
		if self.endTime == moveFile["nb_temps"]:	#si on est a la derniere partie
			self.PoppyGRR.MOVING_ENABLE = False

#primitive jouer un exo ou une seance
class goExoPrimitive(pypot.primitive.Primitive):
	def __init__(self, poppy, exoName, exoType, tempsPause=0):
		self.PoppyGRR=poppy
		self.exoName=exoName
		self.exoType=exoType
		self.tempsPause=tempsPause
		pypot.primitive.Primitive.__init__(self, self.PoppyGRR.Poppyboid)

	def run(self):
		self.PoppyGRR.NUM_MOV = 0
		with open('./move/'+self.exoType+'/'+self.exoName+'.json', 'r') as f:
			moveConfig= json.load(f)
		#VOIX
		if self.exoType == "exo":
			self.nbTemps = moveConfig["nb_temps"]
			description = {}
			if "description" in moveConfig.keys():
				description = moveConfig["description"]
				description["offset"] = self.PoppyGRR.EXO_TEMPS
				
		for i in range(int(moveConfig["nb_fichiers"])):		#verifie les parametres du fichier config
			while self.PoppyGRR.EXO_SLEEP == True and self.PoppyGRR.EXO_ENABLE == True:				#tant que l'exercice est en pause
				time.sleep(0.05)
			if self.PoppyGRR.EXO_ENABLE == False:					#si ordre d'arreter la primitive
				break
			namefile = moveConfig["fichier"+str(i+1)]["namefile"]
			#Si c'est un exercice
			if self.PoppyGRR.directory(namefile) == "exo":
				self.PoppyGRR.PLAYING_SEANCE=True
				time.sleep(1.5)
				while (self.PoppyGRR.PLAYING_EXO == True or self.PoppyGRR.EXO_SLEEP):	#on attend que pas d'exo en cours
					time.sleep(0.2)
				while self.PoppyGRR.WAIT_REPET:
					time.sleep(0.5)
				if self.PoppyGRR.kinectName != 'none' and self.PoppyGRR.repetitions:
					time.sleep(0.5)
					self.PoppyGRR.waitVoice()
				if self.PoppyGRR.EXO_ENABLE == False:			#si ordre d'arreter la primitive
					print "---stop seance 1---"
					return
				self.PoppyGRR.NUM_EXO +=1
				self.PoppyGRR.NUM_MOV = 0
				self.PoppyGRR.logger.info("Exercice : "+str(self.PoppyGRR.NUM_EXO)+", Mouvement : "+str(self.PoppyGRR.NUM_MOV))
				if i==0:
					time.sleep(1)
				if self.PoppyGRR.EXO_ENABLE == False:			#si ordre d'arreter la primitive
					print "---stop seance 2---"
					return
				#communication kinect
				if self.PoppyGRR.kinectName != "none":
					self.PoppyGRR.waitKinect = True
					print "give exoname : "+namefile+" to "+self.PoppyGRR.kinectName
					kinect = requests.post("http://"+self.PoppyGRR.kinectName+".local:4567/?Submit=give+exoname&exoname="+namefile)
					if kinect.status_code==200:
						print "attention, la kinect ne connait pas l'exercice !"
						self.PoppyGRR.logger.warning("kinect does not know the exercise !")
					elif kinect.status_code==201:
						print "kinect ok pour nom exo"
					while self.PoppyGRR.waitKinect:
						time.sleep(0.5)
				self.PoppyGRR.NUM_PHASE = 0
				print "goExoPrimitive : "+namefile
				self.PoppyGRR.logger.warning("goExoPrimitive : "+namefile)
				goExoPrimitive(self.PoppyGRR,namefile, "exo", moveConfig["fichier"+str(i+1)]["pause"]).start()
				time.sleep(1)
			#si c'est un mouvement
			else:
				self.PoppyGRR.PLAYING_EXO = True
				self.PoppyGRR.waitVoice()
				speed = moveConfig["fichier"+str(i+1)]["vitesse"]
			#JOUE LE MOUVEMENT i+1
				self.PoppyGRR.NUM_MOV +=1
				self.PoppyGRR.logger.info("Exercice : "+str(self.PoppyGRR.NUM_EXO)+", Mouvement : "+str(self.PoppyGRR.NUM_MOV))
				move = self.PoppyGRR.GoMove(namefile, speed, description=description)
				if move == "stop":
					print "---stop exo via stop move---"
					self.PoppyGRR.logger.warning("stop exo via stop move")
					self.PoppyGRR.PLAYING_EXO = False
					self.PoppyGRR.PLAYING_SEANCE = False
					return
				if self.PoppyGRR.EXO_ENABLE == False:			#si ordre d'arreter la primitive
					print "---stop exo 1---"
					self.PoppyGRR.logger.warning("stop exo 1")
					self.PoppyGRR.PLAYING_EXO = False
					self.PoppyGRR.PLAYING_SEANCE = False
					return
				self.PoppyGRR.PAUSE = True
				if moveConfig["fichier"+str(i+1)]["pause"]!=0:
					time.sleep(float(moveConfig["fichier"+str(i+1)]["pause"]))
				self.PoppyGRR.PAUSE = False
				self.PoppyGRR.EXO_TEMPS += int(moveConfig["fichier"+str(i+1)]["pause"])
				if self.PoppyGRR.EXO_ENABLE == False:			#si ordre d'arreter la primitive
					print "---stop exo 2---"
					self.PoppyGRR.logger.warning("stop exo 2")
					self.PoppyGRR.PLAYING_EXO = False
					self.PoppyGRR.PLAYING_SEANCE = False
					return

		if self.PoppyGRR.directory(namefile) == "mov": 		#dernier mov
			if not self.PoppyGRR.REPET:						#si pas une repetition de l exercice
				if self.PoppyGRR.kinectName != "none":
					self.PoppyGRR.waitFeedback = True
					print "pause apres exo"
					self.PoppyGRR.PauseExo()							#pause entre chaque exercice d'une seance
					startKinectTh = Thread(target=self.startKinect)
					startKinectTh.start()
					time.sleep(1.5)
					while self.PoppyGRR.EXO_SLEEP and self.PoppyGRR.EXO_TEMPS<self.PoppyGRR.EXO_TEMPS_LIMITE or self.PoppyGRR.REPET:
						time.sleep(0.5)
				if self.tempsPause == 0:
					time.sleep(1)
				else:
					self.PoppyGRR.PAUSE = True
					self.PoppyGRR.EXO_TEMPS += int(self.tempsPause)
					if self.tempsPause>2:
						self.tempsPause-=2
					time.sleep(self.tempsPause)
					self.PoppyGRR.PAUSE = False
				if self.PoppyGRR.EXO_TEMPS<self.PoppyGRR.EXO_TEMPS_LIMITE:
					while self.PoppyGRR.waitFeedback:
						time.sleep(0.5)
					rand = randint(1,3)
					if self.PoppyGRR.PLAYING_SEANCE:
						self.PoppyGRR.voice.play("./sound/sounds/exerciceSuivant"+str(rand)+".mp3")
				elif self.PoppyGRR.NUM_EXO!=0:
					while self.PoppyGRR.waitFeedback:
						time.sleep(0.5)
					#if self.PoppyGRR.PLAYING_SEANCE:
					self.PoppyGRR.voice.play("./sound/sounds/finSeance.mp3")
			else:										# si en cours de repetition
				self.PoppyGRR.PauseExo()
				self.PoppyGRR.REPET = False
			time.sleep(2)
			self.PoppyGRR.PLAYING_EXO = False
			self.PoppyGRR.PLAYING_SEANCE = False
			if not self.PoppyGRR.REPET and self.PoppyGRR.WAIT_REPET:
				self.PoppyGRR.WAIT_REPET = False

		if self.PoppyGRR.EXO_TEMPS>=self.PoppyGRR.EXO_TEMPS_LIMITE and not self.PoppyGRR.REPET:
			print "fini : "+str(self.PoppyGRR.EXO_TEMPS)+"/"+str(self.PoppyGRR.EXO_TEMPS_LIMITE)
			self.PoppyGRR.EXO_ENABLE = False
		#return "played"

	def startKinect(self):
		kinect = requests.post("http://"+self.PoppyGRR.kinectName+".local:4567/?Submit=start+kinect&nb_repetition=1")
		if kinect.status_code==201:
			print "kinect commence"
		print "a toi !"
		self.PoppyGRR.voice.play('./sound/sounds/atoi.mp3')
		if self.PoppyGRR.repetitions:
			self.PoppyGRR.REPET = True
			self.PoppyGRR.WAIT_REPET = True
			time.sleep(0.25)
			self.PoppyGRR.NUM_PHASE = 0
			#self.PoppyGRR.NUM_MOV = 0
			#self.PoppyGRR.NUM_EXO -= 1
			self.PoppyGRR.EXO_TEMPS -= self.nbTemps
			self.PoppyGRR.EXO_SLEEP = False
			goExoPrimitive(self.PoppyGRR,self.exoName, "exo").start()
			time.sleep(1)
			while self.PoppyGRR.PLAYING_EXO:
				time.sleep(0.5)

#primitive mode semi-mou
class semiCompliantPrimitive(pypot.primitive.Primitive):
	def __init__(self, poppy):
		self.PoppyGRR=poppy
		self.Poppyboid=self.PoppyGRR.Poppyboid
		pypot.primitive.Primitive.__init__(self, self.Poppyboid)

	def run(self):
		t = 0.01
		while len(self.PoppyGRR.SEMI_MOU) != 0:
			if self.PoppyGRR.creature == "humanoid":
				if "jambe_gauche" in self.PoppyGRR.SEMI_MOU :
					self.Poppyboid.goto_position({'l_hip_x':self.Poppyboid.l_hip_x.present_position}, t, wait=False)
					self.Poppyboid.goto_position({'l_hip_z':self.Poppyboid.l_hip_z.present_position}, t, wait=False)
					self.Poppyboid.goto_position({'l_hip_y':self.Poppyboid.l_hip_y.present_position}, t, wait=False)
					self.Poppyboid.goto_position({'l_knee_y': self.Poppyboid.l_knee_y.present_position}, t, wait=False)
					self.Poppyboid.goto_position({'l_ankle_y':self.Poppyboid.l_ankle_y.present_position}, t, wait=False)
				if "jambe_droite" in self.PoppyGRR.SEMI_MOU :
					self.Poppyboid.goto_position({'r_hip_x':self.Poppyboid.r_hip_x.present_position}, t, wait=False)
					self.Poppyboid.goto_position({'r_hip_z':self.Poppyboid.r_hip_z.present_position}, t, wait=False)
					self.Poppyboid.goto_position({'r_hip_y': self.Poppyboid.r_hip_y.present_position}, t, wait=False)
					self.Poppyboid.goto_position({'r_knee_y':self.Poppyboid.r_knee_y.present_position}, t, wait=False)
					self.Poppyboid.goto_position({'r_ankle_y':self.Poppyboid.r_ankle_y.present_position}, t, wait=False)
			if "colonne" in self.PoppyGRR.SEMI_MOU :
				self.Poppyboid.goto_position({'abs_y':self.Poppyboid.abs_y.present_position}, t, wait=False)
				self.Poppyboid.goto_position({'abs_x':self.Poppyboid.abs_x.present_position}, t, wait=False)
				self.Poppyboid.goto_position({'abs_z':self.Poppyboid.abs_z.present_position}, t, wait=False)
				self.Poppyboid.goto_position({'bust_y':self.Poppyboid.bust_y.present_position}, t, wait=False)
				self.Poppyboid.goto_position({'bust_x':self.Poppyboid.bust_x.present_position}, t, wait=False)
			if "bras_droit" in self.PoppyGRR.SEMI_MOU :
				self.Poppyboid.goto_position({'r_shoulder_y':self.Poppyboid.r_shoulder_y.present_position}, t, wait=False)
				self.Poppyboid.goto_position({'r_shoulder_x':self.Poppyboid.r_shoulder_x.present_position}, t, wait=False)
				self.Poppyboid.goto_position({'r_arm_z':self.Poppyboid.r_arm_z.present_position}, t, wait=False)
				self.Poppyboid.goto_position({'r_elbow_y': self.Poppyboid.r_elbow_y.present_position}, t, wait=False)
#				self.Poppyboid.goto_position({'r_wrist_z': self.Poppyboid.r_wrist_z.present_position}, t, wait=False)
#				self.Poppyboid.goto_position({'r_wrist_x': self.Poppyboid.r_wrist_x.present_position}, t, wait=False)
				if self.PoppyGRR.wrists:
					if self.Poppyboid.r_wrist_z.compliant == False:
						self.Poppyboid.r_wrist_z.compliant = True
						self.Poppyboid.r_wrist_x.compliant = True
			if "bras_gauche" in self.PoppyGRR.SEMI_MOU :
				self.Poppyboid.goto_position({'l_shoulder_y':self.Poppyboid.l_shoulder_y.present_position},t, wait=False)
				self.Poppyboid.goto_position({'l_shoulder_x':self.Poppyboid.l_shoulder_x.present_position}, t, wait=False)
				self.Poppyboid.goto_position({'l_arm_z':self.Poppyboid.l_arm_z.present_position}, t, wait=False)
				self.Poppyboid.goto_position({'l_elbow_y': self.Poppyboid.l_elbow_y.present_position}, t, wait=False)
#				self.Poppyboid.goto_position({'l_wrist_z': self.Poppyboid.l_wrist_z.present_position}, t, wait=False)
#				self.Poppyboid.goto_position({'l_wrist_x': self.Poppyboid.l_wrist_x.present_position}, t, wait=False)
				if self.PoppyGRR.wrists:
					if self.Poppyboid.l_wrist_z.compliant == False:
						self.Poppyboid.l_wrist_z.compliant = True
						self.Poppyboid.l_wrist_x.compliant = True
			if "tete" in self.PoppyGRR.SEMI_MOU :
				self.Poppyboid.goto_position({'head_z':self.Poppyboid.head_z.present_position}, t, wait=False)
				self.Poppyboid.goto_position({'head_y':self.Poppyboid.head_y.present_position}, t, wait=False)
			time.sleep(t/2.0)

#primitive scan moteurs regulier
class scanMotorsLoop(pypot.primitive.Primitive):
	def __init__(self, poppy):
		self.PoppyGRR=poppy
		self.surchauffeState=False
		self.surchauffeTimer=0
		pypot.primitive.Primitive.__init__(self, self.PoppyGRR.Poppyboid)

	def run(self):
		while True:
			try:
				self.scanMotors()
			except:
				self.PoppyGRR.logger.exception("***** scanMotors error *****")
			time.sleep(5)

	def scanMotors(self):
		stop = False
		temps = time.time()-self.PoppyGRR.t0
		#mesures
		imoteur=0
		if self.PoppyGRR.creature == "humanoid":
			self.PoppyGRR.poppyPart_alert['JG'] = 'ok'
			self.PoppyGRR.poppyPart_alert['JD'] = 'ok'
		self.PoppyGRR.poppyPart_alert['T'] = 'ok'
		self.PoppyGRR.poppyPart_alert['Col'] = 'ok'
		self.PoppyGRR.poppyPart_alert['BG'] = 'ok'
		self.PoppyGRR.poppyPart_alert['BD'] = 'ok'

		for m in self.PoppyGRR.Poppyboid.motors:
			self.PoppyGRR.position[imoteur] = m.present_position
			self.PoppyGRR.voltage[imoteur] = m.present_voltage
			if m.present_temperature<60: 	#erreur de communication moteur sinon
				self.PoppyGRR.temperature[imoteur] = m.present_temperature
			self.PoppyGRR.couple[imoteur] = m.present_load
			if round(self.PoppyGRR.temperature[imoteur], 1)>=self.PoppyGRR.SEUIL_TEMP:
				if self.PoppyGRR.creature == "humanoid":
					if self.PoppyGRR.idmoteur[imoteur]>=11 and self.PoppyGRR.idmoteur[imoteur]<=19:
						poppyPart = "JG"
					if self.PoppyGRR.idmoteur[imoteur]>=21 and self.PoppyGRR.idmoteur[imoteur]<=29:
						poppyPart = "JD"
				if self.PoppyGRR.idmoteur[imoteur]>=31 and self.PoppyGRR.idmoteur[imoteur]<=35:
					poppyPart = "Col"
				if self.PoppyGRR.idmoteur[imoteur]>=36 and self.PoppyGRR.idmoteur[imoteur]<=37:
					poppyPart = "T"
					self.PoppyGRR.Compliant("tete")	#desactive la tete car chauffe vite
				if self.PoppyGRR.idmoteur[imoteur]>=41 and self.PoppyGRR.idmoteur[imoteur]<=49:
					poppyPart = "BG"
				if self.PoppyGRR.idmoteur[imoteur]>=51 and self.PoppyGRR.idmoteur[imoteur]<=59:
					poppyPart = "BD"
				if poppyPart not in self.PoppyGRR.poppyPart_alert:
					self.PoppyGRR.poppyPart_alert[poppyPart]=""
				if self.PoppyGRR.poppyPart_alert[poppyPart]!="stop" and round(self.PoppyGRR.temperature[imoteur],1)<self.PoppyGRR.SEUIL_TEMP_ARRET:
					self.PoppyGRR.poppyPart_alert[poppyPart]="warning"
					if self.surchauffeState==False and not self.PoppyGRR.poppyCompliant():
						self.surchauffeState=True
						self.surchauffeTimer=6
						#self.PoppyGRR.voice.play("./sound/sounds/surchauffe.mp3")
					else:
						self.surchauffeTimer-=1
						if self.surchauffeTimer==0:
							self.surchauffeState=False
				elif round(self.PoppyGRR.temperature[imoteur],1)>=self.PoppyGRR.SEUIL_TEMP_ARRET:
					self.PoppyGRR.poppyPart_alert[poppyPart]="stop"
					self.PoppyGRR.logger.warning("motor %s is overheating ! Preparing security mode.", self.PoppyGRR.idmoteur[imoteur])
					stop = True
			imoteur=imoteur+1

		resetSurchauffeState=True
	 	for key,value in self.PoppyGRR.poppyPart_alert.iteritems():
			if value!="ok":
				resetSurchauffeState=False
		if resetSurchauffeState:
			surchauffeState=False

		if stop == True and self.PoppyGRR.SecurityStop == False:
			if not self.PoppyGRR.poppyCompliant():
				self.PoppyGRR.logger.warning("set security mode")
				self.PoppyGRR.setSecurityMode()
				time.sleep(10)
				self.PoppyGRR.logger.warning("security mode : stop exo")
				self.PoppyGRR.StopExo()
				time.sleep(5)
				self.PoppyGRR.logger.warning("security mode : semi compliant")
				self.PoppyGRR.semiCompliant()
				time.sleep(20)
				self.PoppyGRR.logger.warning("security mode : compliant")
				self.PoppyGRR.Compliant()
				time.sleep(5)
				self.PoppyGRR.logger.warning("security mode OFF")
				self.PoppyGRR.SecurityStop = False
		#sauvegarde csv si seconde compris entre 0 et 5 : 1 mesure/minute
		seconds = int(time.strftime('%S', time.localtime()))
		if (seconds>0 and seconds<=5):
			with open("log/logs_"+str(self.PoppyGRR.year)+"-"+str(self.PoppyGRR.month)+"/motor.csv", "a") as csvfile:
				fieldnames=[ 'ID', 'posit.', 'U', 'temp.', 'couple']
				writer = csv.writer(csvfile, delimiter='	')
				writer.writerow([time.strftime('%d/%m/%Y %H:%M:%S', time.localtime()),''])
				writer.writerow(fieldnames)

			for imoteur in range(self.PoppyGRR.nbmoteurs):
				with open("log/logs_"+str(self.PoppyGRR.year)+"-"+str(self.PoppyGRR.month)+"/motor.csv", "a") as csvfile:
					writer = csv.writer(csvfile, delimiter='	')
					writer.writerow((self.PoppyGRR.idmoteur[imoteur], round(self.PoppyGRR.position[imoteur],2), round(self.PoppyGRR.voltage[imoteur],1), self.PoppyGRR.temperature[imoteur], self.PoppyGRR.couple[imoteur]))

class PoppyGRR:
	"""
		contains all the functions managing the robot and the motors
	"""

	def __init__(self, face, voice, kinectName, internet, creature, wrists, seuil_bien, seuil_nul, seuil_minable, repetitions):
		#Creation de l'objet robot
		self.creature = creature
		if creature == "humanoid":
			self.Poppyboid = PoppyHumanoid()
		elif creature == "torso":
			self.Poppyboid = PoppyTorso()
		self.face = face
		self.voice = voice
		self.internet = internet
		self.wrists = wrists
		self.repetitions = repetitions
		#feedbacks
		self.SEUIL_BIEN = seuil_bien
		self.SEUIL_NUL = seuil_nul
		self.SEUIL_MINABLE = seuil_minable
		self.NUM_PHASE = 0
		#variables moteurs
		self.idmoteur=[m.id for m in self.Poppyboid.motors]	#variable ID
		self.nbmoteurs=len(self.idmoteur)				#nombre de moteurs
		self.temps=0						#variable temps
		self.position=range(self.nbmoteurs)			#variable present position
		self.voltage=range(self.nbmoteurs)			#variable inumpyut voltage
		self.temperature=range(self.nbmoteurs)			#variable temperature
		self.couple=range(self.nbmoteurs)				#variable pourcentage of couple
		self.poppyPart_alert = {}			# dict contenant les parties du robot en surchauffe
		self.SEUIL_TEMP = 52					# seuil de temperature pour alerter
		self.SEUIL_TEMP_ARRET = 55			# seuil de temperature pour arreter le moteur
		self.SecurityStop = False
		#Ivalue=0					#variable intensite
		self.TIME_LIMIT = 10
		self.SEUIL_ANGLE = 5						# angle min de detection enregistrement et pour bouger
		self.SEUIL_ANGLE_MAX = 20				# angle max a l'initialisation de la pos avant mvt
		self.LIMITE_ANGLE = 40					# amplitude de mouvement : angle max de deplacement
		self.SEMI_MOU = list()					# liste des parties Poppy en mode semi-mou
		self.PLAYING_MOVE = False				# mouvement ou partie de mouvement en cours
		self.MOVING_ENABLE = False				# autorisation mouvement (False = stop mouvement)
		self.PLAYING_EXO = False				# exercice en cours ou non
		self.EXO_ENABLE = False					# autorise exercice (False = stop exercice)
		self.PLAYING_SEANCE = False				# seance en cours ou non
		self.EXO_SLEEP = False					# pause exercice
		self.PAUSE = False						# pause inter mouvement ou inter exercice
		self.EXO_TEMPS = 0					# compteur de temps pendant exercice ou seance
		self.EXO_TEMPS_LIMITE = 0				# valeur max de temps d'un exercice ou seance
		self.NUM_EXO = 0						# numero de l'exercice en cours
		self.NUM_MOV = 0						# numero du mouvement en cours
		self.SCANNING = 0					# en train de scanner les positions moteurs ou non
		#Face and eyes
		self.FACE_MANAGING_ENABLE = False 		# thread face managing
		self.DIRECTION_MANAGING_ON = False		# thread looking-direction active
		self.FaceState = 'happy'				# default state of Poppy eyes
		self.RestEyesDirection = 'center'		# eyes looking direction while not moving
		self.EyesDirection = self.RestEyesDirection		# eyes looking direction
		self.directionPoppypart = {}			# active poppyparts to determine direction
		# variables temporelles pour les logs
		self.year = int(time.strftime('%Y', time.localtime()))	#annee en cours
		self.month = int(time.strftime('%m', time.localtime()))	#mois en cours
		# communication avec la kinect
		self.kinectName = kinectName			# nom du serveur kinect
		self.waitKinect = False					# attente que la kinect soit prete
		self.waitFeedback = False				# attente que les feedbacks soient donnes
		self.REPET = False						# en cours de repetition d un exo par le robot
		self.WAIT_REPET = False					# attente fin repet

		self.t0 = time.time()
		if self.face!='none':
			self.startFaceManager()					# demarre thread face managing
		#ser=serial.Serial('/dev/ttyACM1', 9600)		#ouverture du port seriel pour mesure I
		#configuration logs
		self.logger = logging.getLogger('PoppyGRR_log')
		time.sleep(1)
		#primitives
		self.Poppyboid.attach_primitive(scanMotorsLoop(self), 'scan')
		self.Poppyboid.attach_primitive(positionPrimitive(self), 'scanPosition')
		self.Poppyboid.attach_primitive(positionPrimitive(self, 'debout'), 'initDebout')
		self.Poppyboid.attach_primitive(positionPrimitive(self, 'assis'), 'initAssis')
		self.Poppyboid.attach_primitive(positionPrimitive(self, 'chaise'), 'initChaise')

	def setSecurityMode(self):
		self.voice.play("./sound/sounds/securityMode.mp3")
		self.SecurityStop = True


	def scanResults(self):
		results = {}
		results["states"]={}
		results["states"]["face_managing_enable"]=self.FACE_MANAGING_ENABLE
		results["states"]["direction_managing_on"]=self.DIRECTION_MANAGING_ON
		results["states"]["playing_move"]=self.PLAYING_MOVE
		results["states"]["moving_enable"]=self.MOVING_ENABLE
		results["states"]["playing_exo"]=self.PLAYING_EXO
		results["states"]["exo_enable"]=self.EXO_ENABLE
		results["position"]={}
		results["voltage"]={}
		results["temperature"]={}
		results["couple"]={}
		results["temperature"]["max"]=0
		for imoteur in range(self.nbmoteurs):		
			#print"ID : ", idmoteur[imoteur], "\t", round(temps, 2), "s\tposition : ", position[imoteur], "\tvoltage : ", round(voltage[imoteur], 1), "\ttemperature : ", temperature[imoteur], "\tcouple : ", couple[imoteur]
			results["position"][self.idmoteur[imoteur]] = self.position[imoteur]
			results["voltage"][self.idmoteur[imoteur]] = round(self.voltage[imoteur], 1)
			results["temperature"][self.idmoteur[imoteur]] = round(self.temperature[imoteur], 1)
			results["couple"][self.idmoteur[imoteur]] = self.couple[imoteur]
			if round(self.temperature[imoteur], 1)>results["temperature"]["max"]:
				results["temperature"]["max"]=round(self.temperature[imoteur], 1)
		if "poppyPart_alert" in results:
			del results["poppyPart_alert"]
		results["poppyPart_alert"]=self.poppyPart_alert

		results[u'compliant'] = self.poppyCompliant()
		results[u'compliant'] = "u'"+str(results[u'compliant'] )+"'"
		results[u'compliantBG'] = "u'"+str(self.Poppyboid.l_arm_z.compliant)+"'"
		results[u'compliantBD'] = "u'"+str(self.Poppyboid.r_arm_z.compliant)+"'"
		results[u'compliantT'] = "u'"+str(self.Poppyboid.head_z.compliant)+"'"
		results[u'compliantJG'] = "u'"+str(self.Poppyboid.l_hip_z.compliant)+"'"
		results[u'compliantJD'] = "u'"+str(self.Poppyboid.r_hip_z.compliant)+"'"
		results[u'compliantCol'] = "u'"+str(self.Poppyboid.abs_z.compliant)+"'"

		if "tete" in self.SEMI_MOU:
			results[u'semiCompliantT']="u'True'"
		else:
			results[u'semiCompliantT']="u'False'"
		if "bras_gauche" in self.SEMI_MOU:
			results[u'semiCompliantBG']="u'True'"
		else:
			results[u'semiCompliantBG']="u'False'"
		if "bras_droit" in self.SEMI_MOU:
			results[u'semiCompliantBD']="u'True'"
		else:
			results[u'semiCompliantBD']="u'False'"
		if "colonne" in self.SEMI_MOU:
			results[u'semiCompliantCol']="u'True'"
		else:
			results[u'semiCompliantCol']="u'False'"
		if self.creature == "humanoid":
			if "jambe_gauche" in self.SEMI_MOU:
				results[u'semiCompliantJG']="u'True'"
			else:
				results[u'semiCompliantJG']="u'False'"
			if "jambe_droite" in self.SEMI_MOU:
				results[u'semiCompliantJD']="u'True'"
			else:
				results[u'semiCompliantJD']="u'False'"
		return results

	#FONCTIONS
	def Compliant(self, poppyParts='all'): 
		if poppyParts == 'all':
			while len(self.SEMI_MOU)>0:
				del self.SEMI_MOU[0]
			for m in self.Poppyboid.motors: 
				m.compliant = True
		else :
			if self.creature == "humanoid":
				if 'jambe_gauche' in poppyParts:
					if 'jambe_gauche' in self.SEMI_MOU:
						self.SEMI_MOU.remove("jambe_gauche")
					self.Poppyboid.l_hip_x.compliant = True
					self.Poppyboid.l_hip_z.compliant = True
					self.Poppyboid.l_hip_y.compliant = True
					self.Poppyboid.l_knee_y.compliant = True
					self.Poppyboid.l_ankle_y.compliant = True
				if 'jambe_droite' in poppyParts:
					if 'jambe_droite' in self.SEMI_MOU:
						self.SEMI_MOU.remove("jambe_droite")
					self.Poppyboid.r_hip_x.compliant = True
					self.Poppyboid.r_hip_z.compliant = True
					self.Poppyboid.r_hip_y.compliant = True
					self.Poppyboid.r_knee_y.compliant = True
					self.Poppyboid.r_ankle_y.compliant = True
			if 'bras_gauche' in poppyParts:
				if 'bras_gauche' in self.SEMI_MOU:
					self.SEMI_MOU.remove("bras_gauche")
				self.Poppyboid.l_shoulder_y.compliant = True
				self.Poppyboid.l_shoulder_x.compliant = True
				self.Poppyboid.l_arm_z.compliant = True
				self.Poppyboid.l_elbow_y.compliant = True
				if self.wrists:
					self.Poppyboid.l_wrist_z.compliant = True
					self.Poppyboid.l_wrist_x.compliant = True
			if 'bras_droit' in poppyParts:
				if 'bras_droit' in self.SEMI_MOU:
					self.SEMI_MOU.remove("bras_droit")
				self.Poppyboid.r_shoulder_y.compliant = True
				self.Poppyboid.r_shoulder_x.compliant = True
				self.Poppyboid.r_arm_z.compliant = True
				self.Poppyboid.r_elbow_y.compliant = True
				if self.wrists:
					self.Poppyboid.r_wrist_z.compliant = True
					self.Poppyboid.r_wrist_x.compliant = True
			if 'colonne' in poppyParts:
				if 'colonne' in self.SEMI_MOU:
					self.SEMI_MOU.remove("colonne")
				self.Poppyboid.abs_y.compliant = True
				self.Poppyboid.abs_x.compliant = True
				self.Poppyboid.abs_z.compliant = True
				self.Poppyboid.bust_y.compliant = True
				self.Poppyboid.bust_x.compliant = True
			if 'tete' in poppyParts:
				if 'tete' in self.SEMI_MOU:
					self.SEMI_MOU.remove("tete")
				self.Poppyboid.head_z.compliant = True
				self.Poppyboid.head_y.compliant = True

	def NonCompliant(self, poppyParts='all', torqueLimit = 100, notMoving = False): 
		sleep = 0
		if poppyParts == 'all':
			while len(self.SEMI_MOU)>0:
				del self.SEMI_MOU[0]
				sleep = 1
			for m in self.Poppyboid.motors: 
				m.torque_limit = torqueLimit
				m.compliant = False 
		else:
			poppyPartsCompliant = list()
			if self.creature == "humanoid":
				if 'jambe_gauche' in poppyParts:
					if 'jambe_gauche' in self.SEMI_MOU and torqueLimit==100:
						self.SEMI_MOU.remove("jambe_gauche")
						sleep=1
					self.Poppyboid.l_hip_x.torque_limit = torqueLimit
					self.Poppyboid.l_hip_x.compliant = False
					self.Poppyboid.l_hip_z.torque_limit = torqueLimit
					self.Poppyboid.l_hip_z.compliant = False
					self.Poppyboid.l_hip_y.torque_limit = torqueLimit
					self.Poppyboid.l_hip_y.compliant = False
					self.Poppyboid.l_knee_y.torque_limit = torqueLimit
					self.Poppyboid.l_knee_y.compliant = False
					self.Poppyboid.l_ankle_y.torque_limit = torqueLimit
					self.Poppyboid.l_ankle_y.compliant = False
				elif 'jambe_gauche' not in self.SEMI_MOU:
					poppyPartsCompliant.append('jambe_gauche')
				if 'jambe_droite' in poppyParts:
					if 'jambe_droite' in self.SEMI_MOU and torqueLimit==100:
						self.SEMI_MOU.remove("jambe_droite")
						sleep=1
					self.Poppyboid.r_hip_x.torque_limit = torqueLimit
					self.Poppyboid.r_hip_x.compliant = False
					self.Poppyboid.r_hip_z.torque_limit = torqueLimit
					self.Poppyboid.r_hip_z.compliant = False
					self.Poppyboid.r_hip_y.torque_limit = torqueLimit
					self.Poppyboid.r_hip_y.compliant = False
					self.Poppyboid.r_knee_y.torque_limit = torqueLimit
					self.Poppyboid.r_knee_y.compliant = False
					self.Poppyboid.r_ankle_y.torque_limit = torqueLimit
					self.Poppyboid.r_ankle_y.compliant = False
				elif 'jambe_droite' not in self.SEMI_MOU:
					poppyPartsCompliant.append('jambe_droite')
			if 'bras_gauche' in poppyParts:
				if 'bras_gauche' in self.SEMI_MOU and torqueLimit==100:
					self.SEMI_MOU.remove("bras_gauche")
					sleep=1
				self.Poppyboid.l_shoulder_y.torque_limit = torqueLimit
				self.Poppyboid.l_shoulder_y.compliant = False
				self.Poppyboid.l_shoulder_x.torque_limit = torqueLimit
				self.Poppyboid.l_shoulder_x.compliant = False
				self.Poppyboid.l_arm_z.torque_limit = torqueLimit
				self.Poppyboid.l_arm_z.compliant = False
				self.Poppyboid.l_elbow_y.torque_limit = torqueLimit
				self.Poppyboid.l_elbow_y.compliant = False
				if self.wrists:
					self.Poppyboid.l_wrist_z.torque_limit = torqueLimit
					self.Poppyboid.l_wrist_z.compliant = False
					self.Poppyboid.l_wrist_x.torque_limit = torqueLimit
					self.Poppyboid.l_wrist_x.compliant = False
			elif 'bras_gauche' not in self.SEMI_MOU:
				poppyPartsCompliant.append('bras_gauche')
			if 'bras_droit' in poppyParts:
				if 'bras_droit' in self.SEMI_MOU and torqueLimit==100:
					self.SEMI_MOU.remove("bras_droit")
					sleep=1
				self.Poppyboid.r_shoulder_y.torque_limit = torqueLimit
				self.Poppyboid.r_shoulder_y.compliant = False
				self.Poppyboid.r_shoulder_x.torque_limit = torqueLimit
				self.Poppyboid.r_shoulder_x.compliant = False
				self.Poppyboid.r_arm_z.torque_limit = torqueLimit
				self.Poppyboid.r_arm_z.compliant = False
				self.Poppyboid.r_elbow_y.torque_limit = torqueLimit
				self.Poppyboid.r_elbow_y.compliant = False
				if self.wrists:
					self.Poppyboid.r_wrist_z.torque_limit = torqueLimit
					self.Poppyboid.r_wrist_z.compliant = False
					self.Poppyboid.r_wrist_x.torque_limit = torqueLimit
					self.Poppyboid.r_wrist_x.compliant = False
			elif 'bras_droit' not in self.SEMI_MOU:
				poppyPartsCompliant.append('bras_droit')
			if 'colonne' in poppyParts:
				if 'colonne' in self.SEMI_MOU and torqueLimit==100:
					self.SEMI_MOU.remove("colonne")
					sleep=1
				self.Poppyboid.abs_y.torque_limit = torqueLimit
				self.Poppyboid.abs_y.compliant = False
				self.Poppyboid.abs_x.torque_limit = torqueLimit
				self.Poppyboid.abs_x.compliant = False
				self.Poppyboid.abs_z.torque_limit = torqueLimit
				self.Poppyboid.abs_z.compliant = False
				self.Poppyboid.bust_y.torque_limit = torqueLimit
				self.Poppyboid.bust_y.compliant = False
				self.Poppyboid.bust_x.torque_limit = torqueLimit
				self.Poppyboid.bust_x.compliant = False
			elif 'colonne' not in self.SEMI_MOU:
				poppyPartsCompliant.append('colonne')
			if 'tete' in poppyParts:
				if 'tete' in self.SEMI_MOU and torqueLimit==100:
					self.SEMI_MOU.remove("tete")
					sleep=1
				self.Poppyboid.head_z.torque_limit = torqueLimit
				self.Poppyboid.head_z.compliant = False
				self.Poppyboid.head_y.torque_limit = torqueLimit
				self.Poppyboid.head_y.compliant = False
			elif 'tete' not in self.SEMI_MOU:
				poppyPartsCompliant.append('tete')
			if notMoving == True:
				self.Compliant(poppyPartsCompliant)
		time.sleep(sleep)

	def semiCompliant(self, poppyParts='all'): 
		if len(self.SEMI_MOU)>0:
			self.NonCompliant(self.SEMI_MOU)
		while len(self.SEMI_MOU)>0:
			self.NonCompliant(self.SEMI_MOU)
			del self.SEMI_MOU[0]
		time.sleep(1)
		for i in range(len(poppyParts)):
			self.SEMI_MOU.append(poppyParts[i]) 
		print "semi_mou"+ str(self.SEMI_MOU)
		self.NonCompliant(poppyParts, torqueLimit = 1)
		semiCompliantPrimitive(self).start()

	def SavePosInit(self, namePos):
		#positionPrimitive(Poppyboid, namePos).start
		if namePos == 'debout':
			self.Poppyboid.initDebout.start()
		elif namePos == 'chaise':
			self.Poppyboid.initChaise.start()
		elif namePos == 'assis':
			self.Poppyboid.initAssis.start()
		time.sleep(1.5)
		self.voice.play("./sound/sounds/fait.mp3")

	def GoPosInit(self, namePos):
		print ('going to initial position')
		self.PLAYING_MOVE=True
		speed = {}
		speed["tete"] = 0.15
		speed["colonne"] = 0.15
		speed["bras_gauche"] = 0.15
		speed["bras_droit"] = 0.15
		if self.creature == "humanoid":
			speed["jambe_gauche"] = 0.15
			speed["jambe_droite"] = 0.15
		with open('./position/'+namePos+'.json', 'r') as f:
			    position = json.load(f)
		self.NonCompliant()
		time.sleep(0.5)
		self.goFirstPos(position, speed, 'True')
		time.sleep(0.5)
		self.PLAYING_MOVE=False

	def SaveMovePart(self, poppyParts, moveName, semiMou, playedMove = ''):
		if self.directory(moveName) != '':
			return 'move already exists'
		#Verification, si on joue mov en meme temps (playedMove), que pas de doublons PoppyParts
		if playedMove!= '':
			dir = self.directory(playedMove)
			if dir == '':
				return 'move to play '+playedMove+' does not exist'
			elif dir == 'exo' or dir == 'seance':
				return 'move to play '+playedMove+' is not a move'
			with open('./move/'+dir+'/'+playedMove+'.json', 'r') as f:
				moveToPlay = json.load(f)
			for i in range(len(poppyParts)):
				if poppyParts[i] in moveToPlay["speed"].keys():
					return poppyParts[i]+' is already in the move to play' 
		self.NonCompliant(poppyParts)
		time.sleep(0.5)
		self.voice.play("./sound/sounds/cestparti.mp3")
		time.sleep(0.5)
		if semiMou == 'True':
			self.semiCompliant(poppyParts)
		else:
			self.Compliant(poppyParts)
		saveMovePart = movePartPrimitive(self, poppyParts, moveName)
		saveMovePart.start()
		if playedMove != '' :
			self.GoMove(playedMove, save = True)
		saveMovePart.join()
		self.voice.play("./sound/sounds/fait.mp3")
		self.NonCompliant(poppyParts)
		self.majMoveList('mov', moveName, poppyParts)
		time.sleep(0.2)
		self.Compliant(poppyParts)
		#TODO : Rajouter un bruit sonore
		return 'move part saved'
		
		#mise a jour de la liste des fichiers mouvements
	def majMoveList(self, moveDir, moveName, poppyParts):
		with open('./move/movelist.json','r') as f:
			jsondata = json.load(f)
		if moveName not in jsondata["list_"+moveDir]:
			jsondata["nb_"+moveDir] += 1
		jsondata["list_"+moveDir][moveName] = poppyParts
		with open('./move/movelist.json','w') as f:
			json.dump(jsondata, f, indent=4)
		#self.voice.play("./sound/sounds/majmovelist.mp3")

	def rename(self, previousName, newName):
		moveDir = self.directory(previousName)
		if moveDir == '':
			if self.internet:
				self.voice.say(previousName+" n'existe pas.")
			else:
				self.voice.play("./sound/sounds/nexistepas.mp3")
			return previousName+' does not exist'
		if self.directory(newName) != '':
			if self.internet:
				self.voice.say(newName+" existe deja.")
			else:
				self.voice.play("./sound/sounds/existedeja.mp3")
			return newName+' already exists'
		previousFile = './move/'+moveDir+'/'+previousName+'.json'
		newFile = './move/'+moveDir+'/'+newName+'.json'
		os.rename(previousFile, newFile)	#MAJ fichier json

		with open('./move/movelist.json','r') as f:
			movelist = json.load(f)
		movelist["list_"+moveDir][newName]=movelist["list_"+moveDir][previousName]
		del movelist["list_"+moveDir][previousName]
		with open('./move/movelist.json','w') as f:
			json.dump(movelist, f, indent=4)
		self.voice.play("./sound/sounds/fait.mp3")
		return previousName+" renamed in "+newName

	def symetry(self, moveName):
		dir = self.directory(moveName)
		if dir == '':
			if self.internet:
				self.voice.say(moveName+" n'existe pas.")
			else:
				self.voice.play("./sound/sounds/nexistepas.mp3")
			return 'move file does not exist'
		if dir != 'mov':
			self.voice.play("./sound/sounds/notamove.mp3")
			return 'not a move'
		moveFile = './move/'+dir+'/'+moveName+'.json'
		symName = moveName+'Sym'
		symFile = './move/'+dir+'/'+symName+'.json'
		if self.directory(symName) != '':
			if self.internet:
				self.voice.say("la symetrie de "+moveName+" existe deja.")
			else:
				self.voice.play("./sound/sounds/existedeja.mp3")
			return 'symetry '+symName+' already exists'
		with open(moveFile, 'r') as f:
			moveData = json.load(f)
		symData = {}
		symData["nb_temps"] = moveData["nb_temps"]
		for nb_temps in range(moveData["nb_temps"]):
			if str(nb_temps+1) in moveData :
				symData[str(nb_temps+1)] = {}
				#bras gauche en bras droit
				if '41' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["51"] = moveData[str(nb_temps+1)]["41"]
				if '42' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["52"] = - moveData[str(nb_temps+1)]["42"]
				if '43' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["53"] = - moveData[str(nb_temps+1)]["43"]
				if '44' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["54"] = moveData[str(nb_temps+1)]["44"]
				if "45" in moveData[str(nb_temps+1)]:
					symData[str(nb_temps+1)]["55"] = moveData[str(nb_temps+1)]["45"]
				if '46' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["56"] = moveData[str(nb_temps+1)]["46"]
				#bras droit en bras gauche
				if '51' in moveData[str(nb_temps+1)] : 	
					symData[str(nb_temps+1)]["41"] = moveData[str(nb_temps+1)]["51"]
				if '52' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["42"] = - moveData[str(nb_temps+1)]["52"]
				if '53' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["43"] = - moveData[str(nb_temps+1)]["53"]
				if '54' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["44"] = moveData[str(nb_temps+1)]["54"]
				if "55" in moveData[str(nb_temps+1)]:
					symData[str(nb_temps+1)]["45"] = moveData[str(nb_temps+1)]["55"]
				if '56' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["46"] = moveData[str(nb_temps+1)]["56"]
				#jambe gauche en jambe droite
				if '11' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["21"] = - moveData[str(nb_temps+1)]["11"]
				if '12' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["22"] = - moveData[str(nb_temps+1)]["12"]
				if '13' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["23"] = moveData[str(nb_temps+1)]["13"]
				if '14' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["24"] = moveData[str(nb_temps+1)]["14"]
				if '15' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["25"] = moveData[str(nb_temps+1)]["15"]
				#jambe droite en jambe gauche
				if '21' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["11"] = - moveData[str(nb_temps+1)]["21"]
				if '22' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["12"] = - moveData[str(nb_temps+1)]["22"]
				if '23' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["13"] = moveData[str(nb_temps+1)]["23"]
				if '24' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["14"] = moveData[str(nb_temps+1)]["24"]
				if '25' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["15"] = moveData[str(nb_temps+1)]["25"]
				#colonne
				if '31' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["31"] = moveData[str(nb_temps+1)]["31"]
				if '32' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["32"] = - moveData[str(nb_temps+1)]["32"]
				if '33' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["33"] = - moveData[str(nb_temps+1)]["33"]
				if '34' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["34"] = moveData[str(nb_temps+1)]["34"]
				if '35' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["35"] = - moveData[str(nb_temps+1)]["35"]
				#tete
				if '36' in moveData[str(nb_temps+1)] :
					symData[str(nb_temps+1)]["36"] = - moveData[str(nb_temps+1)]["36"]
				if '37' in moveData[str(nb_temps+1)] :
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
		self.majMoveList(dir, symName, poppyParts)
		self.voice.play("./sound/sounds/fait.mp3")
		return dir
		
	def reverse(self, moveName):
		dir = self.directory(moveName)
		if dir == '':
			if self.internet:
				self.voice.say(moveName+" n'existe pas.")
			else:
				self.voice.play("./sound/sounds/nexistepas.mp3")
			return 'move file does not exist'
		if dir != 'mov':
			self.voice.play("./sound/sounds/notamove.mp3")
			return 'not a move'
		moveFile = './move/'+dir+'/'+moveName+'.json'
		revName = moveName+'Rev'
		revFile = './move/'+dir+'/'+revName+'.json'
		if self.directory(revName) != '':
			self.voice.play("./sound/sounds/existedeja.mp3")
			return 'reverse '+revName+' already exists'
		with open(moveFile, 'r') as f:
			moveData = json.load(f)
		revData = {}
		revData["nb_temps"] = moveData["nb_temps"]
		nb_tps_max = moveData["nb_temps"]
		for nb_temps in range(moveData["nb_temps"]):
			if str(nb_temps+1) in moveData :
				revData[str(nb_tps_max-nb_temps)] = {}
				#bras gauche
				if '41' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["41"] = moveData[str(nb_temps+1)]["41"]
				if '42' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["42"] = moveData[str(nb_temps+1)]["42"]
				if '43' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["43"] = moveData[str(nb_temps+1)]["43"]
				if '44' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["44"] = moveData[str(nb_temps+1)]["44"]
				if "45" in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["45"] = moveData[str(nb_temps+1)]["45"]
				if '46' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["46"] = moveData[str(nb_temps+1)]["46"]
				#bras droit
				if '51' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["51"] = moveData[str(nb_temps+1)]["51"]
				if '52' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["52"] = moveData[str(nb_temps+1)]["52"]
				if '53' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["53"] = moveData[str(nb_temps+1)]["53"]
				if '54' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["54"] = moveData[str(nb_temps+1)]["54"]
				if "55" in moveData[str(nb_temps+1)]:
					revData[str(nb_tps_max-nb_temps)]["55"] = moveData[str(nb_temps+1)]["55"]
				if '56' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["56"] = moveData[str(nb_temps+1)]["56"]
				#jambe gauche
				if '11' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["11"] = moveData[str(nb_temps+1)]["11"]
				if '12' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["12"] = moveData[str(nb_temps+1)]["12"]
				if '13' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["13"] = moveData[str(nb_temps+1)]["13"]
				if '14' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["14"] = moveData[str(nb_temps+1)]["14"]
				if '15' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["15"] = moveData[str(nb_temps+1)]["15"]
				#jambe droite
				if '21' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["21"] = moveData[str(nb_temps+1)]["21"]
				if '22' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["22"] = moveData[str(nb_temps+1)]["22"]
				if '23' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["23"] = moveData[str(nb_temps+1)]["23"]
				if '24' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["24"] = moveData[str(nb_temps+1)]["24"]
				if '25' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["25"] = moveData[str(nb_temps+1)]["25"]
				#colonne
				if '31' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["31"] = moveData[str(nb_temps+1)]["31"]
				if '32' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["32"] = moveData[str(nb_temps+1)]["32"]
				if '33' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["33"] = moveData[str(nb_temps+1)]["33"]
				if '34' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["34"] = moveData[str(nb_temps+1)]["34"]
				if '35' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["35"] = moveData[str(nb_temps+1)]["35"]
				#tete
				if '36' in moveData[str(nb_temps+1)] :
					revData[str(nb_tps_max-nb_temps)]["36"] = moveData[str(nb_temps+1)]["36"]
				if '37' in moveData[str(nb_temps+1)] :
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
		self.majMoveList(dir, revName, poppyParts)
		self.voice.play("./sound/sounds/fait.mp3")
		return dir

	def RemoveMove(self, moveName):
		remove = False
		#mise a jour de la liste des fichiers mouvements
		dir = self.directory(moveName)	#recupere le type de mouvement
		if dir != '':
			with open('./move/movelist.json',  'r') as f:
				movelist = json.load(f)
			nbInDir = 'nb_'+dir
			movelist[nbInDir] -= 1
			if dir == "exo":
				with open('./move/exo/'+moveName+'.json',  'r') as f:
					movefile = json.load(f)
				if "description" in movefile:
					for key, value in movefile["description"].iteritems():
						print key, value
						#self.voice.play('./sound/sounds/descriptions/'+value)
						os.remove('./sound/sounds/descriptions/'+value)
			os.remove('./move/'+dir+'/'+moveName+'.json')
			realDir = 'list_'+dir
			del movelist[realDir][moveName]
			remove = True
			if remove == True:
				with open('./move/movelist.json','w') as f:
					json.dump(movelist, f, indent=4)
				self.voice.play('./sound/sounds/fait.mp3')
		time.sleep(1)
		return remove

	#fonction mise en premiere position du mouvement
	def goFirstPos(self, position, speed, init = False):
			self.Poppyboid.scanPosition.start()
			time.sleep(0.1)
			while self.SCANNING == 1:
				time.sleep(0.05)
			if init == True:
				vitesse = 40
			else:
				vitesse = 80
			temps_attente = 0
			if init == 'True':
				seuil = 0
			else:
				seuil = self.SEUIL_ANGLE_MAX
			positionActu={} #Position de depart
			positionFin={} #Position a atteindre
			#charge un fichier Json - position courante
			with open('./position/currentPos.json', 'r') as f:
			    positionActu = json.load(f)
			
			positionFin = position
			print speed.keys()
			if "bras_droit" in speed.keys() and "51" in positionFin:
				if abs(positionFin["51"]-positionActu["51"])>seuil :
					v =  abs(positionFin["51"]-positionActu["51"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'r_shoulder_y':positionFin["51"]},v, wait=False)
				if abs(positionFin["52"]-positionActu["52"])>seuil :
					v = abs(positionFin["52"]-positionActu["52"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'r_shoulder_x':positionFin["52"]}, v, wait=False)
				if abs(positionFin["53"]-positionActu["53"])>seuil :
					v =abs(positionFin["53"]-positionActu["53"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'r_arm_z':positionFin["53"]}, v, wait=False)
				if abs(positionFin["54"]-positionActu["54"])>seuil :
					v = abs(positionFin["54"]-positionActu["54"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'r_elbow_y': positionFin["54"]}, v, wait=False)
				if "55" in positionFin and self.wrists:
					if abs(positionFin["55"]-positionActu["55"])>seuil :
						v = abs(positionFin["55"]-positionActu["55"])/vitesse
						if v > temps_attente:
							temps_attente = v
						self.Poppyboid.goto_position({'r_wrist_z': positionFin["55"]}, v, wait=False)
					if abs(positionFin["56"]-positionActu["56"])>seuil :
						v = abs(positionFin["56"]-positionActu["56"])/vitesse
						if v > temps_attente:
							temps_attente = v
						self.Poppyboid.goto_position({'r_wrist_x': positionFin["56"]}, v, wait=False)
			if "bras_gauche" in speed.keys() and "41" in positionFin:
				if abs(positionFin["41"]-positionActu["41"])>seuil :
					v = abs(positionFin["41"]-positionActu["41"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'l_shoulder_y':positionFin["41"]}, v, wait=False)
				if abs(positionFin["42"]-positionActu["42"])>seuil:
					v = abs(positionFin["42"]-positionActu["42"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'l_shoulder_x':positionFin["42"]}, v, wait=False)
				if abs(positionFin["43"]-positionActu["43"])>seuil :
					v = abs(positionFin["43"]-positionActu["43"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'l_arm_z':positionFin["43"]}, v, wait=False)
				if abs(positionFin["44"]-positionActu["44"])>seuil :
					v = abs(positionFin["44"]-positionActu["44"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'l_elbow_y': positionFin["44"]}, v, wait=False)
				if "45" in positionFin and self.wrists:
					if abs(positionFin["45"]-positionActu["45"])>seuil :
						v = abs(positionFin["45"]-positionActu["45"])/vitesse
						if v > temps_attente:
							temps_attente = v
						self.Poppyboid.goto_position({'l_wrist_z': positionFin["45"]}, v, wait=False)
					if abs(positionFin["46"]-positionActu["46"])>seuil :
						v = abs(positionFin["46"]-positionActu["46"])/vitesse
						if v > temps_attente:
							temps_attente = v
						self.Poppyboid.goto_position({'l_wrist_x': positionFin["46"]}, v, wait=False)
			if "colonne" in speed.keys() and "31" in positionFin:
				if abs(positionFin["31"]-positionActu["31"])>seuil :
					v = abs(positionFin["31"]-positionActu["31"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'abs_y':positionFin["31"]}, v, wait=False)
				if abs(positionFin["32"]-positionActu["32"])>seuil :
					v = abs(positionFin["32"]-positionActu["32"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'abs_x':positionFin["32"]}, v, wait=False)
				if abs(positionFin["33"]-positionActu["33"])>seuil :
					v = abs(positionFin["33"]-positionActu["33"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'abs_z':positionFin["33"]},v, wait=False)
				if abs(positionFin["34"]-positionActu["34"])>seuil :
					v = abs(positionFin["34"]-positionActu["34"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'bust_y':positionFin["34"]}, v, wait=False)
				if abs(positionFin["35"]-positionActu["35"])>seuil :
					v =  abs(positionFin["35"]-positionActu["35"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'bust_x':positionFin["35"]},v, wait=False)
			if "tete" in speed.keys() and "36" in positionFin:
				if abs(positionFin["36"]-positionActu["36"])>seuil :
					v = abs(positionFin["36"]-positionActu["36"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'head_z':positionFin["36"]},v , wait=False)
				if abs(positionFin["37"]-positionActu["37"])>seuil :
					v = abs(positionFin["37"]-positionActu["37"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'head_y':positionFin["37"]}, v, wait=False)
			time.sleep(temps_attente/4.0)
			if "jambe_gauche" in speed.keys() and "11" in positionFin and self.creature == "humanoid":
				if abs(positionFin["11"]-positionActu["11"])>seuil :
					v = abs(positionFin["11"]-positionActu["11"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'l_hip_x':positionFin["11"]}, v, wait=False)
				if abs(positionFin["12"]-positionActu["12"])>seuil :
					v = abs(positionFin["12"]-positionActu["12"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'l_hip_z':positionFin["12"]}, v, wait=False)
				if abs(positionFin["13"]-positionActu["13"])>seuil :
					v = abs(positionFin["13"]-positionActu["13"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'l_hip_y':positionFin["13"]}, v, wait=False)
				if abs(positionFin["14"]-positionActu["14"])>seuil :
					v = abs(positionFin["14"]-positionActu["14"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'l_knee_y': positionFin["14"]}, v, wait=False)
				if abs(positionFin["15"]-positionActu["15"])>seuil :
					v = abs(positionFin["15"]-positionActu["15"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'l_ankle_y':positionFin["15"]}, v, wait=False)
			if "jambe_droite" in speed.keys() and "21" in positionFin and self.creature == "humanoid":
				if abs(positionFin["21"]-positionActu["21"])>seuil :
					v = abs(positionFin["21"]-positionActu["21"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'r_hip_x':positionFin["21"]}, v, wait=False)
				if abs(positionFin["22"]-positionActu["22"])>seuil :
					v =  abs(positionFin["22"]-positionActu["22"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'r_hip_z':positionFin["22"]},v, wait=False)
				if abs(positionFin["23"]-positionActu["23"])>seuil :
					v = abs(positionFin["23"]-positionActu["23"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'r_hip_y': positionFin["23"]}, v, wait=False)
				if abs(positionFin["24"]-positionActu["24"])>seuil :
					v = abs(positionFin["24"]-positionActu["24"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'r_knee_y':positionFin["24"]}, v, wait=False)
				if abs(positionFin["25"]-positionActu["25"])>seuil :
					v = abs(positionFin["25"]-positionActu["25"])/vitesse
					if v > temps_attente:
						temps_attente = v
					self.Poppyboid.goto_position({'r_ankle_y':positionFin["25"]}, v, wait=False)
			print "waiting "+str(temps_attente)+"s"
			time.sleep(temps_attente)

	def GoMove(self, moveName, speed=5, rev=False, save=False, poppyParts='', description=''):
		print "GoMove - movename : "+moveName
		if self.SecurityStop == True:
			self.voice.play('./sounds/securityModeError.mp3')
			return "Security mode"
		self.EXO_SLEEP = False
		self.MOVING_ENABLE = True
		if len(poppyParts) == 0:
			poppyParts = list()
			poppyParts.append("tete")
			poppyParts.append("bras_droit")
			poppyParts.append("bras_gauche")
			if self.creature == "humanoid":
				poppyParts.append("jambe_gauche")
				poppyParts.append("jambe_droite")
			poppyParts.append("colonne")
		moveType = self.directory(moveName)
		if int(speed)>10:
			speed=10
		elif int(speed) <1:
			speed = 1
		if moveType == '':
			if internet:
				self.voice.say("Le fichier "+moveName+" n'existe pas")
			else:
				self.voice.play("./sound/sounds/nexistepas.mp3")
			return 'move file does not exist'
		elif moveType == 'exo' or moveType == 'seance':
			self.voice.play("./sound/sounds/movetypeError.mp3")
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
				self.NonCompliant(speedList, 25)
			else:
				self.NonCompliant(speedList)
			if self.PLAYING_EXO==False:		#juste un mouvement en lecture
				while self.PLAYING_MOVE:
					time.sleep(0.1)
				done = goMovePrimitive(self, rev, moveType, moveName, speedDict, tempsboucle, startTime, endTime).start()
				time.sleep(0.05)
			else:
				done = self.goMoveFunction(rev, moveType, moveName, speedDict, tempsboucle, startTime, endTime, description)
				time.sleep(0.05)
		if done == "stop":
			return done
		return 'Move has started'

	def goMoveFunction(self, rev, moveType, moveName, speedDict, tempsboucle, startTime, endTime, description):
		print "verif si playing move"
		print description
		startTime=int(startTime)
		endTime=int(endTime)
		if description == '':
			description={}
		while self.PLAYING_MOVE:
			time.sleep(0.1)
		self.PLAYING_MOVE=True
		self.directionPoppypart = speedDict
		if self.FACE_MANAGING_ENABLE and not self.DIRECTION_MANAGING_ON:
			self.DIRECTION_MANAGING_ON = True
			self.directionTh = Thread(target=self.setDirectionEyes)
			self.directionTh.start()
		print "startTime : "+str(startTime)+", endTime : "+str(endTime)
		with open('./move/'+moveType+'/'+moveName+'.json', 'r') as f:
			moveFile = json.load(f)
		if rev == False:
			for temps in range(startTime, endTime):
				while self.EXO_SLEEP == True and self.MOVING_ENABLE == True:
					time.sleep(0.1)
				if self.MOVING_ENABLE == False:
					self.PLAYING_MOVE = False
					print "---stop move 1 "+moveName+" ---"
					self.logger.warning("stop move 1 "+moveName)
					return "stop"
				#VOIX
				if "offset" in description.keys():
					if str(self.EXO_TEMPS-description["offset"]) in description.keys():
						self.NUM_PHASE+=1
						print description[str(self.EXO_TEMPS-description["offset"])]
						sayDescriptionTh = Thread(target=self.sayDescription, args=(self.NUM_PHASE, description[str(self.EXO_TEMPS-description["offset"])]))
						sayDescriptionTh.start()
				if temps+1 == 1:
					self.goFirstPos(moveFile[str(temps+1)], moveFile["speed"])
				else:
					if str(temps+1) in moveFile:
						miseEnPosPrimitive(self,moveFile[str(temps+1)], speedDict).start()
					if self.MOVING_ENABLE == False:
						self.PLAYING_MOVE = False
						print "---stop move 2---"
						self.logger.warning("stop move 2")
						return "stop"
					time.sleep(tempsboucle)
					if self.MOVING_ENABLE == False:
						self.PLAYING_MOVE = False
						print "---stop move 3---"
						self.logger.warning("stop move 3")
						return "stop"
				self.EXO_TEMPS += 1
		else:
			return "stop" 	#TODO : lecture non geree a l'envers !!!
			for temps in range(moveFile["nb_temps"]):
				while self.EXO_SLEEP == True and self.MOVING_ENABLE == True:
					time.sleep(0.5)
				if self.MOVING_ENABLE == False:
					self.PLAYING_MOVE = False
					return "stop"
				if temps+1 == 1:
					self.goFirstPos(moveFile[str(moveFile["nb_temps"]-temps)], moveFile["speed"])
				else:
					if str(moveFile["nb_temps"]-temps) in moveFile:
						miseEnPosPrimitive(self,moveFile[str(moveFile["nb_temps"]-temps)], speedDict).start()
					if self.MOVING_ENABLE == False:
						self.PLAYING_MOVE = False
						return "stop"
					time.sleep(tempsboucle)
					if self.MOVING_ENABLE == False:
						self.PLAYING_MOVE = False
						print "---stop move 3---"
						return "stop"
				self.EXO_TEMPS += 1
		self.PLAYING_MOVE = False
		if endTime == moveFile["nb_temps"]:
			print "MOVING_ENABLE = False "+moveName
			self.logger.warning("MOVING_ENABLE = False "+moveName)
			self.MOVING_ENABLE = False

	def sayDescription(self, num_phase, descriptionFile):
		if self.kinectName!='none':
			self.voice.play("./sound/sounds/feedbacks/segment"+str(num_phase)+".mp3")
			self.waitVoice()
		self.voice.play("./sound/sounds/descriptions/"+descriptionFile)

	def sayEndKinectObserv(self):
		self.voice.play("./sound/sounds/sayEndKinectObserv1.mp3")
		return "ended"

	def GoExo(self, exoName):
		if self.SecurityStop == True:
			return "Security mode"
		#time.sleep(0.5)	#le temps que la seance precedente se finnisse si existante
		self.PLAYING_EXO = False
		self.EXO_ENABLE = True
		self.EXO_SLEEP = False
		self.EXO_TEMPS = 0
		self.NUM_EXO = 0
		self.NUM_MOV = 0
		self.NUM_PHASE = 0
		exoType = self.directory(exoName)
		if exoType == '':
			if internet:
				self.voice.say("Le fichier "+exoName+" n'existe pas")
			else:
				self.voice.play("./sound/sounds/nexistepas.mp3")	
			return exoName + ' does not exist'
		elif exoType == 'mov':
			return 'not an exercice or a seance !'
		print ('preparing the file')
		with open('./move/'+exoType+'/'+exoName+'.json', 'r') as f:
			moveFile = json.load(f)
		#tous les fichiers existent ?
		for i in range(int(moveFile['nb_fichiers'])):
			if self.directory(moveFile['fichier'+str(i+1)]['namefile']) == '':
				if internet:
					self.voice.say("Le fichier "+moveFile['fichier'+str(i+1)]['namefile']+" n'existe pas")
				else:
					self.voice.play("./sound/sounds/nexistepas.mp3")
				return moveFile['fichier'+str(i+1)]['namefile'] + " is missing !"
			elif self.directory(moveFile['fichier'+str(i+1)]['namefile']) == 'exo':
				with open('./move/exo/'+moveFile['fichier'+str(i+1)]['namefile']+'.json', 'r') as f:
					exoFile = json.load(f)
				for j in range(exoFile['nb_fichiers']):
					if self.directory(exoFile['fichier'+str(j+1)]['namefile']) == '':
						if internet:
							self.voice.say("Le fichier "+exoFile['fichier'+str(j+1)]['namefile']+" n'existe pas")
						else:
							self.voice.play("./sound/sounds/nexistepas.mp3")
						return exoFile['fichier'+str(j+1)]['namefile'] + " in "+moveFile['fichier'+str(i+1)]['namefile'] +" is missing !"
		self.EXO_TEMPS_LIMITE = moveFile['nb_temps']
		goexosuite = Thread(target=self.GoExoSuite, args=(exoType, exoName))
		goexosuite.start()
		return 'Exercice has started'

	def GoExoSuite(self, exoType, exoName):		
		#communication kinect si exo
		if self.kinectName != "none" and exoType == 'exo':
			self.waitKinect = True
			print "give exoname : "+exoName+" to "+self.kinectName
			kinect = requests.post("http://"+self.kinectName+".local:4567/?Submit=give+exoname&exoname="+exoName)
			if kinect.status_code==200:
				print "attention, la kinect ne connait pas l'exercice !"
				self.logger.warning("kinect does not know the exercise !")
			elif kinect.status_code==201:
				print "kinect ok pour nom exo"
			while self.waitKinect:
				time.sleep(0.5)
		goExoPrimitive(self,exoName, exoType).start()
		time.sleep(1)

	def StopExo(self):
		while self.PAUSE == True:		#si on est en pause inter-exo ou inter-mouvements
			time.sleep(0.2)
	#	if self.kinectName != "none":
	#		print "kinectName : "+self.kinectName
	#		kinect = requests.post("http://"+self.kinectName+".local:4567/?Submit=start+kinect")
		if self.PLAYING_EXO == True:
			self.EXO_ENABLE = False
			self.MOVING_ENABLE = False
			self.PLAYING_EXO = False
			self.PLAYING_MOVE = False
			self.PLAYING_SEANCE = False
			return 'exercice stopped'
		elif self.PLAYING_MOVE == True:
			self.EXO_ENABLE = False
			self.MOVING_ENABLE = False
			self.PLAYING_EXO = False
			self.PLAYING_MOVE = False
			self.PLAYING_SEANCE = False
			return 'movement stopped'
		else:
			self.EXO_ENABLE = False
			self.MOVING_ENABLE = False
			self.PLAYING_EXO = False
			self.PLAYING_MOVE = False
			self.PLAYING_SEANCE = False
			return 'no exercice or movement is running'

	def PauseExo(self):
		if self.EXO_SLEEP == False:
		#	if self.kinectName != "none":
		#		kinect = requests.post("http://"+self.kinectName+".local:8080/?Submit=pause+kinect")
			self.EXO_SLEEP = True
			return 'move paused'
		else:
			return 'no exercice is running'

	def ResumeExo(self):
		print "resume exo"
		if self.EXO_SLEEP == True and self.EXO_ENABLE == True:
		#	if self.kinectName != "none":
		#		kinect = requests.post("http://"+self.kinectName+".local:8080/?Submit=resume+kinect")
			self.EXO_SLEEP = False
			return 'exercice resumed'
		elif self.EXO_SLEEP == True and self.MOVING_ENABLE == True:
			self.EXO_SLEEP = False
			return 'move resumed'
		else:
			return 'no exercice or movement in pause'

	def verifFinExo(self):
		verif = {}
		if self.EXO_SLEEP == True :
			verif["state"] = "pause"
		else:
			verif["state"] = "playing"
		if self.EXO_ENABLE == False :
			verif["info"]= "end"
		else:
			verif["info"]= "moving " + str(self.EXO_TEMPS)+"/"+str(self.EXO_TEMPS_LIMITE)
		verif["num_exo"]=str(self.NUM_EXO)
		verif["num_mov"]=str(self.NUM_MOV)
		return verif

	def verifFinMov(self):
		if self.MOVING_ENABLE == False :
			return "end"
		else:
			return "moving"

	def mesure(self):
		self.Poppyboid.scan.start()

	def readConfig(self, moveConfig, movename=''):
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
			dir = self.directory(shortnamefile)
			if dir == '':						# chaque partie existe ?
				if self.internet:
					self.voice.say(shortnamefile+" n'existe pas.")
				else:
					if internet:
						self.voice.say("Le fichier "+shortnamefile+" n'existe pas")
					else:
						self.voice.play("./sound/sounds/nexistepas.mp3")
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
									self.voice.play("./sound/sounds/samepoppypart.mp3")
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
					succeed = self.readConfig(moveConfig2, exoname)
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
				
		#voix si exo
		if moveDir == "exo":
			volumeTmp = self.voice.volume
			self.voice.setVolume(0)
			tmpDesc={}
			for key, value in moveConfig["description"].iteritems():
				if value!="":
					self.voice.say(value, "./sound/sounds/descriptions/"+movename+"_"+str(key)+".mp3", False)
					tmpDesc[key]=movename+"_"+str(key)+".mp3"
			moveConfig["description"]=tmpDesc
			self.voice.setVolume(volumeTmp)
	
		if moveDir == "exo" or moveDir == "seance":	# si on cree un exo ou une seance
			moveConfig["nb_temps"] = nb_temps_max
			with open(moveName, 'w') as f:
				json.dump(moveConfig, f, indent=4)	
		else:									# si pas exo ou seance
			moveFile["parties"]["offsetPart1"]["min"]=0			# premier offset = 0
			with open(moveName, 'w') as f:
				json.dump(moveFile, f, indent=4)
	
		self.majMoveList(moveDir, movename, poppyParts)
		self.voice.play("./sound/sounds/fait.mp3")
		if moveDir == 'exo':
			return "exercice created"
		elif moveDir == 'seance':
			return "seance created"
		else:
			return "move created"

	def addMove(self, moveName, moveType, moveFile):
		moveFile = json.loads(moveFile)
		print type(moveFile)
		moveDir = self.directory(moveName)
		if moveDir != '':
			return moveName+" already exists"
		moveFile["nb_temps"]=int(moveFile["nb_temps"])
		if moveType == "mov":
			self.logger.info("suppr les guillemets")
			for key, value in moveFile["speed"].iteritems():
				self.logger.info("speed "+str(key)+" - "+str(value))
				moveFile["speed"][key]=float(value)
			for key, value in moveFile.iteritems():
				if key!="speed" and key!="nb_temps" and key!="poppyParts":
					self.logger.info(key)
					for key2, value2 in moveFile[key].iteritems():
						moveFile[key][key2]=float(value2)
		else:
			moveFile["nb_fichiers"]=int(moveFile["nb_fichiers"])
			for iter in range(moveFile["nb_fichiers"]):
				moveFile["fichier"+str(iter+1)]["pause"]=int(moveFile["fichier"+str(iter+1)]["pause"])
				if moveType == "exo":
					moveFile["fichier"+str(iter+1)]["vitesse"]=int(moveFile["fichier"+str(iter+1)]["vitesse"])
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
		self.majMoveList(moveType, moveName, poppyParts)
		return moveName+" added"
		
	def directory(self, moveName):
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

	def readExoCompo(self, exoName):
		exoDir = self.directory(exoName)
		exoCompo = {}
		exoCompo['nom'] = exoName
		with open('./move/'+exoDir+'/'+exoName+'.json', 'r') as f:
			exoConfig=json.load(f)
		exoCompo['nb_fichiers'] = exoConfig['nb_fichiers']
		for i in range(int(exoConfig["nb_fichiers"])):		#on deroule tous les fichiers de la liste
			if self.directory(exoConfig['fichier'+str(i+1)]['namefile']) == 'exo' : # si c'est un exo
				exoCompo[str(i+1)] = {}
				exoCompo[str(i+1)] = self.readExoCompo(exoConfig['fichier'+str(i+1)]['namefile'])
			else:								#si c'est un mouvement
				exoCompo[str(i+1)] = exoConfig['fichier'+str(i+1)]['namefile']
		return exoCompo
			
	def loadData(self, moveName, BDD):
		dir = self.directory(moveName)
		jsondata={}
		if moveName == 'movelist':
			moveName = './move/'+moveName+'.json'
		elif dir == '':
			if self.internet:
				self.voice.say(moveName+" n'existe pas")
			else:
				self.voice.play("./sound/sounds/nexistepas.mp3")
			return 'does not exist'
		elif (dir == 'exo' or dir == 'seance') and BDD == "false":
			jsondata = self.readExoCompo(moveName)
			return jsondata
		else:
			moveName='./move/'+dir+'/'+moveName+'.json'
		
		with open(moveName, 'r') as f:
			jsondata=json.load(f)
		if moveName == './move/movelist.json':
			jsondata[u'compliant'] = self.poppyCompliant()
			jsondata[u'compliant'] = "u'"+str(jsondata[u'compliant'] )+"'"
			jsondata[u'compliantBG'] = "u'"+str(self.Poppyboid.l_arm_z.compliant)+"'"
			jsondata[u'compliantBD'] = "u'"+str(self.Poppyboid.r_arm_z.compliant)+"'"
			jsondata[u'compliantT'] = "u'"+str(self.Poppyboid.head_z.compliant)+"'"
			jsondata[u'compliantJG'] = "u'"+str(self.Poppyboid.l_hip_z.compliant)+"'"
			jsondata[u'compliantJD'] = "u'"+str(self.Poppyboid.r_hip_z.compliant)+"'"
			jsondata[u'compliantCol'] = "u'"+str(self.Poppyboid.abs_z.compliant)+"'"
			if "tete" in self.SEMI_MOU:
				jsondata[u'semiCompliantT']="u'True'"
			else:
				jsondata[u'semiCompliantT']="u'False'"
			if "bras_gauche" in self.SEMI_MOU:
				jsondata[u'semiCompliantBG']="u'True'"
			else:
				jsondata[u'semiCompliantBG']="u'False'"
			if "bras_droit" in self.SEMI_MOU:
				jsondata[u'semiCompliantBD']="u'True'"
			else:
				jsondata[u'semiCompliantBD']="u'False'"
			if "colonne" in self.SEMI_MOU:
				jsondata[u'semiCompliantCol']="u'True'"
			else:
				jsondata[u'semiCompliantCol']="u'False'"
			if "jambe_gauche" in self.SEMI_MOU:
				jsondata[u'semiCompliantJG']="u'True'"
			else:
				jsondata[u'semiCompliantJG']="u'False'"
			if "jambe_droite" in self.SEMI_MOU:
				jsondata[u'semiCompliantJD']="u'True'"
			else:
				jsondata[u'semiCompliantJD']="u'False'"
		return jsondata

	def poppyCompliant(self):
	#	if len(Poppyboid.compliant) == 25:
	#		return True
		if self.Poppyboid.l_arm_z.compliant == False:
			return False
		if self.Poppyboid.r_arm_z.compliant == False:
			return False
		if self.Poppyboid.head_z.compliant == False:
			return False
		if self.creature == "humanoid":
			if self.Poppyboid.l_hip_z.compliant == False:
				return False
			if self.Poppyboid.r_hip_z.compliant == False:
				return False
		if self.Poppyboid.abs_z.compliant == False:
			return False
		return True

	def kinectReady(self):
		if self.waitKinect:
			self.waitKinect=False
			print "kinect exercise resumed"
			return "resumed"
		else:
			print "self.waitKinect : "+str(self.waitKinect)
			return "failed"

	def kinectFeedback(self, kiFeedback):
		nbSegs = kiFeedback["globalSequence"]["nbSegs"]
		print "nombres de parties " +str(nbSegs)
		feedback = {}
		feedback["globalSequence"]=kiFeedback["globalSequence"]

		if kiFeedback["globalSequence"]["global"]>=self.SEUIL_BIEN:
			feedback["globalSequence"]["global"]="bien"
		elif kiFeedback["globalSequence"]["global"]>=self.SEUIL_NUL:
			feedback["globalSequence"]["global"]="moyen"
		elif kiFeedback["globalSequence"]["global"]>=self.SEUIL_MINABLE:
			feedback["globalSequence"]["global"]="nul"
		else:
			feedback["globalSequence"]["global"]="minable"

		for i in range(nbSegs):
			if kiFeedback["segment"+str(i+1)]["global"]<self.SEUIL_NUL:
				feedback["segment"+str(i+1)]={}
				feedback["segment"+str(i+1)]["global"]="nul"
			elif kiFeedback["segment"+str(i+1)]["global"]<self.SEUIL_BIEN:
				feedback["segment"+str(i+1)]={}
				minPart={}
				minPart["part"]="leftArm"
				minPart["value"]=kiFeedback["segment"+str(i+1)]["leftArm"]
				for part in ["leftArm", "rightArm", "leftLeg", "rightLeg", "spine"]:
					if kiFeedback["segment"+str(i+1)][part]<self.SEUIL_NUL:
						feedback["segment"+str(i+1)][part]="nul"	
					if kiFeedback["segment"+str(i+1)][part]<minPart["value"]:
						minPart["part"]=part
						minPart["value"]=kiFeedback["segment"+str(i+1)][part]

				if minPart["value"]>=self.SEUIL_NUL:
					feedback["segment"+str(i+1)][minPart["part"]]="moyen"

		print feedback
		while self.REPET:
			time.sleep(0.3)
		self.sayFeedback(feedback)
		return "ok"

	def sayFeedback(self, feedback):
		self.voice.play("./sound/sounds/feedbacks/"+feedback["globalSequence"]["global"]+".mp3")
		self.waitVoice()
		if feedback["globalSequence"]["global"]!="minable":
			for i in range(feedback["globalSequence"]["nbSegs"]):
			#for key, value in feedback.iteritems():
				key = "segment"+str(i+1)
				#if key != "globalSequence":
				if key in feedback.keys():
					print key
					self.voice.play("./sound/sounds/feedbacks/phase.mp3")
					self.waitVoice()
					self.voice.play("./sound/sounds/feedbacks/"+key+".mp3")
					self.waitVoice()
					time.sleep(0.2)
					if "global" in feedback[key]:
						self.voice.play("./sound/sounds/feedbacks/moveNul.mp3")
						self.waitVoice()
					elif "moyen" in feedback[key].values():
						self.voice.play("./sound/sounds/feedbacks/partDebut.mp3")
						self.waitVoice()
						self.voice.play("./sound/sounds/feedbacks/"+feedback[key].keys()[0]+".mp3")
						self.waitVoice()
						self.voice.play("./sound/sounds/feedbacks/partMoyen.mp3")
						self.waitVoice()
					else:
						self.voice.play("./sound/sounds/feedbacks/partDebut.mp3")
						self.waitVoice()
						for part, value in feedback[key].iteritems():
							print part, value
							self.voice.play("./sound/sounds/feedbacks/"+part+".mp3")
							self.waitVoice()
						self.voice.play("./sound/sounds/feedbacks/partNul.mp3")
						self.waitVoice()
				time.sleep(0.5)
		self.waitFeedback=False

	def waitVoice(self):
		while pygame.mixer.music.get_busy():
			time.sleep(0.1)

	def kinectEnd(self):
		resumed = self.ResumeExo()
		if "resumed" in resumed:
			print "ended"
			return "ended"
		else:
			return resumed

	def say(self, sentence):
		sentence = json.loads(sentence)
		print sentence["data"]
		self.voice.say(sentence["data"])
		print "sentence said"
		return "ok"

	def giveIP(self):
		IPaddress = ([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
		return IPaddress

	def send_logs(self, previous = False):
		if previous == True:
			if month == 1:
				realMonth = 12
				realYear = year-1
			else:
				realMonth = month-1
				realYear = year
		else:
			realMonth = month
			realYear = year
		f = open("log/logs_"+str(realYear)+'-'+str(realMonth)+".tar.gz", 'rb')
		logs = f.read()
		f.close()
		return logs

	def compress_log(self):
		nb_logs = 0
		for element in os.listdir('log/'):					#pour chaque fichier/dossier
			if os.path.isdir('log/'+element):						#si c'est un dossier
				if element != ('logs_'+str(self.year)+'-'+str(self.month)):	#si c'est pas les logs en cours
					try:
						self.make_tarfile("log/"+element+".tar.gz", "log/"+element)
						shutil.rmtree("log/"+element)				#supprime le dossier logs compresse
						nb_logs +=1
					except:
						return "error compressing logs : "+element
				else:												#si c'est les logs en cours
						if element+".tar.gz" in os.listdir('log/'):	#si les logs en cours existent en compresse
							os.remove("log/"+element+".tar.gz")	# supprime
						try:
							self.make_tarfile("log/"+element+".tar.gz", "log/"+element)	#met a jour le compresse
							nb_logs +=1
						except:
							return "error compressing logs : "+element

		if nb_logs==0:
			return "no logs compressed"
		else:
			print str(nb_logs)+" logs compressed"
			return str(nb_logs)+" logs compressed"

	def make_tarfile(self, output_filename, source_dir):
		with tarfile.open(output_filename, "w:gz") as tar:
			tar.add(source_dir, arcname=os.path.basename(source_dir))

	def setDirectionEyes(self):
		#gives the global direction of the poppyParts for the eyes
		while self.PLAYING_MOVE and self.FACE_MANAGING_ENABLE:
			if self.EXO_SLEEP:
				self.EyesDirection = "center"
			elif "bras_gauche" in self.directionPoppypart and "bras_droit" not in self.directionPoppypart:
				if self.Poppyboid.l_shoulder_y.present_position<-120 or self.Poppyboid.l_shoulder_x.present_position>120:
					self.EyesDirection = "topright"
				else:
					self.EyesDirection = "right"
			elif "bras_droit" in self.directionPoppypart and "bras_gauche" not in self.directionPoppypart:
				if self.Poppyboid.r_shoulder_y.present_position<-120 or self.Poppyboid.r_shoulder_x.present_position<-120:
					self.EyesDirection = "topleft"
				else:
					self.EyesDirection = "left"
			elif "jambe_gauche" in self.directionPoppypart and "jambe_droite" not in self.directionPoppypart:
				self.EyesDirection = "bottomright"
			elif "jambe_droite" in self.directionPoppypart and "jambe_gauche" not in self.directionPoppypart:
				self.EyesDirection = "bottomleft"
			elif "jambe_gauche" in self.directionPoppypart and "jambe_droite" in self.directionPoppypart:
				self.EyesDirection = "bottom"
			else:
				if self.Poppyboid.l_shoulder_y.present_position<-120 or self.Poppyboid.l_shoulder_x.present_position>120:
					if self.Poppyboid.r_shoulder_y.present_position<-120 or self.Poppyboid.r_shoulder_x.present_position<-120:
						self.EyesDirection = "top"
					else:
						self.EyesDirection = "topright"
				elif self.Poppyboid.r_shoulder_y.present_position<-120 or self.Poppyboid.r_shoulder_x.present_position<-120:
					self.EyesDirection = "topleft"
				else:
					self.EyesDirection = "center"
			time.sleep(0.5)
		self.DIRECTION_MANAGING_ON = False
		print "fin du thread direction"

	def setVolume(self, volume):
		if float(volume)<0:
			return "error"
		self.voice.setVolume(float(volume))
		self.voice.play("./sound/sounds/fait.mp3")
		return 'done'

	def faceManager(self):
		while self.FACE_MANAGING_ENABLE:
			#animation mode
			if self.PLAYING_MOVE or self.PLAYING_EXO:
				self.face.stopAnimation()
			else:
				self.face.startAnimation()
			#eyes looking direction initialized if no playing move
			if not self.PLAYING_MOVE:
				self.EyesDirection = self.RestEyesDirection
			#eyes state
			if "warning" in self.poppyPart_alert.values() and "stop" not in self.poppyPart_alert.values() and not self.poppyCompliant():
				self.face.update("forcing", self.EyesDirection)
			elif "stop" in self.poppyPart_alert.values():
				self.face.update("dead", self.EyesDirection)
			else:
				if self.poppyCompliant() and self.FaceState=='happy':
					self.face.update("bored", self.EyesDirection)
				else:
					self.face.update(self.FaceState, self.EyesDirection)
			time.sleep(0.5)

	def setFaceState(self, newFaceState):
		newFaceState = json.loads(newFaceState)
		if newFaceState["data"] in self.face.availableStates:
			self.FaceState = newFaceState["data"]
		return 'ok'

	def setRestEyeDirection(self, newEyeDirection):
		newEyeDirection = json.loads(newEyeDirection)
		if newEyeDirection["data"] in self.face.availableDirections:
			self.RestEyesDirection = newEyeDirection["data"]
		return 'ok'

	def startFaceManager(self):
		if not self.FACE_MANAGING_ENABLE:
			self.FACE_MANAGING_ENABLE=True
			self.faceThread = Thread(target=self.faceManager)
			self.faceThread.start()

	def stopFaceManager(self):
		if self.FACE_MANAGING_ENABLE:
			self.FACE_MANAGING_ENABLE=False

	def setMotorPosition(self, motorPosition):
		motorPosition = json.loads(motorPosition)
		for key, value in motorPosition.iteritems():
			print key, value
			value = int(value)
			#print type(value), value
			if key == "52":
				if abs(value-self.Poppyboid.r_shoulder_y.present_position)>5:
					if value-self.Poppyboid.r_shoulder_y.present_position>20:
						value = self.Poppyboid.r_shoulder_y.present_position+20
					elif value-self.Poppyboid.r_shoulder_y.present_position<-20:
						value = self.Poppyboid.r_shoulder_y.present_position-20
					self.Poppyboid.r_shoulder_y.goto_position(value, 0.5, wait=False)
			if key == "42":
				if abs(value-self.Poppyboid.l_shoulder_y.present_position)>5:
					if value-self.Poppyboid.l_shoulder_y.present_position>20:
						value = self.Poppyboid.l_shoulder_y.present_position+20
					elif value-self.Poppyboid.l_shoulder_y.present_position<-20:
						value = self.Poppyboid.l_shoulder_y.present_position-20
					self.Poppyboid.l_shoulder_y.goto_position(value, 0.5, wait=False)
			if key == "54":
				if abs(value-self.Poppyboid.r_elbow_y.present_position)>5:
					if value-self.Poppyboid.r_elbow_y.present_position>20:
						value = self.Poppyboid.r_elbow_y.present_position+20
					elif value-self.Poppyboid.r_elbow_y.present_position<-20:
						value = self.Poppyboid.r_elbow_y.present_position-20
					print "OK!!! "+str(value)
					self.Poppyboid.r_elbow_y.goto_position(value, 0.5, wait=False)
			if key == "44":
				if abs(value-self.Poppyboid.l_elbow_y.present_position)>5:
					if value-self.Poppyboid.l_elbow_y.present_position>20:
						value = self.Poppyboid.l_elbow_y.present_position+20
					elif value-self.Poppyboid.l_elbow_y.present_position<-20:
						value = self.Poppyboid.l_elbow_y.present_position-20
					self.Poppyboid.l_elbow_y.goto_position(value, 0.5, wait=False)

	def stopAll(self):
		if self.face!='none':
			self.stopFaceManager()
			self.face.stop()
		self.StopExo()
		sys.exit()

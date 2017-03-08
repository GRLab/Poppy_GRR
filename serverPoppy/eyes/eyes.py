#!/usr/bin/env python

import os
import pygame
import math
import numpy as np
import time
from threading import Thread,Lock

import random


class Face:
	"""
		manages the eyes/face display on the screen and animation
		contains the left_eye(EyeManager), right_eye(EyeManager), accessory(AccessoryManager)
	"""
	def __init__(self, datapath, screen_width=480, screen_height=320, bgcolor=[240, 240, 255], fullscreen=True):
		"""
			:param datapath (string): path to the images repertory
			:param screen_width (int): width of the screen in pixel
			:param screen_height (int): height of the screen in pixel
			:param bgcolor (int list[3]): RGB color of the background
			:param fullscreen (bool): set to False if do not want fullscreen display
		"""
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.bgcolor=[]
		self.bgcolor.append(bgcolor[0])
		self.bgcolor.append(bgcolor[1])
		self.bgcolor.append(bgcolor[2])
		print "bgcolor : "+str(self.bgcolor)
		#pygame initialisation
		pygame.init()
		pygame.mouse.set_visible(False)
		if fullscreen:
			self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
		else:
			self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
		self.setBackgroundColor(bgcolor)
		#available states and eyes looking-direction
		self.availableStates = ['happy', 'confused', 'angry', 'bored', 'sad', 'forcing', 'asleep', 'dead']
		self.availableDirections = ['topleft', 'top', 'topright', 'left', 'center', 'right', 'bottomleft', 'bottom', 'bottomright']
		#face composition
		self.accessory = AccessoryManager(datapath, screen_width, screen_height)
		self.left_eye = EyeManager(datapath, 'left', screen_width, screen_height)
		self.right_eye = EyeManager(datapath, 'right', screen_width, screen_height)
		# states initialisation
		self.state='happy'
		self.direction='topleft'
		self.isRunningAnimation = False	#animation thread
		self.isPlayingAnimation = False	#random animation
		self.setState('asleep')
		self.setDirection('center')
		self.display()

		#start the animation thread
		self.STOP = False
		self.animationThread=Thread(target=self.runAnimation)
		self.animationThread.start()
		self.startAnimation()

	def setBackgroundColor(self, bgcolor=''):
		"""
			:param bgcolor (int list[3]): RGB color of the background
		"""
		if bgcolor == '':
			bgcolor = self.bgcolor
		for i in range(3):
			if bgcolor[i]<0 or bgcolor[i]>255:
				print "error : bgcolor is not a RGB color"
				return "error : bgcolor is not a RGB color"
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((bgcolor[0], bgcolor[1], bgcolor[2]))

	def update(self, newState='', newDirection='', forceDisplay=False):
		"""
			sets the new robot screen state and direction, updates the eyes and accessory and display it
			:param newState(string): the newState. Value = one of the self.availableStates
			:param newDirection(string): the newDirection. Value = one of the self.availableDirections
			:param forceDisplay(bool): display in anycase even if there is no change
			availableStates = ['happy', 'confused', 'angry', 'bored', 'sad', 'forcing', 'asleep', 'dead']
			availableDirections = ['topleft', 'top', 'topright', 'left', 'center', 'right', 'bottomleft', 'bottom', 'bottomright']
		"""
		changed = False
		if newState != '' and newState != self.state and not self.isPlayingAnimation or forceDisplay:
			self.setState(newState)
			changed = True
		if newDirection != ''and newDirection != self.direction and not self.isPlayingAnimation or forceDisplay:
			self.setDirection(newDirection)
			changed = True
		if changed:
			self.display()

	def setState(self, newState):
		"""
			sets the robot screen state with newState and updates the eyes and accessory
			:param newState(string): the newState. Value = one of the self.availableStates
		"""
		#print "setting state "+newState
		if self.state == 'forcing':
			self.setBackgroundColor()
		if newState not in self.availableStates : 
			return False
		self.state = newState
		self.updateEyes()

	def setDirection(self, newDirection):
		"""
			sets the robot eyes looking-direction with newDirection and updates the eyes
			:param newDirection(string): the newDirection. Value = one of the self.availableDirections
		"""
		#print "setting looking direction "+newDirection
		if newDirection not in self.availableDirections :
			return False
		self.direction = newDirection
		self.updateEyes()

	def updateEyes(self):
		"""
			updates the eyes and accessory
		"""
		self.left_eye.updateEye(self.state, self.direction)
		self.right_eye.updateEye(self.state, self.direction)
		self.accessory.updateAccessory(self.state)

	def display(self, picName=""):
		"""
			update the screen picture considering the state and looking-direction
			if a picture name is passed in parameter, this picture is displayed

			:param picName (str): path and file name of the picture
		""" 
		self.screen.blit(self.background, (0,0))
		if picName!="":
			picture = pygame.transform.scale(pygame.image.load(picName).convert_alpha(), (self.screen_width, self.screen_height))
			self.screen.blit(picture)
			pygame.display.update()

		else:
			self.screen.blit(self.accessory.getAccessory(), self.accessory.getPosition())
			self.screen.blit(self.left_eye.getEye('eye'), self.left_eye.getPosition('eye'))
			self.screen.blit(self.left_eye.getEye('pupil'), self.left_eye.getPosition('pupil'))
			self.screen.blit(self.left_eye.getEye('eyelid'), self.left_eye.getPosition('eyelid'))
			self.screen.blit(self.left_eye.getEye('eyebrow'), self.left_eye.getPosition('eyebrow'))
			self.screen.blit(self.right_eye.getEye('eye'), self.right_eye.getPosition('eye'))
			self.screen.blit(self.right_eye.getEye('pupil'), self.right_eye.getPosition('pupil'))
			self.screen.blit(self.right_eye.getEye('eyelid'), self.right_eye.getPosition('eyelid'))
			self.screen.blit(self.right_eye.getEye('eyebrow'), self.right_eye.getPosition('eyebrow'))
			pygame.display.update()

	def startAnimation(self):
		"""
			starts the animation thread (blinking, random actions)
		"""
		if not self.isRunningAnimation:
			print "start animation mode"
			self.isRunningAnimation=True
			
	def stopAnimation(self):
		"""
			stops the animation thread (random actions, keep blinking)
		"""
		if self.isRunningAnimation:
			print "pause animation mode"
			self.isRunningAnimation=False

	def runAnimation(self):
		"""
			animation definition (blinking, random actions)
			Automatic Thread. Use startAnimation and stopAnimation
		"""
		count = 0
		blinkTime = random.randint(6,12)
		animationTime = random.randint(15,90)
		while not self.STOP:
			time.sleep(1)
			if self.state=='asleep' or self.state=='confused' or self.state=='forcing' or self.state=='dead':
				continue
			else:
				count+=1
				if count>= blinkTime:
					blinkTime = random.randint(6,12)
					animationTime -= count
					count = 0
					self.blink()
					if not self.isRunningAnimation:
						animationTime = random.randint(15,90)
				if count>= animationTime and self.isRunningAnimation:
					animationTime = random.randint(15,90)
					blinkTime -= count
					count = 0
					animationTh = Thread(target=self.playRandomAnimation)
					animationTh.start()
			#if KeyboardInterrupt:	#CTRL + C
			#	self.isRunningAnimation=False

	def blink(self, side=''):
		"""
			animation: makes poppy blink or wink
			:param side(string): '' 	--> blink
								 left 	--> left wink
								 right 	--> right wink 
		"""
		if side!='right':
			self.left_eye.wink()
		if side!='left':
			self.right_eye.wink()
		self.display()
		if side=='':
			time.sleep(0.05)
		else:
			self.isPlayingAnimation = True
			time.sleep(0.4)
			self.isPlayingAnimation = False
		self.update(self.state, self.direction, True)

	def playRandomAnimation(self):
		"""
			plays a random animation
		"""
		if self.state == 'happy':
			animChoice = random.randint(1,6)
			if animChoice == 1:
				self.blink('left')
			elif animChoice == 2:
				self.blink('right')
			elif animChoice == 3:
				self.lookAround()
			elif animChoice == 4:
				self.lookAround('top')
			elif animChoice == 5:
				self.lookAround('bottom')
			elif animChoice == 6:
				self.squint()
		
		elif self.state == 'angry':
			animChoice = random.randint(1,1)
			if animChoice == 1:
				self.lookAround()
			
		elif self.state == 'bored':
			animChoice = random.randint(1,3)
			if animChoice == 1:
				self.lookAround()
			if animChoice == 2:
				self.lookAround('bottom')
			if animChoice == 3:
				self.squint()
		
		elif self.state == 'sad':
			animChoice = random.randint(1,1)
			if animChoice == 1:
				self.lookAround('bottom')

	def stopCurrentAnimation(self):
		"""
			stops the playing animation
		"""
		if self.isPlayingAnimation:
			self.isPlayingAnimation = False

	def lookAround(self, height=''):
		"""
			animation : looks left and right, at top, middle or bottom
			:param height(string): look at top, middle or bottom
		"""
		if height!='' and height!='bottom' and height!='top':
			return False
		self.isPlayingAnimation = True
		previousDirection = self.direction
		steps = [height+'left',height+'center',height+'right',height+'center',height+'left']
		for step in steps:
			if not self.isPlayingAnimation:
				break
			if step=='bottomcenter':
				step = 'bottom'
			elif step=='topcenter':
				step = 'top'
			self.update(newDirection=step)
			if step=='center' or step=='bottom' or step=='top':
				time.sleep(0.3)
			else:
				time.sleep(1)
		if self.isPlayingAnimation:
			self.update(newDirection=previousDirection)
			self.isPlayingAnimation = False

	def squint(self):
		"""
			animation: funny animation (loucher)
		"""
		self.isPlayingAnimation = True
		previousDirection = self.direction
		self.left_eye.updateEye(self.state, 'right')
		self.right_eye.updateEye(self.state, 'left')
		self.display()
		time.sleep(2.5)
		if self.isPlayingAnimation:
			self.update(newDirection=previousDirection)
			self.isPlayingAnimation = False
		
	def stop(self):
		"""
			stops the display
		"""
		self.STOP=True
		self.stopAnimation()
		pygame.quit()

class AccessoryManager:
	"""
		manage the accessories on the face
	"""
	def __init__(self, datapath, screen_width, screen_height):
		"""
			:param datapath (string): path to the images repertory
			:param screen_width (int): width of the screen in pixel
			:param screen_height (int): height of the screen in pixel
		"""
		self.screen_width = screen_width
		self.screen_height = screen_height
		#available accessories
		self.accessories = {'none':datapath+'empty.png','tear':datapath+'face/accessories/tear.png','nerve':datapath+'face/accessories/nerve.png'}
		for key, value in self.accessories.iteritems():
			self.accessories[key] = pygame.transform.scale(pygame.image.load(value).convert_alpha(), (self.screen_width/2, self.screen_height/2))
		self.accessories['crytear']=pygame.transform.scale(self.accessories['tear'], (self.screen_width/5, self.screen_height/5))
		self.accessories['tear']=pygame.transform.scale(self.accessories['tear'], (self.screen_width/3, self.screen_height/3))
		#position of the accessory
		self.xPosition = -(self.screen_width/8)
		self.yPosition = self.screen_height/64
		self.initAccessory()

	def initAccessory(self):
		"""
			initialise the accessory configuration
		"""
		self.currentAccessory='tear'
		self.accessoryPosition=(self.xPosition, self.yPosition)

	def getAccessory(self):
		"""
			returns the pygame image of the current accessory
		"""
		return self.accessories[self.currentAccessory]

	def getPosition(self):
		"""
			returns the x and y accessory position of the current accessory
		"""
		return self.accessoryPosition

	def updateAccessory(self, state):
		"""
			update the accessory depending on the state
			:param state (string): the new state of the robot screen eyes
		"""
		if state == 'happy':
			self.currentAccessory='none'
			self.accessoryPosition=(self.xPosition, self.yPosition)
		if state == 'confused':
			self.currentAccessory='tear'
			self.accessoryPosition=(self.xPosition, self.yPosition)
		if state == 'angry':
			self.currentAccessory='nerve'
			self.accessoryPosition=(self.xPosition, self.yPosition)
		if state == 'bored':
			self.currentAccessory='none'
			self.accessoryPosition=(self.xPosition, self.yPosition)
		if state == 'sad':
			self.currentAccessory='crytear'
			self.accessoryPosition=(self.screen_width/12, 4*self.screen_height/7)
		if state == 'forcing':
			self.currentAccessory='tear'
			self.accessoryPosition=(self.xPosition, self.yPosition)
		if state == 'asleep':
			self.currentAccessory='none'
			self.accessoryPosition=(self.xPosition, self.yPosition)
		if state == 'dead':
			self.currentAccessory='none'
			self.accessoryPosition=(self.xPosition, self.yPosition)

class EyeManager:
	"""
		manage each eye on the face
	"""
	def __init__(self, datapath, side, screen_width, screen_height):
		"""
			:param datapath (string): path to the images repertory
			:param side (string): 'left' or 'right' eye
			:param screen_width (int): width of the screen in pixel
			:param screen_height (int): height of the screen in pixel
		"""
		self.side = side
		self.screen_width = screen_width
		self.screen_height = screen_height
		#available eyes components
		self.eyebrow = {'none':datapath+'empty.png','0':datapath+"face/eyes/eyebrow_0.png",'1':datapath+"face/eyes/eyebrow_1.png",'2':datapath+"face/eyes/eyebrow_2.png",'3':datapath+"face/eyes/eyebrow_3.png",'4':datapath+"face/eyes/eyebrow_4.png",'5':datapath+"face/eyes/eyebrow_5.png",'6':datapath+"face/eyes/eyebrow_6.png"}
		self.eyes = {'0':datapath+"face/eyes/eye.png",'closed':datapath+"face/eyes/closed_eye.png", 'confused':datapath+"face/eyes/confused_eye.png", 'forcing':datapath+"face/eyes/forced_eye.png", 'forcing2':datapath+"face/eyes/forced_eye2.png",'wink':datapath+"face/eyes/eyebrow_4.png", 'crossed':datapath+"face/eyes/crossed_eye.png"}
		self.pupils = {'none':datapath+'empty.png','blue':datapath+"face/eyes/pupil.png",'red':datapath+"face/eyes/pupil_red.png"}
		self.eyelids = {'none':datapath+'empty.png','0':datapath+"face/eyes/eyelid_0.png",'1':datapath+"face/eyes/eyelid_1.png",'2':datapath+"face/eyes/eyelid_2.png",'3':datapath+"face/eyes/eyelid_3.png",'close':datapath+"face/eyes/eyelid_close.png",'open':datapath+"face/eyes/eyelid_open.png"}
		for key, value in self.eyebrow.iteritems():
			self.eyebrow[key] = pygame.transform.scale(pygame.image.load(value).convert_alpha(), (self.screen_width/2, self.screen_height/2)).convert_alpha()
		for key, value in self.eyes.iteritems():
			self.eyes[key] = pygame.transform.scale(pygame.image.load(value).convert_alpha(), (self.screen_width/2, self.screen_height/2)).convert_alpha()
		for key, value in self.pupils.iteritems():
			self.pupils[key] = pygame.transform.scale(pygame.image.load(value).convert_alpha(), (self.screen_width/2, self.screen_height/2)).convert_alpha()
		for key, value in self.eyelids.iteritems():
			self.eyelids[key] = pygame.transform.scale(pygame.image.load(value).convert_alpha(), (self.screen_width/2, self.screen_height/2)).convert_alpha()
		#position of the eye
		if side == 'left':
			self.xPosition = self.screen_width/4-self.screen_width/5
		else:
			self.xPosition = self.screen_width/4+self.screen_width/5
		self.yPosition = self.screen_height/4
		self.initEye()

	def initEye(self):
		"""
			initialise the eye configuration
		"""
		self.currentEyebrow='0'
		self.currentEye='0'
		self.currentPupil='blue'
		self.currentEyelid='0'
		self.eyebrowPosition=(self.xPosition, self.yPosition-self.screen_height/4)
		self.eyePosition=(self.xPosition, self.yPosition)
		self.pupilPosition=(self.xPosition, self.yPosition)
		self.eyelidPosition=(self.xPosition, self.yPosition)

	def getEye(self, part):
		"""
			returns the pygame image of the current eye
			:param part (string): part of the eye to display (eyebrow, eye, pupil, eyelid) 
		"""
		if part == 'eyebrow' : return self.eyebrow[self.currentEyebrow]
		elif part == 'eye' : return self.eyes[self.currentEye]
		elif part == 'pupil' : return self.pupils[self.currentPupil]
		elif part == 'eyelid' : return self.eyelids[self.currentEyelid]
		else : return False

	def getPosition(self, part):
		"""
			returns the x and y eye part position of the current eye
			:param part (string): part of the eye to display (eyebrow, eye, pupil, eyelid) 
		"""
		if part == 'eyebrow' : return self.eyebrowPosition
		elif part == 'eye' : return self.eyePosition
		elif part == 'pupil' : return self.pupilPosition
		elif part == 'eyelid' : return self.eyelidPosition
		else : return False

	def updateEye(self, state, direction):
		"""
			update the eye depending on the state and direction
			:param state (string): the new state of the robot screen eyes
			:param direction (string): the new looking-direction of the robot screen eyes
		"""
		if state == 'happy':
			self.currentEyebrow='4'
			self.currentEye='0'
			self.currentPupil='blue'
			self.currentEyelid='open'
		if state == 'confused':
			self.currentEyebrow='none'
			self.currentEye='confused'
			self.currentPupil='none'
			self.currentEyelid='none'
		if state == 'angry':
			if self.side=='left':
				self.currentEyebrow='3'
			else:
				self.currentEyebrow='2'
			self.currentEye='0'
			self.currentPupil='red'
			self.currentEyelid='3'
		if state == 'bored':
			self.currentEyebrow='4'
			self.currentEye='0'
			self.currentPupil='blue'
			self.currentEyelid='1'
		if state == 'sad':
			if self.side=='left':
				self.currentEyebrow='5'
			else:
				self.currentEyebrow='6'
			self.currentEye='0'
			self.currentPupil='blue'
			self.currentEyelid='2'
		if state == 'forcing':
			self.currentEyebrow='none'
			if self.side=='left':
				self.currentEye='forcing'
			else:
				self.currentEye='forcing2'
			self.currentPupil='none'
			self.currentEyelid='none'
		if state == 'asleep':
			self.currentEyebrow='4'
			self.currentEye='closed'
			self.currentPupil='none'
			self.currentEyelid='none'
		if state == 'dead':
			self.currentEyebrow='none'
			self.currentEye='crossed'
			self.currentPupil='none'
			self.currentEyelid='none'

		if direction == 'topleft':
			self.pupilPosition=(self.xPosition-2-self.screen_width/24, self.yPosition+4-self.screen_height/12)
		if direction == 'top':
			self.pupilPosition=(self.xPosition-2, self.yPosition+4-self.screen_height/10)
		if direction == 'topright':
			self.pupilPosition=(self.xPosition-2+self.screen_width/24, self.yPosition+4-self.screen_height/12)
		if direction == 'left':
			self.pupilPosition=(self.xPosition-2-self.screen_width/15, self.yPosition+4)
		if direction == 'center':
			self.pupilPosition=(self.xPosition-2, self.yPosition+4)
		if direction == 'right':
			self.pupilPosition=(self.xPosition-2+self.screen_width/15, self.yPosition+4)
		if direction == 'bottomleft':
			self.pupilPosition=(self.xPosition-2-self.screen_width/24, self.yPosition+4+self.screen_height/12)
		if direction == 'bottom':
			self.pupilPosition=(self.xPosition-2, self.yPosition+4+self.screen_height/10)
		if direction == 'bottomright':
			self.pupilPosition=(self.xPosition-2+self.screen_width/24, self.yPosition+4+self.screen_height/12)

	def wink(self):
		"""
			winks or blinks. Puts the correct eyes keeping the current eyebrow
		"""
		if self.side == 'left':
			self.currentEye='wink'
		else:
			self.currentEye='wink'
		self.currentPupil='none'
		self.currentEyelid='none'

if __name__=="__main__":
	#face = Face(datapath="/home/poppy//poppy_dev/serverPoppy/eyes/", bgcolor=[220,230,255])
	face = Face(datapath="/home/damiend/damien/poppy_dev/serverPoppy/eyes/", bgcolor=[220,230,255])
	time.sleep(2)
	print 'happy center'
	face.stopCurrentAnimation()
	face.update('happy', 'center')
	time.sleep(4)
	print 'happy topleft'
	face.stopCurrentAnimation()
	face.update('happy', 'topleft')
	time.sleep(1)
	print 'happy top'
	face.stopCurrentAnimation()
	face.update('happy', 'top')
	time.sleep(1)
	print 'happy topright'
	face.stopCurrentAnimation()
	face.update('happy', 'topright')
	time.sleep(1)
	print 'happy right'
	face.stopCurrentAnimation()
	face.update('happy', 'right')
	time.sleep(1)
	print 'happy bottomright'
	face.stopCurrentAnimation()
	face.update('happy', 'bottomright')
	time.sleep(1)
	print 'happy bottom'
	face.stopCurrentAnimation()
	face.update('happy', 'bottom')
	time.sleep(1)
	print 'happy bottomleft'
	face.stopCurrentAnimation()
	face.update('happy', 'bottomleft')
	time.sleep(1)
	print 'happy left'
	face.stopCurrentAnimation()
	face.update('happy', 'left')
	time.sleep(1)
	print 'happy center'
	face.stopCurrentAnimation()
	face.update('happy', 'center')
	time.sleep(2)

	print 'confused'
	face.stopCurrentAnimation()
	face.update('confused')
	time.sleep(4)
	print 'angry center'
	face.stopCurrentAnimation()
	face.update('angry', 'center')
	time.sleep(4)
	print 'bored left'
	face.stopCurrentAnimation()
	face.update('bored', 'left')
	time.sleep(4)
	print 'sad bottom'
	face.stopCurrentAnimation()
	face.update('sad', 'bottom')
	time.sleep(4)
	print 'forcing'
	face.stopCurrentAnimation()
	face.update('forcing')
	time.sleep(4)
	print 'happy center'
	face.stopCurrentAnimation()
	face.update('happy', 'center')
	time.sleep(4)
	face.stop()
	#availableStates = ['happy', 'confused', 'angry', 'bored', 'sad', 'forcing', 'asleep']

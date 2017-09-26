#!/usr/bin/env python

import os
import pygame
import time
from threading import Thread,Lock
from speak import TextToSpeech

import random

class Sound():
	"""
		manage the sound player (mp3), by playing sounds or doing text to speech
	"""

	def __init__(self, language = 'fr', frequence=29000, volume=0.7):
		"""
			:param language (string): language for the robot voice
			:param frequence (int): voice frequence (~20000 = male, ~26000=female, ~30000=child), but low = low speed speaking
			:param volume (int): voice volume [0-1]
		"""
		self.speak = TextToSpeech(language)
		self.frequence = frequence
		pygame.mixer.quit()
		pygame.mixer.init(frequence)
		self.volume=volume
		pygame.mixer.music.set_volume(self.volume)

	def setLanguage(self, language = "fr"):
		self.speak.set_language(language)

	def setFrequence(self, frequence=29000):
		"""
			change the voice frequence
			:param frequence (int): voice frequence (~20000 = male, ~26000=female, ~30000=child), but low = low speed speaking
		"""
		self.frequence = frequence
		pygame.mixer.quit()
		time.sleep(0.5)
		pygame.mixer.init(frequence)
		pygame.mixer.music.set_volume(self.volume)

	def say(self, text, filename="", remove=True):
		"""
			say a text
			:param text (string): text to say
			:param filename (string): mp3 file name
			:param remove (bool): if remove the mp3 file or not after saying the text
		"""
		if filename == "":
			filename='text.mp3'

		self.speak.textToMP3(text, filename)
		self.play(filename)
		if remove:
			self.speak.removeMP3File(filename)

	def setVolume(self, volume=0.7):
		"""
			set the voice volume (0-1)
			:param volume (int): volume [0-1]
		"""
		self.volume=volume
		pygame.mixer.music.set_volume(self.volume)

	def play(self, filename):
		"""
			plays an existing sound
			:param filename (string): mp3 file name 
		"""
		try:
			pygame.mixer.music.load(filename)
			pygame.mixer.music.play()
		except:
			print str(filename)+" does not exist"

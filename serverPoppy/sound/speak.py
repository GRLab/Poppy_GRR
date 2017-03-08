#!/usr/bin/env python

import os
from gtts import gTTS

class TextToSpeech():
	"""
		manage text to speech in order to create mp3 sound file. Needs network to work.
	"""

	def __init__(self, language='fr'):
		"""
			:param language (string): language for the robot voice
		"""
		self.language = language

	def set_language(self, language='fr'):
		"""
			change the language
			:param language (string): language for the robot voice 
		"""
		self.language = language

	def textToMP3(self, text, filename):
		"""
			converts the text into MP3 file
			:param text (string): text to convert (tts)
			:param filename (string): name of the mp3 file to create
		"""
		if text == "":
			return False
		if ".mp3" not in filename:
			return False
		tts = gTTS(text, lang=self.language)
		tts.save(filename)

	def removeMP3File(self, filename):
		"""
			removes the mp3 file
			:param filename (string): name of the mp3 file to remove
		"""
		os.remove(filename)

	def getLanguage(self):
		"""
			returns the language
		"""
		return self.language
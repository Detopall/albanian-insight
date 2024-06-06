"""
This module contains functions for translating text from Albanian to English.
"""
from googletrans import Translator

def translate_text(text: str) -> str:
	"""
	Translate the input text from Albanian to English.
	"""

	translator = Translator()
	translated_text = translator.translate(text, dest='en').text

	return translated_text

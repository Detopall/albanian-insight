"""
This module contains the function to predict the POS for a new English text.
"""

from typing import List

import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.downloader import Downloader

# Check if the NLTK data is downloaded
if not Downloader().is_installed('punkt') or not Downloader().is_installed('stopwords') or not Downloader().is_installed('averaged_perceptron_tagger'):
	# Download necessary NLTK resources
	nltk.download('punkt')
	nltk.download('stopwords')
	nltk.download('averaged_perceptron_tagger')

def english_predict_pos(translated_text: str) -> List:
	"""
	Predict the POS tags for the translated text.
	"""

	# Tokenize the text into sentences and words
	sentences = sent_tokenize(translated_text)
	words = [word_tokenize(sentence) for sentence in sentences]

	# Remove perform POS tagging without removing stopwords
	english_tokens = [word for sentence in words for word in sentence]
	
	# Perform POS tagging
	pos_tags = [nltk.pos_tag(sentence) for sentence in words]

	# Filter out the words and POS tags
	pos_tags = [tag for _, tag in pos_tags[0]]

	# Return the filtered words and POS tags
	return english_tokens, pos_tags

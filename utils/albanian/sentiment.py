"""
This module contains the functions to predict the sentiment of a text.
"""

from typing import List
import string
from .stopwords import stopwords_al

def process_text(text: str, count_vect: object, tfidf_transformer: object) -> object:
	"""
	Process the input text by removing punctuation, converting to lowercase, and removing stopwords, and non-ASCII characters.
	"""
	text = text.lower()
	for punctuation in string.punctuation:
		text = text.replace(punctuation, '')
	text = text.strip()

	# Remove non-ASCII characters (such as emojis)
	text = text.encode('ascii', 'ignore').decode('ascii')
	text = ' '.join([word for word in text.split()
					if word not in stopwords_al])
	
	text = count_vect.transform([text])
	text = tfidf_transformer.transform(text)

	return text

def predict_sentiment(text: str, model: object, count_vect: object, tfidf_transformer: object) -> List:
	"""
	Predict the sentiment of a given text.
	"""
	text = process_text(text, count_vect, tfidf_transformer)
	prediction = model.predict(text)[0]

	# Return the prediction as a string using the mapping
	sentiment_mapping = {
		0: "Neutral",
		1: "Positive",
		2: "Negative"
	}
	
	return sentiment_mapping[prediction]

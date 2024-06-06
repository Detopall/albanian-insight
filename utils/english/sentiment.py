"""
This script is used to determine the sentiment of a given text. It uses the VADER sentiment analysis tool from the NLTK library.
"""

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
from nltk.downloader import Downloader

# Check if the NLTK data is downloaded
if not Downloader().is_installed('vader_lexicon'):
	
	# Download necessary NLTK resources
	nltk.download('vader_lexicon')

def english_predict_sentiment(text: str) -> str:
	"""
	Predict the sentiment of a given English text.
	"""

	# Tokenize the text into sentences and words
	sentences = sent_tokenize(text)

	sia = SentimentIntensityAnalyzer()

	sentiment_scores = [sia.polarity_scores(sentence) for sentence in sentences]

	# Remove the compound score
	sentiment_scores = [{k: v for k, v in score.items() if k != 'compound'} for score in sentiment_scores]

	# Show the highest sentiment score
	highest_sentiment = max(sentiment_scores, key=lambda x: max(x.values()))

	highest_score = max(highest_sentiment.values())
	highest_sentiment = {k: v for k, v in highest_sentiment.items() if v == highest_score}
	highest_sentiment = list(highest_sentiment.keys())[0]

	sentiment_mapping = {
		'pos': 'Positive',
		'neg': 'Negative',
		'neu': 'Neutral'
	}

	return sentiment_mapping[highest_sentiment]

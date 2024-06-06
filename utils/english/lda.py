"""
This module contains functions for predicting the part of speech of English text.
"""

import string
from typing import List, Dict

from nltk.corpus import stopwords
from gensim import corpora
from gensim.models import LdaMulticore
from gensim.utils import simple_preprocess

# Define the mapping from keywords to general topics
topic_mapping = {
	"Politics": {"prime", "minister", "government", "policy", "election", "vote"},
	"Finance": {"market", "finance", "investment", "economy", "stock", "bank"},
	"Technology": {"technology", "software", "hardware", "innovation", "tech"},
	"Health": {"health", "medicine", "doctor", "hospital", "disease", "treatment"},
	"Education": {"education", "school", "university", "student", "teacher", "learning"},
	"Immigration": {"immigrant", "immigration", "camp", "refugee", "border", "Migration"},
	"COVID-19": {"covid", "pandemic", "virus", "quarantine", "lockdown", "vaccine"},
	"Time, Days": {"day", "night", "morning", "afternoon", "evening", "hour", "minute", "second", "time"},
	"Money, Finance": {"money", "cash", "currency", "payment", "income", "expense", "debt", "credit", "savings"},
	"Sports": {"sport", "football", "soccer", "basketball", "tennis", "athlete", "game", "match", "tournament"}
}

def english_predict_topics(text: str) -> Dict[str, float]:
	"""
	Predict the topics for an English text using the filtered words.
	Returns a dictionary of general topics and their relevance.
	"""

	# Preprocess the text
	tokenized_text = preprocess_text(text)

	# Create a dictionary from the filtered words
	dictionary = corpora.Dictionary([tokenized_text])

	# Create a corpus
	corpus = [dictionary.doc2bow(tokenized_text)]

	# Train the LDA model
	lda_model = LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=5)

	# Get the topics for the first document in the corpus
	topics = lda_model.get_document_topics(corpus[0])

	# Initialize a dictionary to hold the general topic relevance
	general_topics = {key: 0 for key in topic_mapping.keys()}

	# Extract the topics and their word distributions
	for topic in topics:
		topic_number = topic[0]
		topic_words = lda_model.show_topic(topic_number, topn=10)
		for word, prob in topic_words:
			for general_topic, keywords in topic_mapping.items():
				if word in keywords:
					general_topics[general_topic] += prob

	# Normalize the relevance scores
	total_prob = sum(general_topics.values())
	if total_prob > 0:
		for key in general_topics:
			general_topics[key] /= total_prob

	general_topics = [{"topic": topic, "score": score} for topic, score in general_topics.items()]
	
	return general_topics


def preprocess_text(text: str) -> List[str]:
	"""
	Process the input text by removing punctuation, converting to lowercase,
	removing stopwords, and non-ASCII characters.
	"""

	text = text.lower()
	for punctuation in string.punctuation:
		text = text.replace(punctuation, '')
	text = text.strip()

	# Remove non-ASCII characters (such as emojis)
	text = text.encode('ascii', 'ignore').decode('ascii')

	# Remove stopwords by using the stopwords list from the NLTK library
	stop_words = set(stopwords.words('english'))
	text = [word for word in text.split() if word not in stop_words]

	# Tokenize the text using simple_preprocess
	tokenized_text = simple_preprocess(' '.join(text))

	return tokenized_text

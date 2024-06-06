"""
This module contains the functions for predicting topics for a new text using the trained LDA model.
"""

from typing import List, Dict, Union

from gensim import corpora
from gensim.models import LdaModel
from gensim.utils import simple_preprocess

from .stopwords import stopwords_al


def predict_topics(new_text: str, lda_model: LdaModel, dictionary: corpora.Dictionary, topic_mapping: Dict[int, str]) -> List[Dict[str, Union[str, float]]]:
	"""
	Predict the topics for a new text using the trained LDA model.
	"""
	# Preprocess the new text
	new_text_preprocessed = preprocess(new_text)

	# Convert the preprocessed text into a bag-of-words representation
	new_text_bow = dictionary.doc2bow(new_text_preprocessed)

	# Predict the topic distribution for the new text
	topics = lda_model.get_document_topics(new_text_bow)

	# Return the topics and their mapping
	return [{"topic": topic_mapping[topic[0]], "score": topic[1]} for topic in topics]


def preprocess(text_list: List[str]):
	"""
	Preprocess the text by removing stopwords and tokenizing it.
	"""
	text = "".join(text_list)

	return [word for word in simple_preprocess(str(text)) if word not in stopwords_al]

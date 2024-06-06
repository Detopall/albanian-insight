"""
POS tagging utility functions.
"""

import joblib


def predict_pos(text: str, pos_model: str):
	"""
	Predict the POS tags for a given text using the trained POS tagger model.
	"""
	# Load the model
	model = joblib.load(pos_model)

	tokens = text.split()
	pos_tags = model.predict([tokens])[0]

	# Return both the tokens and the POS tags
	return tokens, pos_tags

import pickle
from typing import Dict

import numpy as np
import uvicorn
from fastapi import FastAPI
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from gensim import corpora
from gensim.models import LdaModel

from utils.albanian.lda import predict_topics
from utils.albanian.pos import predict_pos
from utils.albanian.sentiment import predict_sentiment

from utils.english.translation import translate_text
from utils.english.pos import english_predict_pos
from utils.english.lda import english_predict_topics
from utils.english.sentiment import english_predict_sentiment


# Create the FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"]
)

# Serve static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Load the dictionary
dictionary = corpora.Dictionary.load('./models/lda/dictionary')

# Load the corpus
corpus = corpora.MmCorpus('./models/lda/corpus.mm')

# Load the LDA model
lda_model = LdaModel.load('./models/lda/lda_model')

# Load the POS tagger model
pos_model_file = "./models/pos/pos_model.pkl"

# Load the sentiment model
with open('./models/sentiment/sentiment_model.pkl', 'rb') as f:
	sentiment_model = pickle.load(f)

# Load the CountVectorizer object
with open('./models/sentiment/count_vectorizer.pkl', 'rb') as f:
	count_vect = pickle.load(f)

# Load the TfidfTransformer object
with open('./models/sentiment/tfidf_transformer.pkl', 'rb') as f:
	tfidf_transformer = pickle.load(f)


# Load the topic mapping
topic_mapping = {
	0: "Politics, Political Statements",
	1: "Advice, Opinions",
	2: "Social Media, Online News",
	3: "Police, Crime",
	4: "COVID-19, Health",
	5: "Time, Days",
	6: "Kosovo, Politics",
	7: "News, Media",
	8: "Money, Finance",
	9: "Kosovo, Prishtina"
}


@app.get("/")
def home(request: Request):
	return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/predict")
def predict(request: Dict):
	# Get the text from the request
	text = request.get("text")

	# Predict the topics for the text
	topics = predict_topics(text, lda_model, dictionary, topic_mapping)

	# Predict the POS tags for the text
	tokens, pos_tags = predict_pos(text, pos_model_file)

	# Predict the sentiment of the text
	sentiment = predict_sentiment(
		text, sentiment_model, count_vect, tfidf_transformer)

	# Translation
	translated_text = translate_text(text)

	# Predict the topics for the translated text
	english_topics = english_predict_topics(translated_text)

	# Predict the POS tags for the translated text
	english_tokens, english_pos_tags = english_predict_pos(translated_text)

	# Predict the sentiment of the translated text
	english_sentiment = english_predict_sentiment(translated_text)

	response = {
		"albanian": {
			"topics": topics,
			"pos_tags": pos_tags,
			"pos_tokens": tokens,
			"sentiment": sentiment
		},
		"english": {
			"translated_text": translated_text,
			"topics": english_topics,
			"pos_tags": english_pos_tags,
			"pos_tokens": english_tokens,
			"sentiment": english_sentiment
		}
	}

	# Convert any NumPy types to native Python types
	response = convert_numpy_types(response)

	# Encode the response as JSON
	return JSONResponse(content=response, status_code=status.HTTP_200_OK)


def convert_numpy_types(obj):
	"""
	Convert NumPy types to native Python types.
	"""

	if isinstance(obj, np.generic):
		return obj.item()
	elif isinstance(obj, dict):
		return {k: convert_numpy_types(v) for k, v in obj.items()}
	elif isinstance(obj, list):
		return [convert_numpy_types(i) for i in obj]
	elif isinstance(obj, tuple):
		return tuple(convert_numpy_types(i) for i in obj)
	return obj


if __name__ == '__main__':
	uvicorn.run('app:app', host='localhost', port=8000, reload=True)

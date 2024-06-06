"use strict";

const form = document.querySelector("form");
const input = document.querySelector("input");
const textInput = document.querySelector("#text");
const exampleText = document.querySelector("#example-albanian");

exampleText.addEventListener("click", () => {
	// Source: https://www.balkanweb.com/qeveria-e-kosoves-perjashton-nga-shpronesimi-disa-toka-ne-veri/#gsc.tab=0
	const albanianExampleText = "Në vendimin përfundimtar të Qeverisë së Kosovës për shpronësimin e tokave në Leposaviq dhe Zubin Potok, komuna të banuara me shumicë serbe në veri të Kosovës janë përjashtuar disa parcela private, por vetëm të atyre qytetarëve që e kanë fituar procesin në gjykatë, konfirmon për REL, Nebojsha Vllajiq, njëri prej avokatëve që kanë përfaqësuar banorët e pakënaqur para gjyqësorit të Kosovës. Politika është një detyrë delikate.";
	// Translation: "In the final decision of the Government of Kosovo on the expropriation of lands in Leposaviq and Zubin Potok, municipalities inhabited by a Serbian majority in northern Kosovo, several private parcels have been excluded, but only those citizens who have won the process in court, confirms for REL, Nebojsha Vllajiq, one of the lawyers who have represented the dissatisfied residents before the courts of Kosovo. Politics is a delicate task."
	textInput.textContent = albanianExampleText;
});

form.addEventListener("submit", async (e) => {
	e.preventDefault();

	// Hide results
	const resultsDivs = document.querySelectorAll(".results");
	resultsDivs.forEach((result) => {
		result.childNodes.forEach((child) => {
			if (child.tagName === 'DIV') {
				child.innerHTML = '';
			}
		});
	});

	// Destroy previous bar charts
	const barCharts = document.querySelectorAll("canvas");
	barCharts.forEach((chart) => {
		chart.remove();
	});

	// Create new canvas elements for bar charts
	resultsDivs.forEach((container) => {
		container.innerHTML += `<canvas id="${container.id}-bar-chart" width="500" height="500"></canvas>`;
	});

	// Show loading spinner
	const loadingSpinner = document.getElementById("loading-spinner");
	loadingSpinner.classList.remove("hidden");

	// Disable the buttons
	const buttons = document.querySelectorAll("button");
	buttons.forEach((button) => {
		button.disabled = true;
	});

	const response = await fetch("/api/predict", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ text: textInput.value }),
	});
	const data = await response.json();

	// Display Albanian results
	displayResults(data, 'albanian', 'albanian-text', 'albanian-legend', 'albanian-bar-chart', 'albanian-sentiment');
	// Display English results
	displayResults(data, 'english', 'english-text', 'english-legend', 'english-bar-chart', 'english-sentiment');

	// Remove hidden class from results
	resultsDivs.forEach((result) => {
		result.classList.remove("hidden");
	});

	// Scroll to results
	const results = document.querySelector(".results");
	results.scrollIntoView({ behavior: "smooth" });

	// Hide loading spinner
	loadingSpinner.classList.add("hidden");
});


function displayResults(response, language, textContainerId, legendContainerId, barChartCanvasId, sentimentContainerId) {
	const textContainer = document.getElementById(textContainerId);
	const legendContainer = document.getElementById(legendContainerId);
	const ctx = document.getElementById(barChartCanvasId).getContext('2d');
	ctx.canvas.width = 500;
	ctx.canvas.height = 500;

	// Display text with POS styling and legend
	response[language].pos_tokens.forEach((token, index) => {
		const pos = response[language].pos_tags[index];
		const span = document.createElement('span');
		span.className = 'token';
		applyStyleToToken(span, pos);
		span.textContent = token + ' ';
		textContainer.appendChild(span);
	});

	// Display legend
	const uniqueTags = [...new Set(response[language].pos_tags)];
	uniqueTags.forEach(pos => {
		const legendItem = document.createElement('div');
		legendItem.className = 'legend-item';
		const colorBox = document.createElement('div');
		colorBox.className = 'legend-color';
		colorBox.style.backgroundColor = POS_COLORS[pos].color;
		legendItem.appendChild(colorBox);
		const legendText = document.createTextNode(pos);
		legendItem.appendChild(legendText);
		legendContainer.appendChild(legendItem);
	});

	// Display bar chart
	displayBarChart(ctx, response[language].topics);

	// Display sentiment
	displaySentiment(document.getElementById(sentimentContainerId), response[language].sentiment);
}

function applyStyleToToken(token, pos) {
	const defaultStyle = { color: "black" };
	const style = POS_COLORS[pos] || defaultStyle;
	token.style.color = style.color;
}

function displayBarChart(ctx, topics) {
	const labels = topics.map(topic => topic.topic);
	const data = topics.map(topic => topic.score);

	const colors = [
		'rgb(255, 99, 132)',
		'rgb(54, 162, 235)',
		'rgb(255, 206, 86)',
		'rgb(75, 192, 192)',
		'rgb(153, 102, 255)',
		'rgb(255, 159, 64)',
		'rgb(255, 99, 132)',
		'rgb(54, 162, 235)',
		'rgb(255, 206, 86)',
	];

	// bar chart
	new Chart(ctx, {
		type: 'bar', // Set chart type to 'bar'
		data: {
			labels: labels,
			datasets: [{
				label: 'Topic Scores',
				data: data,
				backgroundColor: colors,
				borderColor: colors,
				borderWidth: 1
			}]
		},
		options: {
			scales: {
				y: {
					beginAtZero: true // Start y-axis at 0
				}
			},
			responsive: false,
			plugins: {
				legend: {
					display: false
				}
			}
		}
	});
}

function displaySentiment(sentimentContainer, sentiment) {
	let sentimentSymbol;
	if (sentiment === 'Positive') {
		sentimentSymbol = '😀';
	} else if (sentiment === 'Negative') {
		sentimentSymbol = '😡';
	} else if (sentiment === 'Neutral') {
		sentimentSymbol = '😐';
	} else {
		sentimentSymbol = '😶'
	};

	sentimentContainer.innerHTML = `<span class="sentiment">${sentimentSymbol}</span>`;
}


const POS_COLORS = {
	"NOUN": {
		"color": "blue",
		"fontStyle": "normal",
		"fontWeight": "bold",
		"textDecoration": "none"
	},
	"DET": {
		"color": "green",
		"fontStyle": "italic",
		"fontWeight": "normal",
		"textDecoration": "underline"
	},
	"PROPN": {
		"color": "red",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"AUX": {
		"color": "purple",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"VERB": {
		"color": "orange",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"CCONJ": {
		"color": "yellow",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"PART": {
		"color": "pink",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"ADP": {
		"color": "brown",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"ADJ": {
		"color": "cyan",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"NNP": {
		"color": "magenta",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"POS": {
		"color": "lime",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"VBD": {
		"color": "teal",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"VB": {
		"color": "indigo",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"RB": {
		"color": "violet",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"IN": {
		"color": "black",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"CD": {
		"color": "gold",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"PRP": {
		"color": "azure",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"TO": {
		"color": "orange",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"VBZ": {
		"color": "brown",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"VBN": {
		"color": "green",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"VBP": {
		"color": "lavender",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"DT": {
		"color": "salmon",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"CC": {
		"color": "plum",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"NNS": {
		"color": "olive",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"NUM": {
		"color": "silver",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"PRON": {
		"color": "black",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"JJ": {
		"color": "coral",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"VBG": {
		"color": "olive",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	".": {
		"color": "gray",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	",": {
		"color": "gray",
		"fontStyle": "normal",
		"fontWeight": "normal",
		"textDecoration": "none"
	},
	"SCONJ": {
		"color": "orange",
		"fontStyle": "normal",
		"fontWeight": "bold",
		"textDecoration": "underline"
	},
	"PUNCT": {
		"color": "green",
		"fontStyle": "italic",
		"fontWeight": "bold",
		"textDecoration": "underline"
	},
	"NN": {
		"color": "blue",
		"fontStyle": "normal",
		"fontWeight": "bold",
		"textDecoration": "none"
	},
	"WP": {
		"color": "red",
		"fontStyle": "italic",
		"fontWeight": "bold",
		"textDecoration": "none"
	}
}

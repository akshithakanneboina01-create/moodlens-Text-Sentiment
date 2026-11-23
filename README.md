# MoodLens — Text Sentiment Demo

**Project #116 | Python for Good**

MoodLens is a small educational Python application that estimates whether a written review is Positive, Negative, or Neutral.

## Features
- Streamlit dashboard with a modern gradient interface and subtle CSS animations
- Rule-based sentiment analysis with a small positive/negative vocabulary
- Basic negation handling (for example, "not good")
- Save records in CSV and JSON
- Search reviews by keyword and filter by sentiment
- Summary statistics and Matplotlib charts
- Download filtered CSV and JSON data
- Input validation and file error handling

## Requirements
- Python 3.10 or newer
- Internet connection for the first installation of Python packages

## Run on Windows
1. Extract the ZIP file.
2. Open the `Text_Sentiment_Demo` folder.
3. Click the address bar in File Explorer, type `cmd`, and press Enter.
4. Run:

```bash
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

If `py` does not work but `python` does, use `python` instead of `py`.

The application opens in your browser, usually at `http://localhost:8501`.

## Project structure
```text
Text_Sentiment_Demo/
├── app.py
├── sentiment.py
├── storage.py
├── reports.py
├── requirements.txt
├── README.md
├── data/
│   ├── reviews.csv
│   └── reviews.json
└── charts/
```

## How sentiment analysis works
This project uses a transparent word-based scoring method. Positive vocabulary adds points and negative vocabulary subtracts points. The final score determines the label:
- Score above zero: Positive
- Score below zero: Negative
- Score equal to zero: Neutral

This is a classroom demonstration, not a professional AI language model. It may not understand sarcasm, complex context, spelling variations, or every form of negation.

## Notes for the project demonstration
Demonstrate:
1. Enter a positive review and analyse it.
2. Save it.
3. Enter a negative review and save it.
4. Search for a keyword in Review Library.
5. Show the dashboard counts and Insights charts.
6. Download CSV and JSON exports.
7. Restart the app and show that saved records remain.

## Customisation
Add more words to `POSITIVE_WORDS` and `NEGATIVE_WORDS` in `sentiment.py` to improve the simple demo vocabulary.


## Interface design
The interface uses a responsive lavender, violet and rose gradient theme, soft glass-style panels, hover transitions, subtle entrance animation, and polished dashboard cards. An internet connection is used only to load the optional Google Fonts; the app itself runs locally.

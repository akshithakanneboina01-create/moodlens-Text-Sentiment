"""Simple, explainable rule-based sentiment analysis."""

POSITIVE_WORDS = {
    "amazing", "awesome", "best", "beautiful", "brilliant", "clear", "comfortable",
    "delicious", "easy", "enjoy", "excellent", "fantastic", "fast", "friendly",
    "good", "great", "happy", "helpful", "impressive", "love", "loved", "lovely",
    "perfect", "positive", "quick", "recommend", "smooth", "super", " wonderful",
    "thank", "thanks", "useful", "value", "well", "wonderful", "worth"
}
NEGATIVE_WORDS = {
    "annoying", "awful", "bad", "boring", "broken", "complaint", "confusing",
    "damage", "damaged", "delay", "disappoint", "disappointed", "disappointing",
    "difficult", "dirty", "dislike", "hate", "horrible", "late", "mess", "negative",
    "poor", "problem", "rude", "sad", "slow", "terrible", "uncomfortable", "unhappy", "upset", "lonely", "miserable",
    "useless", "waste", "worst", "wrong"
}
NEGATIONS = {"not", "never", "no", "hardly", "isn't", "wasn't", "don't", "didn't"}

def analyze_sentiment(text: str) -> dict:
    """Return sentiment label, score, confidence estimate and matched words."""
    words = [w.strip(".,!?;:()[]{}\"'").lower() for w in text.split()]
    positive_found, negative_found = [], []
    score = 0
    for index, word in enumerate(words):
        previous = words[max(0, index - 2):index]
        negated = any(item in NEGATIONS for item in previous)
        if word in POSITIVE_WORDS:
            positive_found.append(word)
            score += -1 if negated else 1
        elif word in NEGATIVE_WORDS:
            negative_found.append(word)
            score += 1 if negated else -1

    if score > 0:
        sentiment = "Positive"
    elif score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    evidence = len(positive_found) + len(negative_found)
    confidence = 55 if evidence == 0 else min(95, 55 + int(abs(score) * 12) + evidence * 4)
    if sentiment == "Neutral":
        confidence = 60 if evidence == 0 else 65

    if sentiment == "Positive":
        explanation = "The text contains more positive expressions than negative ones."
    elif sentiment == "Negative":
        explanation = "The text contains more negative expressions than positive ones."
    else:
        explanation = "The text is balanced or contains no words from the demo vocabulary."

    return {
        "sentiment": sentiment,
        "score": score,
        "confidence": confidence,
        "positive_words": sorted(set(positive_found)),
        "negative_words": sorted(set(negative_found)),
        "explanation": explanation
    }

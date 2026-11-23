"""Summary calculations and Matplotlib visualisations."""
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt

def sentiment_summary(records: list) -> dict:
    counts = Counter(str(item.get("sentiment", "Neutral")) for item in records)
    total = len(records)
    positive, negative, neutral = counts["Positive"], counts["Negative"], counts["Neutral"]
    return {
        "total": total, "positive": positive, "negative": negative, "neutral": neutral,
        "positive_pct": round(positive * 100 / total) if total else 0,
        "negative_pct": round(negative * 100 / total) if total else 0
    }

def create_sentiment_chart(records: list):
    summary = sentiment_summary(records)
    labels = ["Positive", "Negative", "Neutral"]
    values = [summary["positive"], summary["negative"], summary["neutral"]]
    fig, ax = plt.subplots(figsize=(6, 4), facecolor="#ffffff")
    ax.set_facecolor("#ffffff")
    if sum(values) == 0:
        ax.text(.5, .5, "No reviews yet", ha="center", va="center", color="#777")
        ax.axis("off")
    else:
        ax.pie(values, labels=labels, autopct="%1.0f%%", startangle=90,
               wedgeprops={"width": .42, "edgecolor": "white", "linewidth": 3},
               textprops={"color": "#30334a", "fontsize": 10})
        ax.set_title("Sentiment distribution", color="#29264f", pad=14, fontsize=13, fontweight="bold")
    fig.tight_layout()
    return fig

def create_timeline_chart(records: list):
    fig, ax = plt.subplots(figsize=(6, 4), facecolor="#ffffff")
    ax.set_facecolor("#ffffff")
    dates = []
    for item in records:
        try:
            dates.append(datetime.strptime(str(item.get("date", ""))[:10], "%Y-%m-%d").date())
        except ValueError:
            pass
    if not dates:
        ax.text(.5, .5, "No activity data yet", ha="center", va="center", color="#777")
        ax.axis("off")
    else:
        from collections import Counter
        counts = Counter(dates)
        ordered = sorted(counts.items())
        ax.plot([str(x[0]) for x in ordered], [x[1] for x in ordered],
                marker="o", linewidth=2.5, markersize=7)
        ax.fill_between(range(len(ordered)), [x[1] for x in ordered], alpha=.12)
        ax.set_ylabel("Reviews saved")
        ax.set_title("Review activity", color="#29264f", pad=14, fontsize=13, fontweight="bold")
        ax.tick_params(axis="x", rotation=25, labelsize=8)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", alpha=.2)
    fig.tight_layout()
    return fig

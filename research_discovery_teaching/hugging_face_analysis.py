import pandas as pd
import numpy as np
from transformers import pipeline

df = pd.read_csv("COM212_question4_cleaned.csv")

emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

def get_emotion_scores(text):
    if pd.isna(text):
        return np.nan
    results = emotion_classifier(text)[0]
    return {item['label']: round(item['score'], 4) for item in results}

df['emotion_scores'] = df['clean'].apply(get_emotion_scores)

emotion_df = df['emotion_scores'].apply(pd.Series)

df = pd.concat([df, emotion_df], axis=1)

df['dominant_emotion'] = emotion_df.idxmax(axis=1)

df.to_csv("COM212_q4_emotions.csv", index=False)

print(df[['clean', 'dominant_emotion'] + list(emotion_df.columns)].head())

from transformers import pipeline

print("=" * 50)
print("Hugging Face Text Analyzer")
print("=" * 50)

classifier = pipeline(
    task="sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

emotion_classifier = pipeline(
    task="text-classification",
    model="j-hartmann/emotion-english-distilroberta-base"
)
text = input("\nEnter text: ")

result = classifier(text)

sentiment = classifier(text)[0]
emotion = emotion_classifier(text)[0]

print("\n" + "=" * 50)
print("Analysis Result")
print("=" * 50)

print("\nSentiment")
print(f"Label      : {sentiment['label']}")
print(f"Confidence : {sentiment['score']:.4f}")

print("\nEmotion")
print(f"Label      : {emotion['label']}")
print(f"Confidence : {emotion['score']:.4f}")
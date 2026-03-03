from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

class SentimentAnalyzer:
    def __init__(self):
        self.tokenizer=AutoTokenizer.from_pretrained(
            "cardiffnlp/twitter-roberta-base-sentiment"
            )
        
        self.model=AutoModelForSequenceClassification.from_pretrained(
            "cardiffnlp/twitter-roberta-base-sentiment"
            )
        
    import torch.nn.functional as F

    def analyze(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True)
        outputs = self.model(**inputs)
    
        probs = F.softmax(outputs.logits, dim=-1)[0]
    
        predicted_index = probs.argmax().item()
        confidence = probs[predicted_index].item()
    
        labels = ["Negative", "Neutral", "Positive"]
    
        return {
            "label": labels[predicted_index],
            "confidence": confidence,
            "negative_score": probs[0].item(),
            "neutral_score": probs[1].item(),
            "positive_score": probs[2].item(),
        }
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class TextPreprocessor:
    def __init__(self, language="spanish", extra_stopwords=None):
        nltk.download("stopwords")
        self.stemmer = SnowballStemmer(language)
        self.stopwords = set(stopwords.words(language))
        
        if extra_stopwords:
            self.stopwords.update(extra_stopwords)
    
    def preprocess_text(self, text):
        '''
        Preprocess a text by removing punctuation, numbers, special characters, and stopwords.
        Tokenize the text and convert it to lowercase.
        '''
        if not isinstance(text, str):
            return ""
        
        text = re.sub(r'[^a-zA-Záéíóúüñ\s]', '', text)  # Remove punctuation, numbers, special characters
        words = text.lower().split()  # Tokenize and convert to lowercase
        processed_words = [self.stemmer.stem(word) for word in words if word not in self.stopwords]
        
        return " ".join(processed_words)
    
    @staticmethod
    def generate_wordcloud(text, title):
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(text))
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title(title, fontsize=14)
        plt.show()

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

def load_and_vectorize(csv_path):
    df = pd.read_csv(csv_path)
    X = df['message_text']
    y = df['label']
    
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    X_vec = vectorizer.fit_transform(X)
    
    # Save the vectorizer so we can use it later for new messages
    with open('vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
        
    return X_vec, y
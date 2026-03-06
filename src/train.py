from sklearn.linear_model import LogisticRegression
from preprocess import load_and_vectorize
import pickle

def train_model():
    print("Loading data and vectorizing...")
    X_vec, y = load_and_vectorize('../data/dataset.csv')
    
    print("Training Logistic Regression model...")
    model = LogisticRegression()
    model.fit(X_vec, y)
    
    # Save the trained model to disk
    with open('scam_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Model saved successfully!")

if __name__ == "__main__":
    train_model()
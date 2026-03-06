import pickle

def predict_message(message):
    # Load the saved model and vectorizer
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    with open('scam_model.pkl', 'rb') as f:
        model = pickle.load(f)
        
    # Vectorize the incoming text
    vec_message = vectorizer.transform([message])
    
    # Predict
    prediction = model.predict(vec_message)[0]
    return prediction

if __name__ == "__main__":
    test_msg = "Your UPI has been restricted. Click here to verify KYC immediately."
    print(f"Message: '{test_msg}'")
    print(f"Prediction: {predict_message(test_msg)}")
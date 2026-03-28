from pipeline.scam_detector.detector import process_message

if __name__ == "__main__":
    print("🛡️ ScamGuard AI CLI")
    test_msg = input("Enter a message to analyze: ")
    result = process_message(test_msg)
    print("\n--- Final Analysis ---")
    print(result)
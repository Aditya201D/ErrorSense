import joblib

model = joblib.load(
    "model/error_classifier.pkl"
)

print("Model loaded.")

while True:

    message = input("\nEnter error message: ")

    if message.lower() == "exit":
        break

    prediction = model.predict([message])[0]

    print("\nPredicted Category:")
    print(prediction)
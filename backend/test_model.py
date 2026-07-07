import joblib

model = joblib.load(
    "model/error_classifier.pkl"
)

print("Model loaded.")

while True:

    request = input("\nRequest: ")
    response = input("Response: ")

    if (
        request.lower() == "exit"
        or response.lower() == "exit"
    ):
        break

    combined_text = (
        f"REQUEST:\n{request}\n\nRESPONSE:\n{response}"
    )

    prediction = model.predict(
        [combined_text]
    )[0]

    print("\nPredicted Category:")
    print(prediction)
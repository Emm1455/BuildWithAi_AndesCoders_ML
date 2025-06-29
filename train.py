import pandas as pd
from google.cloud import storage
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier

BUCKET = "my-ml-data-bucket-ods"
BLOB = "training_data.csv"
LOCAL_FILE = "/tmp/training_data.csv"

def download_csv():
    client = storage.Client()
    bucket = client.bucket(BUCKET)
    blob = bucket.blob(BLOB)
    blob.download_to_filename(LOCAL_FILE)

def train_model():
    download_csv()
    df = pd.read_csv(LOCAL_FILE)
    X = df[["humidity", "temperature"]]
    y = df[["motor_1", "motor_2"]]

    model = MultiOutputClassifier(RandomForestClassifier())
    model.fit(X, y)

    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)

if __name__ == "__main__":
    train_model()
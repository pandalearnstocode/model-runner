import pandas as pd
import pathlib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf

tf.random.set_seed(42)


def _get_directory_path():
    return pathlib.Path(__file__).parent.resolve()


def _load_data(
    env="develop", data_dir="data", io_type="input", file_name="modelling_data.csv"
):
    dir_path = _get_directory_path()
    file_path = os.path.join(
        os.path.join(os.path.join(os.path.join(dir_path, env), data_dir), io_type),
        file_name,
    )
    return pd.read_csv(file_path)


def _preprocess_data(df):
    df = df.dropna()
    df["is_white_wine"] = [1 if typ == "white" else 0 for typ in df["type"]]
    df = df.drop("type", axis=1)
    df["is_good_wine"] = [1 if quality >= 6 else 0 for quality in df["quality"]]
    df = df.drop("quality", axis=1)
    return df


def _get_train_test_data(df):
    X = df.drop("is_good_wine", axis=1)
    y = df["is_good_wine"]
    return train_test_split(X, y, test_size=0.2, random_state=42)


def _scale_data(X_train, X_test, scaler=StandardScaler()):
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled


def _get_model():
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(256, activation="relu"),
            tf.keras.layers.Dense(256, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ]
    )
    model.compile(
        loss=tf.keras.losses.binary_crossentropy,
        optimizer=tf.keras.optimizers.Adam(lr=0.03),
        metrics=[
            tf.keras.metrics.BinaryAccuracy(name="accuracy"),
            tf.keras.metrics.Precision(name="precision"),
            tf.keras.metrics.Recall(name="recall"),
        ],
    )
    return model


def _train_model(model, X_train_scaled, y_train):
    history = model.fit(X_train_scaled, y_train, epochs=10)
    return history, model


def _save_model(model, model_name="iris_model"):
    dir_path = _get_directory_path()
    model.save(os.path.join(dir_path, model_name))

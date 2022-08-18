from loguru import logger
import typer
import pandas as pd
import pathlib
import os
import joblib
from train import (
    _preprocess_data,
    _get_train_test_data,
    _scale_data,
    _get_model,
    _train_model,
)
import numpy as np

app = typer.Typer()


def upload_model(model_directory="model_object", env="develop", model_name="mmm_model"):
    logger.info(f"Uploading model to blob, env name: {env}...")
    logger.info(f"Environment: {env}")
    logger.info(f"Model directory: {model_directory}")
    logger.info(f"Model name: {model_name}")
    return True


def _get_directory_path():
    return pathlib.Path(__file__).parent.resolve()


def _load_data(
    env="develop", data_dir="data", io_type="input", file_name="modelling_data.csv"
):
    dir_path = _get_directory_path()
    file_path = os.path.join(dir_path, env, data_dir, io_type, file_name)
    return pd.read_csv(file_path)


def _save_model(
    model, model_directory="model_object", env="develop", model_name="mmm_model"
):
    dir_path = _get_directory_path()
    model.save(os.path.join(dir_path, env, model_directory, model_name))
    return True


def check_data(
    env: str, country: str, brand: str, year: str, period: str, period_value: int
):
    logger.info(f"Checking data if data exists or not in {env}...")
    logger.info(f"Environment: {env}")
    logger.info(f"Country: {country}")
    logger.info(f"Brand: {brand}")
    logger.info(f"Year: {year}")
    logger.info(f"Period: {period}")
    logger.info(f"Period value: {period_value}")
    return False


def download_data(
    env: str, country: str, brand: str, year: str, period: str, period_value: int
):
    logger.info(f"Downloading data from blob, env name: {env}...")
    logger.info(f"Environment: {env}")
    logger.info(f"Country: {country}")
    logger.info(f"Brand: {brand}")
    logger.info(f"Year: {year}")
    logger.info(f"Period: {period}")
    logger.info(f"Period value: {period_value}")
    return pd.read_csv("data.csv")


def generate_model_output(
    env: str,
    country: str,
    brand: str,
    year: str,
    period: str,
    period_value: int,
    model_name: str,
    rc_level: str,
):
    logger.info(f"Generating model output, env name: {env}...")
    logger.info(f"Environment: {env}")
    logger.info(f"Country: {country}")
    logger.info(f"Brand: {brand}")
    logger.info(f"Year: {year}")
    logger.info(f"Period: {period}")
    logger.info(f"Period value: {period_value}")
    logger.info(f"Model name: {model_name}")
    logger.info(f"RC level: {rc_level}")
    roi_curves = pd.DataFrame(
        np.random.randint(0, 100, size=(100, 4)), columns=list("ABCD")
    )
    weekly_decomps = pd.DataFrame(
        np.random.randint(0, 100, size=(100, 4)), columns=list("ABCD")
    )
    roi_warehouse = pd.DataFrame(
        np.random.randint(0, 100, size=(100, 4)), columns=list("ABCD")
    )
    roi_facts = pd.DataFrame(
        np.random.randint(0, 100, size=(100, 4)), columns=list("ABCD")
    )
    imp_level_response_curve_brand = pd.DataFrame(
        np.random.randint(0, 100, size=(100, 4)), columns=list("ABCD")
    )
    imp_level_response_curve_country = pd.DataFrame(
        np.random.randint(0, 100, size=(100, 4)), columns=list("ABCD")
    )
    return (
        True,
        roi_curves,
        weekly_decomps,
        roi_warehouse,
        roi_facts,
        imp_level_response_curve_brand,
        imp_level_response_curve_country,
    )


def upload_model_results(env, data_dir, io_type, model_name, model_output_dfs):
    dir_path = _get_directory_path()
    base_path = os.path.join(dir_path, env, data_dir, io_type)
    for k, v in model_output_dfs.items():
        file_path = os.path.join(base_path, f"{model_name}_{k}.csv")
        logger.info(f"Uploading file in blob location: {file_path}")
    return True


def save_model_results(env, data_dir, io_type, model_name, model_output_dfs):
    dir_path = _get_directory_path()
    base_path = os.path.join(dir_path, env, data_dir, io_type)
    for k, v in model_output_dfs.items():
        file_path = os.path.join(base_path, f"{model_name}_{k}.csv")
        v.to_csv(file_path)
        logger.info(f"Saving file in local location: {file_path}")
    return True


@app.command()
def run_modelling(
    env: str = "develop",
    country="all",
    brand: str = "skol",
    rc_level: str = "brand",
    year: int = 2020,
    period: str = "monthly",
    period_value: int = 1,
    commit_id: str = "commit_hash",
):
    logger.info(f"Running MMM for {env}")
    logger.info(f"Country: {country}")
    logger.info(f"Brand: {brand}")
    logger.info(f"RC level: {rc_level}")
    logger.info(f"Year: {year}")
    logger.info(f"Period: {period}")
    logger.info(f"Period value: {period_value}")
    data_status = check_data(env, country, brand, year, period, period_value)
    if data_status:
        logger.info("Data exists.....")
    else:
        logger.warning("Data does not exists!!!!")
        data = download_data(env, country, brand, year, period, period_value)
        data.to_csv(f"{env}/data/input/modelling_data.csv")
    df = _load_data(
        env=env, data_dir="data", io_type="input", file_name="modelling_data.csv"
    )
    data_id = joblib.hash(df)
    logger.info(f"Data hash: {data_id}.")
    logger.info(f"Loaded {len(df)} rows...")
    iris_processed = _preprocess_data(df)
    logger.info(f"Preprocessed {len(iris_processed)} rows...")
    X_train, X_test, y_train, y_test = _get_train_test_data(iris_processed)
    logger.info(f"Train test split created data....")
    X_train_scaled, X_test_scaled = _scale_data(X_train, X_test)
    logger.info(f"Data scaling done...")
    model = _get_model()
    logger.info(f"Model creation compleat....")
    history, model = _train_model(model, X_train_scaled, y_train)
    logger.info(f"Trained model....")
    model_name = f"{commit_id}_{data_id}_{country}_{brand}_{rc_level}_{year}_{period}_{period_value}"
    save_model_status = _save_model(
        model=model, model_name=model_name, model_directory="model_object", env=env
    )
    if save_model_status:
        logger.info(f"Saved model....")
    else:
        logger.warning(f"Failed to save model....")
    upload_status = upload_model(
        model_name=model_name, model_directory="model_object", env=env
    )
    if upload_status:
        logger.info(f"Uploaded model....")
    else:
        logger.warning(f"Failed to upload model....")
    (
        model_output_status,
        roi_curves,
        weekly_decomps,
        roi_warehouse,
        roi_facts,
        imp_level_response_curve_brand,
        imp_level_response_curve_country,
    ) = generate_model_output(
        env=env,
        country=country,
        brand=brand,
        year=year,
        period=period,
        period_value=period_value,
        model_name=model_name,
        rc_level=rc_level,
    )
    if model_output_status:
        logger.info(f"Generated model output....")
    else:
        logger.warning(f"Failed to generate model output....")
    model_output_dfs = {
        "roi_curves": roi_curves,
        "weekly_decomps": weekly_decomps,
        "roi_warehouse": roi_warehouse,
        "roi_facts": roi_facts,
        "imp_level_response_curve_brand": imp_level_response_curve_brand,
        "imp_level_response_curve_country": imp_level_response_curve_country,
    }
    upload_status = upload_model_results(
        env=env,
        data_dir="data",
        io_type="output",
        model_name=model_name,
        model_output_dfs=model_output_dfs,
    )
    if upload_status:
        logger.info(f"Uploaded model output....")
    else:
        logger.warning(f"Failed to upload model output....")
    save_model_status = save_model_results(
        env=env,
        data_dir="data",
        io_type="output",
        model_name=model_name,
        model_output_dfs=model_output_dfs,
    )
    if save_model_status:
        logger.info(f"Saved model output....")
    else:
        logger.warning(f"Failed to save model output....")
    return True


@app.command()
def run_optimization(env:str = "develop", rc_id: str = "1_adfd10caf2b78e08a190fdb187ef5f24_us_skol_brand_2020_monthly_1"):
    logger.info(f"Running optimization for {rc_id}")
    logger.info("Loading RC for optimization....")
    rc_df = pd.read_csv(f"{env}/data/output/{rc_id}_roi_curves.csv")
    logger.info(f"Loaded {len(rc_df)} rows...")
    logger.info("Running optimization....")
    return True


@app.command()
def run_simulation(env:str = "develop", rc_id: str = "1_adfd10caf2b78e08a190fdb187ef5f24_us_skol_brand_2020_monthly_1"):
    logger.info(f"Running simulation for {rc_id}")
    logger.info("Loading RC for simulation....")
    rc_df = pd.read_csv(f"{env}/data/output/{rc_id}_roi_curves.csv")
    logger.info(f"Loaded {len(rc_df)} rows...")
    logger.info("Running simulation....")
    return True


if __name__ == "__main__":
    app()

import os
import sys
from dataclasses import dataclass
from typing import Any, Dict

import yaml
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException
from src.logger import logging


@dataclass
class HyperParamTunerConfig:
    """
    Configuration for the HyperparameterTuner.

    Attributes:
        param_file_path (str): Path to the YAML file containing hyperparameter grids.
    """

    param_file_path: str = os.path.join("config", "hyperparams.yaml")


class HyperparameterTuner:
    """
    Loads and applies hyperparameter tuning using GridSearchCV for supported models.
    """

    def __init__(self):
        self.config = HyperParamTunerConfig()

    def load_param_grid(self) -> Dict[str, Dict[str, Any]]:
        """
        Loads the hyperparameter grid for all models from a YAML file.

        Returns:
            dict: Dictionary of hyperparameter grids for all models.
        """
        try:
            logging.info(
                f"📂 Loading hyperparameter grid from: {self.config.param_file_path}"
            )
            with open(self.config.param_file_path, "r") as file:
                param_grid = yaml.safe_load(file)
            logging.info("✅ Hyperparameter grid loaded successfully.")
            return param_grid
        except Exception as e:
            logging.error("❌ Failed to load hyperparameter grid.")
            raise CustomException(e, sys)

    def tune_model(self, model_name: str, model_obj, X_train, y_train, X_test, y_test):
        """
        Tunes the hyperparameters for a specific model using GridSearchCV.

        Args:
            model_name (str): Name of the model.
            model_obj: The model object to be tuned.
            X_train (array-like): Training features.
            y_train (array-like): Training labels.
            X_test (array-like): Test features.
            y_test (array-like): Test labels.

        Returns:
            tuple: (best_model, r2_score)
        """
        try:
            logging.info(f"🔍 Tuning hyperparameters for: {model_name}")
            param_grid = self.load_param_grid().get(model_name)

            # Skip tuning if no parameters are defined
            if not param_grid:
                logging.warning(
                    f"⚠️ No parameters found for {model_name}, skipping tuning."
                )
                model_obj.fit(X_train, y_train)
                predictions = model_obj.predict(X_test)
                return model_obj, r2_score(y_test, predictions)

            # Perform grid search
            grid_search = GridSearchCV(
                estimator=model_obj,
                param_grid=param_grid,
                cv=3,
                n_jobs=-1,
                verbose=1,
                scoring="r2",
            )
            grid_search.fit(X_train, y_train)

            best_model = grid_search.best_estimator_
            predictions = best_model.predict(X_test)
            score = r2_score(y_test, predictions)

            logging.info(f"✅ Best score for {model_name}: {score:.4f}")
            logging.info(f"🏆 Best parameters: {grid_search.best_params_}")
            return best_model, score

        except Exception as e:
            logging.error(f"❌ Error tuning {model_name}")
            raise CustomException(e, sys)

import os
import sys
from dataclasses import dataclass
from datetime import datetime

import yaml
from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

from src.component.model_hyperparameter_tuning import HyperparameterTuner
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass
class ModelTrainerConfig:
    """
    Configuration class for setting the model file save path and model score save path.
    """

    model_file_path: str = os.path.join("artifacts", "model.pkl")
    model_scores_file_path: str = os.path.join("artifacts", "model_scores.yaml")


class ModelTrainer:
    """
    Handles model training, hyperparameter tuning, model evaluation,
    and saving of the best model and model scores.
    """

    def __init__(self):
        self.config = ModelTrainerConfig()
        self.tuner = HyperparameterTuner()

    def initiate_model_training(self, train_array, test_array):
        """
        Trains multiple models with hyperparameter tuning and selects the best model
        based on R² score. Saves the best model and leaderboard of all scores.

        Args:
            train_array (np.ndarray): Training dataset including features and target.
            test_array (np.ndarray): Testing dataset including features and target.

        Returns:
            tuple: (best_model, best_score, best_model_name)
        """
        try:
            logging.info("⏳ Starting model training pipeline...")

            # Split the train and test arrays into features and targets
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            # Define candidate models
            models = {
                "RandomForest": RandomForestRegressor(),
                "DecisionTree": DecisionTreeRegressor(),
                "LinearRegression": LinearRegression(),
                #                "XGBRegressor": XGBRegressor(),
                "CatBoost": CatBoostRegressor(verbose=0),
                "KNeighbors": KNeighborsRegressor(),
                "AdaBoost": AdaBoostRegressor(),
                "GradientBoosting": GradientBoostingRegressor(),
            }

            model_scores = {}
            best_model = None
            best_score = float("-inf")
            best_model_name = ""

            # Loop through models and tune each
            for name, model in models.items():
                tuned_model, score = self.tuner.tune_model(
                    name, model, X_train, y_train, X_test, y_test
                )
                model_scores[name] = score

                if score > best_score:
                    best_model = tuned_model
                    best_score = score
                    best_model_name = name

            logging.info("📊 Model tuning complete. Here's the leaderboard:")
            for model, score in model_scores.items():
                logging.info(f"{model}: {score:.4f}")

            # Save model leaderboard to file
            with open(self.config.model_scores_file_path, "w") as f:
                yaml.dump(model_scores, f)
            logging.info(
                f"📁 Model scores saved at: {self.config.model_scores_file_path}"
            )

            # Raise exception if no model is suitable
            if best_score < 0.6:
                raise CustomException("No suitable model found with R² > 0.6")

            logging.info(f"🏆 Best Model: {best_model_name} (R² = {best_score:.4f})")

            # Add timestamp and model name to model file name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            model_file_path = self.config.model_file_path.replace(
                "model.pkl", f"model_{best_model_name}_{timestamp}.pkl"
            )

            # Save the best model
            save_object(
                file_path=model_file_path,
                obj=best_model,
            )

            logging.info(f"✅ Best model saved at: {model_file_path}")
            return best_model, best_score, best_model_name

        except Exception as e:
            logging.error("❌ Model training failed.")
            raise CustomException(e, sys)

        finally:
            logging.info("🔚 Model training pipeline finished.")

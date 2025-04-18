import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    """
    Configuration class that holds the path where the preprocessor object will be saved.
    """

    preprocessor_object_file_path: str = os.path.join("artifacts", "preprocessor.pkl")


class DataTransformation:
    """
    Handles all data transformation steps:
    - Missing value imputation
    - Feature scaling
    - Categorical encoding
    """

    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        Creates preprocessing pipelines for both numerical and categorical features.

        Returns:
            preprocessor (ColumnTransformer): Combined transformer for preprocessing
        """
        try:
            logging.info("🔧 Creating preprocessing pipelines...")

            # Define feature types
            numerical_columns = ["writing score", "reading score"]
            categorical_columns = [
                "gender",
                "race/ethnicity",
                "parental level of education",
                "lunch",
                "test preparation course",
            ]

            # Pipeline for numerical features
            numerical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]
            )

            # Pipeline for categorical features
            categorical_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("encoder", OneHotEncoder(handle_unknown="ignore")),
                    (
                        "scaler",
                        StandardScaler(with_mean=False),
                    ),  # Avoid dense matrix warning
                ]
            )

            # Combine both into a single transformer
            preprocessor = ColumnTransformer(
                transformers=[
                    ("numerical_pipeline", numerical_pipeline, numerical_columns),
                    ("categorical_pipeline", categorical_pipeline, categorical_columns),
                ]
            )

            logging.info("✅ Preprocessor object created successfully.")
            return preprocessor

        except Exception as e:
            logging.error("❌ Failed to create preprocessor.")
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path: str, test_path: str):
        """
        Applies preprocessing to train and test datasets and returns transformed arrays.

        Args:
            train_path (str): Path to training data CSV
            test_path (str): Path to testing data CSV

        Returns:
            tuple: (train_array, test_array, preprocessor_path)
        """
        try:
            logging.info("📥 Reading train and test data...")
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("🔧 Preparing transformation pipeline...")
            preprocessor = self.get_data_transformer_object()

            target_column = "math score"
            columns_to_drop = [target_column]

            if "Unnamed: 0" in train_df.columns:
                columns_to_drop.append("Unnamed: 0")

            # Split features and targets
            input_features_train = train_df.drop(columns=columns_to_drop, axis=1)
            target_feature_train = train_df[target_column]

            input_features_test = test_df.drop(columns=columns_to_drop, axis=1)
            target_feature_test = test_df[target_column]

            logging.info("⚙️ Transforming datasets...")
            input_features_train_array = preprocessor.fit_transform(
                input_features_train
            )
            input_features_test_array = preprocessor.transform(input_features_test)

            # Combine transformed features with target
            train_array = np.c_[input_features_train_array, target_feature_train]
            test_array = np.c_[input_features_test_array, target_feature_test]

            logging.info(
                "✅ Transformation complete. Ready to save preprocessor separately."
            )
            save_object(
                file_path=self.data_transformation_config.preprocessor_object_file_path,
                obj=preprocessor,
            )
            logging.info("✅ Preprocessor object saved successfully.")
            return (
                train_array,
                test_array,
                self.data_transformation_config.preprocessor_object_file_path,
            )

        except Exception as e:
            logging.error("❌ Error occurred during data transformation.")
            raise CustomException(e, sys)

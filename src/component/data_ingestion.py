import os
import sys
from dataclasses import dataclass

import pandas as pd
from sklearn.model_selection import train_test_split

from src.component.data_transformation import (
    DataTransformation,
)
from src.component.model_trainer import ModelTrainer
from src.exception import CustomException
from src.logger import logging


@dataclass
class DataIngestionConfig:
    """
    Configuration class for data ingestion paths.
    Stores paths where raw, train, and test data will be saved.
    """

    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    raw_data_path: str = os.path.join("artifacts", "data.csv")


class DataIngestion:
    """
    Handles the full data ingestion process:
    - Reads raw data
    - Saves a raw backup
    - Splits into train/test sets
    - Saves the processed data
    """

    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        """
        Orchestrates the data ingestion process.
        Reads dataset, saves a raw copy, splits it into train/test,
        and saves those sets to disk.

        Returns:
            Tuple[str, str]: Paths to the train and test data files.
        """
        logging.info("⏳ Starting the data ingestion process...")

        try:
            # Step 1: Load the dataset
            df = pd.read_csv("notebook/data/StudentsPerformance.csv")
            logging.info("✅ Successfully loaded dataset into DataFrame.")

            # Step 2: Ensure the artifacts directory exists
            os.makedirs(
                os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True
            )
            logging.info("📂 Ensured that artifacts directory exists.")

            # Step 3: Save the raw data for backup or debugging
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info(
                f"💾 Raw dataset saved at: {self.ingestion_config.raw_data_path}"
            )

            # Step 4: Split data into train and test sets
            logging.info("✂️ Splitting data into train and test sets...")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Step 5: Save the split datasets
            train_set.to_csv(
                self.ingestion_config.train_data_path, index=False, header=True
            )
            test_set.to_csv(
                self.ingestion_config.test_data_path, index=False, header=True
            )
            logging.info(
                f"✅ Train/Test split complete. Train at: {self.ingestion_config.train_data_path}, Test at: {self.ingestion_config.test_data_path}"
            )

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )

        except Exception as e:
            logging.error("❌ An error occurred during data ingestion.")
            raise CustomException(e, sys) from e


# Entry point of the script (only runs when executed directly)
if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    logging.info("📥 Data ingestion completed. Now starting data transformation...")
    data_transformation = DataTransformation()
    logging.info("🔧 Initiating data transformation...")
    train_array, test_array, _ = data_transformation.initiate_data_transformation(
        train_data, test_data
    )
    logging.info(
        f"✅ Data transformation complete. Train array shape: {train_array.shape}, Test array shape: {test_array.shape}"
    )
    model_trainer = ModelTrainer()
    print(model_trainer.initiate_model_training(train_array, test_array))
    print(f"Model trained and saved at: {model_trainer.config.model_file_path}")
    logging.info("🔄 Data transformation pipeline completed.")

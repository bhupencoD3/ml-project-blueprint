import sys

import pandas as pd

from src.exception import CustomException
from src.logger import logging
from src.utils import load_object


class PredictPipeline:
    """
    Pipeline to load pre-trained model and preprocessor,
    and make predictions on incoming feature data.
    """

    def __init__(self):
        # No initialization needed right now, but keeping it for structure
        pass

    def predict(self, features):
        """
        Accepts raw feature data, preprocesses it, and returns predictions.

        Args:
            features (pd.DataFrame or dict): Input feature data

        Returns:
            predictions (np.ndarray): Predicted values (e.g., math scores)
        """
        try:
            # Paths to the saved model and preprocessor artifacts
            model_path = "artifacts/model.pkl"
            preprocessor_path = "artifacts/preprocessor.pkl"

            # Load the preprocessor and model
            model = load_object(file_path=model_path)
            model_input = load_object(file_path=preprocessor_path)

            # Convert input data to DataFrame
            data_frame = pd.DataFrame(features)

            # Preprocess the input
            data_frame = model_input.transform(data_frame)

            # Generate predictions
            predictions = model.predict(data_frame)

            logging.info("Prediction successful")
            return predictions

        except Exception as e:
            logging.info("Error occurred in prediction")
            raise CustomException(e, sys)


class CustomData:
    """
    Structure for incoming data from the user.
    Converts raw form inputs into a format ready for the model.
    """

    def __init__(
        self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education,
        lunch: str,
        test_course: str,
        reading_score: float,
        writing_score: float,
    ):
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_course = test_course
        self.reading_score = reading_score
        self.writing_score = writing_score

    def get_data_as_dataframe(self):
        """
        Converts class fields into a single-row pandas DataFrame,
        formatted exactly as required by the model pipeline.

        Returns:
            pd.DataFrame: A one-row DataFrame ready for prediction.
        """
        try:
            custom_data_input_dict = {
                "gender": [self.gender],
                "race/ethnicity": [self.race_ethnicity],
                "parental level of education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test preparation course": [self.test_course],
                "reading score": [self.reading_score],
                "writing score": [self.writing_score],
            }

            df = pd.DataFrame(custom_data_input_dict)
            logging.info("DataFrame created from user input")
            return df

        except Exception as e:
            logging.info("Error occurred in get_data_as_dataframe")
            raise CustomException(e, sys)

        finally:
            logging.info("Exiting get_data_as_dataframe method")

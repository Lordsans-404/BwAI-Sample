"""
Train an ML model on Iris dataset
"""
import os
import pathlib
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb
import numpy as np
from dataclasses import dataclass

from src.utils.loader import load_config, load_data





ROOT = pathlib.Path(__file__).parent.parent.parent

@dataclass
class IrisModel:
    """
    Train a Logistic Regression model on the Iris dataset
    """
    config_path:os.PathLike

    def __post_init__(self):
        self.config = load_config(self.config_path)
        self.model = None
        self.best_params = None
        self.hypar_params = None

    def model_dict(self, model_name: str):
        self.models = {
            "LogisticRegression": LogisticRegression,
            "RandomForest": RandomForestClassifier,
            "XGBoost": xgb.XGBClassifier, 
            "DecisionTree": DecisionTreeClassifier
        }
        return self.models.get(model_name, LogisticRegression)
    
    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Trains the model on the input data.

        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            The input data.
        y : array-like of shape (n_samples,)
            The target values.
        """
        try:
            model_name = self.config['model']['classifier']
            ModelClass = self.model_dict(model_name)
            self.model = ModelClass()
            self.model.fit(X, y)

            print(f"Model {model_name} trained successfully.")
        except Exception as e:
            print(f"Error during model training: {e}")


    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predicts the target values for the input data.

        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            The input data.

        Returns:
        --------
        y : array-like of shape (n_samples,)
        """
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predicts the class probabilities for the input data.

        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            The input data.

        Returns:
        --------
        y_proba : array-like of shape (n_samples, n_classes)
        """
        return self.model.predict_proba(X)

    def save(self, model_path: os.PathLike) -> None:
        """
        Saves the model to disk.

        Parameters:
        -----------
        model_path : os.PathLike
            The path to save the model.
        """
        joblib.dump(self.model, model_path)

    def load(self, model_path: os.PathLike):
        """
        Loads the model from disk.
        """
        self.model = joblib.load(model_path)
        return self.model
    

def main():
    
    config_path = os.path.join(ROOT, "config", "main.yml") 

    
    # Model instantiation
    model = IrisModel(config_path=config_path)

    # Load data
    X_train, y_train = load_data(
        data_path=model.config['data']['data_path'],
        is_train=True,
        test_size=model.config['data']['test_size'],
        random_state=model.config['data']['random_state']
    )

    # Train the model
    model.train(X_train, y_train)

    # Save the model
    model_dir = model.config['model']['model_dir']
    model_name = model.config['model']['classifier']
    model_path = os.path.join(ROOT, model_dir, f"{model_name}_model.joblib")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    model.save(model_path)
    print(f"Model saved at {model_path}")

    # Test prediction
    X_test, y_test = load_data(
        data_path=model.config['data']['data_path'],
        is_train=False,
        test_size=model.config['data']['test_size'],
        random_state=model.config['data']['random_state']
    )
    predictions = model.predict(X_test)
    
    # Accuracy
    accuracy = np.mean(predictions == y_test)
    print(f"Test Accuracy: {accuracy * 100:.2f}%")

if __name__ == "__main__":
    main()
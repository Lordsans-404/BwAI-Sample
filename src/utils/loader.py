import yaml
import pandas as pd
from sklearn.model_selection import train_test_split
import pathlib

ROOT = pathlib.Path(__file__).parent.parent.parent

def load_config(config_path: str) -> dict:
    """
    Loads a YAML configuration file.

    Parameters:
    -----------
    config_path : str
        The path to the YAML configuration file.

    Returns:
    --------
    config : dict
        The configuration as a dictionary.
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config   

def load_data(data_path: str, is_train: bool = True, test_size: float = 0.2, random_state: int = 42, get_all: bool = False, original: bool = False):
    """
    Loads data from a CSV file.

    Parameters:
    -----------
    data_path : str
        The path to the CSV data file.

    Returns:
    --------
    X, y : np.ndarray, np.ndarray
        The features and target arrays
    """
    if get_all:
        df =  pd.read_csv(data_path)
        if original:
            return df
        X = df.drop(columns=['species']).values
        # ecode species labels
        species_mapping = {species: idx for idx, species in enumerate(df['species'].unique())}
        df['species'] = df['species'].map(species_mapping)
        y = df['species'].values
        return X, y
    
    # Load the data
    data = pd.read_csv(data_path)

    train_data, test_data = train_test_split(data, test_size=test_size, random_state=random_state)

    # encode species labels
    species_mapping = {species: idx for idx, species in enumerate(data['species'].unique())}
    train_data['species'] = train_data['species'].map(species_mapping)
    test_data['species'] = test_data['species'].map(species_mapping)
    
    X_train = train_data.drop(columns=['species']).values
    y_train = train_data['species'].values
    X_test = test_data.drop(columns=['species']).values
    y_test = test_data['species'].values

    if is_train:
        return X_train, y_train
    else:
        return X_test, y_test

if __name__ == "__main__":
    # Example usage
    config = load_config('config/main.yml')
    
    data = load_data(
        data_path=config['data']['data_path'],
        test_size=config['data']['test_size'],
        random_state=config['data']['random_state']
    )
    print(data)
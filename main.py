import pathlib
import os
from fastapi import FastAPI
import joblib
from typing import List
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import uvicorn
import numpy as np
from src.utils.loader import load_data, load_config

ROOT = pathlib.Path(__file__).parent
config_path = os.path.join(ROOT, 'config', 'main.yml')
config = load_config(config_path)

app = FastAPI()
app.mount("/app", StaticFiles(directory="src/app", html=True), name="app")

# get the iris dataset
@app.get("/iris")
def get_iris_dataset():
    
    # load the iris dataset
    iris = load_data(config['data']['data_path'], get_all=True, original=True)
    
    return iris.to_dict(orient="records")

# load the pre-trained model
def load_model(config):
    model_path = config['model']['model_dir']
    model_path = os.path.join(ROOT, model_path, f"{config['app']['use_model']}_model.joblib")
    try:
        model = joblib.load(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        raise e
    return model

model = load_model(config)

# define the input data model
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


# define the prediction endpoint
@app.post("/predict", response_model=List[float])
async def predict(data: IrisInput):
    input_data = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]
    
    prediction = model.predict(np.array(input_data))
    pred_prob = model.predict_proba(input_data)
    
    return prediction[0], pred_prob.max() * 100

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
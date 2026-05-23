"""
Iris dataset pair plot
"""
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests

import os

# get the head data from fastapi endpoint /iris
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
url = f"{API_URL}/iris"
r = requests.get(url)
df = pd.DataFrame(r.json())

# darkgrid
sns.set_style("darkgrid")

# display the pair plot
st.title("Iris dataset pair plot")
fig, ax = plt.subplots()
fig = sns.pairplot(df, hue="species", kind="reg")
st.pyplot(fig)

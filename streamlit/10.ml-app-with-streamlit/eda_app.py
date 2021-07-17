import streamlit as st

import pandas as pd

import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import plotly.express as px

matplotlib.use("Agg")


@st.cache
def load_data(data):
    df = pd.read_csv(data)
    return df


def run_eda_app():
    st.subheader("Exploratory Data Analysis")
    df = load_data("data/diabetes_data_upload.csv")
    df_encoded = load_data("data/diabetes_data_upload_clean.csv")

    submenu = st.sidebar.selectbox("Submenu", ["Descriptive", "Plots"])
    if submenu == "Descriptive":
        st.dataframe(df)

        with st.beta_expander("Data Types"):
            st.dataframe(df.dtypes)

        with st.beta_expander("Descriptive Summary"):
            st.dataframe(df_encoded.describe())

        with st.beta_expander("Class Distribution"):
            st.dataframe(df['class'].value_counts())

        with st.beta_expander("Gender Distribution"):
            st.dataframe(df['Gender'].value_counts())
    elif submenu == "Plots":
        pass

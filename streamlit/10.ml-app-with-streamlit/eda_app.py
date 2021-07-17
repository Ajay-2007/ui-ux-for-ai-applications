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
    freq_df = load_data("data/freqdist_of_age_data.csv")

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
        st.subheader("Plots")

        col1, col2 = st.beta_columns([2, 1])

        with col1:
            # For Gender Distribution
            with st.beta_expander("Dist Plot of Gender"):
                # fig = plt.figure()
                # sns.countplot(df['Gender'])
                # st.pyplot(fig)

                gen_df = df['Gender'].value_counts().to_frame()
                gen_df = gen_df.reset_index()
                gen_df.columns = ["Gender Type", "Count"]

                p1 = px.pie(data_frame=gen_df,
                            names='Gender Type',
                            values='Count')
                st.plotly_chart(p1, use_container_width=True)

            # For Class Distribution
            with st.beta_expander("Dist Plot of Class"):
                fig = plt.figure()
                sns.countplot(df['class'])
                st.pyplot(fig)

            with col2:
                with st.beta_expander("Gender Distribution"):
                    st.dataframe(gen_df)

                with st.beta_expander("Class Distribution"):
                    st.dataframe(df['class'].value_counts())

            # Freq Dist
            with st.beta_expander("Frequency Dist of Age"):
                # st.dataframe(freq_df)
                p2 = px.bar(data_frame=freq_df,
                            x='Age',
                            y='count')
                st.plotly_chart(p2, use_container_width=True)

            # Outlier Detection
            with st.beta_expander("Outlier Detection Plot"):
                p3 = px.box(data_frame=df,
                            x='Age',
                            color='Gender')
                st.plotly_chart(p3, use_container_width=True)

            # Correlation
            with st.beta_expander("Correlation Plot"):
                corr_matrix = df_encoded.corr()
                fig = plt.figure(figsize=(20, 10))
                sns.heatmap(corr_matrix, annot=True)
                st.pyplot(fig)

                p4 = px.imshow(corr_matrix)
                st.plotly_chart(p4, use_container_width=True)

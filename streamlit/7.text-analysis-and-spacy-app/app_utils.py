# core packages
import streamlit as st

# Load NLP Packages
import spacy

from spacy import displacy
from textblob import TextBlob

import pandas as pd
from collections import Counter

# Data Visualization Packages
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

# File Processing Packages
import docx2txt
import pdfplumber
import base64

# utils
import time

timestr = time.strftime("%Y%m%d-%H%M%S")

matplotlib.use("Agg")

# Function to get Wordcloud
from wordcloud import WordCloud

nlp = spacy.load("en_core_web_sm")


# Functions
def text_analyzer(my_text):
    docx = nlp(my_text)
    all_data = [
        (
            token.text,
            token.shape_,
            token.pos_,
            token.tag_,
            token.lemma_,
            token.is_alpha,
            token.is_stop,
        )
        for token in docx
    ]
    df = pd.DataFrame(
        all_data,
        columns=["Token", "Shape", "Pos", "Tag", "Lemma", "IsAlpha", "Is_Stopword"],
    )
    return df


def get_entities(my_text):
    docx = nlp(my_text)
    entities = [(entity.text, entity.label_) for entity in docx.ents]
    return entities


HTML_WRAPPER = ""


# @st.cache
def render_entities(raw_text):
    docx = nlp(raw_text)
    html = displacy.render(docx, style="ent")
    html = html.replace("\n\n", "\n")
    # result = HTML_WRAPPER.format(html)
    return html


# Function to get most common tokens
def get_most_common_tokens(my_text, num=5):
    word_tokens = Counter(my_text.split())
    most_common_tokens = dict(word_tokens.most_common(num))
    return most_common_tokens


# Function to get Sentiment
def get_sentiment(my_text):
    blob = TextBlob(my_text)
    sentiment = blob.sentiment
    return sentiment


def plot_wordcloud(my_text):
    my_wordcloud = WordCloud().generate(my_text)
    fig = plt.figure()
    plt.imshow(my_wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(fig)


# Function to Download Text Analysis Results
def make_downloadable(data):
    csvfile = data.to_csv(index=False)
    b64 = base64.b64encode(csvfile.encode()).decode()
    new_filename = "nlp_result_{}_.csv".format(timestr)
    st.markdown("### ** Download CSV file **")
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click here !</a>'
    st.markdown(href, unsafe_allow_html=True)


# Function to read PDF
from PyPDF2 import PdfFileReader
import pdfplumber


def read_pdf(file):
    pdf_reader = PdfFileReader(file)
    count = pdf_reader.numPages
    all_page_text = ""
    for i in range(count):
        page = pdf_reader.getPage(i)
        all_page_text += page.extractText()

    return all_page_text


def read_pdf2(file):
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]
        return page.extract_text()

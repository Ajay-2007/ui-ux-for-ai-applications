import streamlit as st
import streamlit.components.v1 as stc

# Load EDA Packages
import pandas as pd

# Load NLP Packages
import spacy
from spacy import displacy
from textblob import TextBlob

# Text Cleaning Packages
import neattext as nt
import neattext.functions as nfx

# utils
from collections import Counter
import base64
import time

timestr = time.strftime('%Y%m%d-%H%M%S')

# Data Visualization Packages
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

# File Processing Packages
import docx2txt
import pdfplumber

matplotlib.use("Agg")

nlp = spacy.load('en_core_web_sm')


# Functions
def text_analyzer(my_text):
    docx = nlp(my_text)
    all_data = [(token.text, token.shape_, token.pos_, token.tag_, token.lemma_, token.is_alpha, token.is_stop)
                for token in docx]
    df = pd.DataFrame(all_data, columns=['Token', 'Shape', 'Pos', 'Tag', 'Lemma',
                                         'IsAlpha', 'Is_Stopword'])
    return df


def get_entities(my_text):
    docx = nlp(my_text)
    entities = [(entity.text, entity.label_) for entity in docx.ents]
    return entities


HTML_WRAPPER = ""


# @st.cache
def render_entities(raw_text):
    docx = nlp(raw_text)
    html = displacy.render(docx, style='ent')
    html = html.replace('\n\n', '\n')
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


# Function to get Wordcloud
from wordcloud import WordCloud


def plot_wordcloud(my_text):
    my_wordcloud = WordCloud().generate(my_text)
    fig = plt.figure()
    plt.imshow(my_wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(fig)


# Function to Download Text Analysis Results
def make_downloadable(data):
    csvfile = data.to_csv(index=False)
    b64 = base64.b64encode(csvfile.encode()).decode()
    new_filename = 'nlp_result_{}_.csv'.format(timestr)
    st.markdown('### ** Download CSV file **')
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


def main():
    st.title("NLP App with Streamlit")
    menu = ["Home", "NLP(files)", "About"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home: Analyse Text")
        raw_text = st.text_area("Enter Text Here")
        num_of_most_common = st.sidebar.number_input("Most Common Tokens", 5, 15)
        if st.button("Analyze"):
            with st.beta_expander("Original Text"):
                st.write(raw_text)

            with st.beta_expander("Text Analysis"):
                token_result_df = text_analyzer(raw_text)
                st.dataframe(token_result_df)

            with st.beta_expander("Entities"):
                # entity_result = get_entities(raw_text)
                # st.write(entity_result)

                entity_result = render_entities(raw_text)
                stc.html(entity_result, height=1000, scrolling=True)

            # Layout
            col1, col2 = st.beta_columns(2)
            with col1:
                with st.beta_expander("Word Stats"):
                    st.info("Word Statistics")
                    docx = nt.TextFrame(raw_text)
                    st.write(docx.word_stats())

                with st.beta_expander("Top Keywords"):
                    st.info("Top Keywords/Tokens")
                    processed_text = nfx.remove_stopwords(raw_text)
                    keywords = get_most_common_tokens(processed_text, num_of_most_common)
                    st.write(keywords)

                with st.beta_expander("Sentiment"):
                    sent_result = get_sentiment(my_text=raw_text)
                    st.write(sent_result)

            with col2:
                with st.beta_expander("Plot Word Freq"):
                    fig = plt.figure()
                    sns.countplot(token_result_df['Token'])
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

                with st.beta_expander("Plot Part of Speech"):
                    fig = plt.figure()
                    # sns.countplot(token_result_df['Pos'])
                    # plt.xticks(rotation=45)
                    top_keywords = get_most_common_tokens(processed_text, num_of_most_common)
                    plt.bar(top_keywords.keys(), top_keywords.values())
                    st.pyplot(fig)

                with st.beta_expander("Plot Wordcloud"):
                    plot_wordcloud(my_text=raw_text)

            with st.beta_expander("Download Text Analysis Results"):
                make_downloadable(token_result_df)

    elif choice == "NLP(files)":
        st.subheader("NLP Task")
        num_of_most_common = st.sidebar.number_input("Most Common Tokens", 5, 15)
        text_file = st.file_uploader("Upload Files", type=["pdf", "docx", "txt"])
        if text_file is not None:
            if text_file.type == 'application/pdf':
                raw_text = read_pdf(text_file)
                # st.write(raw_text)
            elif text_file.type == 'text/plain':
                # st.write(text_file.read()) # read as bytes
                raw_text = str(text_file.read(), encoding='utf-8')
                # st.write(raw_text)
            else:
                raw_text = docx2txt.process(text_file)
                # st.write(raw_text)

            if st.button("Analyze"):
                with st.beta_expander("Original Text"):
                    st.write(raw_text)

                with st.beta_expander("Text Analysis"):
                    token_result_df = text_analyzer(raw_text)
                    st.dataframe(token_result_df)

                with st.beta_expander("Entities"):
                    # entity_result = get_entities(raw_text)
                    # st.write(entity_result)

                    entity_result = render_entities(raw_text)
                    stc.html(entity_result, height=1000, scrolling=True)

                # Layout
                col1, col2 = st.beta_columns(2)
                with col1:
                    with st.beta_expander("Word Stats"):
                        st.info("Word Statistics")
                        docx = nt.TextFrame(raw_text)
                        st.write(docx.word_stats())

                    with st.beta_expander("Top Keywords"):
                        st.info("Top Keywords/Tokens")
                        processed_text = nfx.remove_stopwords(raw_text)
                        keywords = get_most_common_tokens(processed_text, num_of_most_common)
                        st.write(keywords)

                    with st.beta_expander("Sentiment"):
                        sent_result = get_sentiment(my_text=raw_text)
                        st.write(sent_result)

                with col2:
                    with st.beta_expander("Plot Word Freq"):
                        fig = plt.figure()
                        sns.countplot(token_result_df['Token'])
                        plt.xticks(rotation=45)
                        st.pyplot(fig)

                    with st.beta_expander("Plot Part of Speech"):
                        try:
                            fig = plt.figure()
                            # sns.countplot(token_result_df['Pos'])
                            # plt.xticks(rotation=45)
                            top_keywords = get_most_common_tokens(processed_text, num_of_most_common)
                            plt.bar(top_keywords.keys(), top_keywords.values())
                            st.pyplot(fig)
                        except:
                            st.warning("Insufficient Data")

                    with st.beta_expander("Plot Wordcloud"):
                        plot_wordcloud(my_text=raw_text)

                with st.beta_expander("Download Text Analysis Results"):
                    make_downloadable(token_result_df)

    else:
        st.subheader("About")


if __name__ == '__main__':
    main()

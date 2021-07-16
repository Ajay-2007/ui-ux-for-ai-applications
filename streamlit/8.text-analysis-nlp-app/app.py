import streamlit as st
import streamlit.components.v1 as stc

# EDA Package
import pandas as pd

# NLP Packages
import neattext.functions as nfx
from wordcloud import WordCloud
from collections import Counter
from textblob import TextBlob

# Data Visualization Packages
import matplotlib.pyplot as plt
import matplotlib
import altair as alt

matplotlib.use("Agg")


def plot_wordcloud(docx):
    mywordcloud = WordCloud().generate(docx)
    fig = plt.figure(figsize=(20, 10))
    plt.imshow(mywordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(fig)


def plot_word_freq(docx, num=10):
    word_freq = Counter(docx.split())
    most_common_tokens = word_freq.most_common(num)
    x, y = zip(*most_common_tokens)
    fig = plt.figure(figsize=(20, 10))
    plt.bar(x, y)
    plt.xticks(rotation=45)
    st.pyplot(fig)


def plot_word_freq_with_altair(docx, num=10):
    word_freq = Counter(docx.split())
    most_common_tokens = dict(word_freq.most_common(num))
    word_freq_df = pd.DataFrame(
        {
            "tokens": most_common_tokens.keys(),
            "counts": most_common_tokens.values(),
        }
    )
    brush = alt.selection(type="interval", encodings=["x"])
    c = (
        alt.Chart(word_freq_df)
        .mark_bar()
        .encode(
            x="tokens",
            y="counts",
            opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7)),
        )
        .add_selection(brush)
    )

    st.altair_chart(c, use_container_width=True)


def plot_mendelhall_curve(docx):
    word_length = [len(token) for token in docx.split()]
    word_length_count = Counter(word_length)
    sorted_word_length_count = sorted(dict(word_length_count).items())
    x, y = zip(*sorted_word_length_count)
    mendelhall_df = pd.DataFrame({"tokens": x, "counts": y})
    st.line_chart(mendelhall_df["counts"])


def get_pos_tags(docx):
    blob = TextBlob(docx)
    tagged_docx = blob.tags
    tagged_df = pd.DataFrame(tagged_docx, columns=["token", "tags"])
    return tagged_df


TAGS = {
    "NN": "green",
    "NNS": "green",
    "NNP": "green",
    "NNPS": "green",
    "VB": "blue",
    "VBD": "blue",
    "VBG": "blue",
    "VBN": "blue",
    "VBP": "blue",
    "VBZ": "blue",
    "JJ": "red",
    "JJR": "red",
    "JJS": "red",
    "RB": "cyan",
    "RBR": "cyan",
    "RBS": "cyan",
    "IN": "darkwhite",
    "POS": "darkyellow",
    "PRP$": "magenta",
    "PRP$": "magenta",
    "DET": "black",
    "CC": "black",
    "CD": "black",
    "WDT": "black",
    "WP": "black",
    "WP$": "black",
    "WRB": "black",
    "EX": "yellow",
    "FW": "yellow",
    "LS": "yellow",
    "MD": "yellow",
    "PDT": "yellow",
    "RP": "yellow",
    "SYM": "yellow",
    "TO": "yellow",
    "None": "off",
}


def mytag_visualizer(tagged_docx):
    colored_text = []
    for i in tagged_docx:
        if i[1] in TAGS.keys():
            token = i[0]
            color_for_tag = TAGS.get(i[1])
            result = '<span style="color:{}">{}</span>'.format(color_for_tag, token)
            colored_text.append(result)

    result = " ".join(colored_text)
    return result


def main():
    st.title("Text Analysis NLP App")

    menu = ["Home", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        # Text Area
        raw_text = st.text_area("Enter Text Here")
        if st.button("Submit"):
            if len(raw_text) > 2:
                st.success("Processing")
            elif len(raw_text) == 1:
                st.warning("Insufficient Text, minimum is 2")
            else:
                st.write("Enter Text")
            # if raw_text is not None:
            #     st.success(raw_text)

            # Layout
            col1, col2 = st.beta_columns(2)
            processed_text = nfx.remove_stopwords(raw_text)

            with col1:
                with st.beta_expander("Original Text"):
                    st.write(raw_text)

                with st.beta_expander("PoS Tagged Text"):
                    # tagged_docx = get_pos_tags(raw_text)
                    # st.dataframe(tagged_docx)

                    # Components HTML
                    tagged_docx = TextBlob(raw_text).tags
                    processed_tags = mytag_visualizer(tagged_docx)
                    stc.html(processed_tags, scrolling=True)

                with st.beta_expander("Plot Word Freq"):
                    # plot_word_freq(processed_text)
                    plot_word_freq_with_altair(processed_text)

            with col2:

                with st.beta_expander("Processed Text"):
                    st.write(processed_text)

                with st.beta_expander("Plot Wordcloud"):
                    st.success("Wordcloud")
                    plot_wordcloud(processed_text)

                with st.beta_expander("Plot Stylometry Curve"):
                    st.success("Mendelhall Curve")
                    plot_mendelhall_curve(raw_text)

    else:
        st.subheader("About")


if __name__ == "__main__":
    main()

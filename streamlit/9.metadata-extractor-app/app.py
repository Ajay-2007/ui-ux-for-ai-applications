import streamlit as st
import streamlit.components.v1 as stc

# EDA Packages
import pandas as pd
import numpy as np

# Data Visualization Packages
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")  # TkAgg

# Opening Files
# For Images
from PIL import Image
import exifread
import os
from datetime import datetime
# For Audio
import mutagen

# For PDF
from PyPDF2 import PdfFileReader

# HTML
metadata_wiki = """
Metadata is defined as the data providing information about one or more aspects of the data; it is used to summarize basic information about data which can make tracking and working with specific data easier
"""

HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">MetaData Extractor App </h1>
    </div>
    """


# Functions
@st.cache
def load_image(image_file):
    img = Image.open(image_file)
    return img


def get_readable_time(my_time):
    """ Function to get Human Readable Time"""
    return datetime.fromtimestamp(my_time).strftime('%Y-%m-%d-%H:%M')
# Forensic MetaData Extraction


# App Structure
def main():
    """Meta Data Extraction App"""
    st.title("MetaData Extraction App")
    stc.html(HTML_BANNER)

    menu = ["Home", "Image", "Audio", "DocumentFiles", "About"]
    choice = st.sidebar.selectbox(label="Menu",
                                  options=menu)

    if choice == "Home":
        st.subheader("Home")
        # Image
        st.image(load_image("images/metadataextraction_app_jcharistech.png"))
        # Description
        st.write(metadata_wiki)

        # Expanders & Columns
        col1, col2, col3 = st.beta_columns(3)
        with col1:
            with st.beta_expander('Get Image Metadata 📷'):
                st.info("Image Metadata")
                st.text("Upload JPEG, JPG, PNG Images")

        with col2:
            with st.beta_expander('Get Audio Metadata 🔉'):
                st.info("Audio Metadata")
                st.text("Upload Mp3, Ogg")

        with col3:
            with st.beta_expander('Get Document Metadata 📄📁'):
                st.info("Document Files Metadata")
                st.text("Upload PDF, Docx")

    elif choice == "Image":
        st.subheader("Image MetaData Extraction")
        image_file = st.file_uploader("Upload Image",
                                      type=["png", "jpeg", "jpg"])
        if image_file is not None:
            # Binary Byte
            # st.write(type(image_file))
            # st.write(dir(image_file))
            with st.beta_expander("File Stats"):
                file_details = {
                    "FileName": image_file.name,
                    "FileSize": image_file.size,
                    "FileType": image_file.type
                }
                st.write(file_details)
                st.image(load_image(image_file))

                statinfo = os.stat(image_file.readable())
                st.write(statinfo)
                stats_details = {
                    "Accessed_Time": get_readable_time(statinfo.st_atime),
                    "Creation_Time": get_readable_time(statinfo.st_ctime),
                    "Modified_Time": get_readable_time(statinfo.st_mtime)
                }
                st.write(stats_details)

                # Combine all details
                file_details_combined = {
                    "FileName": image_file.name,
                    "FileSize": image_file.size,
                    "FileType": image_file.type,
                    "Accessed_Time": get_readable_time(statinfo.st_atime),
                    "Creation_Time": get_readable_time(statinfo.st_ctime),
                    "Modified_Time": get_readable_time(statinfo.st_mtime)
                }
                # Convert to DataFrame
                df_file_details = pd.DataFrame(list(file_details_combined.items()),
                                               columns=["Meta Tags", "Value"])
                st.dataframe(df_file_details)

            # Layouts
            c1, c2 = st.beta_columns(2)
            with c1:
                with st.beta_expander("View Image"):
                    img = load_image(image_file)
                    st.image(img, width=250)

            with c2:
                with st.beta_expander("Default(JPEG)"):
                    st.info("Using PILLOW")
                    img = load_image(image_file)
                    # st.write(dir(img))
                    img_details = {
                        "format": img.format,
                        "format_desc": img.format_description,
                        "filename": img.filename,
                        "size": img.size,
                        "height": img.height,
                        "width": img.width,
                        "info": img.info,
                        "encoder": img.encoderinfo
                    }
                    # st.write(img_details)
                    df_img_details_default = pd.DataFrame(list(img_details.items()),
                                                          columns=["Meta Tags", "Value"])
                    st.dataframe(df_img_details_default)
    elif choice == "Audio":
        st.subheader("Audio MetaData Extraction")
    elif choice == "DocumentFiles":
        st.subheader("DocumentFiles MetaData Extraction")
    else:
        st.subheader("About")
        # Image
        st.image(load_image("images/metadataextraction_app_jcharistech.png"))


if __name__ == '__main__':
    main()

import base64

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


from PIL.ExifTags import TAGS, GPSTAGS


# Forensic MetaData Extraction
def get_exif(filename):
    exif = Image.open(filename)._getexif()

    if exif is not None:
        for key, value in exif.items():
            name = TAGS.get(key, key)
            exif[name] = exif.pop(key)

        if 'GPSInfo' in exif:
            for key in exif['GPSInfo'].keys():
                name = GPSTAGS.get(key, key)
                exif['GPSInfo'][name] = exif['GPSInfo'].pop(key)

    return exif


def get_coordinates(info):
    for key in ['Latitude', 'Longitude']:
        if 'GPS' + key in info and 'GPS' + key + 'Ref' in info:
            e = info['GPS' + key]
            ref = info['GPS' + key + 'Ref']
            info[key] = (str(e[0][0] / e[0][1]) + '°' +
                         str(e[1][0] / e[1][1]) + '′' +
                         str(e[2][0] / e[2][1]) + '″ ' +
                         ref)

    if 'Latitude' in info and 'Longitude' in info:
        return [info['Latitude'], info['Longitude']]


def get_decimal_coordinates(info):
    for key in ['Latitude', 'Longitude']:
        if 'GPS' + key in info and 'GPS' + key + 'Ref' in info:
            e = info['GPS' + key]
            ref = info['GPS' + key + 'Ref']
            info[key] = (e[0][0] / e[0][1] +
                         e[1][0] / e[1][1] / 60 +
                         e[2][0] / e[2][1] / 3600
                         ) * (-1 if ref in ['S', 'W'] else 1)

    if 'Latitude' in info and 'Longitude' in info:
        return [info['Latitude'], info['Longitude']]


import time

timestr = time.strftime("%Y%m%d-%H%M%S")


# Function to Download
def make_downloadable(data: pd.DataFrame):
    csv_file = data.to_csv(index=False)
    # B64 encoding
    b64 = base64.b64encode(csv_file.encode()).decode()  # B64 encoding
    st.markdown("### ** Download CSV File **")
    new_filename = "metadata_result_{}.csv".format(timestr)
    href = f'''
    <a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!</a>
    '''
    st.markdown(href, unsafe_allow_html=True)


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
            # UploadFile Class is File-Like Binary Byte
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

            # Layout For Forensic
            fcol1, fcol2 = st.beta_columns(2)
            with fcol1:
                with st.beta_expander("Exifread Tool"):
                    # img = load_image(image_file)
                    # st.image(img)
                    meta_tags = exifread.process_file(image_file)
                    # st.write(meta_tags)

                    df_img_details_exifread = pd.DataFrame(list(meta_tags.items()),
                                                           columns=["Meta Tags", "Value"])
                    st.dataframe(df_img_details_exifread)

            with fcol2:
                with st.beta_expander("Image GeoCoordinates"):
                    img_details_with_exif = get_exif(image_file)
                    try:
                        gps_info = img_details_with_exif
                    except:
                        gps_info = "None Found"

                    st.write(gps_info)
                    try:
                        img_coordinates = get_decimal_coordinates(gps_info)
                        st.write(img_coordinates)
                    except:
                        st.write("None Found")

            with st.beta_expander("Download Results"):
                final_df = pd.concat([df_file_details,
                                      df_img_details_default,
                                      df_img_details_exifread])
                # st.dataframe(final_df)
                make_downloadable(final_df)
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
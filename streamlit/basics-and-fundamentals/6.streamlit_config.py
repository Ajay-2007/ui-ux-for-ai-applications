import streamlit as st
from PIL import Image

img = Image.open('data/image_03.jpg')
# Configuring the app must be the first activity of streamlit

# Method 1
# st.set_page_config(page_title='hello',
#                    page_icon=img,
#                    layout='wide',
#                    initial_sidebar_state='auto')

# Method 2: Dictionary
PAGE_CONFIG = {
    "page_title": "Hello Streamlit",
    "page_icon": img,
    "layout": "centered",
}
st.set_page_config(**PAGE_CONFIG)


def main():
    st.title("Hello Streamlit Lovers 😅")
    st.sidebar.success("Menu")


if __name__ == '__main__':
    main()

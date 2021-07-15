import streamlit as st

# Working with Widgets
# Buttons/Radio/Checkbox/Select/

# Working with Button
name = "Ajay"
if st.button("Submit"):
    st.write("Name: {}".format(name.upper()))

if st.button("Submit", key='new02'):
    st.write("First Name: {}".format(name.lower()))

# Working with RadioButtons
status = st.radio("What is your status", ("Active", "Inactive"))
if status == 'Active':
    st.success("You are Active")
elif status == 'Inactive':
    st.warning("Inactive")

# Working with Checkbox
if st.checkbox("Show/Hide"):
    st.text("Showing something")

# Working with Beta Expander
# if st.beta_expander("Python"):
#     st.success("Hello Python")

with st.beta_expander("Julia"):
    st.text("Hello Julia")

# Select/Multiple select
my_lang = ["Python", "Julia", "Go", "Rust"]

choice = st.selectbox("Language", my_lang)
st.write("you selected {}".format(choice))

# Multiple Selection
spoken_lang = ("English", "French", "Spanish", "Twi")
my_spoken_lang = st.multiselect("Spoken Lang", spoken_lang, default="English")

# Slider
# Numbers (Int/Float/Dates)
age = st.slider("Age", 1, 100)

# Any Datatype
# Select Slider
color = st.select_slider("Choose Color", options=["yellow", "red", "blue", "black", "white"],
                         value=("yellow", "red"))
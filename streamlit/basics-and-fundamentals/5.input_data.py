import streamlit as st

# Text Input
fname = st.text_input("Enter Firstname", max_chars=10)
# Text Input Hide Password
password = st.text_input("Enter Password", type='password')
st.title(fname)

# Text Area
message = st.text_area("Enter Message", height=100)
st.write(message)

# Numbers
number = st.number_input("Enter Number", 1.0, 25.0)

# Date Input
my_appointment = st.date_input("Appointment")

# Time Input
my_time = st.time_input("My Time")

# Color Picker
color = st.color_picker("Select Color")
##########################################
# The app:
# Displays a web UI using Streamlit
# Lets the user choose a cuisine from a dropdown
# Calls a LangChain helper function
# Shows an AI-generated restaurant name and menu
#  In short: An AI-powered restaurant name & menu generator web app
# run below command in command line
# streamlit run C:\Rama\Learn\LangChain\05_AIBasedRestaurantMenuGenerator.py American
# https://www.youtube.com/watch?v=d4yCWBGFCEs
# FYI:  Streamlit lets you create web UIs using only Python, mainly for ML, AI, analytics, and dashboards.
#
##########################################

import streamlit as st
import LangChainHelper


st.title("Restaurant name Generator")
cusine = st.sidebar.selectbox("Pick a Cuisine", ("Indian","Mexican","Italian","American"))
st.title(" Cusine choosen is ="+ cusine)



if cusine:
    response = LangChainHelper.generate_restaurant_name_and_menu_items(cusine)
    st.header(response['restaurant_name'].strip())
    menu_items = response['menu_items'].split(",")
    st.write("**Menu Items**")
    for menu_item in menu_items:
        st.write("-",menu_item)



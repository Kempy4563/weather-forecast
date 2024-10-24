import traceback
from backend import get_data

import streamlit as st
import plotly.express as px

# widgets
st.title("Weather Forecast for the Next Days")
place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5,
                help="Select the number of forecasted days")
option = st.selectbox("Select data to view",
                      ("Temperature", "Sky"))
st.subheader(f"{option} for the next {days} days in {place}")

#if place is provided execute below (avoids error when app is first started as no place is provided
if place:

    #get the temp/sky data
    filtered_data = get_data(place=place, forecast_days=days)

    if option == "Temperature":
        temperatures = [dict["main"]["temp"] for dict in filtered_data]

        #note dt is the key which will give you raw date and dt_txt coverts to format like '2024-10-24 12:00:00' _
        dates = [dict["dt_txt"] for dict in filtered_data]
        #create a temp plot
        figure = px.line(x=dates, y=temperatures,
                         labels={"x": "Date", "y": "Temperature (C)"})
        st.plotly_chart(figure)

    if option == "Sky":
        # note that weather is a list containing one dict thereofre we reference the index of that single dict with [0].
        # The main key holds required key, eg Rain, Cloud etc..
        filtered_data = [dict["weather"][0]["main"] for dict in filtered_data]
        st.image()
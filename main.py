from PIL import Image
from backend import get_data
import streamlit as st
import plotly.express as px

# widgets
st.title("Weather Forecast")
place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select the number of forecasted days")
option = st.selectbox("Select data to view",
                      ("Temperature", "Sky"))
st.subheader(f"Forecast the next {days} days for {place} GMT")

# if place is provided execute below (avoids error when app is first started as no place is provided
if place:

    try:

        # get the temp/sky data
        filtered_data = get_data(place=place, forecast_days=days)

        if option == "Temperature":
            temperatures = [dict["main"]["temp"] for dict in filtered_data]

            #dt_txt coverts to format like '2024-10-24 12:00:00' _
            dates = [dict["dt_txt"] for dict in filtered_data]
            # create a temp plot
            figure = px.line(x=dates, y=temperatures,
                             labels={"x": "Date", "y": "Temperature (C)"})
            st.plotly_chart(figure)

        if option == "Sky":
            images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
                      "Rain": "images/rain.png", "Snow": "images/snow.png"}

            # note that weather is a list containing one dict therefore we
            # reference the index of that single dict with [0].
            # The main key holds required key, eg Rain, Cloud etc.
            sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]

            #obtain the image filepath for each sky_condition, ie Clear, Rain etc
            image_paths = [images[condition] for condition in sky_conditions]

            #obtain the weather description for each dictionary in filtered_data
            sky_description = [f"{dict['weather'][0]['description']}" for dict in filtered_data]
            dates = [dict["dt_txt"] for dict in filtered_data]

            #obtain the temperatures
            temperatures = [dict["main"]["temp"] for dict in filtered_data]
            temperatures = list(map(str, temperatures))

            #zip the 3 lists
            concatenated_list = [f"{date}:GMT {description} Temp:{temp}c" for date, description, temp in
                                 zip(dates, sky_description, temperatures)]

            print(concatenated_list)

            #create dict with concatenated list and the associated image filepaths
            dictionary = dict(zip(concatenated_list, image_paths))

            # Convert dictionary to a list of tuples for easier iteration
            items = list(dictionary.items())

            # Iterate through the dictionary and display images in a 4-column layout
            for i in range(0, len(items), 4):
                cols = st.columns(4)
                for col, (date, image_path) in zip(cols, items[i:i + 4]):

                    image = Image.open(image_path)
                    col.image(image, caption=f'Weather for {date}', use_column_width=True)

    except KeyError:
        st.write("Unknown place. Please enter a valid place..")
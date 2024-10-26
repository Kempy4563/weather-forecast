from PIL import Image
from backend import get_data
import streamlit as st
import plotly.express as px
import glob
from datetime import datetime, timedelta

# widgets
st.title("Weather Forecast")
place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="Select the number of forecasted days")
option = st.selectbox("Select data to view",
                      ("Temperature", "Sky"))
st.subheader(f"Forecast the next {days} days for {place} in local timezone")

# if place is provided execute below (avoids error when app is first started as no place is provided
if place:

    try:
        # get the temp/sky data
        filtered_data, offset = get_data(place=place, forecast_days=days)
        print(f"the offset local timezone is {offset}")

        if option == "Temperature":
            temperatures = [dict["main"]["temp"] for dict in filtered_data]

            # dt_txt contains the dates
            dates = [dict["dt_txt"] for dict in filtered_data]

            # Convert strings to datetime objects and apply the offset
            offset_seconds = offset
            offset = timedelta(seconds=offset_seconds)

            date_objects_with_offset = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S") + offset for date in dates]
            # Convert datetime objects back to strings
            date_strings_with_offset = [date.strftime("%Y-%m-%d %H:%M:%S") for date in date_objects_with_offset]

            print(date_strings_with_offset)

            # create a temp plot
            figure = px.line(x=date_strings_with_offset, y=temperatures,
                             labels={"x": "Date", "y": "Temperature (C)"})
            st.plotly_chart(figure)

        if option == "Sky":

            file_directory = 'images/*.png'
            images = []

            for filename in glob.glob(file_directory):
                images.append(filename)

            image_codes = [dict["weather"][0]["icon"] for dict in filtered_data]

            # Create a dictionary to map codes to file paths
            code_to_filepath = {filepath.split('/')[-1].split('@')[0]: filepath for filepath in images}

            associated_filepaths = [code_to_filepath[code] for code in image_codes]

            print(associated_filepaths)

            # obtain the weather description for each dictionary in filtered_data
            sky_description = [f"{dict['weather'][0]['description']}" for dict in filtered_data]

            # get the dates
            dates = [dict["dt_txt"] for dict in filtered_data]

            # Convert strings to datetime objects and apply the offset
            offset_seconds = offset
            offset = timedelta(seconds=offset_seconds)

            date_objects_with_offset = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S") + offset for date in dates]

            # Convert datetime objects back to strings
            date_strings_with_offset = [date.strftime("%Y-%m-%d %H:%M:%S") for date in date_objects_with_offset]

            print(date_strings_with_offset)

            print(dates)

            # obtain the temperatures
            temperatures = [dict["main"]["temp"] for dict in filtered_data]
            temperatures = list(map(str, temperatures))

            # zip the 3 lists
            concatenated_list = [f"{date} {description} Temperature {temp} °c" for date, description, temp in
                                 zip(date_strings_with_offset, sky_description, temperatures)]

            formatted_weather_data = [item.replace(' Temp', '\nTemp') for item in concatenated_list]

            print(formatted_weather_data)

            # create dict with concatenated list and the associated image filepaths
            dictionary = dict(zip(formatted_weather_data, associated_filepaths))

            # Convert dictionary to a list of tuples for easier iteration
            items = list(dictionary.items())

            # Iterate through the dictionary and display images in a 4-column layout
            for i in range(0, len(items), 4):
                cols = st.columns(4)
                for col, (date, image_path) in zip(cols, items[i:i + 4]):
                    image = Image.open(image_path)
                    col.image(image, caption=f'{date}', use_column_width=True)

    except KeyError:
        st.write("Unknown place. Please enter a valid place..")

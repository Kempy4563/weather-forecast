from PIL import Image
from backend import get_data, get_current_weather
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
                      ("Weather Conditions", "Temperature"))
st.subheader(f"Forecast the next {days} days for {place} in local timezone")


# if place is provided execute below (avoids error when app is first started as no place is provided
if place:

    try:
        # get the temp/sky data
        filtered_data, offset, long, lat = get_data(place=place, forecast_days=days)
        print(f"the offset local timezone is {offset}")
        print(f"the longitude is {long}")
        print(f"the latitude is {lat}")

        coord_data = get_current_weather(lon=long, lat=lat)
        print(coord_data)

        temperature_k = coord_data['main']['temp']
        temperature_c = int(temperature_k - 273.15)
        timezone = coord_data['timezone']
        timezone_offset = coord_data['timezone']
        current_description = coord_data['weather'][0]['description']
        weather_image = coord_data['weather'][0]['icon']

        # Current UTC time
        utc_time = datetime.utcnow()

        # Convert UTC time to local time using the timezone offset
        local_time = utc_time + timedelta(seconds=timezone_offset)

        # Formatting the local time
        formatted_local_time = local_time.strftime('%Y-%m-%d %H:%M:%S')

        # Printing the values
        print(f"Temperature: {temperature_c:.2f} °C")
        print(f"Timezone: {formatted_local_time}")
        print(f"Description: {current_description}")
        print(f"Weather icon: {weather_image}")

        # fetch the day of week
        date_object = datetime.strptime(formatted_local_time, "%Y-%m-%d %H:%M:%S")

        # strip the date so it represents time only
        date_object = datetime.strptime(formatted_local_time, "%Y-%m-%d %H:%M:%S")
        current_time_str = date_object.strftime("%H:%M")

        # get the filepath for the weather images
        current_weather_filepath = f"images/{weather_image}@2x.png"
        print(f"Current weather filepath: {current_weather_filepath}")

        # concat string with current weather details
        local_weather_info = f"{current_time_str} {current_description} Temperature: {temperature_c:.2f} °c"
        print(local_weather_info)

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

        if option == "Weather Conditions":

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

            print(sky_description)

            # get the dates
            dates = [dict["dt_txt"] for dict in filtered_data]

            # Extract dates and convert to days of the week
            days_of_week = []
            for dt_str in dates:
                date_object = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
                day_of_week = date_object.strftime("%A")
                days_of_week.append(day_of_week)

            # Print the list of days of the week
            print(days_of_week)

            # Convert strings to datetime objects and apply the offset
            offset_seconds = offset
            offset = timedelta(seconds=offset_seconds)

            date_objects_with_offset = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S") + offset for date in dates]

            # Convert datetime objects back to strings
            date_strings_with_offset = [date.strftime("%Y-%m-%d %H:%M:%S") for date in date_objects_with_offset]
            print(date_strings_with_offset)

            # extract just the time for the offset dates
            times = []
            for dt_str in date_strings_with_offset:
                date_object = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
                time_str = date_object.strftime("%H:%M")
                times.append(time_str)

            print(times)

            # obtain the temperatures
            temperatures = [dict["main"]["temp"] for dict in filtered_data]

            # Convert each temperature to an integer and map to string
            temperatures = [int(float(temp)) for temp in temperatures]
            temperatures = list(map(str, temperatures))
            print(temperatures)

            # zip the lists into a list of tuples
            items = list(zip(days_of_week, times, sky_description, temperatures, associated_filepaths))
            for item in items:
                print(item)

            st.write(f"Current weather conditions {local_weather_info}")

            col1, col2, col3 = st.columns([1, 2, 1])

            with col1:
                st.write("")

            with col2:
                st.image(current_weather_filepath,
                         use_column_width=True)

            with col3:
                st.write("")

            #Iterate through the items and display images in a 4-column layout
            for i in range(0, len(items), 4):
                cols = st.columns(4)
                for col, (day, time, sky, temp, image_path) in zip(cols, items[i:i + 4]):
                    image = Image.open(image_path)
                    col.image(image, use_column_width=True)
                    caption = f'<div style="text-align:center;">{day} {time}<br>{sky}<br>Temperature: {temp}°C</div>'
                    col.markdown(caption, unsafe_allow_html=True)


    except KeyError:
        st.write("Unknown place. Please enter a valid place..")

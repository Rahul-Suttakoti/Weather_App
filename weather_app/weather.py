# Import all the required Libraries
from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
from PIL import Image, ImageTk
from io import BytesIO  # To handle image downloads safely

# Create a basic layout of the app
root = Tk()
root.title("WEATHER APP")
root.geometry("900x500+300+200")
root.config(bg="#93d1ff")

# Define the function to get the weather information
def getWeather():
    try:
        city = textfield.get().strip()
        if not city:
            messagebox.showwarning("Weather APP", "Please enter a city name!")
            return

        # Weather API
        api_key = "d6ddc1872ddf0b49b3e5a667845ef35a"
        api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        response = requests.get(api)
        json_data = response.json()

        if response.status_code != 200:
            messagebox.showerror("Weather APP", f"Error: {json_data.get('message', 'Invalid city')}")
            return

        # Extracting weather data
        condition = json_data['weather'][0]['main']
        icon_id = json_data['weather'][0]['icon']
        icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
        description = json_data['weather'][0]['description']
        temp = int(json_data['main']['temp'] - 273.15)
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']
        city_name = json_data['name']
        country = json_data['sys']['country']
        latitude = json_data['coord']['lat']
        longitude = json_data['coord']['lon']

        # Update Labels
        t.config(text=f"{temp}°")
        c.config(text=f"{condition} | FEELS LIKE {temp}°", font=("poppins", 25, "bold"), fg="#ce0f7f")
        w.config(text=f"{wind} m/s", font=("poppins", 25, "bold"))
        h.config(text=f"{humidity}%", font=("poppins", 25, "bold"))
        d.config(text=f"{description}", font=("poppins", 25, "bold"))
        p.config(text=f"{pressure} hPa", font=("poppins", 25, "bold"))
        ct.config(text=f"City: {city_name}", fg="blue")
        co.config(text=f"Country: {country}", fg="#36454F")

        get_current_time(latitude, longitude)

        # Download and display the weather icon
        img_response = requests.get(icon_url)
        img_data = img_response.content
        image = Image.open(BytesIO(img_data))
        icon = ImageTk.PhotoImage(image)
        icon_label.config(image=icon)
        icon_label.image = icon

    except Exception as e:
        messagebox.showerror("Weather APP", f"Error: {str(e)}")

def get_current_time(latitude, longitude):
    """Fetch and display the current time based on latitude & longitude."""
    try:
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lng=longitude, lat=latitude)
        if timezone_str:
            tz = pytz.timezone(timezone_str)
            current_time = datetime.now(tz)
            result_label.config(text=f"Current Time: {current_time.strftime('%I:%M %p')}", fg="#900C3F")
        else:
            result_label.config(text="Time Zone Not Found", fg="red")
    except Exception as e:
        result_label.config(text="Error fetching time", fg="red")

# SEARCH BOX
try:
    Search_image = PhotoImage(file="Copy of search.png")
    myimage = Label(image=Search_image, bg="#93d1ff")
    myimage.place(x=20, y=20)
except:
    messagebox.showerror("Error", "Search image not found!")

textfield = tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg="#404040", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()

try:
    Search_icon = PhotoImage(file="Copy of search_icon.png")
    myimage_icon = Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#36454F", command=getWeather)
    myimage_icon.place(x=400, y=34)
except:
    messagebox.showerror("Error", "Search icon not found!")

# Buttons box
try:
    Frame_image = PhotoImage(file="Copy of box.png")
    frame_my_image = Label(image=Frame_image, bg="#93d1ff")
    frame_my_image.place(x=60, y=375)
except:
    messagebox.showerror("Error", "Frame image not found!")

# Labels
Label(root, text="WIND", font=("helvetica", 18, "bold"), fg="white", bg="#1ab5ef").place(x=120, y=400)
Label(root, text="HUMIDITY", font=("helvetica", 18, "bold"), fg="white", bg="#1ab5ef").place(x=250, y=400)
Label(root, text="DESCRIPTION", font=("helvetica", 18, "bold"), fg="white", bg="#1ab5ef").place(x=430, y=400)
Label(root, text="PRESSURE", font=("helvetica", 18, "bold"), fg="white", bg="#1ab5ef").place(x=650, y=400)

t = Label(font=("arial", 70, "bold"), fg="#FDDA0D", bg="#93d1ff")
t.place(x=390, y=240)

c = Label(font=("arial", 20, "bold"), bg="#93d1ff")
c.place(x=380, y=330)

w = Label(text="...", font=("arial", 22, "bold"), bg="#1ab5ef")
w.place(x=100, y=430)

h = Label(text="...", font=("arial", 22, "bold"), bg="#1ab5ef")
h.place(x=250, y=430)

d = Label(text="...", font=("arial", 22, "bold"), bg="#1ab5ef")
d.place(x=430, y=430)

p = Label(text="...", font=("arial", 22, "bold"), bg="#1ab5ef")
p.place(x=650, y=430)

ct = Label(font=("arial", 23, "bold"), bg="#93d1ff")
ct.place(x=400, y=106)

co = Label(font=("arial", 23, "bold"), bg="#93d1ff")
co.place(x=400, y=138)

result_label = Label(root, font=("helvetica", 23, "bold"), bg="#93d1ff")
result_label.place(x=400, y=172)

icon_label = tk.Label(root, bg="#93d1ff")
icon_label.place(x=130, y=190)

root.mainloop()

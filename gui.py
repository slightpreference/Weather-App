import tkinter as tk
import customtkinter as ctk
import pprint
from PIL import Image, ImageTk
from api import *
from datetime import datetime, date

class GUI:
    """Create separate classes for both frames that inherit from Frame object"""
    window = ctk.CTk()

    def __init__(self, weather_data: WeatherBitApi):
        # use separate attributes for current and forecast data
        self.weather_data = weather_data
        self.configure_window('700x450', 'WeatherInfo', 'Light',
                              True, True,
                              r"C:\Users\Rafaz\OneDrive\Desktop\weather\icon.ico")
        self.format_window()
        self.window.mainloop()

    def configure_window(self, geometry : str, title : str, appearance_mode : str,
                         resizable_width : bool, resizable_height : bool, icon_address : str
                         ) -> None:

        self.window.geometry(geometry)
        self.window.title(title)
        ctk.set_appearance_mode(appearance_mode)
        self.window.resizable(resizable_width, resizable_height)
        self.window.iconbitmap(icon_address)

    @staticmethod
    def get_week_day(str_dt):
        date_obj = datetime.strptime(str_dt, '%Y-%m-%d').date()
        return date_obj.strftime('%A')

    @staticmethod
    def get_icon_obj(icon, width, height):
        path = "C:\\Users\\Rafaz\\OneDrive\\Desktop\\weather\\icons\\" + icon + '.png'
        image = Image.open(path)
        image = image.resize((width, height), Image.LANCZOS)
        image_obj = ImageTk.PhotoImage(image)
        return image_obj

    def format_left_frame(self, left_frame: ctk.CTkFrame) -> None:
        azure_color = '#007FFF'

        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(2, weight=1)

        # time label
        time_label = ctk.CTkLabel(left_frame, text=get_formatted_time(), text_color=azure_color, font=('arial', 30))

        time_label.grid(row=0, padx=10, pady=5, sticky='w')

        # city, country name label
        city_country_label = ctk.CTkLabel(left_frame,
                                          text=f"{self.weather_data.city},{self.weather_data.parse_current_weather()['country_code']}",
                                          text_color=azure_color, font=('arial', 15))
        city_country_label.grid(row=1, padx=18, sticky='w')

        # creating the search bar using separate frame
        search_frame = ctk.CTkFrame(left_frame, fg_color='#E8E9EB')

        entry = ctk.CTkEntry(search_frame, placeholder_text=fetch_current_location(), corner_radius=15)
        entry.grid(row=0, pady=15)

        city_name = ctk.StringVar()

        def update():
            self.weather_data.city = city_name.get()
            self.weather_data = self.weather_data.weather_info
            self.format_right_frame(self.right_fr)

        image = Image.open(r'C:\Users\Rafaz\OneDrive\Desktop\weather\search1.png')
        image = ctk.CTkImage(image)
        button = ctk.CTkButton(search_frame, text='', image=image, command=update, corner_radius=15, width=35)
        button.grid(row=1)

        search_frame.grid(row=2)

        # lat,lon label
        lat_lon_label = ctk.CTkLabel(left_frame,
                                     text=f"{self.weather_data.parse_current_weather()['lat']}° {self.weather_data.parse_current_weather()['lon']}°",
                                     text_color=azure_color, font=('arial', 12))
        lat_lon_label.grid(row=3, padx=10, sticky='e')

        # timezone label
        timezone_label = ctk.CTkLabel(left_frame,
                                      text=f"{self.weather_data.parse_current_weather()['timezone']}", text_color=azure_color,
                                      font=('arial', 15, 'bold'))
        timezone_label.grid(row=4, padx=18, pady=5, sticky='e')

    def format_right_frame(self, right_frame: ctk.CTkFrame) -> None:
        self.forecast = self.weather_data.parse_forecast_weather()
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        # frame for current weather data
        cw_frame = ctk.CTkFrame(right_frame, fg_color='white', corner_radius=25)

        # current weather icon
        icon = self.weather_data.parse_current_weather()['icon']
        cw_icon = ctk.CTkLabel(cw_frame, text='', image=GUI.get_icon_obj(icon, 100, 100), width=75)
        cw_icon.grid(sticky='nsew', row=0, column=0, pady=42)

        # current weather details
        cw_details = self.weather_data.parse_current_weather()
        cw_details_label = ctk.CTkLabel(cw_frame,
                                        text=f"temperature\t{cw_details['temp']} °C\n"
                                             f"description\t{cw_details['description']}\n"
                                             f"max temp\t{cw_details['maxtemp']} °C\n"
                                             f"min temp\t\t{cw_details['mintemp']} °C\n"
                                             f"visibility\t\t{cw_details['vis']} km \n",
                                        justify='left',
                                        corner_radius=10,
                                        )
        cw_details_label.grid(row=0, column=1, padx=10)
        cw_frame.grid(sticky='nsew', padx=30, pady=25)

        # weather forecast - day one
        fc_first = ctk.CTkLabel(right_frame,
                                text='   ' + GUI.get_week_day(self.forecast[0]['date'])[:3] + '\t' + str(self.forecast[0]['temp'])
                                + ' °C\t  ' + self.forecast[0]['description'],
                                image=GUI.get_icon_obj(self.forecast[0]['icon'], 50,50),
                                compound='left',
                                corner_radius=25,
                                anchor='w',
                                width=310,
                                fg_color='white'
                                )
        fc_first.grid( pady=5 )

        # weather forecast - day two
        fc_sec = ctk.CTkLabel(right_frame,
                                text='   ' + GUI.get_week_day(self.forecast[1]['date'])[:3] + '\t' + str(self.forecast[1]['temp'])
                                + ' °C\t' + self.forecast[1]['description'],
                                image=GUI.get_icon_obj(self.forecast[1]['icon'], 50,50),
                                compound='left',
                                fg_color='white',
                                corner_radius=25,
                                anchor='w',
                                width=310
                                )
        fc_sec.grid(pady=5)

        # weather forecast - day three
        fc_third = ctk.CTkLabel(right_frame,
                                text='   ' + GUI.get_week_day(self.forecast[2]['date'])[:3] + '\t' + str(self.forecast[2]['temp'])
                                + ' °C\t' + self.forecast[2]['description'],
                                image=GUI.get_icon_obj(self.forecast[2]['icon'], 50,50),
                                compound='left',
                                fg_color='white',
                                anchor='w',
                                corner_radius=25,
                                width=310
                                )
        fc_third.grid(pady=5)

        # weather forecast - day four
        fc_fourth = ctk.CTkLabel(right_frame,
                                text='   ' + GUI.get_week_day(self.forecast[3]['date'])[:3] + '\t' + str(self.forecast[3]['temp'])
                                + ' °C\t' + self.forecast[3]['description'],
                                image=GUI.get_icon_obj(self.forecast[3]['icon'], 50,50),
                                compound='left',
                                fg_color='white',
                                anchor='w',
                                corner_radius=25,
                                width=310
                                )
        fc_fourth.grid(pady=5)

        # weather forecast - day five
        fc_five = ctk.CTkLabel(right_frame,
                                 text='   ' + GUI.get_week_day(self.forecast[4]['date'])[:3] + '\t' + str(
                                     self.forecast[4]['temp'])
                                      + ' °C\t' + self.forecast[4]['description'],
                                 image=GUI.get_icon_obj(self.forecast[4]['icon'], 50, 50),
                                 compound='left',
                                 fg_color='white',
                                 anchor='w',
                                 corner_radius=25,
                                 width=310
                                 )
        fc_five.grid( pady=5)

        # weather forecast - day six
        fc_five = ctk.CTkLabel(right_frame,
                               text='    '+ GUI.get_week_day(self.forecast[5]['date'])[:3] + '\t' + str(
                                   self.forecast[5]['temp'])
                                    + ' °C\t' + self.forecast[5]['description'],
                               image=GUI.get_icon_obj(self.forecast[5]['icon'], 50, 50),
                               compound='left',
                               fg_color='white',
                               anchor='w',
                               corner_radius=25,
                               width=310
                               )

        fc_five.grid(pady=5)

    def format_window(self, left_frame_fg_color: str = '#E8E9EB', right_frame_fg_color: str='#5D8AA8') -> None:
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(self.window, fg_color=left_frame_fg_color)
        right_frame = ctk.CTkFrame(self.window, fg_color=right_frame_fg_color)
        right_frame.grid_propagate(False)
        self.right_fr = right_frame
        self.format_left_frame(left_frame)
        self.format_right_frame(right_frame)
        left_frame.grid(row=0, column=0, sticky='nsew')
        right_frame.grid(row=0, column=1, sticky='nsew')


def get_formatted_time() -> datetime.strftime:
    current_time = datetime.now().time()
    return current_time.strftime("%I:%M %p")


api = WeatherBitApi()
gui = GUI(api)

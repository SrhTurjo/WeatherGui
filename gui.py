from tkinter import *
from tkinter import ttk
from weather import WeatherApp
import threading


class MyWeather:
    def __init__(self):

        self.source = WeatherApp()
        self.source.event_flag = threading.Event()
        
        self.root = Tk()
        self.root.title("Weather App")
        self.root.height = 400

        self.label = Label(self.root, text="Enter location: ")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.entry = Entry(self.root)
        self.entry.grid(row=0, column=1, padx=10, pady=10)

        self.button = Button(self.root, text="Search", command=self.search)
        self.button.grid(row=0, column=2, padx=10, pady=10)

        
        #location results frame, it can have only 1 column
        self.results_frame = Frame(self.root)
        self.results_frame.grid(row=1, column=0, columnspan=3)

        self.root.resizable(False, True)
        self.root.mainloop()

    def switch_entry(self):
        if self.button["state"] == "disabled" or self.entry["state"] == "disabled":
            self.button.config(state="normal")
            self.entry.config(state="normal")
        else:
            self.button.config(state="disabled")
            self.entry.config(state="disabled")

    def display_search_results(self):

        self.source.event_flag.wait()

        for widget in self.results_frame.winfo_children():
            widget.destroy()

        names , coordinates = self.source.names , self.source.coordinates
        Label(self.results_frame, text="Matching locations: ").grid(row=0, column=0, pady=10, sticky="w")
        if names == None or self.source.search == "":
            sorry = Label(self.results_frame, text="No matching locations found, try naming differently", fg="red")
            sorry.grid(row=1, column=0, pady=10, sticky="w")
        else:
            for i, location in enumerate(names):
                btn = Button(self.results_frame, text=location, bg="lightblue", command=lambda: self.get_weather(coordinates[i]) )
                btn.grid(row=i+1, column=0,  pady=10, sticky="w")
        
        self.switch_entry()

    def search(self):
        # clear the results frame
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        self.source.search = self.entry.get()
        if self.source.search == "":
            return None
        
        self.switch_entry()

        Label(self.results_frame, text="Loading...", fg = "red" , font= ("helvetica", 20)).grid(row=0, column=0, pady=10, sticky="w")
        
        threading.Thread(target=self.source.search_for_locations).start()
        threading.Thread(target=self.display_search_results).start()

    def display_weather(self):
        self.source.event_flag.wait()

        #delete search results
        for widget in self.results_frame.winfo_children():
            widget.destroy()        
        
        today, tomorrow = self.source.today, self.source.tomorrow

        today_title = Label(self.results_frame, text="Todays Weather", fg="blue")
        today_title.grid(row=0, column=0, pady=10, sticky="w")

        row = self.display_day_weather(today, 1)

        tomorrow_title = Label(self.results_frame, text="Tomorrows Weather", fg="blue")
        tomorrow_title.grid(row=row+1, column=0, pady=10, sticky="w")

        self.display_day_weather(tomorrow, row+2)

        self.switch_entry()

    def display_day_weather(self ,  data , row_start = 1):

        col = 3
        row = row_start+ len(data) // col
        if len(data) % col != 0:
            row += 1

        indexes = []

        for i in range(row_start, row):
            for j in range(col):
                indexes.append((i,j))

        for i, data in enumerate(data):
            row , col = indexes[i]
            #weather frame
            w_frm = Frame(self.results_frame)
            w_frm.grid(row=row, column=col, pady=5, sticky="w")
            
            Label(w_frm, text=data['time'].capitalize()).grid(row=0, column=0, sticky="w", padx=3)
            Label(w_frm, text=f"{data['temp']} celcius").grid(row=1, column=0, sticky="w", padx=3)
            Label(w_frm, text=f"{data['weather'].capitalize()}").grid(row=2, column=0, sticky="w", padx=3)

        return row

    def get_weather(self, coordinates):
        self.switch_entry()

        #delete search results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        Label(self.results_frame, text="Loading...", fg = "red" , font= ("helvetica", 20)).grid(row=0, column=0, pady=10, sticky="w")        

        self.source.event_flag.clear()

        threading.Thread(target=self.source.get_weather, args=(coordinates,)).start()
        threading.Thread(target=self.display_weather).start()



    

app = MyWeather()
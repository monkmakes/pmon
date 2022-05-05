import threading
import time
from guizero import App, Text
from plant_monitor import PlantMonitor

pm = PlantMonitor()

app = App(title="Plant Monitor", width=550, height=300, layout="grid")

def update_readings(): # update fields with new temp and eCO2 readings
    while True:
        wetness_field.value = str(pm.get_wetness())
        temp_c_field.value = str(pm.get_temp())
        humidity_field.value = str(pm.get_humidity())
        time.sleep(2)

t1 = threading.Thread(target=update_readings)

# define the user interface
Text(app, text="Wetness (%)", grid=[0,0], size=20)
wetness_field = Text(app, text="-", grid=[1,0], size=100)
Text(app, text="Temp (C)", grid=[0,1], size=20)
temp_c_field = Text(app, text="-", grid=[1,1], size=50)
Text(app, text="Humidity (%)", grid=[0,2], size=20)
humidity_field = Text(app, text="-", grid=[1,2], size=50)
t1.start() # start the thread that updates the readings
app.display()

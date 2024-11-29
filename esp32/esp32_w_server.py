from network import WLAN, STA_IF
from microdot import Microdot
from pmon import PlantMonitor
from time import sleep

ssid = 'ssid'
password = 'password'

html = """
<!DOCTYPE html>
<meta http-equiv="refresh" content="1" >
<html>
    <head> <title>My Plant</title> </head>
    <body>
        <h1>ESP32 Plant Monitor</h1>
        <h2>Water: {water}</h2>
        <h2>Temp (C): {temp}</h2>
        <h2>Humidity: {humidity}</h2>
    </body>
</html>
"""

pm = PlantMonitor(uart=2)
app = Microdot()

def connect_wifi(ssid, password):
    wlan = WLAN(STA_IF)
    wlan.active(True)
    print('connecting to ' + ssid)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print('.', end='')
        sleep(1)
    print('IP address:', wlan.ifconfig()[0])
    
connect_wifi(ssid, password)

@app.route('/')
def index(request):
    w = pm.get_wetness()
    t = pm.get_temp()
    h = pm.get_humidity()
    response = html.format(water=w, temp=t, humidity=h)
    return response, {'Content-Type': 'text/html'}

app.run(port=80)

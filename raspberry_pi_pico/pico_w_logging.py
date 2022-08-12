import network
import socket
from pmon import PlantMonitor
import time
import uasyncio as asyncio

ssid = 'MONKMAKES_GUEST'
password = '6KeCt4cu9YfY'

html = """
<!DOCTYPE html>
<meta http-equiv="refresh" content="1" >
<html>
    <head> <title>My Plant</title> </head>
    <body>
        <h1>My fancy Plant Monitor</h1>
        <h2>Water: {water}</h2>
        <h2>Temp (C): {temp}</h2>
        <h2>Humidity: {humidity}</h2>
    </body>
</html>
"""
pm = PlantMonitor()
wlan = network.WLAN(network.STA_IF)

def connect_to_network():
    wlan.active(True)
    wlan.config(pm = 0xa11140)  # Disable power-save mode
    wlan.connect(ssid, password)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])

async def serve_client(reader, writer):
    request_line = await reader.readline()
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass
    w = pm.get_wetness()
    t = pm.get_temp()
    h = pm.get_humidity()
    response = html.format(water=w, temp=t, humidity=h)
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)

    await writer.drain()
    await writer.wait_closed()
    print("Client disconnected")

async def main():
    print('Connecting to Network...')
    connect_to_network()

    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    while True:
        await asyncio.sleep(5)
        
try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()

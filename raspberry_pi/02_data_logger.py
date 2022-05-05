import time

from plant_monitor import PlantMonitor
pm = PlantMonitor()

interval = int(input("Enter interval between readings (seconds):"))
file_name = input("Enter filename:")
current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print("Logging started at: " + current_time)
print("Press CTRL-c to end logging")

f = open(file_name, "w")
f.write("time(s)\twetness\ttemp(C)\thumidity(%)\n")
print("time(s)\twetness\ttemp(C)\thumidity(%)\n")

last_update = 0
t0 = int(time.monotonic())

try:
    while True:
        now = time.monotonic()
        if (now > last_update + interval):
            last_update = now
            t = str(int(now) - t0)
            wetness = str(pm.get_wetness())
            temp_c = str(pm.get_temp())
            humidity = str(int(pm.get_humidity()))
            f.write(t + "\t")
            f.write(wetness + "\t")
            f.write(temp_c + "\t")
            f.write(humidity + "\n")
            print(t + "\t" + wetness + "\t" + temp_c + "\t" + humidity)
except:
    f.close()
    print("\nLogging to file " + file_name + " complete")
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("Logging ended at: " + current_time)

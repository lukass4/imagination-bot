from datetime import datetime
ts = 1587826048403 / 1000
print(datetime.fromtimestamp(ts).strftime("%d-%m-%Y"))
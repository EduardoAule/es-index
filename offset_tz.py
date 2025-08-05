from datetime import datetime, timedelta
from pytz import timezone, UTC

# utc = pytz.UTC

creation_date = 1754337002087

LAST_DAYS = 20
tz = timezone('America/Mexico_City')
ds = datetime.now(tz) # .replace(tzinfo=UTC)
d = ds - timedelta(days=LAST_DAYS)
print("datestring:", d, ds)

my_datetime = datetime.fromtimestamp(creation_date/1000)
my_datetime = my_datetime.replace(tzinfo=UTC)
print("my_datetime:", my_datetime)

if my_datetime > d:
    print( my_datetime, "vigente")
else:
    print( my_datetime, "old")
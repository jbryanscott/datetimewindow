# datetimewindow
Easily create and manipulate windows of `datetime` types.

# Examples
```
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetimewindow import DatetimeWindow
```
#### Last 28 days
    
````
trailing_28_days = DatetimeWindow(relativedelta(days=-28))
trailing_28_days.start.date()
````
    
`datetime.date(2017, 10, 13)`
    
````
trailing_28_days.end.date()
````
`datetime.date(2017, 11, 10)`

````
trailing_28_days.duration
````
`relativedelta(days=+28)`
    
#### Specific date plus a month (can be any `relativedelta`)
````
january = DatetimeWindow(relativedelta(months=1), datetime(2017, 1, 1))
(january.start.date(), january.end.date())
````    
`(datetime.date(2017, 1, 1), datetime.date(2017, 2, 1))`


#### Rolling window in a loop

````
step = dict(days=-28)
dtw = DatetimeWindow(relativedelta(**step))
print(dtw)
````

`{'start': datetime.datetime(2017, 10, 13, 2, 51, 15, 514207, tzinfo=<UTC>), 'end': datetime.datetime(2017, 11, 10, 2, 51, 15, 514207, tzinfo=<UTC>), 'duration': relativedelta(days=+28)}`

Sometimes it's useful for rolling windows to overlap...

````
# Expand the window symmetrically by 1 minute to create an overlap
dtw = dtw.window_expand(minutes=1)
print(dtw)
````

`{'start': datetime.datetime(2017, 10, 13, 2, 50, 15, 514207, tzinfo=<UTC>), 'end': datetime.datetime(2017, 11, 10, 2, 52, 15, 514207, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}`

...for example, in parsing data from an API that doesn't have appropriate time resolution.

````
for i in range(12):
    dtw = dtw.window_add(**step)
    # with Session as s:
    #     r = s.get(url, dict(updated_at_min=dtw.start, updated_at_max=dtw.end))
    #     ...
    print(dtw)
````
````
{'start': datetime.datetime(2017, 9, 15, 2, 50, 15, 514207, tzinfo=<UTC>), 'end': datetime.datetime(2017, 10, 13, 2, 52, 15, 514207, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
{'start': datetime.datetime(2017, 8, 18, 2, 50, 15, 514207, tzinfo=<UTC>), 'end': datetime.datetime(2017, 9, 15, 2, 52, 15, 514207, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
{'start': datetime.datetime(2017, 7, 21, 2, 50, 15, 514207, tzinfo=<UTC>), 'end': datetime.datetime(2017, 8, 18, 2, 52, 15, 514207, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
{'start': datetime.datetime(2017, 6, 23, 2, 50, 15, 514207, tzinfo=<UTC>), 'end': datetime.datetime(2017, 7, 21, 2, 52, 15, 514207, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
{'start': datetime.datetime(2017, 5, 26, 2, 50, 15, 514207, tzinfo=<UTC>), 'end': datetime.datetime(2017, 6, 23, 2, 52, 15, 514207, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
{'start': datetime.datetime(2017, 4, 28, 2, 50, 15, 514207, tzinfo=<UTC>), 'end': datetime.datetime(2017, 5, 26, 2, 52, 15, 514207, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
{'start': datetime.datetime(2017, 3, 31, 2, 50, 15, 514207, tzinfo=<UTC>), 'end': datetime.datetime(2017, 4, 28, 2, 52, 15, 514207, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
{'start': datetime.datetime(2017, 3, 3, 2, 50, 15, 514207, tzinfo=<UTC>), 'end': datetime.datetime(2017, 3, 31, 2, 52, 15, 514207, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
{'start': datetime.datetime(2017, 2, 3, 2, 50, 15, 514207, tzinfo=<UTC>), 'end': datetime.datetime(2017, 3, 3, 2, 52, 15, 514207, tzinfo=<UTC>), 'duration': relativedelta(months=+1, minutes=+2)}
{'start': datetime.datetime(2017, 1, 6, 2, 50, 15, 514207, tzinfo=<UTC>), 'end': datetime.datetime(2017, 2, 3, 2, 52, 15, 514207, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
{'start': datetime.datetime(2016, 12, 9, 2, 50, 15, 514207, tzinfo=<UTC>), 'end': datetime.datetime(2017, 1, 6, 2, 52, 15, 514207, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
{'start': datetime.datetime(2016, 11, 11, 2, 50, 15, 514207, tzinfo=<UTC>), 'end': datetime.datetime(2016, 12, 9, 2, 52, 15, 514207, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
````

### Comparison
#### Get the overlapping window of two Datetime Windows, or `None` if there's no overlap
````
quarter = DatetimeWindow(relativedelta(months=3), datetime(2017, 1, 1))
month = DatetimeWindow(relativedelta(months=1), datetime(2017, 1, 1))
week = DatetimeWindow(relativedelta(weeks=1), datetime(2017, 1, 28))
other_week = DatetimeWindow(relativedelta(weeks=1), datetime(2017, 3, 1))

month.overlaps(week).duration       # relativedelta(days=+4)
other_week.overlaps(week)           # None

month.ends_before(week.start)       # False
month.ends_before(week.end)         # True

month.contains(week)                # False
quarter.contains(month)             # True
````

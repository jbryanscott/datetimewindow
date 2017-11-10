# datetimewindow
Easily create and manipulate windows of `datetime` types.

# Examples
```python
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetimewindow import DatetimeWindow
```
#### Last 28 days
    
```python
trailing_28_days = DatetimeWindow(relativedelta(days=-28))
trailing_28_days.start.date()       # datetime.date(2017, 10, 13)
trailing_28_days.end.date()         # datetime.date(2017, 11, 10)
trailing_28_days.duration           # relativedelta(days=+28)
```
    
#### Specific date plus a month (can be any `relativedelta`)
```python
january = DatetimeWindow(relativedelta(months=1), datetime(2017, 1, 1))
(january.start.date(), january.end.date())
```
```python
(datetime.date(2017, 1, 1), datetime.date(2017, 2, 1))
```


#### Rolling window in a loop

```python
step = dict(days=-28)
dtw = DatetimeWindow(relativedelta(**step), datetime(2017, 1, 1))
print(dtw)
```

```python
{'start': datetime.datetime(2016, 12, 4, 0, 0, tzinfo=<UTC>), 'end': datetime.datetime(2017, 1, 1, 0, 0, tzinfo=<UTC>), 'duration': relativedelta(days=+28)}
```

Sometimes it's useful for rolling windows to overlap...

```python
# Expand the window symmetrically by 1 minute to create an overlap
dtw = dtw.window_expand(minutes=1)
print(dtw)
```

```python
{'start': datetime.datetime(2016, 12, 3, 23, 59, tzinfo=<UTC>), 'end': datetime.datetime(2017, 1, 1, 0, 1, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
```

...for example, in parsing data from an API that doesn't have appropriate time resolution.

```python
for i in range(12):
    dtw = dtw.window_add(**step)
    # with Session as s:
    #     r = s.get(url, dict(updated_at_min=dtw.start, updated_at_max=dtw.end))
    #     ...
    print(dtw)
```
```python
{'start': datetime.datetime(2016, 11, 5, 23, 59, tzinfo=<UTC>), 'end': datetime.datetime(2016, 12, 4, 0, 1, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
{'start': datetime.datetime(2016, 10, 8, 23, 59, tzinfo=<UTC>), 'end': datetime.datetime(2016, 11, 6, 0, 1, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
{'start': datetime.datetime(2016, 9, 10, 23, 59, tzinfo=<UTC>), 'end': datetime.datetime(2016, 10, 9, 0, 1, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
{'start': datetime.datetime(2016, 8, 13, 23, 59, tzinfo=<UTC>), 'end': datetime.datetime(2016, 9, 11, 0, 1, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
{'start': datetime.datetime(2016, 7, 16, 23, 59, tzinfo=<UTC>), 'end': datetime.datetime(2016, 8, 14, 0, 1, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
{'start': datetime.datetime(2016, 6, 18, 23, 59, tzinfo=<UTC>), 'end': datetime.datetime(2016, 7, 17, 0, 1, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
{'start': datetime.datetime(2016, 5, 21, 23, 59, tzinfo=<UTC>), 'end': datetime.datetime(2016, 6, 19, 0, 1, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
{'start': datetime.datetime(2016, 4, 23, 23, 59, tzinfo=<UTC>), 'end': datetime.datetime(2016, 5, 22, 0, 1, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
{'start': datetime.datetime(2016, 3, 26, 23, 59, tzinfo=<UTC>), 'end': datetime.datetime(2016, 4, 24, 0, 1, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
{'start': datetime.datetime(2016, 2, 27, 23, 59, tzinfo=<UTC>), 'end': datetime.datetime(2016, 3, 27, 0, 1, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
{'start': datetime.datetime(2016, 1, 30, 23, 59, tzinfo=<UTC>), 'end': datetime.datetime(2016, 2, 28, 0, 1, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
{'start': datetime.datetime(2016, 1, 2, 23, 59, tzinfo=<UTC>), 'end': datetime.datetime(2016, 1, 31, 0, 1, tzinfo=<UTC>), 'duration': relativedelta(days=+28, minutes=+2)}
```

### Comparison
#### Get the overlapping window of two Datetime Windows, or `None` if there's no overlap
```python
quarter = DatetimeWindow(relativedelta(months=3), datetime(2017, 1, 1))
month = DatetimeWindow(relativedelta(months=1), datetime(2017, 1, 1))
week = DatetimeWindow(relativedelta(weeks=1), datetime(2017, 1, 28))
other_week = DatetimeWindow(relativedelta(weeks=1), datetime(2017, 3, 1))

month.overlaps(week).duration       # relativedelta(days=+4)
other_week.overlaps(week)           # None

month.ends_after(week.start)        # True
month.ends_after(week.end)          # False

month.contains(week)                # False
quarter.contains(month)             # True
```
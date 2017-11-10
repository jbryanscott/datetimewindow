from typing import Union
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
import pytz


class DatetimeWindow:
    '''
    Make a window between two datetimes, and easily create new windows using
    the first window as a reference point.
    '''
    default_timezone = pytz.UTC

    def __init__(
        self, date1: Union[datetime, relativedelta], date2: datetime=None
    ) -> None:
        date2 = self.now_if_none(date2)

        if isinstance(date1, relativedelta):
            date1 = date2 + date1

        date1 = self.ensure_timezone(date1)
        date2 = self.ensure_timezone(date2)

        self.start = min([date1, date2])
        self.end = max([date1, date2])

        self.duration = relativedelta(self.end, self.start)

    def __repr__(self) -> str:
        return '{}({}, {})'.format(
            self.__class__.__name__,
            repr(self.start),
            repr(self.end)
        )

    def __str__(self) -> str:
        return str({
            'start':        self.start,
            'end':          self.end,
            'duration':     self.duration,
        })

    @staticmethod
    def now_if_none(dt: Union[None, datetime]
                    ) -> Union[datetime, relativedelta]:
        if dt is None:
            return datetime.now(DatetimeWindow.default_timezone)
        else:
            return dt

    @staticmethod
    def ensure_timezone(dt: datetime=None, tzinfo: 'pytz'=None) -> datetime:
        if tzinfo is None:
            tzinfo = DatetimeWindow.default_timezone

        dt = DatetimeWindow.now_if_none(dt)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=tzinfo)
        return dt

    @staticmethod
    def create_explicit(
        start: datetime=None, end: datetime=None
    ) -> 'DatetimeWindow':
        start = DatetimeWindow.now_if_none(start)
        end = DatetimeWindow.now_if_none(end)

        if start > end:
            raise ValueError(('Cannot have a start after the end'
                              '({},{})').format(start, end))
        return DatetimeWindow(start, end)

    def start_add(self, **relativedelta_kwargs) -> 'DatetimeWindow':
        '''
        Add a relativedelta to the start of the DatetimeWindow. Uses the
        relativedelta args, e.g.    dtw.start_add(days=1)
        Can be negative, e.g.       dtw.start_add(days=-1)
        '''
        return self.create_explicit(
            start=self.start + relativedelta(**relativedelta_kwargs),
            end=self.end,
        )

    def end_add(self, **relativedelta_kwargs) -> 'DatetimeWindow':
        '''
        Add a relativedelta to the end of the DatetimeWindow. Uses the
        relativedelta args, e.g.    dtw.end_add(days=1)
        Can be negative, e.g.       dtw.end_add(days=-1)
        '''
        return self.create_explicit(
            start=self.start,
            end=self.end + relativedelta(**relativedelta_kwargs),
        )

    def window_add(self, **relativedelta_kwargs) -> 'DatetimeWindow':
        '''
        Add a relativedelta to both the start and end of the DatetimeWindow.
        Uses the relativedelta args, e.g.       dtw.window_add(days=1)
        Can be negative, e.g.                   dtw.window_add(days=-1)
        '''
        return self.create_explicit(
            start=self.start + relativedelta(**relativedelta_kwargs),
            end=self.end + relativedelta(**relativedelta_kwargs),
        )

    def window_expand(self, **relativedelta_kwargs) -> 'DatetimeWindow':
        '''
        Symmetrically expand the DatetimeWindow by relativedelta at both the
        start and the end.
        Uses the relativedelta args, e.g.       dtw.window_expand(days=1)
        Can be negative, e.g.                   dtw.window_expand(days=-1)
        '''
        return self.create_explicit(
            start=self.start - relativedelta(**relativedelta_kwargs),
            end=self.end + relativedelta(**relativedelta_kwargs),
        )

    def duration_days(self) -> float:
        '''
        Calculates the duration of the DatetimeWindow using only `days` as the
        unit, to one-second precision. `days` is a special case, because
        `dateutil.relativedelta` rounds `days` to `months`, and there's no
        consistent number of `days` in a `month` (or a `year`).
        '''
        return ((self.end - self.start).total_seconds()
                / timedelta(days=1).total_seconds())

    '''
    Comparisons
    '''
    @staticmethod
    def is_positive_relativedelta(rd: relativedelta) -> bool:
        '''
        Can't compare relativedeltas directly, so as a hack, add it to a
        datetime and compare those.
        '''
        now = datetime.now()
        now_delta = now + rd
        return now_delta >= now

    def starts_after(self, dt: datetime) -> bool:
        '''
        Does the DatetimeWindow start after the specified datetime?
        '''
        if not isinstance(dt, datetime):
            raise ValueError('Must compare a datetime to the DatetimeWindow')
        return dt < self.start

    def contains(self, dt: Union[datetime, 'DatetimeWindow']) -> bool:
        '''
        Does the DatetimeWindow contain the
        specified datetime or DatetimeWindow?
        '''
        if isinstance(dt, datetime):
            dtw = DatetimeWindow(dt, dt)
        elif isinstance(dt, DatetimeWindow):
            dtw = dt
        else:
            raise TypeError('Must compare a datetime or DatetimeWindow')
        return dtw.start >= self.start and dtw.end <= self.end

    def ends_after(self, dt: datetime) -> bool:
        '''
        Does the DatetimeWindow end after the specified datetime?
        '''
        if not isinstance(dt, datetime):
            raise ValueError('Must compare a datetime to the DatetimeWindow')
        return dt < self.end

    def overlaps(self, dtw: 'DatetimeWindow') -> Union['DatetimeWindow', None]:
        '''
        Provide a new DatetimeWindow of the overlap, or None if the
        DatetimeWindows don't overlap.
        '''
        if not isinstance(dtw, DatetimeWindow):
            raise TypeError('Must compare a DatetimeWindow')

        w_overall = DatetimeWindow(
            min([dtw.start, self.start]), max([dtw.end, self.end]))
        w_end_to_end = DatetimeWindow(
            min([dtw.end, self.end]), max([dtw.end, self.end]))
        w_start_to_start = DatetimeWindow(
            min([dtw.start, self.start]), max([dtw.start, self.start]))
        overlap_duration = (
            w_overall.duration - w_end_to_end.duration
            - w_start_to_start.duration
        )

        if not self.is_positive_relativedelta(overlap_duration):
            return None
        else:
            return DatetimeWindow(w_start_to_start.end, w_end_to_end.start)

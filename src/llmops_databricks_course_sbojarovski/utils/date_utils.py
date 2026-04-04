"""Date and time utility functions."""

from collections.abc import Iterator
from datetime import datetime, timedelta


def iterate_day_intervals(
    start: datetime, end: datetime
) -> Iterator[tuple[datetime, datetime]]:
    """Iterate over day intervals between start and end datetime.

    Each interval is a tuple of (start_of_day, end_of_day) where:
    - start_of_day is the beginning of the day (00:00:00)
    - end_of_day is the end of the day (23:59:59)

    Args:
        start: Start datetime
        end: End datetime

    Yields:
        Tuples of (start_of_day, end_of_day) for each day

    Raises:
        ValueError: If start > end
    """
    if start > end:
        raise ValueError(
            f"start datetime must be <= end datetime, got start={start}, end={end}"
        )

    # Get the start date at 00:00:00
    current_start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    # Get the end date at 23:59:59
    end_date = end.replace(hour=23, minute=59, second=59, microsecond=0)

    while current_start.date() <= end_date.date():
        # End of current day
        current_end = current_start.replace(hour=23, minute=59, second=59, microsecond=0)
        yield current_start, current_end
        # Move to next day
        current_start += timedelta(days=1)

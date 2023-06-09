from django import template
from django.utils import timezone
from datetime import timedelta
import datetime
register = template.Library()

@register.filter
def elapsed_time(dt: timedelta):
    if not dt:
        return None

    zero = timedelta()
    one_hour = timedelta(hours=1)
    one_day = timedelta(days=1)
    one_week = timedelta(days=7)
    two_weeks = timedelta(days=14)
    one_month = timedelta(days=30)

    if dt < zero:
        if -dt > one_day:
            passed_time = f"{-dt.days}日"
        elif -dt > one_hour:
            passed_time = f"{(-dt).seconds // 3600}時間{(-dt).seconds % 60}分"
        else:
            passed_time = f"{(-dt).seconds // 60}分"
        return f"締切を{passed_time}過ぎています"
    else:
        if dt < one_hour:  # 経過時間が 1 時間以内のとき
            return f"{dt.seconds // 60}分"
        elif dt < one_day:  # 経過時間が 1 日以内のとき
            return f"{dt.seconds // 3600}時間"
        elif dt < one_week:  # 経過時間が 1 週間以内のとき
            return f"{dt.days}日"
        elif dt < two_weeks:
            return f"1週間と{dt.days - 7}日"
        elif dt < one_month:
            return f"{dt.days}日"
        else:
            return f"{dt.days // 30}か月と{dt.days % 30}日"
    
@register.filter
def deadline_passed_elapsed_time(dt):
    if not dt:
        return None

    one_hour = timedelta(hours=1)
    one_day = timedelta(days=1)

    if -dt < one_hour:
        passed_time = f"{(-dt).seconds // 60}分"
    elif -dt < one_day:
        passed_time = f"{(-dt).seconds // 3600}時間{(-dt).seconds % 60}分"
    else:
        passed_time = f"{-dt.days}日"
    return passed_time

@register.filter
def extract_date_from_datetime(dt: datetime.datetime):
    dt = timezone.localdate(dt)
    return dt.strftime("%Y-%m-%d")

@register.filter
def extract_time_from_datetime(dt: datetime.datetime):
    dt = timezone.localtime(dt)
    return dt.strftime("%H:%M")
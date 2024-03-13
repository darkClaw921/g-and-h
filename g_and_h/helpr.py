from datetime import datetime
import pytz

def get_moscow_date():
    moscow_tz = pytz.timezone('Europe/Moscow')
    moscow_time = datetime.now(moscow_tz)
    return moscow_time.strftime('%Y-%m')


listName = get_moscow_date()
sheet = Sheet(PATH_JSON_ACCAUNT, SHEET_NAME, listName)
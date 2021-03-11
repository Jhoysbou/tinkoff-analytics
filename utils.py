from datetime import datetime
from decimal import Decimal
from xml.etree import ElementTree
from functools import lru_cache
import requests
from pytz import timezone


def localize(d: datetime) -> datetime:
    return timezone('Europe/Moscow').localize(d)


def get_now() -> datetime:
    return localize(datetime.now())


@lru_cache(maxsize=32)
def get_usd_course_by_date(date: datetime) -> Decimal:
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date.strftime('%d/%m/%Y')}"
    r = requests.get(url=url)

    root = ElementTree.fromstring(r.content)
    for child in root.iter('Valute'):
        if child.attrib["ID"] == "R01235":
            return Decimal(child.find("Value").text.replace(",", "."))

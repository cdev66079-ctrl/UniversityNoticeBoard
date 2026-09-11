from django import template
import nepali_datetime

register = template.Library()

NEPALI_MONTHS = {
    1: "बैशाख",
    2: "जेठ",
    3: "असार",
    4: "श्रावण",
    5: "भदौ",
    6: "आश्विन",
    7: "कार्तिक",
    8: "मंसिर",
    9: "पौष",
    10: "माघ",
    11: "फागुन",
    12: "चैत्र",
}

def nepali_numbers(value):
    english = "0123456789"
    nepali = "०१२३४५६७८९"
    return str(value).translate(
        str.maketrans(english, nepali)
    )


@register.filter
def bs_date(value):
    if not value:
        return ""

    try:
        if hasattr(value, "date"):
            value = value.date()

        bs = nepali_datetime.date.from_datetime_date(value)

        return (
            f"{nepali_numbers(bs.year)} "
            f"{NEPALI_MONTHS[bs.month]} "
            f"{nepali_numbers(bs.day)}"
        )

    except Exception:
        return ""


@register.filter
def bs_datetime(value):
    if not value:
        return ""

    try:
        bs = nepali_datetime.datetime.from_datetime_datetime(value)

        return (
            f"{nepali_numbers(bs.year)} "
            f"{NEPALI_MONTHS[bs.month]} "
            f"{nepali_numbers(bs.day)}, "
            f"{nepali_numbers(bs.hour)}:"
            f"{nepali_numbers(bs.minute)}"
        )

    except Exception:
        return ""
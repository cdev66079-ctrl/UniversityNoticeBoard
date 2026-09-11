import nepali_datetime


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
    12: "चैत्र"
}


def to_nepali_numbers(value):

    english = "0123456789"
    nepali = "०१२३४५६७८९"

    return str(value).translate(
        str.maketrans(
            english,
            nepali
        )
    )


def format_bs_date(date_value):

    if not date_value:
        return ""

    try:

        if hasattr(date_value, "date"):
            date_value = date_value.date()

        bs_date = (
            nepali_datetime.date
            .from_datetime_date(date_value)
        )

        return (
            f"{to_nepali_numbers(bs_date.year)} "
            f"{NEPALI_MONTHS.get(bs_date.month, '')} "
            f"{to_nepali_numbers(bs_date.day)}"
        )

    except Exception as e:

        print(
            "BS date conversion error:",
            e
        )

        return str(date_value)


def format_bs_datetime(datetime_value):

    if not datetime_value:
        return ""

    try:

        bs_datetime = (
            nepali_datetime.datetime
            .from_datetime_datetime(
                datetime_value
            )
        )

        return (
            f"{to_nepali_numbers(bs_datetime.year)} "
            f"{NEPALI_MONTHS.get(bs_datetime.month, '')} "
            f"{to_nepali_numbers(bs_datetime.day)}, "
            f"{to_nepali_numbers(bs_datetime.hour)}:"
            f"{to_nepali_numbers(bs_datetime.minute)}"
        )

    except Exception as e:

        print(
            "BS datetime conversion error:",
            e
        )

        return str(datetime_value)
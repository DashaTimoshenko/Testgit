import csv
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

URL = "https://skyup.aero/api/site/calendar"
PARAMS = {"language": "uk", "currency": "EUR"}

PAYLOAD = {
    "AirlineCode": "U5",
    "OriginCityCode": "RMO",
    "DestinationCityCode": "SKG",
    "Date": "2027-05-01",
    "EndDate": "2027-06-30",
    "needReturnFlights": True,
    "originAndDestIsAirports": True,
    "TotalPaxCount": 1,
    "DayRange": 1,
    "PaxCountDetails": [{"PaxType": "ADULT", "PaxCount": 1}],
    "PointOfPurchase": "PL",
}

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 Safari/537.36"
    ),
    "origin": "https://skyup.aero",
    "referer": "https://skyup.aero/uk/booking/flights",
}

TARGET_DATE = "2027-05-29"
THRESHOLD = 87
CSV_PATH = Path(__file__).with_name("prices.csv")
CSV_COLUMNS = ["run_datetime", "price"]


def fetch_calendar() -> dict:
    response = requests.post(
        URL, params=PARAMS, headers=HEADERS, json=PAYLOAD, timeout=30
    )
    response.raise_for_status()
    data = response.json()
    if not data.get("success"):
        raise RuntimeError(f"API error: {data.get('error')}")
    return data


def append_price(run_datetime: str, price: float) -> None:
    write_header = not CSV_PATH.exists() or CSV_PATH.stat().st_size == 0
    with CSV_PATH.open("a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
        if write_header:
            writer.writeheader()
        writer.writerow({"run_datetime": run_datetime, "price": price})


def main() -> None:
    data = fetch_calendar()
    onward = data.get("OnwardBestFareDetails") or []
    fare = next((item for item in onward if item.get("flight_date") == TARGET_DATE), None)

    if fare is None:
        raise RuntimeError(f"No Onward fare found for {TARGET_DATE}")

    price = float(fare["display_amount"])
    rounded = fare.get("display_amount_rounded")
    price = float(rounded) if rounded is not None else price
    tz_utc_plus_3 = timezone(timedelta(hours=3))
    run_datetime = datetime.now(tz_utc_plus_3).strftime("%Y-%m-%d %H:%M:%S UTC+3")

    append_price(run_datetime, price)
    print(f"Saved {run_datetime}, {price} to {CSV_PATH.name}")

    if price > THRESHOLD:
        print(f"Price is MORE than {THRESHOLD}")
    elif price < THRESHOLD:
        print(f"Price is LESS than {THRESHOLD}")
    else:
        print(f"Price is EQUAL to {THRESHOLD}")


if __name__ == "__main__":
    main()

import requests
import datetime as dt
from twilio.rest import Client
import time

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

news_api = ""
twilio_api_key = ""


def send_msg(STOCK, up_down, diff_percent, titles):
    print("Sending Message...")
    twilio_account_sid = ""
    twilio_auth_token = ""
    verify_sid = ""
    twilio_phone_number = "+"
    twilio_client = Client(twilio_account_sid, twilio_auth_token)
    message = twilio_client.messages.create(
        from_=twilio_phone_number,
        body=f"{STOCK} {up_down} {diff_percent}\n\n{title}",
        to="phone_number"
    )


def news_response():
    news_url = "https://newsapi.org/v2/everything"
    news_parametres = {
        "q": COMPANY_NAME,
        "searchln": "title",
        "apiKey": news_api,
        "language": "en",
        "pagesize": 40
    }
    news_response = requests.get(url=news_url, params=news_parametres)
    articles = news_response.json()["articles"][:4]
    titles_list = [article["title"] for article in articles]
    return titles_list


alpha_advantage_key = ""
stock_url = "https://www.alphavantage.co/query"
stock_parametres = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "datatype": "json",
    "apikey": alpha_advantage_key

}

stock_response = requests.get(url=stock_url, params=stock_parametres)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]
date = dt.datetime.now().date()
yesterday = date - dt.timedelta(days=2)
day_before_yesterday = date - dt.timedelta(days=3)
stock_price_yesterday = float(stock_data[str(yesterday)]["4. close"])
stock_price_day_before_yesterday = float(
    stock_data[str(day_before_yesterday)]["4. close"])
difference = stock_price_yesterday-stock_price_day_before_yesterday
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((difference / float(stock_price_yesterday)) * 100)

if abs(diff_percent) >= 0:
    title_list = news_response()
    for title in title_list:
        send_msg(STOCK, up_down, diff_percent, title)
        time.sleep(2)

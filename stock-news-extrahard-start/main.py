import itertools
from twilio.rest import Client
import requests
import os
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
alphavantage_key = os.environ["key_alphavantage"]
newsapi_key = os.environ["key_newsapi"]

print(type(alphavantage_key))

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "outputsize": "compact",
    "datatype": "json",
    "apikey": alphavantage_key,
}

url = 'https://www.alphavantage.co/query'
r = requests.get(url, params=parameters)
data = r.json()
# two_last_days_data = data["Time Series (Daily)"]
two_last_days_data = dict(itertools.islice(data["Time Series (Daily)"].items(), 2))

yesterday = list(two_last_days_data.items())[0]
day_before_yesterday = list(two_last_days_data.items())[1]

yesterday_date = next(iter(yesterday))
day_before_yesterday_date = next(iter(day_before_yesterday))

close_yesterday = float(two_last_days_data[yesterday_date]["4. close"])
close_day_before_yesterday = float(two_last_days_data[day_before_yesterday_date]["4. close"])

close_day_before_yesterday_minus_5_percent = close_day_before_yesterday * .95
close_day_before_yesterday_plus_5_percent = close_day_before_yesterday * 1.05

if close_yesterday < close_day_before_yesterday_minus_5_percent or \
        close_yesterday > close_day_before_yesterday_plus_5_percent:
    print("Get News")
    percentage_change = round((close_yesterday - close_day_before_yesterday) / close_yesterday * 100, 2)
    if percentage_change > 0:
        triangle_sign = "🔺"
    else:
        triangle_sign = "🔻"


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

    parameters = {
        "qInTitle": COMPANY_NAME,
        "apiKey": newsapi_key,
    }

    url = "https://newsapi.org/v2/everything"
    r = requests.get(url, params=parameters)
    data = r.json()
    print(data)
    print("----------------------------------------------------------------")

    first_3_news_piece_list = data["articles"][:3]
    title_list = [i["title"] for i in first_3_news_piece_list]
    print(title_list)
    print("----------------------------------------------------------------")
    url_list = [i["url"] for i in first_3_news_piece_list]
    print(url_list)
    print("----------------------------------------------------------------")


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=f"\n"
                              f"TSLA: {triangle_sign}{percentage_change}%\n"
                              f"Headline: {title_list[0]}\n"
                              f"url: {url_list[0]}",
                         from_="+19039450694",
                         to="+972545898999"
                     )

    message = client.messages \
                    .create(
                         body=f"\n"
                              f"TSLA: {triangle_sign}{percentage_change}%\n"
                              f"Headline: {title_list[1]}\n"
                              f"url: {url_list[1]}",
                         from_="+19039450694",
                         to="+972545898999"
                     )

    message = client.messages \
                    .create(
                         body=f"\n"
                              f"TSLA: {triangle_sign}{percentage_change}%\n"
                              f"Headline: {title_list[2]}\n"
                              f"url: {url_list[2]}",
                         from_="+19039450694",
                         to="+972545898999"
                     )

    print(message.sid)


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


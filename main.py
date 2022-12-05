import requests
from twilio.rest import Client


STOCK_NAME = {"TSLA", "GOOGL"}
COMPANY_NAME = ["Tesla", "Google"]
index = 0



STOCK_ENDPOINT = "https://www.alphavantage.co/query"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "F446JJR7YA3PQ3RU"
NEWS_API_KEY = "0d1ee5db156d46fda3a61006e567dd99"
TWILIO_SID = "AC15a392c64139ab53029e341d72f65a38"
TWILIO_AUTH_TOKEN = "8d3ac8b7888bc89e6612ea5ae78fe573"

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

for stock in STOCK_NAME:
    stock_params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": stock,
        "apikey": STOCK_API_KEY,

    }

    response = requests.get(STOCK_ENDPOINT, params=stock_params)
    data = response.json()["Time Series (Daily)"]
    data_list = [value for (key, value) in data.items()]
    yesterday_data = data_list[0]
    yesterday_closing_price = yesterday_data["4. close"]
    #print(data_list)
    print(stock+ "[YCP]: "+yesterday_closing_price)


#TODO 2. - Get the day before yesterday's closing stock price
    day_before_yesterday = data_list[1];
    day_before_yesterday_closing_price = day_before_yesterday["4. close"]
    #print(day_before_yesterday)
    print(stock+"[DBYCP]: "+day_before_yesterday_closing_price)


#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp

    difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
    up_down = None
    if difference > 0:
        up_down = "🔺"
    else:
        up_down = "🔻"

    print(stock+"[dif]:", difference)



#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
    diff_percent = (difference / float(yesterday_closing_price)) * 100
    print(stock+"[%dif]:",diff_percent)


#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").


#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
    if abs(diff_percent) > 0.01:
        news_params = {
            "apiKey": NEWS_API_KEY,
            "qInTitle": COMPANY_NAME[index]
        }

        news_response = requests.get(NEWS_ENDPOINT, params=news_params)
        articles = news_response.json()["articles"]
        

#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
        three_articles = articles[:3]
        #print(three_articles)

        formatted_articles = [f"{stock}: {up_down}{round(diff_percent)} \n Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
        print(COMPANY_NAME[index])
        print(formatted_articles)
    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
        # for article in formatted_articles:
        #     message = client.messages.create(
        #     body=article,
        #     from_="+19148955272",
        #     to="+17866583767"
    )
    index = +1
    #for article in fo



#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


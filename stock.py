from yahoo_fin.stock_info import *
from yahoo_fin import news
import requests
import random
from datetime import datetime
from dateutil.parser import *
import matplotlib.pyplot as plt
import smms

def stock_live_price(stock):
    sto = stock.upper()
    price = get_live_price(sto)

    return str(price)


def stock_news(stock):
    res = ''
    sto = stock.upper()
    news_list = news.get_yf_rss(sto)
    output = []
    for n in news_list:
        output.append(n['title'])
        output.append(n['link'])
        res = '\n'.join([str(var) for var in output])

    return res

def get_historical_data(stock, start_t, end_t, int):
    start = parse(start_t)
    end = parse(end_t)
    hist_df = get_data(stock, start, end, interval=int)
    # if interval == "1wk":
    #     hist_df = get_data(stock, start, end, interval="1wk")
    # elif interval == "1mo":
    #     hist_df = get_data(stock, start, end, interval="1mo")
    # elif interval == "1d":
    #     hist_df = get_data(stock, start, end, interval="1d")
    # else :
    #     raise Exception("Wrong format of interval")
    return hist_df['close'].to_string()



def get_historical_graph(stock, start_t, end_t, int):
    start = parse(start_t)
    end = parse(end_t)
    hist_df = get_data(stock, start, end, interval=int)
    # if interval == "1wk":
    #     hist_df = get_data(stock, start, end, interval="1wk")
    # elif interval == "1mo":
    #     hist_df = get_data(stock, start, end, interval="1mo")
    # elif interval == "1d":
    #     hist_df = get_data(stock, start, end, interval="1d")
    # else:
    #     raise Exception("Wrong format of interval")
    plt.xticks(rotation=45)
    plt.plot(hist_df['close'])
    plt.tight_layout()
    plt.savefig('stock')
    login = smms.SMMS('aannn106', 'lyt1998106')
    login.get_api_token()
    url = login.upload_image('stock.png')
    return url


if __name__ == '__main__':
    #time_list = ('Jan 04 2021 to Feb 11 2022')
    #print(stock_news('fb') == '')
    # try:
    #     print(get_data('tsla', '2020-01-01', '2020-05-01', '1week'))
    # except Exception as e:
    #     print("here")
    #
    print(get_historical_graph('aapl', '2020-01-01', '2020-05-01', '1mo'))
    # try:
    #     print(get_historical_data('tsla', '2020-sdfsdfsd-01', '2020-05-01', "1wk"))
    # except AssertionError as ae:
    #     if str(ae) == "interval must be of of '1d', '1wk', '1mo', or '1m'":
    #         print("here")
    #     else:
    #         print(ae)
    # except Exception as e:
    #     print(e)

    #print(get_historical_data('tesla', '2015-01-01', '2020-05-01', '1mo'))
    #print(stock_news('nflx'))

    #print(stock_live_price('abcd'))
    # stock = 'facebook'
    # try:
    #     if stock:
    #         price = stock_live_price(stock)
    #         if price == 'nan':
    #             st = random.choice(['AMZN', 'NVDA'])
    #             r1 = "I can't find the stock price you want, please check if there is any type error."
    #             r2 = "I don't think I can find the stock price, the symbol usually look like this: {}".format(st) + "."
    #             r3 = "I'm sorry I can find the price for you, I might not have the data."
    #             response = random.choice([r1, r2, r3])
    #         else:
    #             r4 = 'The live stock price of ' + stock + ' is ' + price + ' USD.'
    #             r5 = 'It is ' + price + ' USD.'
    #             r6 = 'OK, The price of ' + stock + ' is ' + price + ' USD.'
    #             r7 = 'Well, it is '+ price + ' USD for stock ' + stock + '.'
    #             response = random.choice([r4, r5, r6, r7])
    #     else:
    #         stock = random.choice(['TSLA', 'AAPL'])
    #         price = stock_live_price(stock)
    #         r8 = "Alright, I can't get your purpose. Maybe you can say tell me the price of {} before you make up your mind".format(
    #             stock)
    #         r9 = 'I think you give me the wrong format, try this:"tell me the price of {}."'.format(stock)
    #         r10 = 'I am sorry that I cannot find empty stock price.'
    #         response = random.choice([r8, r9, r10])
    # except:
    #     r11 = "Can't grab the live stock price, try again later"
    #     r12 = 'I am sorry that I cannot recognize your stock.'
    #     r13 = 'Sorry I cannot understand you.'
    #     r14 = "Sorry I didn't know this stock name, try to provide the valid ticker symbol"
    #     r15 = "Sorry I don't know this stock, try this one: AAPL "
    #     response = random.choice([r11, r12, r13, r14, r15])
    # print(response)


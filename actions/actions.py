# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import re
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet,EventType
from stock import stock_live_price, stock_news, get_historical_data, get_historical_graph
import requests
import random
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
class ActionWaster(Action):

    def name(self) -> Text:
        return "action_waster"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = random.choice(
            ["GOOD, good.. umm... make-up words, you can total play with me, It's not silly at all I guess.",
            "Are you sure that's a real English word, my friend?",
            "Good. But what is that?",
            "I cannot understand you.",
            "Lol, is that your secret code?"])
        dispatcher.utter_message(response)

        return []

class ActionScope(Action):

    def name(self) -> Text:
        return "action_out_of_scope"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = random.choice(
            ["I wish I could answer your question, Please ask some other question.",
             "Sorry I don't know the answer.",
             "I am still learning! Please ask me some other question.",
             "This questions is out of my ability.",
             "I wish I can help you in the future.",
             "I don't know the answer right now, ask me about the stock"])
        dispatcher.utter_message(response)

        return []

class ActionStockPrice(Action):

    def name(self) -> Text:
        return "action_stock_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        stock = tracker.get_slot('stock')
        stock.replace(' ', '')
        try:
            if stock:

                price = stock_live_price(stock)
                if price == 'nan':
                    st = random.choice(['AMZN', 'NVDA'])
                    r1 = "I can't find the stock price you want, please check if there is any type error."
                    r2 = "I don't think I can find the stock price, the symbol usually look like this: {}".format(
                        st) + "."
                    r3 = "I'm sorry I can find the price for you, I might not have the data."
                    response = random.choice([r1, r2, r3])

                else:
                    r4 = 'The live stock price of ' + stock + ' is ' + price + ' USD.'
                    r5 = 'It is ' + price + ' USD.'
                    r6 = 'OK, The price of ' + stock + ' is ' + price + ' USD.'
                    r7 = 'Well, it is ' + price + ' USD for stock ' + stock + '.'
                    response = random.choice([r4, r5, r6, r7])

            else:
                stock = random.choice(['TSLA', 'AAPL'])
                r8 = "Alright, I can't get your purpose. Maybe you can say tell me the price of {} before you make up your mind".format(
                    stock)
                r9 = 'I think you give me the wrong format, try this:"tell me the price of {}."'.format(stock)
                r10 = 'I am sorry that I cannot find empty stock price.'
                response = random.choice([r8, r9, r10])
        except:
            r11 = "Can't grab the live stock price, try again later"
            r12 = 'I am sorry that I cannot recognize your stock.'
            r13 = 'Sorry I cannot understand you.'
            r14 = "Sorry I didn't know this stock name, try to provide the valid ticker symbol"
            r15 = "Sorry I don't know this stock, try this one: AAPL "
            response = random.choice([r11, r12, r13, r14, r15])

        dispatcher.utter_message(response)

        return [SlotSet('stock', stock)]


class ActionStockNews(Action):
    def name(self) -> Text:
        return "action_stock_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        stock = tracker.get_slot('stock')
        if stock_news(stock) == '':
            sto = random.choice(['TSLA', 'AAPL'])
            r1 = "Can't grab the the news, try again later"
            r2 = "Please provide an valid ticker symbol."
            r3 = "Sorry, I cannot find the news for the stock you provided, please check the typo!"
            r4 = "Sorry, I cannot find the news, try {}".format(sto)
            r5 = "I don't think I can find the news for this stock, try: {}".format(sto)
            response = random.choice([r1, r2, r3, r4, r5])

        else:
            result = stock_news(stock)
            r6 = 'I found some recent Yahoo Finance news for stock: ' + stock.upper() + ' \n ' + result
            r7 = 'I found news of: ' + stock.upper() + ' \n ' + result
            r8 = 'Here is some latest news of  ' + stock.upper() + ' \n ' + result
            r9 = 'Here is what you want for  ' + stock.upper() + ' \n ' + result
            response = random.choice([r6, r7, r8, r9])

        dispatcher.utter_message(response)

        return [SlotSet('stock', stock)]


class ActionHistoricalPrice(Action):
    def name(self) -> Text:
        return 'action_historical_price'

    def extract_date(self, date_message):
        timelist = date_message.split('to')
        st = timelist[0]
        et = timelist[1]
        return st, et

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        date_message = tracker.get_slot('date_message')
        stime, etime = self.extract_date(date_message)
        stock = tracker.get_slot('stock')
        interval = tracker.get_slot('interval')
        inte = 'flag'
        if interval == '1' or interval == '1 day':
            inte = '1d'

        if interval == '2' or interval == '1 month':
            inte = '1mo'

        if interval == '3' or interval == '1 week':
            inte = '1wk'

        try:
            data = get_historical_data(stock, stime, etime, inte)
            r1 = "I found the data using the given time and interval: \n" + data
            r2 = "The historical data you want is here: \n" + data
            r3 = "I found this for you: \n" + data
            response = random.choice([r1, r2, r3])
        except AssertionError as ae:
            if str(ae) == "interval must be of of '1d', '1wk', '1mo', or '1m'":
                r4 = "You have to give me '1d', '1wk', '1mo', or '1m' as interval."
                r5 = "The interval should be '1d', '1wk', '1mo', or '1m'"
                r6 = "The format of interval should be '1d', '1wk', '1mo', or '1m'"
                r7 = "Try to give me a right interval, such as '1d', '1wk', '1mo', or '1m'"
                response = random.choice([r4, r5, r6, r7])
            else:
                r8 = "I cannot understand the stock you give me, try: AAPL"
                r9 = "Is that a real stock symbol? Try this one: FB"
                r10 = "I failed to find the the stock you said."
                response = random.choice([r8, r9, r10])
        except Exception:
            r11 = "I think you give me a wrong time format."
            r12 = "I cannot understand the time you give me "
            r13 = "what is that?"
            r14 = "Is that a real format of time?"
            response = random.choice([r11, r12, r13, r14])
        dispatcher.utter_message(response)

        return [SlotSet('stock', stock)]


class ActionHistoricalPriceGraph(Action):
    def name(self) -> Text:
        return 'action_historical_price_graph'

    def extract_date(self, date_message):
        timelist = date_message.split('to')
        st = timelist[0]
        et = timelist[1]
        return st, et

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        date_message = tracker.get_slot('date_message')
        stime, etime = self.extract_date(date_message)
        stock = tracker.get_slot('stock')
        interval = tracker.get_slot('interval')
        url = ''
        inte = 'flag'
        if interval == '1' or interval == '1 day':
            inte = '1d'

        if interval == '2' or interval == '1 month':
            inte = '1mo'

        if interval == '3' or interval == '1 week':
            inte = '1wk'
        try:
            url = get_historical_graph(stock, stime, etime, inte)
            r1 = "I plot a diagram for you: \n" + url
            r2 = "This is a graph for your data: \n" + url
            r3 = "I sketch this for you \n" + url
            response = random.choice([r1, r2, r3])

        except Exception:
            r11 = "I can't make this to a graph, sorry!"
            r12 = "Sorry, I failed to make the graph "
            r13 = "I can't graph this"
            r14 = "Sorry, I can't graph this for you"
            response = random.choice([r11, r12, r13, r14])
        if url:
            dispatcher.utter_message(response)
            dispatcher.utter_message(img=url)
        else:
            dispatcher.utter_message(response)

        return [SlotSet('stock', stock)]

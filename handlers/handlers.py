# import the following dependencies
import importlib
import os,json,re,logging,requests,sys,time
import pandas as pd
from helpers import *
from threading import Thread
from web3 import Web3
from fetchers import *



# Define event to handle and logs to the console/send to discord
class HandleEvent(Thread):
    def __init__(self, web3,event, alert,contract, event_name, **kwargs):
        super(HandleEvent, self).__init__(**kwargs)
        self.web3 = web3
        self.event = event
        self.alert = alert
        self.event_name = event_name
        self.contract=contract

    def run(self):
        while True:
            try:
                self.tx = json.loads(Web3.toJSON(self.event))

                message = getattr(importlib.import_module(f"messages.events.{self.alert}.{self.event_name}"), "message")

                message_obj = message(self.web3,self.tx).compose()

                webhook = message_obj['webhook']
                title = message_obj['title']
                content = message_obj['content']
                fields = message_obj['fields']
                color = message_obj['color']
                image = message_obj['image']
                send = message_obj['send']

                if send:
                    sendWebhook(webhook, title, fields, content, image, color)

            except Exception as e:
                logging.warning(f'Error in event handler {str(self.alert)}-{str(self.contract.address)}-{str(self.event_name)}')
                logging.error(e)
                sendError(f'Error in event handler {str(self.alert)}-{str(self.contract.address)}-{str(self.event_name)}')
                sendError(e)
                continue
            break

# Define state change to handle and logs to the console/send to discord
class HandleStateVariation(Thread):
    def __init__(self, web3,old_value,value, change, alert, contract, state_function, state_argument, **kwargs):
        super(HandleStateVariation, self).__init__(**kwargs)
        self.web3 = web3
        self.value = value
        self.change = change
        self.contract = contract
        self.alert = alert
        self.state_function = state_function
        self.state_argument = state_argument
        self.old_value = old_value

    def run(self):
        try:
            message = getattr(importlib.import_module(f"handlers.state.{self.alert}.{self.state_function}"), "message")

            message_obj = message(self.web3, self.contract,self.state_function,self.state_argument,self.change,self.value,self.old_value).compose()

            webhook = message_obj['webhook']
            title = message_obj['title']
            content = message_obj['content']
            fields = message_obj['fields']
            color = message_obj['color']
            image = message_obj['image']
            send = message_obj['send']

            if send:
                sendWebhook(webhook, title, fields, content, image, color)

        except Exception as e:
            logging.warning(f'Error in state variation handler {str(self.alert)}-{str(self.contract.address)}-{str(self.state_function)}-{str(self.state_argument)}')
            logging.error(e)
            sendError(f'Error in state variation handler {str(self.alert)}-{str(self.contract.address)}-{str(self.state_function)}-{str(self.state_argument)}')
            sendError(e)
            pass

# Define state change to handle and logs to the console/send to discord
class HandleTx(Thread):
    def __init__(self,web3, tx, alert, contract, name, **kwargs):
        super(HandleTx, self).__init__(**kwargs)
        self.web3 = web3
        self.contract = contract
        self.alert = alert
        self.name = name
        self.tx = tx

    def run(self):
        try:
            self.tx = json.loads(Web3.toJSON(self.event))

            message = getattr(importlib.import_module(f"handlers.tx.{self.alert}.{self.alert}"), "message")

            message_obj = message(self.web3, self.tx,self.name).compose()

            webhook = message_obj['webhook']
            title = message_obj['title']
            content = message_obj['content']
            fields = message_obj['fields']
            color = message_obj['color']
            image = message_obj['image']
            send = message_obj['send']

            if send:
                sendWebhook(webhook, title, fields, content, image, color)

        except Exception as e:
            logging.warning(f'Error in tx handler {str(self.alert)}-{str(self.contract.address)}-{str(self.name)}')
            logging.error(e)
            sendError(f'Error in tx handler {str(self.alert)}-{str(self.contract.address)}-{str(self.name)}')
            sendError(e)
            pass

# Listen to coingecko  price changes every 60 seconds
class HandleCoingecko(Thread):
    def __init__(self, id, old_value,value, change,  **kwargs):
        super(HandleCoingecko, self).__init__(**kwargs)
        self.id = id
        self.old_value = old_value
        self.value = value
        self.change = change

    def run(self):
        try:
            if abs(self.change) > 0:

                message = getattr(importlib.import_module(f"handlers.coingecko.price"),"message")

                message_obj = message(self.id, self.value, self.old_value, self.change).compose()

                webhook = message_obj['webhook']
                title = message_obj['title']
                content = message_obj['content']
                fields = message_obj['fields']
                color = message_obj['color']
                image = message_obj['image']
                send = message_obj['send']

                if send:
                    sendWebhook(webhook, title, fields, content, image, color)

        except Exception as e:
            logging.warning(f'Error in coingecko variation handler')
            logging.error(e)
            sendError(f'Error in coingecko variation handler')
            sendError(e)
            pass

# Listen to coingecko  price changes every 60 seconds
class HandleCoingeckoVolume(Thread):
    def __init__(self, id, old_value,value, change,  **kwargs):
        super(HandleCoingeckoVolume, self).__init__(**kwargs)
        self.value = value
        self.id = id
        self.old_value = old_value
        self.change = change


    def run(self):
        try:
            if abs(self.change) > 0:

                message = getattr(importlib.import_module(f"handlers.coingecko.volume"),"message")

                message_obj = message(self.id, self.value, self.old_value, self.change).compose()

                webhook = message_obj['webhook']
                title = message_obj['title']
                content = message_obj['content']
                fields = message_obj['fields']
                color = message_obj['color']
                image = message_obj['image']
                send = message_obj['send']

                if send:
                    sendWebhook(webhook, title, fields, content, image, color)

        except Exception as e:
            logging.warning(f'Error in coingecko volume variation handler')
            logging.error(e)
            sendError(f'Error in coingecko volume variation handler')
            sendError(e)
            pass

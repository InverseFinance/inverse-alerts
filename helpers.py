import os
import requests
import logging
import sys
from dotenv import load_dotenv
from web3 import Web3
import json
import time

def sendWebhook(webhook, title, fields, content, imageurl, color):
    """
    Send a webhook with embed (title,fields,image,url,color)
    content is used for the body of the message and tagging roles
    :param webhook: string webhook link to send the message to
    :param title: self explanatory, string
    :param fields: a json string of fields with names, values, and inLine paramter filled (use the function makefields)
    :param content: the text body of the message, can be used for tagging roles
    :param imageurl: string link to an embedded image url
    :param color: color of the embed message in discord
    :return:
    """
    error = True
    while error:
        try:
            data = {"content": content,
                    "embeds":[{"fields": fields,
                               "title": title,
                               "color": color,
                               "image": {"url": imageurl}}]}
            result = requests.post(webhook, json=data)
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logging.error(err)
            sendError("Error in sending message to webhook. Waiting 5 seconds to retry...")
            time.sleep(5)
            error = True
        else:
            logging.info("Embed delivered successfully to webhook "+str(webhook)+" code {}.".format(result.status_code))
            error = False
            break

def sendError(content):
    """
    Send a message to a discord channel exclusively used for reporting errors
    :param content: string
    :return:
    """
    load_dotenv()
    webhook = os.getenv('WEBHOOK_ERRORS')
    error = True
    replacers = {'{': '(', '}': ')',']': ')','[': ')',':': '='}  # etc....
    i = 0
    while error and i<5 :
        try:
            i = i+ 1
            for a, b in replacers.items():
                content = str(content).replace(a,b)
            data = {"content": content}
            result = requests.post(webhook, json=data)
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logging.error(err)
            logging.info("Error in sending message to webhook. Waiting 10 seconds to retry... code {}.".format(result.status_code))
            # time sleep is used to avoid throttling the error webhook w/ too many attempts
            time.sleep(10)
            error = True
        else:
            error = False

# Format to 0,000.00
def formatCurrency(value):
    value = "{:,.2f}".format(value)
    return value

# Format to 00.00 %
def formatPercent(value):
    value = "{:.2%}".format(value)
    return value

# Logger settings
def LoggerParams():
    """
    Configure our logger to write in debug.log
    """
    # Logger config
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    # Mute warning when pool is full :: overriden by poolsize parameter
    logging.getLogger("urllib3").setLevel(logging.ERROR)

# Define easiy colors for discord
class colors:
    """
    This color class allows to pass readable arguments to theDiscord Embed
    """
    default = 0
    teal = 0x1abc9c
    dark_teal = 0x11806a
    green = 0x2ecc71
    dark_green = 0x1f8b4c
    blue = 0x3498db
    dark_blue = 0x206694
    purple = 0x9b59b6
    dark_purple = 0x71368a
    magenta = 0xe91e63
    dark_magenta = 0xad1457
    gold = 0xf1c40f
    dark_gold = 0xc27c0e
    orange = 0xe67e22
    dark_orange = 0xa84300
    red = 0xe74c3c
    dark_red = 0x992d22
    lighter_grey = 0x95a5a6
    dark_grey = 0x607d8b
    light_grey = 0x979c9f
    darker_grey = 0x546e7a
    blurple = 0x7289da
    greyple = 0x99aab5

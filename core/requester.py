import requests
import warnings

import core.config as mem

warnings.filterwarnings('ignore') # Disable SSL related warnings

def requester(url, payload={}):
    """
    central function for making http requests
    returns str on error otherwise response object of requests library
    """
    return requests.post(url,
        data=payload,
        verify=False,
        timeout=mem.var['timeout'],
    )

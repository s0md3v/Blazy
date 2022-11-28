import re
import requests

from urllib.parse import urlparse
from core.utils import diff_map, remove_tags


def define(response_1, response_2):
    """
    defines a rule list for detecting anomalies by comparing two HTTP response
    returns dict
    """
    factors = {
        'same_code': False, # if http status code is same, contains that code
        'same_body': False, # if http body is same, contains that body
        'same_plaintext': False, # if http body isn't same but is same after removing html, contains that non-html text
        'lines_num': False, # if number of lines in http body is same, contains that number
        'lines_diff': False, # if http-body or plaintext aren't and there are more than two lines, contain which lines are same
        'same_headers': False, # if the headers are same, contains those headers
        'same_redirect': False, # if both requests redirect in similar manner, contains that redirection
    }
    if type(response_1) == type(response_2) == requests.models.Response:
        body_1, body_2 = response_1.text, response_2.text
        if response_1.status_code == response_2.status_code:
            factors['same_code'] = response_1.status_code
        if response_1.headers.keys() == response_2.headers.keys():
            factors['same_headers'] = list(response_1.headers.keys())
            factors['same_headers'].sort()
        if urlparse(response_1.url).path == urlparse(response_2.url).path:
            factors['same_redirect'] = urlparse(response_1.url).path
        else:
            factors['same_redirect'] = ''
        if response_1.text == response_2.text:
            factors['same_body'] = response_1.text
        elif response_1.text.count('\n') == response_2.text.count('\n'):
            factors['lines_num'] = response_1.text.count('\n')
        elif remove_tags(body_1) == remove_tags(body_2):
            factors['same_plaintext'] = remove_tags(body_1)
        elif body_1 and body_2 and body_1.count('\\n') == body_2.count('\\n'):
                factors['lines_diff'] = diff_map(body_1, body_2)
    return factors


def compare(response, factors):
    """
    detects anomalies by comparing a HTTP response against a rule list
    returns string, list (anomaly, list of parameters that caused it)
    """
    if response == '':
        return ('', [])
    these_headers = list(response.headers.keys())
    these_headers.sort()
    if factors['same_code'] and response.status_code != factors['same_code']:
        return 'http code'
    if factors['same_headers'] and these_headers != factors['same_headers']:
        return 'http headers'
    if factors['same_redirect'] and 'Location' in response.headers:
        if urlparse(response.headers.get('Location', '')).path != factors['same_redirect']:
            return 'redirection'
    if factors['same_body'] and response.text != factors['same_body']:
        return 'body length'
    if factors['lines_num'] and response.text.count('\n') != factors['lines_num']:
        return 'number of lines'
    if factors['same_plaintext'] and remove_tags(response.text) != factors['same_plaintext']:
        return 'text length'
    if factors['lines_diff']:
        for line in factors['lines_diff']:
            if line not in response.text:
                return 'lines'
    return ''

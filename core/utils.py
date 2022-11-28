import re
from urllib.parse import urlparse


def diff_map(body_1, body_2):
    """
    creates a list of lines that are common between two multi-line strings
    returns list
    """
    sig = []
    lines_1, lines_2 = body_1.split('\n'), body_2.split('\n')
    for line_1, line_2 in zip(lines_1, lines_2):
        if line_1 == line_2:
            sig.append(line_1)
    return sig


def remove_tags(html):
    """
    removes all the html from a webpage source
    """
    return re.sub(r'(?s)<.*?>', '', html)


def identify_fields(inputs):
    identified = {
        "username": "",
        "password": ""
    }
    count = 0
    for input_obj in inputs:
        if input_obj['type'] in ("text", "password"):
            count += 1
    if count == 2:
        for input_obj in inputs:
            if input_obj['type'] == "password":
                identified['password'] = input_obj['name']
            elif not identified['username']:
                identified['username'] = input_obj['name']
    else:
        for input_obj in inputs:
            if re.search("login|user|name", input_obj['name']):
                identified['username'] = input_obj['name']
            elif input_obj['type'] == "password":
                identified['password'] = input_obj['name']
    return identified


def prepare_request(url, form):
    parsed = urlparse(url)
    action_path = form['action']
    if not action_path.startswith('/'):
        action_path = '/' + action_path
    full_url = parsed.scheme + "://" + parsed.netloc + form['action']
    return full_url

import lxml.html
import six
from lxml.html import CheckboxValues, MultipleSelectOptions, InputElement


def parse_input(element):
	if isinstance(element, InputElement):
		if element.attrib.get('type') == 'submit':
			return True, None, element.attrib.get('type')
	value_obj = element.value
	if value_obj is None:
		return False, '', element.attrib.get('type')
	if isinstance(value_obj, str):
		value_obj = value_obj.lstrip('\n')
	if isinstance(value_obj, CheckboxValues):
		value_obj = [el.value for el in value_obj.group if el.value is not None]
	if isinstance(value_obj, MultipleSelectOptions):
		value_obj = list(value_obj)
	return False, value_obj, element.attrib.get('type')


def get_login_form(html):
	this_form = {}
	tree = lxml.html.fromstring(html)
	for index in range(len(tree.forms)):
		all_inputs = []
		found_password = False
		for key, element in tree.forms[index].inputs.items():
			skip, value, kind = parse_input(element)
			if not skip:
				kind = kind.lower() if kind else ''
				if kind == "password":
					found_password = True
				all_inputs.append({'name': key, 'value': value, 'type': kind})
		if not found_password:
			continue
		if tree.forms[index].action:
			this_form['action'] = tree.forms[index].action
			this_form['method'] = tree.forms[index].method.lower()
			this_form['inputs'] = all_inputs
		break
	return this_form

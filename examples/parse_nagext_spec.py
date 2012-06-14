#!/usr/bin/env python
# -*- coding: utf-8 -*- vim:set fileencoding=utf-8 ft=python:

import requests
import lxml.html
url = 'http://old.nagios.org/developerinfo/externalcommands/commandinfo.php?command_id=40'
r = requests.get(url)
html = lxml.html.fromstring(r.text)
tds = html.xpath('//td')
td_command_name = tds[1]
td_command_format = tds[4]
td_description = tds[7]
print td_command_name.text.strip()
print td_command_format.text.strip()
print td_description.text.strip()


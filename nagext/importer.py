#!/usr/bin/env python

import re
import requests
import lxml.html


class CommandList(object):

    def __init__(self):
        self._base_url =\
                'http://old.nagios.org/developerinfo/externalcommands/'
        self._relative_path = 'commandlist.php'
        self._command_paths = []

        r = requests.get(self._base_url + self._relative_path)
        html = lxml.html.fromstring(r.text)
        del r
        links = html.xpath('//a')
        for link in links:
            self._command_paths.append(link.attrib['href'])

    def __iter__(self):
        for relative_path in self._command_paths:
            yield Command(self._base_url, relative_path)


class Command(object):

    def __init__(self, base_url, relative_path):
        self._base_url = base_url
        self._relative_path = relative_path
        self._name = ''
        self._params = []
        self._description = ''

        r = requests.get(self.url)
        html = lxml.html.fromstring(r.text)
        del r
        tds = html.xpath('//td')
        name = tds[1].text.strip()
        format_ = tds[4].text.strip()
        description = tds[7].text.strip()

        x = format_.split(';')
        assert name == x[0]
        self._name = x[0]
        self._params = [param[1:-1] for param in x[1:]]
        self._description = description

    @property
    def url(self):
        return self._base_url + self._relative_path

    @property
    def name(self):
        return self._name

    @property
    def params(self):
        return list(self._params)

    @property
    def description(self):
        return self._description


def wrap(txt, indent='', cols=79):
    regexp = re.compile(r"\s")
    string = ''
    line = ''
    for word in regexp.split(txt):
        if word == '':
            continue
        if line == '':
            line += word
        elif len(line) + 1 + len(word) <= cols:
            line += ' ' + word
        else:
            string = string + line + "\n"
            line = indent + word
    string += line
    return string


def cmd2py(command):
    funcname = command.name.lower()
    params = ', '.join(command.params)
    run_args = ', '.join(["'%s'" % command.name] + command.params)
    method_string = "    def %s(self, %s):\n" % (funcname, params) + \
        '        """\n' + \
        '        %s\n' % wrap(command.description, indent='        ') + \
        '        """\n' + \
        "        self.run(%s)\n" % (run_args)
    return method_string

if __name__ == '__main__':
    command_list = CommandList()
    for command in command_list:
        print cmd2py(command)
#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
import requests
import lxml.html
import urllib2
import re, htmlentitydefs


class CommandList(object):

    def __init__(self, url=None):
        if url == None:
            self._url = 'http://old.nagios.org/developerinfo/externalcommands/commandlist.php'
        self._command_urls = []

        r = requests.get(self._url)
        html = lxml.html.fromstring(r.text)
        del r
        links = html.xpath('//a')
        for link in links:
            self._command_urls.append(a_tag.attrib['href'])

    def __iter__():
        for url in self._command_urls:
            yield Command(url)

class Command(object):

    def __init__(self, url):
        self._url = url
        self._name = ''
        self._params = []
        self._description = ''

        r = requests.get(self._url)
        html = lxml.html.fromstring(r.text)
        del r
        tds = html.xpath('//td')
        name = tds[1].text.strip()
        format_ = tds[4].text.strip()
        description = tds[7].text.strip()

        x = format_.split(';')
        assert td_name == x[0]
        self._name = x[0]
        self._params = [ param[1:-1] for param in x[1:] ]


def unescape(text):
    """
    Removes HTML or XML character references 
    and entities from a text string.
    keep &amp;, &gt;, &lt; in the source code.
    from Fredrik Lundh
    http://effbot.org/zone/re-sub.htm#unescape-html
    slightly modified
    """
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                #print "erreur de valeur"
                pass
        else:
            # named entity
            try:
                #print text[1:-1]
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                #print "keyerror"
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def wrap(txt, indent='', cols=80):
    """
    wraps txt (line of text) at cols columns
    """
    word = ''
    col = 0
    line = ''
    char = ''
    if txt[-1] == "\n":
        txt2 = txt[0:-1]
    else:
        txt2 = txt
    for char in txt2:
        if not char.isspace():
            word += char
        else:
            if word:
                if col + len(word) <= cols or not line:
                    line += word
                    col += len(word)
                else:
                    line = line.rstrip() + "\n" + indent + word
                    #col = len(ind + word)
                    col = len(word)
                word = ""
            if char != '\n':
                line += char
                col += 1
            elif line[-1] != ' ':
                line += ' '
                col += 1
    if word:
        if col + len(word) < cols:
            line += word
        else:
            line = line.rstrip() + "\n" + indent + word
    if txt[-1] == '\n':
        line += "\n" 
    return line

def cmd2py(command, description):
    command = command.strip().replace('<', '').replace('>', '')
    description = description.strip()
    c = cmd.split(';')
    name = c[0].lower()
    args = ', '.join(c[1:])
    method = "    def %s(self, %s):\n" % (name, args) + \
        '        """\n' + \
        '        %s\n' % wrap(description, indent='        ') + \
        '        """\n' + \
        "        self.run('%s', %s)\n" % (c[0], args)
    return method

if __name__ == '__main__':
    root_url = 'http://old.nagios.org/developerinfo/externalcommands/'

    r = requests.get(root_url + 'commandlist.php')
    soup = BeautifulSoup(r.text)
    del r

    content_table = soup.find('table', { 'class' : 'Content' })
    hrefs = content_table.findAll('a')[4:]

    for a in hrefs:
        #print a['href']
        #print a.string
        r = requests.get(root_url + a['href'])
        s = BeautifulSoup(r.text)
        del r
        t = s.find('table', { 'class': 'Content' })
        tds = t.findAll('td')
        p = False
        command = ''
        description = ''
        set_command = set_description = False
        for td in tds:
            if set_command:
                command = unescape(td.string.decode())
                set_command = False
            elif set_description:
                description = unescape(td.string.decode())
                set_description = False
            if td.string == 'Command Format:':
                set_command = True
            elif td.string == 'Description:':
                set_description = True
            if command and description:
                break
        if command and description:
            print cmd2py(command, description)


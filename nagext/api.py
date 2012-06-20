#!/usr/bin/env python
# -*- coding: utf-8 -*- vim:set fileencoding=utf-8 ft=python:
from time import time
import os
os.chdir(os.environ['PWD'])
import pickle
from contextlib import closing
from flask import (
        Flask,
        request, g,
        abort, render_template_string, redirect,
        url_for,
        )

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['COMMAND_FILE'] = 'commandfile'
app.config['NAGEXT_COMMAND_LIST'] = 'nagext_commands.pickle'

# Dev server only
app.config['BIND_HOST'] = '127.0.0.1'
app.config['BIND_PORT'] = 5000

app.config.from_envvar('NAGEXT_CONFIGFILE')

nagext_commands = pickle.load(open(app.config['NAGEXT_COMMAND_LIST']))


@app.route('/')
def top():
    return redirect(url_for('command_list'))


@app.route('/commands/')
def command_list():
    template_str = """\
<title>Command List</title>
<ul>
  {% for command in nagext_commands -%}
  <li><a href="{{ url_for('command', name=command|lower) }}">{{ command }}</a></li>
  {% endfor -%}
</ul>
"""
    return render_template_string(template_str, nagext_commands=nagext_commands)


@app.route('/commands/<name>', methods=['GET', 'POST'])
def command(name):
    if name.upper() not in nagext_commands:
        abort(404)
    if request.method == 'POST':
        try:
            return post_command(name)
        except IOError as e:
            abort(500)

    command = nagext_commands[name.upper()]

    template_str = """\
<title>Command {{ name|upper }}</title>
<h1>{{ name|upper }}</h1>
<p>params:{% for param in command.params %} {{ param }}{% endfor %}</p>
<p>{{ command.description }}</p>
<form action="{{url_for('command', name=name)}}" method="post">
<dl>
{% for param in command.params -%}
<dt><label for="{{ param }}">{{ param }}: </label></dt>
<dd><input type="text" name="{{ param }}" /></dd>
{% endfor %}
</dl>
<input type="submit" />
</form>
"""
    return render_template_string(template_str, name=name, command=command)

    return '<h1>%s</h1><p>params: %s</p><p>%s</p>' % (
            name,
            command['params'],
            command['description']
            )


def post_command(name):
    command = nagext_commands[name.upper()]
    args = []
    for argname in command['params']:
        if argname not in request.form:
            abort(400)
        args.append(request.form[argname])
    command_string = "[%lu] %s;%s\n" % (
            time(),
            name.upper(),
            ';'.join(args)
            )
    with open(app.config['COMMAND_FILE'], 'a+') as f:
        f.write(command_string)
    return 'OK'


if __name__ == '__main__':
    app.run(host=app.config['BIND_HOST'],
            port=app.config['BIND_PORT'],
            debug=app.config['DEBUG'])
elif app.config['DEBUG'] == True:
    from werkzeug.debug import DebuggedApplication
    app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)
application = app

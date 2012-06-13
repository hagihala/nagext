#!/usr/bin/env python
# -*- coding: utf-8 -*- vim:set fileencoding=utf-8 ft=python:
from time import time
import os
import pickle
from contextlib import closing
from flask import Flask, request, abort, render_template, g

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['COMMAND_FILE'] = 'commandfile'
app.config['NAGEXT_COMMAND_LIST'] = 'nagext_commands.pickle'
app.config.from_envvar('NAGEXT_CONFIGFILE')

nagext_commands = pickle.load(open(app.config['NAGEXT_COMMAND_LIST']))

@app.route('/')
def top():
    return '<br />'.join(
            ['<a href="/commands/%s">%s</a>' % (command.lower(), command)
                for command in nagext_commands]
            )


@app.route('/commands/<name>', methods=['GET', 'POST'])
def command(name):
    if name.upper() not in nagext_commands:
        abort(404)
    if request.method == 'POST':
        return post_command(name)

    command = nagext_commands[name.upper()]
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
    with closing(open(app.config['COMMAND_FILE'], 'a+')) as f:
        f.write(command_string)
    return 'OK'


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])

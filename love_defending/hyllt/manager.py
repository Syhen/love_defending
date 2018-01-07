# -*- coding: utf-8 -*-
"""
create on 2018-01-07 下午7:39

author @heyao
"""

import os
from logging import FileHandler
from time import strftime

from app import create_app
from flask import request
# from flask_migrate import MigrateCommand, Migrate
from flask_script import Shell, Server, Manager


app = create_app(os.environ.get('LD_CONFIG_NAME', 'default'))
# migrate = Migrate(app, db)


# def shell_command():
#     return dict(app=app, db=db, User=User, Role=Role)


# manager = Manager(app, db)
manager = Manager(app)
server = Server(app.config['HOST'], app.config['PORT'])
# manager.add_command('shell', Shell(make_context=shell_command))
# manager.add_command('db', MigrateCommand)
manager.add_command('runserver', server)

app.logger.setLevel('INFO')
app.logger.addHandler(FileHandler(app.config['LOG_PATH']))


@app.after_request
def after_request(response):
    msg = dict(
        hosts=request.remote_addr,
        method=request.method,
        path='/%s' % '/'.join(request.url.split('/')[3:]),
        date=strftime('%d/%b/%Y %H:%M:%S'),
        status=response.status_code
    )
    if 'favicon.ico' not in msg['path']:
        log_message = '{hosts} - - [{date}] "{method} {path} HTTP/1.1" {status} -'.format(**msg)
        app.logger.info(msg=log_message)
    return response


if __name__ == '__main__':
    manager.run()

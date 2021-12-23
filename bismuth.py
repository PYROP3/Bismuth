from bots import available_bots
from datetime import datetime
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request
from random import random
from threading import Thread, Event
from time import sleep

import logging
import os
import subprocess
import sys

app = Flask(__name__)
app.logger.root.setLevel(logging.getLevelName(os.getenv('LOG_LEVEL') or 'DEBUG'))
socketio = SocketIO(app)

def tag_time(msg):
    return "[{}] {}".format(datetime.now().strftime("%d/%b/%Y %H:%M:%S"), msg)

class LogListener():
    def info(self, msg):
        socketio.emit('data', {'data': tag_time(msg)}, namespace='/log')
        app.logger.info(msg)

    def debug(self, msg):
        socketio.emit('data', {'data': tag_time(msg)}, namespace='/log')
        app.logger.debug(msg)

    def warn(self, msg):
        socketio.emit('data', {'data': tag_time(msg)}, namespace='/log')
        app.logger.warn(msg)

logger = LogListener()

class BotStdoutLogger(Thread):
    def __init__(self, stdout, namespace):
        self.stdout = stdout
        self.namespace = "/logs/" + namespace
        self._kill = Event()
        super(BotStdoutLogger, self).__init__()

    def kill(self):
        self._kill.set()

    def run(self):
        for stdout_line in self.get_lines():
            if len(stdout_line):
                # print(f"{stdout_line.rstrip()} -> {self.namespace}")
                socketio.emit('data', {'data': tag_time(stdout_line)}, namespace=self.namespace)

    def get_lines(self):
        while not self._kill.isSet():
            yield self.stdout.readline()

class BotManager(Thread):
    def __init__(self, bot_folder, bot_file, bot_id):
        self.bot_file = os.path.join(os.getcwd(), "bots", bot_folder, bot_file)
        self.bot_id = bot_id
        self.subprocess = None
        super(BotManager, self).__init__()

    def run(self, *args, **kwargs):
        logger.info(f"Starting manager for {self.bot_file}")

    def start_bot(self, *args, **kwargs):
        logger.info(f"Starting bot {self.bot_file}")
        self.subprocess = subprocess.Popen([sys.executable, self.bot_file], stdout=subprocess.PIPE, universal_newlines=True)
        self.logger = BotStdoutLogger(self.subprocess.stdout, self.bot_id)
        self.logger.start()

    def bot_running(self):
        return self.subprocess is not None and self.subprocess.returncode is not None

    def kill_bot(self):
        if self.subprocess is not None:
            self.subprocess.terminate()
            self.logger.kill()
            self.subprocess = None
            self.logger = None

    def bot_retcode(self):
        return self.subprocess.returncode if self.subprocess is not None else None

# Dictionary with references to all of the bots
bots = {}
for bot_id, folder, bot_file in available_bots:
    bots[bot_id] = BotManager(folder, bot_file, bot_id)


logger.info("Starting all bot managers")
for key in bots:
    logger.debug(f"-> {key}")
    bots[key].start()

@app.route("/")
def _index():
    return render_template('index.html')
    
@app.route("/bots/<bot_id>", methods=["POST"])
def _bots(bot_id, *args, **kwargs):
    data = request.get_json(force=True)
    status = data['status']
    bot_mgr = bots[bot_id]
    logger.debug(f"Bot {bot_id} received setting {status}")
    if status == 'start':
        bot_mgr.start_bot()
    elif status == 'restart':
        bot_mgr.kill_bot()
        bot_mgr.start_bot()
    elif status == 'stop':
        bot_mgr.kill_bot()
    return "Success: {}".format(bot_mgr.bot_retcode())

if __name__ == '__main__':
    try:
        socketio.run(app)
    except KeyboardInterrupt:
        logger.info("Captured KeyboardInterrupt, exiting cleanly")
        for key in bots:
            bots[key].kill_bot()
        exit(0)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author    : Yang
# Creadted  : 2017-04-17 23:10:28

import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def log(s):
    print "[Monitor] %s" % s

class PyChangeEventHandler(FileSystemEventHandler):
    def __init__(self, handler):
        super(PyChangeEventHandler, self).__init__()
        self.handler = handler

    def on_any_event(self, event):
        if event.src_path.endswith(".py"):
            log("Python source file changed: %s" % event.src_path)
            self.handler()

command = ["echo", "ok"]
process = None

def start_process():
    global command, process
    log("Start process %s..." % ' '.join(command))
    process = subprocess.Popen(command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)

def kill_process():
    global command, process
    if process:
        log("Kill process [%s]..." % process.pid)
        process.kill()
        process.wait()
        log("Process exit with code %s." % process.returncode)
        process = None

def restart_process():
    kill_process()
    start_process()

def start_watch(path, recursive=True):
    observer = Observer()
    observer.schedule(PyChangeEventHandler(restart_process), path, recursive=recursive)
    observer.start()
    log("Wathing directory %s..." % path)
    start_process()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    argv = sys.argv[1:]
    if not argv:
        print "Usage: python %s XXX.py" % sys.argv[0]
        exit(0)
    if argv[0] != "python":
        argv.insert(0, "python")
    command = argv
    path = os.path.abspath(".")
    recursive = True
    if len(argv) == 3:
        recursive = False
        command.pop(2)
    start_watch(path, recursive)

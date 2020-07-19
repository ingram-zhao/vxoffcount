# !/usr/bin/env python3
# encoding: utf-8
import sys, logging
from wsgilog import WsgiLog
import config

class Log(WsgiLog):
    def __init__(self, application):
        WsgiLog.__init__(
            self,
            application,
            logformat = config.logformat,
            datefmt = config.datefmt,
            tofile = True,
            file = config.file,
            interval = config.interval,
            backups = config.backups
            )
        # sys.stdout = LogIO(self.logger, logging.INFO)
        # sys.stderr = LogIO(self.logger, logging.ERROR)
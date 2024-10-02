import os
import sys
sys.path.append('./venv/Lib/site-packages')
import logging
import logging.handlers
from colorlog import ColoredFormatter
from io import StringIO

def setupCustomLogging(scriptNameFromMain):
    if scriptNameFromMain:
        scriptName = scriptNameFromMain
    else:
        scriptName = os.path.basename(__file__)
    scriptFolder = os.path.dirname(__file__)
    logFile = scriptName + '-debug.log'
    logFolder = scriptFolder
    logFullPath = logFolder + '\\' + logFile

    print(scriptName)

    # Class for setting specific logging levels for handler.
    class LevelFilter(logging.Filter):
        def __init__(self, levels):
            self.levels = levels

        def filter(self, record):
            return record.levelno in self.levels

    # Configure global logging settings
    loggingGlobalFormatter = logging.Formatter('%(asctime)s %(levelname)-8s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().setLevel(logging.NOTSET) # Change root logger level from WARNING (default) to NOTSET in order for all messages to be delegated.

    # Configure logging to console
    loggingConsoleHandler = logging.StreamHandler(sys.stdout)
    loggingConsoleFormatter = ColoredFormatter('%(log_color)s%(asctime)s %(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s', datefmt='%Y-%m-%d %H:%M:%S')
    loggingConsoleHandler.setFormatter(loggingConsoleFormatter)
    logging.getLogger().addHandler(loggingConsoleHandler)

    # Configure logging to variable for Warnings, Errors and Critical
    loggingVariable = StringIO()
    loggingVariableHanlder = logging.StreamHandler(loggingVariable)
    loggingVariableHanlder.setFormatter(loggingGlobalFormatter)
    loggingVariableHanlder.addFilter(LevelFilter((logging.WARNING, logging.ERROR, logging.CRITICAL)))
    logging.getLogger().addHandler(loggingVariableHanlder)

    # Create logFolder if it doesn't exist
    if not os.path.exists(logFolder):
        try:
            os.makedirs(logFolder)
            logging.info('Logs directory created: [' + logFolder + ']')
        except:
            raise SystemError('Failed to create logs directory [' + logFolder + ']!')

    # Configure logging to file
    loggingRotatingHandler = logging.handlers.RotatingFileHandler(filename=logFullPath, maxBytes=3145728, backupCount=1) # Add file rotating handler with 3MB limit
    loggingRotatingHandler.setFormatter(loggingGlobalFormatter)
    logging.getLogger().addHandler(loggingRotatingHandler)
    
    return logging
#!/usr/bin/env python3
import argparse, logging, glob, importlib
import configparser
from pathlib import Path

def getHandlers():
    handlerFiles = glob.glob("./handlers/*.py")
    handlerModules = []
    for file in handlerFiles:
        moduleName = Path(file).stem
        handlerModules.append(importlib.import_module("handlers."+moduleName).exportedClass)
    return handlerModules


def getHandles(handlers):
    modes = ["auto"]
    for handler in handlers:
        modes.extend(handler.handles)
    return modes


def getMacros():
    config = configparser.ConfigParser(allow_no_value=True)
    config.read('macros.ini')
    macros = {str(key):
                  [str(k) for k in config[key].keys()]
              for key in config.keys() if not str(key) == "DEFAULT"}
    return macros


def parseRequestedHandlers(macros, use):
    handlers = []
    for macro in macros:
        if not macro == "auto":
            handlers.extend(getMacros()[macro])
    if use:
        handlers.extend(use)
    handlers = list(set(handlers)) # remove duplicates
    return handlers


def getArgs(handles, handlers):
    parser = argparse.ArgumentParser(description='Archives digital content.')

    parser.add_argument('macro', help='a set of handlers to use (set this with TODO)'.format(handles),
                        nargs="+", default="auto")
    parser.add_argument('--use', help='what handlers to use'.format(handles), nargs="+",
                        choices=handles)
    parser.add_argument('--upload', action="store_true", help='upload to archive.org')
    parser.add_argument('--debug', action="store_true", help='enable debug logging')
    parser.add_argument('--url-hash', action="store_true", help='upload to archive.org')
    parser.add_argument('--filename', help='filename to archive to')
    parser.add_argument('--overwrite', help='disable prompts if file(s) already exist')
    parser.add_argument('--log', help='filename to write log files to')
    parser.add_argument('--filename-clip', help='limit on length of filename', default=100)
    parser.add_argument('--hash-clip', help='limit on length of hash in filename', default=8)
    parser.add_argument('urls', help='url to archive', nargs="+")

    for handler in handlers:
        parser = handler.add_arguments(parser)

    return parser.parse_args()


def initLogging(logFileName, debug):
    level = logging.DEBUG if debug else logging.INFO
    logFile = logFileName+".sak.log" if logFileName else None
    formatStr = '[%(name)s][%(levelname)8s] %(message)s'
    logging.basicConfig(filename=logFile, level=level, format=formatStr)
    return logging.getLogger("asak")


handlers = getHandlers()
handles = getHandles(handlers)
args = getArgs(handles, handlers)
urls, logFileName, debug = args.urls, args.log, args.debug
macro, use = args.macro, args.use

logger = initLogging(logFileName, debug)
requestedHandlers = parseRequestedHandlers(macro, use)


for url in urls:
    for handler in handlers:
        for requestedHandle in requestedHandlers:
            if requestedHandle in handler.handles:
                handler().handle(url, args, requestedHandle)



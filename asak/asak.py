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

def parseRequestedHandlers(macro, use):
    return ["wayback"]


def getArgs(handles):
    parser = argparse.ArgumentParser(description='Archives digital content.')

    parser.add_argument('macro', help='a set of handlers to use (set this with TODO)'.format(handles),
                        nargs="+", default="auto")
    parser.add_argument('--use', help='what handlers to use'.format(handles), nargs="+",
                        choices=handles)
    parser.add_argument('--upload', action="store_true", help='upload to archive.org')
    parser.add_argument('--debug', action="store_true", help='enable debug logging')
    parser.add_argument('--url-hash', action="store_true", help='upload to archive.org')
    parser.add_argument('--filename', help='filename to archive to')
    parser.add_argument('--log', help='filename to write log files to')
    parser.add_argument('--filename-clip', help='limit on length of filename', default=100)
    parser.add_argument('urls', help='url to archive', nargs="+")

    return parser.parse_args()

handlers = getHandlers()
handles = getHandles(handlers)

args = getArgs(handles)
requestedHandlers = parseRequestedHandlers(args.macro, args.use)
urls = args.urls

level = logging.DEBUG if args.debug else logging.INFO
logFile = args.log+".sak.log" if args.log else None
formatStr = '[%(name)s][%(levelname)8s]\t %(message)s'
logging.basicConfig(filename=logFile, level=level, format=formatStr)


for url in urls:
    for handler in handlers:
        for requestedHandle in requestedHandlers:
            if requestedHandle in handler.handles:
                handler().handle(url, args)



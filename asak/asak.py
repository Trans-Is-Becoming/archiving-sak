#!/usr/bin/env python3
import sys, argparse, logging



modes=["auto", "video", "subreddit", "webpage", "website"]
parser = argparse.ArgumentParser(description='Archives digital content.')

parser.add_argument('mode', help='mode ({})'.format(modes))
parser.add_argument('--upload', action="store_true", help='upload to archive.org')
parser.add_argument('--debug', action="store_true", help='enable debug logging')
parser.add_argument('--url-hash', action="store_true", help='upload to archive.org')
parser.add_argument('--filename', help='filename to archive to')
parser.add_argument('--log', help='filename to write log files to')
parser.add_argument('--filename-clip', help='limit on length of filename', default=100)
parser.add_argument('urls', nargs='+', help='url to archive')

args = parser.parse_args()
mode = args.mode
urls = args.urls

level = logging.DEBUG if args.debug else logging.INFO
logging.basicConfig(level=level)
formatStr = '[%(name)s][%(levelname)8s]\t %(message)s'
formatter = logging.Formatter(formatStr)
timeFormatter = logging.Formatter('[%(asctime)s]'+formatStr)
ch = logging.StreamHandler()
ch.setLevel(level)
ch.setFormatter(formatter)

if args.log:
    fh = logging.FileHandler(args.log+".sak.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(timeFormatter)

for url in urls:
    l = logging.getLogger(url[0:100])
    l.propagate = False
    l.addHandler(ch)
    if args.log:
        l.addHandler(fh)
    if mode == "webpage":
        from handlers.webpage import Webpage
        Webpage().handle(url, args)
    if mode == "subreddit":
        from handlers.subreddit import Subreddit
        Subreddit().handle(url, args)



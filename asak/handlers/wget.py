#!/usr/bin/env python3
import sys, logging, os
from shutil import which
import subprocess

sys.path.append("..")
from base import BaseHandler


class WGet(BaseHandler):
    handles = ["wget"]

    def __init__(self):
        self.name = "wget"
        self.logger = logging.getLogger(self.name)

    @staticmethod
    def add_arguments(parser):
        parser.add_argument('--wget-options', help='url to archive', default="")
        return parser

    @staticmethod
    def urlToFilename(url):
        import unicodedata, re
        value = unicodedata.normalize('NFKD', url.strip().lower()).encode('ascii', 'ignore').decode("ascii")
        value = re.sub('[^\.\w\s-]', '', value)
        return re.sub('[-\s]+', '-', value)

    def handle(self, url, args):
        if which("wget") is None:
            self.logger.critical("Please install wget or add it to your path to use this module!")
            exit(1)
        filename = ""
        if args.filename:
            filename = args.filename
        if args.url_hash or not args.filename:
            from hashlib import sha256
            urlhash = sha256(url.encode()).hexdigest()[0:args.hash_clip]
            if not args.filename:
                filename = urlhash + "-" + self.urlToFilename(url)
            else:
                filename = urlhash + "-" + filename

        if filename[-5:] == ".warc":
            filename = filename[:-5]
        self.logger.info("Writing warc to " + filename + ".warc")
        result = subprocess.check_output(
            f'wget -E -H -k -p -q --delete-after --no-warc-compression --warc-file={filename} {url}',
            shell=True, stderr=subprocess.STDOUT)
        if len(result) == 0:
            self.logger.debug("wget returned no response (which is good).")
        else:
            self.logger.critical("wget returned"+result)
        os.setxattr(filename+".warc", "user.url", url.encode())
        with open(filename+".url", "w") as f:
            self.logger.info("Writing url to " + filename + ".url")
            f.write(url)


exportedClass = WGet

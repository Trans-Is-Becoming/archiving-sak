#!/usr/bin/env python3
import sys, logging, os

sys.path.append("..")
from utils import BaseHandler


class Subreddit(BaseHandler):
    handles = ["reddit"]
    name = "redditPostArchiver"

    def __init__(self):
        self.logger = logging.getLogger(self.name)

    @staticmethod
    def add_arguments(parser):
        return parser

    def handle(self, url, args, handle):
        logging.info("Archiving " + url)
        os.system(f"/home/gwynu/Documents/tibi/redditPostArchiver/subreddit.py {url}")


exportedClass = Subreddit

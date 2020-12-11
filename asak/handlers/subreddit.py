#!/usr/bin/env python3
import sys, logging, os
sys.path.append("..")
from base import BaseHandler

class Subreddit(BaseHandler):
    handles = ["reddit"]
    def __init__(self):
        self.name = "redditPostArchiver"
        self.logger = logging.getLogger(self.name)

    def handle(self, url, args, handle):
        logging.info("Archiving "+url)
        os.system("/home/gwynu/Documents/tibi/redditPostArchiver/subreddit.py ExcavatorSkills")

exportedClass = Subreddit

#!/usr/bin/env python3
import sys, argparse, logging
sys.path.append("..")
from base import BaseHandler

class Webpage(BaseHandler):
    def __init__(self):
        pass

    def handle(self, url, args):
        try:
            from archivenow.handlers import warc_handler
            from archivenow.handlers import ia_handler
            warcHandler = warc_handler.WARC_handler()
            iaHandler = ia_handler.IA_handler()
        except ModuleNotFoundError as e:
            logging.critical(
                "Please install archivenow from https://github.com/oduwsdl/archivenow to download webpages. (alternatively, install via pip `pip install archivenow`)")
            raise e
        filename = ""
        if args.filename:
            filename = args.filename
        if args.url_hash or not args.filename:
            from hashlib import sha256
            urlhash = sha256(url.encode()).hexdigest()[0:args.filename_clip]
            if not args.filename:
                if not args.url_hash:
                    logging.warning(
                        "No filename specified, generating hash to use as filename (use --url-hash to disable this warning)")
                filename = urlhash
            else:
                filename = filename + "-" + urlhash
        archivedUrl = warcHandler.push(url, {"warc": filename})
        logging.info("Writing warc to " + filename + ".warc")
        if args.upload:
            logging.info("Adding to archive.org")
            archivedUrl = iaHandler.push(url)
            logging.info(f"Archived url is {archivedUrl}")
        import os
        os.setxattr(filename + ".warc", "user.url", url.encode())
        with open(filename + ".url", "w") as f:
            logging.info("Writing url to " + filename + ".url")
            f.write(url)
            if args.upload:
                f.write("\n" + archivedUrl)

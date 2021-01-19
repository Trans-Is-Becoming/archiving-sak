#!/usr/bin/env python3
import sys, logging, os
from shutil import which
import subprocess

sys.path.append("..")
import utils


class WGet(utils.BaseHandler):
    handles = ["wget-uri", "wget-crawler"]
    name = "wget"

    def __init__(self):
        self.logger = logging.getLogger(self.name)

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group(WGet.name)
        group.add_argument('--wget-options', help='url to archive', default="")
        return parser


    def wgetUri(self, url, args):
        directory, filename = utils.getUrlDir(args.filename, url, args.url_hash, args.overwrite)
        self.logger.info("Writing warc to " + filename + ".warc")

        try:
            result = subprocess.check_output(
                f'wget -E -H -k -p -q --delete-after --no-warc-compression -o {os.path.join(directory, "wget.log")} --warc-file={filename} {url}',
                shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            self.logger.warning(e)
            result = ""
        if len(result) == 0:
            self.logger.debug("wget returned no response (which is good).")
        else:
            self.logger.warning("wget returned: " + result)
        os.setxattr(filename + ".warc", "user.url", url.encode())
        with open(filename + ".url", "w") as f:
            self.logger.info("Writing url to " + filename + ".url")
            f.write(url)

    def wgetCrawler(self, url, args):
        directory, filename = utils.getUrlDir(args.filename, url, args.url_hash, args.overwrite)
        crawlingCommand = "wget --page-requisites --adjust-extension --convert-links --level inf --recursive " \
                          f"--no-remove-listing --restrict-file-names=windows --no-parent -w 1 --warc-file={os.path.join(directory, 'archive')} " \
                          f"--warc-max-size=1G -o {os.path.join(directory, 'wget.log')} --no-check-certificate --directory-prefix={directory} " # trailing space is important as the url is directly appended to this string
        # proxyFlags = "-e use_proxy=yes -e http_proxy=127.0.0.1:9090 -e https_proxy=127.0.0.1:9090 "
        try:
            result = subprocess.check_output(
                crawlingCommand + url,
                shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            self.logger.warning(e)

    def handle(self, url, args, handle):
        if which("wget") is None:
            self.logger.critical("Please install wget or add it to your path to use this module!")
            exit(1)
        if handle == "wget-uri":
            self.wgetUri(url, args)
        elif handle == "wget-crawler":
            self.wgetCrawler(url, args)


exportedClass = WGet

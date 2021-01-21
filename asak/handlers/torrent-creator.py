#!/usr/bin/env python3
import sys, logging, os

sys.path.append("..")
from . import utils

class TorrentCreator(utils.BaseHandler):
    handles = ["torrent-create", "ctorrent"]
    name = "torrent-creator"

    def __init__(self):
        self.logger = logging.getLogger(self.name)

    @staticmethod
    def add_arguments(parser):
        group = parser.add_argument_group(TorrentCreator.name)
        #group.add_argument('--wget-options', help='url to archive', default="")
        return parser

    def createTorrentFile(self, fileDir, fileName, url):
        try:
            from torf import Torrent
        except ModuleNotFoundError as e:
            self.logger.critical(
                "Please install torf from https://github.com/rndusr/torf to create torrent files.")
            raise e
        trackers = ['udp://tracker.openbittorrent.com:80', 'udp://tracker.leechers-paradise.org:6969',
         'udp://tracker.coppersurfer.tk:6969', 'udp://glotorrents.pw:6969', 'udp://tracker.opentrackr.org:1337',
         'udp://tracker.publicbt.com:80/announce', 'udp://tracker.ccc.de:80', 'udp://tracker.istole.it:80',
         'http://tracker.publicbt.com:80/announce', 'http://tracker.openbittorrent.com/announce']
        t = Torrent(path=fileDir,
                    trackers=trackers,
                    comment=url)
        t.private = True
        t.generate()
        t.write(fileName+'.torrent')

    def handle(self, url, args, handle):
        fileDir, fileName = utils.getUrlDir(None, url, args.url_hash, args.overwrite, createDir=False)
        self.createTorrentFile(fileDir, fileName, url)


exportedClass = TorrentCreator

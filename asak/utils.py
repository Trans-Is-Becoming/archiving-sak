from abc import ABC, abstractmethod
import unicodedata, re
from hashlib import md5
from urllib.parse import urlparse
import os


class BaseHandler(ABC):
    def __init__(self):
        self.handles = []

    def handle(self, url, args, handle):
        pass


def sanitizeUrl(url):
    url = "".join(urlparse(url)[1:])
    if url[-1]=="/":
        url = url[0:-1]
    url = url.replace("/", "-")
    value = unicodedata.normalize('NFKD', url.strip().lower()).encode('ascii', 'ignore').decode("ascii")
    value = re.sub('[^\.\w\s-]', '', value)
    return re.sub('[-\s]+', '-', value)


def urlToFilename(url, hash=True, hash_clip=8):
    if hash:
        urlhash = md5(url.encode()).hexdigest()[0:hash_clip]
        return urlhash + "-" + sanitizeUrl(url)
    else:
        return sanitizeUrl(url)


def getUrlDir(filename, url, useHash, overwrite, createDir=True):
    if filename:
        filename = filename
        if filename[-5:] == ".warc":
            filename = filename[:-5]
    else:
        filename = urlToFilename(url, hash=False)
    directory = urlToFilename(url, hash=useHash)
    if createDir:
        try:
            os.makedirs(directory)
        except FileExistsError as e:
            if not overwrite:
                r = input("{} already exists. overwrite? [N/y]: ".format(directory))
                if not r.lower() in ["y", "yes"]:
                    print("Okay. Exiting...")
                    exit(0)
    filename = os.path.join(directory, filename)
    return directory, filename

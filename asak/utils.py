from abc import ABC, abstractmethod
import unicodedata, re
from hashlib import md5


class BaseHandler(ABC):
    def __init__(self):
        self.handles = []

    def handle(self, url, args, handle):
        pass


def sanitizeUrl(url):
    value = unicodedata.normalize('NFKD', url.strip().lower()).encode('ascii', 'ignore').decode("ascii")
    value = re.sub('[^\.\w\s-]', '', value)
    return re.sub('[-\s]+', '-', value)


def urlToFilename(url, hash=True, hash_clip=8):
    if hash:
        urlhash = md5(url.encode()).hexdigest()[0:hash_clip]
        return urlhash + "-" + sanitizeUrl(url)
    else:
        return sanitizeUrl(url)

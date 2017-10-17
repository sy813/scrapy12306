#!/usr/bin/env python
from scrapy.dupefilters import RFPDupeFilter

import logging

logger = logging.getLogger()


class URLTurnFilter(RFPDupeFilter):
    def request_fingerprint(self, request):
        if "turn" in request.meta:
            return request.url + ("-- %d" % request.meta["turn"])
        else:
            return request.url

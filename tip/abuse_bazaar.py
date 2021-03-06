from ioc import Intel
import requests
import hashlib
from time import time


class URLhaus:

    def __init__(self):
        self._raw_threat_intel = None
        self.intel = []
        self._retrieved = None
        self._feed_url = "https://urlhaus.abuse.ch/downloads/csv_recent/"

    def run(self):
        self._download()
        self._parse()

    def _download(self):
        self._retrieved = time()
        response = requests.get(self._feed_url)
        if response.status_code is 200:
            self._raw_threat_intel = response.text

    def _parse(self):
        for line in self._raw_threat_intel.split("\n"):
            if line[:1] is "#":
                pass
            else:
                split_line = line.split('","')
                try:
                    intel = Intel(
                        original=line,
                        event_type="indicator",
                        event_reference=self._feed_url,
                        event_module="Abuse.ch",
                        event_dataset="URLhaus",
                        threat_first_seen=split_line[1],
                        threat_last_seen=None,
                        threat_type="domain",
                        threat_description=split_line[4]
                    )
                    intel.intel["threat"]["url"] = {}
                    intel.intel["threat"]["url"]["full"] = split_line[2]
                except IndexError:
                    pass
                else:
                    intel._add_docid()
                    self.intel.append(intel)


class MalwareBazaar:

    def __init__(self):
        self._raw_threat_intel = None
        self.intel = []
        self._retrieved = None
        self._feed_url = "https://bazaar.abuse.ch/export/csv/recent/"

    def run(self):
        self._download()
        self._parse()

    def _download(self):
        self._retrieved = time()
        response = requests.get(self._feed_url)
        if response.status_code is 200:
            self._raw_threat_intel = response.text

    def _parse(self):
        for line in self._raw_threat_intel.split("\n"):
            if line[:1] is "#":
                pass
            else:
                try:
                    split_line = line.split('", "')
                    intel = Intel(
                        original=line,
                        event_type="indicator",
                        event_reference=self._feed_url,
                        event_module="Abuse.ch",
                        event_dataset="MalwareBazaar",
                        threat_first_seen=split_line[0],
                        threat_last_seen=None,
                        threat_type="file_hash"
                    )
                    intel.intel["threat"]["file"] = {}
                    intel.intel["threat"]["file"]["hash"] = {}
                    intel.intel["threat"]["file"]["hash"]["sha1"] = split_line[3]
                    intel.intel["threat"]["file"]["hash"]["sha256"] = split_line[1]
                    intel.intel["threat"]["file"]["hash"]["md5"] = split_line[2]
                except Exception as err:
                    print(err)
                else:
                    intel._add_docid()
                    self.intel.append(intel)


class FeodoTracker:

    def __init__(self):
        self._raw_threat_intel = None
        self.intel = []
        self._retrieved = None
        self._feed_url = "https://feodotracker.abuse.ch/downloads/ipblocklist.csv"

    def run(self):
        self._download()
        self._parse()

    def _download(self):
        self._retrieved = time()
        response = requests.get(self._feed_url)
        if response.status_code is 200:
            self._raw_threat_intel = response.text

    def _parse(self):
        for line in self._raw_threat_intel.split("\n"):
            if line[:1] is "#":
                pass
            else:
                split_line = line.split(",")
                try:
                    intel = Intel(
                        original=line,
                        event_type="indicator",
                        event_reference=self._feed_url,
                        event_module="Abuse.ch",
                        event_dataset="FeodoTracker",
                        threat_first_seen=split_line[0],
                        threat_last_seen=split_line[3],
                        threat_type="ip_address",
                        threat_description=split_line[4]
                    )
                    intel.intel["threat"]["ip"] = split_line[1]
                except IndexError as err:
                    pass
                else:
                    intel._add_docid()
                    self.intel.append(intel)


class SSLBlacklist:

    def __init__(self):
        self._raw_threat_intel = None
        self.intel = []
        self._retrieved = None
        self._feed_url = "https://sslbl.abuse.ch/blacklist/sslblacklist.csv"

    def run(self):
        self._download()
        self._parse()

    def _download(self):
        self._retrieved = time()
        response = requests.get(self._feed_url)
        if response.status_code is 200:
            self._raw_threat_intel = response.text

    def _parse(self):
        for line in self._raw_threat_intel.split("\n"):
            if line[:1] is "#":
                pass
            else:
                split_line = line.split(",")
                try:
                    intel = Intel(
                        original=line,
                        event_type="indicator",
                        event_reference=self._feed_url,
                        event_module="Abuse.ch",
                        event_dataset="SSLBlackList",
                        threat_first_seen=split_line[0],
                        threat_last_seen=None,
                        threat_type="ssl_hash",
                        threat_description=split_line[2]
                    )
                    intel.intel["threat"]["server"] = {}
                    intel.intel["threat"]["server"]["hash"] = {}
                    intel.intel["threat"]["server"]["hash"]["sha1"] = split_line[1]
                    if "C&C" in intel.intel["threat"]["description"]:
                        intel.add_mitre("TA0011")
                    elif "" in intel.intel["threat"]["description"]:
                        intel.add_mitre("TA0042", "T1588.001")
                except IndexError as err:
                    pass
                else:
                    intel._add_docid()
                    self.intel.append(intel)
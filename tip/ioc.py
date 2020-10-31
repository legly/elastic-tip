from datetime import datetime
import json
import re
import hashlib


class IOC:

    def __init__(self, ref=[], value="", type="", pname="", pcreator=None, pref=None, original=None):
        self.id = None
        self.ioc = {
          "reference": ref,
          "value": value,
          "type": type,
          "provider": {
            "name": pname
          }
        }
        if pcreator:
            self.ioc["provider"]["creator"] = pcreator
        if original:
            self.ioc["original"] = original
        if pref:
            self.ioc["provider"]["reference"] = pref
        self.threat = None
        self.vulnerability = None
        self.rule = None
        self._validate()
        self._add_docid()

    def _validate(self):
        """Validate the ioc holds to the schema"""

        # reference should be an empty array or an array of URL's
        urlmatch = 'https?:\/\/'
        if len(self.ioc["reference"]) > 0:
            for x in self.ioc["reference"]:
                if re.search(urlmatch, x):
                    continue
                else:
                    raise SchemaException("The IOC reference field is not a URL: {}".format(x))

        # Validate the type is one of the accepted values
        type_accepted = ["hash", "domain", "ip", "string", "unknown"]
        if self.ioc["type"] not in type_accepted:
            raise SchemaException("The IOC type field is not one of {}".format(type_accepted))

    def _add_docid(self):
        self.id = hashlib.sha1(json.dumps(self.ioc).encode('utf-8')).hexdigest()


class Intel:

    def __init__(self,
                 original=None,
                 event_type=None,
                 event_reference=None,
                 event_module=None,
                 event_dataset=None,
                 threat_first_seen=datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
                 threat_last_seen=datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
                 threat_last_update=None,
                 threat_type=None):
        """"""
        self.intel = {
            "event": {
                "kind": "enrichment",
                "category": "threat",
                "type": event_type,
                "reference": event_reference,
                "module": event_module,
                "dataset": event_dataset,
                "severity": 0,
                "risk_score": 0,
                "original": original
            },
            "threat": {
                "time": {
                    "first_seen": threat_first_seen,
                    "last_seen": threat_last_seen,
                    "last_updated": threat_last_update
                },
                "sightings": 0,
                "type": threat_type
            }
        }

    def add_mitre(self, tactic=None, technique=None):
        """

        :param tactic: Tactic ID e.g TA0002
        :param technique: Technique ID e.g T1059
        :return:
        """

        if tactic or technique:
            self.intel["threat"]["framework"] = "MITRE ATT&CK"

        if tactic:
            self.intel["threat"]["tactic"]["id"] = tactic

        if technique:
            self.intel["threat"]["technique"]["id"] = tactic


class SchemaException(Exception):
    pass
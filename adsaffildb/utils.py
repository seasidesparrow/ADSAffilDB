import json
import os
import requests

from adsputils import load_config, setup_logging

proj_home = os.path.realpath(os.path.dirname(__file__))
config = load_config(proj_home=proj_home)
logger = setup_logging(
    "run.py",
    proj_home=proj_home,
    level=config.get("LOGGING_LEVEL", "INFO"),
    attach_stdout=config.get("LOG_STDOUT", False),
)


class AffIdDictException(Exception):
    pass


class MatchDictException(Exception):
    pass


def read_match_dict(filename=None):
    try:
        matchMap = []
        with open(filename, "r") as fd:
            for line in fd.readlines():
                matchData = line.strip().split("\t")
                if len(matchData) != 2:
                    logger.warning("Bad line in %s: %s" % (filename, line.strip()))
                else:
                    match = {"data_id": matchData[0], "data_pubstring": matchData[1]}
                    matchMap.append(match)
        return matchMap
    except Exception as err:
        raise MatchDictException(
            "Could not read curated match dictionary, %s: %s" % (filename, err)
        )


def read_affid_dict(filename=None):
    try:
        affIdDict = {}
        affIdMap = []
        with open(filename, "r") as fd:
            for line in fd.readlines():
                affIdData = line.rstrip().split("\t")
                if len(affIdData) != 5:
                    print(line)
                country = affIdData[0]
                parentId = affIdData[1]
                affId = affIdData[2]
                abbrev = affIdData[3]
                canonical = affIdData[4]
                if not affIdDict.get(affId, None):
                    affIdDict[affId] = {
                        "inst_country": country,
                        "inst_parents": [parentId],
                        "inst_abbreviation": abbrev,
                        "inst_canonical": canonical,
                    }
                else:
                    current = affIdDict.get(affId)
                    current["inst_parents"].append(parentId)
                    affIdDict[affId] = current
        if affIdDict:
            for k, v in affIdDict.items():
                rec = {**v}
                rec["inst_parents"] = json.dumps(rec["inst_parents"])
                rec.setdefault("inst_id", k)
                affIdMap.append(rec)
        return affIdMap
    except Exception as err:
        raise AffIdDictException("Could not read affil id dictionary: %s" % err)


def return_query(url, method="get", data="", headers="", verify=False):
    try:
        if method.lower() == "get":
            rQuery = requests.get(url)
        elif method.lower() == "post":
            rQuery = requests.post(url, data=data, headers=headers, verify=False)       
        if rQuery.status_code != 200:
            raise RequestsException("Return code error: %s" % rQuery.status_code)   
        else:
            return rQuery.json()
    except Exception as err:
        raise RequestsException("Error in return_query: %s" % err)


def solr_query_one(token="*", url=None):
    try:
        resp = return_query(url, method="get")
        new_token = resp.get("nextCursorMark", None)
    except Exception as err:
        raise SolrQueryException("Failed Solr query: %s" % err)
    else:
        documents = resp.get("response", {}).get("docs", [])
        return (new_token, documents)

def parse_one_solr_record(rec):
    record_data = []
    try:
        affid_rec = rec.get("aff_id", "-")
        affil_rec = rec.get("aff", "-")
        if len(affid_rec) == len(affil_rec):
            for affid_auth, affil_auth in zip(affid_rec, affil_rec):
                affids = affid_auth.split(";")
                affil_auth = utils.clean_string(affil_auth)
                affils = affil_auth.split(";")
                if len(affids) == len(affils):
                    for affid, aff in zip(affids, affils):
                        r = {"curation_id": affid,
                             "curation_string": aff,
                             "curation_count": 1}
                        record_data.append(r)
                else:
                    logger.warning("Mismatched affil/affid count for author: (%s, %s)" % (affids, affils))
        else:
            logger.warning("Mismatched affils/affids count in Solr record: %s" % rec)
    except Exception as err:
        logger.warning("Failed to parse solr record: %s" % err)
    return record_data



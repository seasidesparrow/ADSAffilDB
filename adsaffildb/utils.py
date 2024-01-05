import logging

class AffIdDictException(Exception):
    pass


class MatchDictException(Exception):
    pass


def read_match_dict(filename=None):
    try:
        matchDict = {}
        with open(filename, "r") as fd:
            for line in fd.readlines():
                matchData = line.strip().split("\t")
                if len(matchData) != 2:
                    logger.warning("Bad line in %s: %s" % filename, line.strip())
                else:
                    matchDict[matchData[1]] = matchData[0]
        return matchDict
    except Exception as err:
        raise MatchDictException("Could not read curated match dictionary, %s: %s" % (filename, err))


def read_affid_dict(filename=None):
    try:
        affIdDict = {}
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
                    affIdDict[affId] = {"country": country,
                                        "parentId": [parentId],
                                        "abbrev": abbrev,
                                        "canonical": canonical}
                else:
                    current = affIdDict.get(affId)
                    current["parentId"].append(parentId)
                    affIdDict[affId] = current
        return affIdDict
    except Exception as err:
        raise AffIdDictException("Could not read affil id dictionary: %s" % err)

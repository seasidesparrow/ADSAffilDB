import os
import time
import adsaffildb.utils as utils
from adsputils import load_config, setup_logging

proj_home = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))
conf = load_config(proj_home=proj_home)
logger = setup_logging(
    "solr_query",
    proj_home=proj_home,
    level=config.get("LOGGING_LEVEL", "INFO"),
    attach_stdout=config.get("LOG_STDOUT", False),
)

def solr_query_one(token="*", url=None):
    try:
        resp = utils.return_query(url, method="get")
        new_token = resp.get("nextCursorMark", None)
    except Exception as err:
        raise SolrQueryException("Failed Solr query: %s" % err)
    else:
        documents = resp.get("response", {}).get("docs", [])
        return (new_token, documents)


def solr_query():
    host = conf.get("_INDEXER_HOST", "localhost")
    port = conf.get("_INDEXER_PORT", "9983")
    coll = conf.get("_INDEXER_COLLECTION", "collection1")
    token = "*"
    last_token = ""
    nmax = conf.get("_INDEXER_MAXROWS", 5000)
    ntries = 0

    url_string = conf.get("SOLR_QUERY_ALL", None)
    results = []
    if url_string:
        while token != last_token and ntries < 10:
            url = url_string % (host, port, coll, token, nmax)
            try:
                (new_token, documents) = solr_query_one(token, url)
            except Exception as err:
                logger.warning("Error, query result %s: %s" % (ntries, err))
                ntries += 1
                if ntries == 10:
                    raise SolrRetriesException("Too many Solr API query retries, aborting")
                time.sleep(5)
            else:
                results.extend(documents)
                ntries = 0
                last_token = token
                token = new_token
        return results
    else:
        raise MissingSolrURLException("The solr query URL is missing")


def parse_solr_json_record(rec):
    affilsOutputList = []
    try:
        bibc = rec['bibcode']
        affList = rec['aff']
    except Exception as err:
        raise ParseJSONException('Malformed JSON record: %s' % err)
    else:
        try:
            affIDList = rec['aff_id']
        except:
            affIDList = '-'
        # printing both affs and IDs
        for affIDStr, affStr in zip(affIDList, affList):
            if args.clean:
                affStr = utils.clean_string(affStr)
            try:
                aff = affStr.split(';')
            except Exception as notastring:
                print('Problem: %s' % notastring)
            else:
                affID = affIDStr.split(';')
                if len(affID) != len(aff):
                    # data problem: write original strings to badfile
                    if args.baddata:
                        affilsOutputList.append(AffPairRecord(False,affIDStr,affStr,bibc))
                else:
                    for aid,a in zip(affID,aff):
                        affilsOutputList.append(AffPairRecord(True,aid,a,bibc))
    return affilsOutputList

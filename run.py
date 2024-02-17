import argparse
import json
import os

from adsputils import load_config, setup_logging

from adsaffildb import tasks, utils
from adsaffildb.models import AffilCuration as affil_curation
from adsaffildb.models import AffilData as affil_data
from adsaffildb.models import AffilInst as affil_inst
from adsaffildb.models import AffilNorm as affil_norm

proj_home = os.path.realpath(os.path.dirname(__file__))
config = load_config(proj_home=proj_home)
logger = setup_logging(
    "run.py",
    proj_home=proj_home,
    level=config.get("LOGGING_LEVEL", "INFO"),
    attach_stdout=config.get("LOG_STDOUT", False),
)


def get_args():
    parser = argparse.ArgumentParser("Manage affiliation data for augment_pipeline")

    parser.add_argument(
        "-lp",
        "--load_parentchild",
        dest="load_pc",
        action="store_true",
        default=False,
        help="Load parent-child information from file into db",
    )

    parser.add_argument(
        "-lm",
        "--load_matched",
        dest="load_matched",
        action="store_true",
        default=False,
        help="Load matched affiliation strings from file into db",
    )

    parser.add_argument(
        "-f",
        "--filename",
        dest="filename",
        action="store",
        default=None,
        help="Filename to load, if different from what is in config",
    )

    parser.add_argument(
        "-n",
        "--normalize",
        dest="normalize",
        action="store_true",
        default=None,
        help="Normalize affiliations in data table",
    )

    parser.add_argument('-H',
        '--harvest-affils',
        dest='harvest',
        action='store_true',
        default=False,
        help='harvest affils from solr')


    args = parser.parse_args()
    return args


def load_parent_child(filename):
    try:
        affIdMap = utils.read_affid_dict(filename)
    except Exception as err:
        logger.error("Failed to read parent_child dictionary: %s" % err)
    else:
        tasks.task_bulk_insert_data(affil_inst, affIdMap)
    return


def load_matched_affils(filename):
    try:
        affilDataMap = utils.read_match_dict(filename)
    except Exception as err:
        logger.error("Failed to read parent_child dictionary: %s" % err)
    else:
        tasks.task_bulk_insert_data(affil_data, affilDataMap)
    return


def get_current_solr_affils():
    host = conf.get("_INDEXER_HOST", "localhost")
    port = conf.get("_INDEXER_PORT", "9983")
    coll = conf.get("_INDEXER_COLLECTION", "collection1")
    token = "*"
    last_token = ""
    nmax = conf.get("_INDEXER_MAXROWS", 5000)
    ntries = 0
    maxtries = conf.get("_INDEXER_MAXTRIES", 10)

    url_string = conf.get("SOLR_QUERY_ALL", None)
    if url_string:
        while token != last_token and ntries < maxtries:
            url = url_string % (host, port, coll, token, nmax)
            try:
                (new_token, documents) = utils.solr_query_one(token, url)
            except Exception as err:
                logger.warning("Error, query result %s: %s" % (ntries, err))
                ntries += 1
                if ntries == maxtries:
                    raise SolrRetriesException("Too many Solr API query retries, aborting")
                time.sleep(5)
            else:
                tasks.task_load_solr.delay(documents)
                ntries = 0
                last_token = token
                token = new_token
    else:
        raise MissingSolrURLException("The solr query URL is missing")


def main():
    args = get_args()

    if args.load_pc:
        if args.filename:
            file_parent_child = args.filename
        else:
            file_parent_child = config.get("PARENT_CHILD_FILE", None)
        if not file_parent_child:
            logger.error("No parent_child data file name specified.")
        else:
            load_parent_child(file_parent_child)

    if args.load_matched:
        if args.filename:
            file_matched = args.filename
        else:
            file_matched = config.get("MATCHED_AFFILS_FILE", None)
        if not file_matched:
            logger.error("No matched affiliation file name specified.")
        else:
            load_matched_affils(file_matched)

    if args.normalize:
        tasks.task_normalize_affils()

    if args.harvest:
        get_current_solr_affils()

    return


if __name__ == "__main__":
    main()

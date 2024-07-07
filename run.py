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

    args = parser.parse_args()
    return args

def write_to_database(table_def, data):
    try:
        blocksize = conf.get("CLASSIC_DATA_BLOCKSIZE", 10000)
        total_rows = len(data)
        if data and table_def:
            i = 0
            while i < total_rows:
                logger.debug(
                    "Writing to db: %s of %s rows remaining" % (len(data) - i, total_rows)
                )
                insertblock = data[i : (i + blocksize)]
                tasks.task_write_block(table_def, insertblock)
                i += blocksize
    except Exception as err:
        raise DBWriteException(err)

def load_parent_child(filename):
    try:
        affIds = utils.read_affid_dict(filename)
        write_to_database(affil_inst, affIds)
    except Exception as err:
        logger.error("Failed to load parent_child dictionary into db: %s" % err)
    return


def load_matched_affils(filename):
    try:
        affilMatches = utils.read_match_dict(filename)
        write_to_database(affil_data, affilMatches)
    except Exception as err:
        logger.error("Failed to read parent_child dictionary: %s" % err)
    return


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

    return


if __name__ == "__main__":
    main()

import os
import argparse
from adsaffildb import tasks, utils
from adsputils import setup_logging, load_config

proj_home = os.path.realpath(os.path.dirname(__file__))
config = load_config(proj_home=proj_home)
logger = setup_logging('run.py', proj_home=proj_home,
                        level=config.get('LOGGING_LEVEL', 'INFO'),
                        attach_stdout=config.get('LOG_STDOUT', False))



def get_args():
    parser = argparse.ArgumentParser('Manage affiliation data for augment_pipeline')

    parser.add_argument('-lp',
                        '--load_parentchild',
                        dest='load_pc',
                        action='store_true',
                        default=False,
                        help='Load parent-child information from file into db')

    parser.add_argument('-lm',
                        '--load_matched',
                        dest='load_matched',
                        action='store_true',
                        default=False,
                        help='Load matched affiliation strings from file into db')

    parser.add_argument('-f',
                        '--filename',
                        dest='filename',
                        action='store',
                        default=None,
                        help='Filename to load, if different from what is in config')

    args = parser.parse_args()
    return args


def load_parent_child(filename):
    try:
        affIdDict = utils.read_affid_dict(filename)
    except Exception as err:
        logger.error("Failed to read parent_child dictionary: %s" % err)
    else:
        tasks.task_load_parent_child_relations(affIdDict)
    return

def load_matched_affils(filename):
    try:
        affilData = utils.read_affid_dict(filename)
    except Exception as err:
        logger.error("Failed to read parent_child dictionary: %s" % err)
    else:
        tasks.task_load_matched_affils(affilData)
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


    return


if __name__ == '__main__':
    main()



import os
import argparse
from adsaffildb import utils
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

    args = parser.parse_args()
    return args


def main():
    args = get_args()

    if args.load_pc:
        file_parent_child = config.get("PARENT_CHILD_FILE", None)
        if not file_parent_child:
            logger.error("The location of the parent_child data file is missing, must be defined in config.PARENT_CHILD_FILE")
        else:
            affIdDict = utils.read_affid_dict(file_parent_child)
    print("Parent ID list has %s items" % len(affIdDict.items()))


if __name__ == '__main__':
    main()



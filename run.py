import argparse
import os
from affildb import utils, normalize, tasks
from adsputils import load_config, setup_logging

from affildb.models import AffilInst as affil_inst
from affildb.models import AffilData as affil_data
from affildb.models import AffilNorm as affil_norm

proj_home = os.path.realpath(os.path.join(os.path.dirname(__file__), "./"))
config = load_config(proj_home=proj_home)

logger = setup_logging("affildb", level=config.get("LOGGING_LEVEL", "WARN"), proj_home=proj_home, attach_stdout=config.get("LOG_STDOUT", "FALSE"))

def get_args():

    parser = argparse.ArgumentParser("Affiliations curation and management")

    parser.add_argument("-lp",
                        "--load-pc",
                        dest="load_pc",
                        action="store_true",
                        default=False,
                        help="Load parent_child relations from .tsv file.")

    parser.add_argument("-la",
                        "--load-affs",
                        dest="load_affs",
                        action="store_true",
                        default=False,
                        help="Load matched affiliation strings from .tsv file.")

    parser.add_argument("-n",
                        "--norm",
                        dest="normalize",
                        action="store_true",
                        default=False,
                        help="Generate normalized version of affil_data")

    parser.add_argument("-ns",
                        "--normstring",
                        dest="normstring",
                        action="store",
                        default=None,
                        help="normalize this string")


    parser.add_argument("-s",
                        "--sanity",
                        dest="sanity",
                        action="store_true",
                        default=False,
                        help="Look for normalized strings pointing to multiple affids.")

    return parser.parse_args()

def main():

    args = get_args()

    if args.load_pc: 
        infile = config.get("COUNTRY_PARENT_CHILD_FILE", "./data/cpc.tsv")
        with_header = True
        delimiter = "\t"
        dataParentChild = utils.read_flat_files(infile,
                                                with_header,
                                                delimiter)
        uniqueParentChild = utils.merge_parents(dataParentChild)
        tasks.task_write_to_database(affil_inst, uniqueParentChild)
        

    if args.load_affs:
        infile = config.get("EXISTING_ID_FILE", "./data/Affils.tsv")
        with_header = False
        delimiter = "\t"
        dataMatchedAffils = utils.read_flat_files(infile,
                                                  with_header,
                                                  delimiter)
        foo = dataMatchedAffils[0:10]
        print(foo, type(foo))
        quit()
        tasks.task_write_to_database(affil_data, dataMatchedAffils)

    if args.normalize:
        tasks.task_normalize_all()

    if args.sanity:
        if dataMatchedAffils:
            sanityDict = {}
            discrepant = []
            for x in dataMatchedAffils:
                affid = x[0]
                affstring = x[1]
                affdict = {"affid": affid, "affstring": affstring}
                affnorm = normalize.normalize_string(affstring, kill_spaces=True, upper_case=True)
                if sanityDict.get(affnorm, None):
                    for s in sanityDict.get(affnorm):
                        sdaffid = s.get("affid", None)
                        sdaffstring = s.get("affstring", None)
                        if affid != sdaffid:
                            discrepant.append((x, (sdaffid, sdaffstring)))
                    sanityDict.get(affnorm, []).append(affdict)
                else:
                    sanityDict[affnorm] = [affdict]
            for d in discrepant:
                print(d)


if __name__ == '__main__':
    main()

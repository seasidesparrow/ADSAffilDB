import os

from adsputils import load_config, setup_logging
from sqlalchemy import func

from adscompstat.models import CompStatAltIdents as alt_identifiers
from adscompstat.models import CompStatIdentDoi as identifier_doi
from adscompstat.models import CompStatIssnBibstem as issn_bibstem
from adscompstat.models import CompStatMaster as master
from adscompstat.models import CompStatSummary as summary

proj_home = os.path.realpath(os.path.join(os.path.dirname(__file__), "../"))
config = load_config(proj_home=proj_home)
logger = setup_logging(
    __name__,
    proj_home=proj_home,
    level=config.get("LOGGING_LEVEL", "INFO"),
    attach_stdout=config.get("LOG_STDOUT", False),
)


class DBClearTableException(Exception):
    pass


class DBWriteException(Exception):
    pass


class DBQueryException(Exception):
    pass

# general use functions, 
def clear_table(app, tabledef):
    with app.session_scope() as session:
        try:
            session.query(tabledef).delete()
            session.commit()
        except Exception as err:
            session.rollback()
            session.flush()
            raise DBClearTableException("Failed to clear table %s: %s" % (str(tabledef), err))

def write_block_to_table(app, table, datablock):
    with app.session_scope() as session:
        try:
            session.execute(insert(table),datablock)
            session.commit()
        except Exception as err:
            session.rollback()
            session.flush()
            raise DBWriteException("Failed to bulk write data block: %s" % err)

#--------leftover from ADSCompStat

def query_master_by_doi(app, doi):
    with app.session_scope() as session:
        try:
            return session.query(master.master_doi).filter_by(master_doi=doi).all()
        except Exception as err:
            raise DBQueryException("Unable to query master by DOI %s: %s" % (doi, err))


def query_bibstem_by_issn(app, issn):
    with app.session_scope() as session:
        try:
            return session.query(issn_bibstem.bibstem).filter(issn_bibstem.issn == issn).first()
        except Exception as err:
            raise DBQueryException("Unable to get bibstem from issn %s: %s" % (issn, err))


def query_completeness_per_bibstem(app, bibstem):
    with app.session_scope() as session:
        try:
            result = (
                session.query(
                    func.substr(master.bibcode_meta, 10, 5),
                    master.status,
                    master.matchtype,
                    func.count(master.bibcode_meta),
                )
                .filter(func.substr(master.bibcode_meta, 5, 5) == bibstem)
                .group_by(func.substr(master.bibcode_meta, 10, 5), master.status, master.matchtype)
                .all()
            )
            return result
        except Exception as err:
            raise DBQueryException(
                "Error querying completeness for bibstem %s: %s" % (bibstem, err)
            )


def query_classic_bibcodes(app, doi, bibcode):
    with app.session_scope() as session:
        bibcodesFromDoi = []
        bibcodesFromBib = []
        try:
            if doi:
                bibcodesFromDoi = (
                    session.query(
                        alt_identifiers.identifier,
                        alt_identifiers.canonical_id,
                        alt_identifiers.idtype,
                    )
                    .join(
                        identifier_doi, alt_identifiers.canonical_id == identifier_doi.identifier
                    )
                    .filter(identifier_doi.doi == doi)
                    .all()
                )
            if bibcode:
                bibcodesFromBib = (
                    session.query(
                        alt_identifiers.identifier,
                        alt_identifiers.canonical_id,
                        alt_identifiers.idtype,
                    )
                    .filter(alt_identifiers.identifier == bibcode)
                    .all()
                )
            return bibcodesFromDoi, bibcodesFromBib
        except Exception as err:
            raise DBQueryException(err)


def query_retry_files(app, rec_type):
    with app.session_scope() as session:
        try:
            return (
                session.query(master.harvest_filepath).filter(master.matchtype == rec_type).all()
            )
        except Exception as err:
            raise DBQueryException(
                "Unable to retrieve retry files of type %s: %s" % (rec_type, err)
            )


def query_bibstem(app, record):
    try:
        issn_list = record.get("publication", {}).get("ISSN", [])
        bibstem = ""
        print("LOL BUTTS", issn_list)
        for issn in issn_list:
            if not bibstem:
                issnString = str(issn.get("issnString", ""))
                if issnString:
                    if len(issnString) == 8:
                        issnString = issnString[0:4] + "-" + issnString[4:]
                    try:
                        bibstem_result = query_bibstem_by_issn(app, issnString)
                        if bibstem_result:
                            bibstem = bibstem_result[0]
                    except Exception as err:
                        logger.warning("Error from database call: %s" % err)
    except Exception as err:
        raise BibstemLookupException(err)
    else:
        return bibstem


def query_master_bibstems(app):
    with app.session_scope() as session:
        try:
            return session.query(func.substr(master.bibcode_meta, 5, 5)).distinct().all()
        except Exception as err:
            raise DBQueryException("Failed to get unique bibstems from master: %s" % err)


def query_summary_bibstems(app):
    with app.session_scope() as session:
        try:
            bibstems = session.query(summary.bibstem).distinct().all()
            bibstems = [x[0] for x in bibstems]
            return bibstems
        except Exception as err:
            raise DBQueryException("Failed to get bibstems from summary: %s" % err)


def query_summary_single_bibstem(app, bibstem):
    with app.session_scope() as session:
        try:
            result = (
                session.query(
                    summary.bibstem,
                    summary.volume,
                    summary.complete_fraction,
                    summary.paper_count,
                )
                .filter(summary.bibstem == bibstem)
                .all()
            )
            return result
        except Exception as err:
            raise DBQueryException(
                "Failed to get completeness for bibstem %s: %s" % (bibstem, err)
            )


def update_master_by_doi(app, update):
    with app.session_scope() as session:
        try:
            doi = update.get("master_doi", None)
            session.query(master).filter_by(master_doi=doi).update(update)
            session.commit()
        except Exception as err:
            session.rollback()
            session.flush()
            raise DBWriteException(
                "Error writing record to master: %s; row data: %s" % (err, update)
            )


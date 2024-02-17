import json
import math
import os

from kombu import Queue

from adsaffildb import app as app_module
from adsaffildb import normalize, utils
from adsaffildb import database as db
from adsaffildb.models import AffilData as affil_data
from adsaffildb.models import AffilNorm as affil_norm
from adsaffildb.models import AffilCuration as affil_curate

proj_home = os.path.realpath(os.path.join(os.path.dirname(__file__), "../"))
app = app_module.ADSAffilDBCelery(
    "affildb-pipeline",
    proj_home=proj_home,
    config=globals().get("config", {}),
    local_config=globals().get("local_config", {}),
)
logger = app.logger

app.conf.CELERY_QUEUES = (
    Queue("normalize", app.exchange, routing_key="normalize"),
    Queue("curate", app.exchange, routing_key="curate"),
)


def task_bulk_insert_data(app, table, data):
    with app.session_scope() as session:
        try:
            session.bulk_insert_mappings(table, data)
            session.commit()
        except Exception as err:
            session.rollback()
            session.flush()
            logger.warning("Failed to bulk insert data: %s" % err)


def task_bulk_update_data(app, table, data):
    with app.session_scope() as session:
        try:
            session.bulk_update_mappings(table, data)
            session.commit()
        except Exception as err:
            session.rollback()
            session.flush()
            logger.warning("Failed to bulk update data: %s" % err)


def task_normalize_affils(app):
    with app.session_scope() as session:
        try:
            results = session.query(affil_data.data_id, affil_data.data_pubstring).all()
            norm_results = normalize.normalize_batch(results)
        except Exception as err:
            logger.warning("Failed to normalize data: %s" % err)
        else:
            try:
                session.query(affil_norm).delete()
                session.commit()
                logger.info("AffilNorm table cleared.")
            except Exception as err:
                session.rollback()
                session.flush()
                logger.error("Failed to clear AffilNorm table: %s" % err)
            else:
                task_bulk_insert_data(affil_norm, norm_results)

def task_load_solr_batch(records):
    data_block = []
    for r in records:
        data_block.extend(utils.parse_one_solr_record(r))
    try:
        db.bulk_insert_data(app, affil_curate, data_block)
    except Exception as err:
        logger.error("Failed to insert data from Solr: %s" % err)

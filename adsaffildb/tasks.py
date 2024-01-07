import json
import math
import os

from kombu import Queue
from sqlalchemy import func

from adsaffildb import app as app_module
from adsaffildb import utils
from adsaffildb import normalize

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
)


def task_bulk_insert_data(table, data):
    with app.session_scope() as session:
        try:
            session.bulk_insert_mappings(table, data)
            session.commit()
        except Exception as err:
            session.rollback()
            session.flush()
            logger.warning("Failed to write data from file: %s" % err)


@app.task(queue="normalize")
def task_normalize_affils():
    with app.session_scope() as session:
        try:
            x = 1
        except Exception as err:
            logger.warning("Normalize exception: %s" % err)

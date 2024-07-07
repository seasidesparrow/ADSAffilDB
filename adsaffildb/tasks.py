import json
import math
import os

from kombu import Queue
from sqlalchemy import func

from adsaffildb import app as app_module
from adsaffildb import normalize, utils
from adsaffildb.models import AffilData as affil_data
from adsaffildb.models import AffilNorm as affil_norm

proj_home = os.path.realpath(os.path.join(os.path.dirname(__file__), "../"))
app = app_module.ADSAffilDBCelery(
    __name__,
    proj_home=proj_home,
    config=globals().get("config", {}),
    local_config=globals().get("local_config", {}),
)
logger = app.logger

app.conf.CELERY_QUEUES = (
    Queue("write", app.exchange, routing_key="write"),
    Queue("normalize", app.exchange, routing_key="normalize"),
    Queue("query", app.exchange, routing_key="query"),
)

@app.task(queue="write")
def task_write_block(table, datablock):
    try:
        db.write_block(app, table, datablock)
    except Exception as err:
        logger.warning("Unable to write block to db: %s" % err)


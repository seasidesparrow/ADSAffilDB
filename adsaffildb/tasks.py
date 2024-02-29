import json
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



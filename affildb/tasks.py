import json
import math
import os

from kombu import Queue
from sqlalchemy import func

from affildb import app as app_module
from affildb import normalize, utils
from affildb.models import AffilData as affil_data
from affildb.models import AffilNorm as affil_norm
from affildb.models import AffilCuration as affil_curation

import affildb.database as db

name_to_table = {"AffilData": affil_data,
                 "AffilNorm": affil_norm, 
                 "AffilCuration": affil_curation}

proj_home = os.path.realpath(os.path.join(os.path.dirname(__file__), "../"))
app = app_module.ADSAffilDBCelery(
    "affildb-pipeline",
    proj_home=proj_home,
    config=globals().get("config", {}),
    local_config=globals().get("local_config", {}),
)
logger = app.logger

app.conf.CELERY_QUEUES = (
    Queue("augment", app.exchange, routing_key="augment"),
    Queue("normalize", app.exchange, routing_key="normalize"),
    Queue("write-db", app.exchange, routing_key="write-db"),
)

# pipeline query tasks
@app.task(queue="augment")
def task_query_one_affil(input_string, normalize=True):
    try:
        query_string = None
        table = None
        if input_string:
            if normalize:
                query_string = normalize.normalize_string(
                    input_string,
                    kill_spaces = app.conf.get("NORM_KILL_SPACES", False),
                    upper_case = app.conf.get("NORM_UPPER_CASE", False)
                )
                table_name = app.conf.get("NORMALIZED_DATA_TABLE", None)
            else:
                query_string = input_string
                table_name = app.conf.get("RAW_DATA_TABLE", None)
            if table_name:
                table = name_to_table.get(table_name, None)
        if query_string and table:
            return db.query_one_string(app, table, query_string)
        else:
            return
    except Exception as err:
        logger.error("Query failed for '%s': %s" % (str(input_string),err))
        return


# data management tasks
@app.task(queue="write-db")
def task_write_block(table, datablock):
    try:
        db.write_block_to_table(app, table, datablock)
    except Exception as err:
        logger.warning("Unable to write block to db: %s" % err)


def task_write_to_database(table_def, data):
    try:
        blocksize = app.conf.get("BLOCKSIZE", 2000)
        total_rows = len(data)
        if data and table_def:
            i = 0
            while i < total_rows:
                logger.debug(
                    "Writing to db: %s of %s rows remaining" % (len(data) - i, total_rows)
                )
                datablock = data[i : (i + blocksize)]
                insertblock = [table_def.toRow(x) for x in datablock]
                task_write_block(table_def, insertblock)
                i += blocksize
    except Exception as err:
        logger.error("Failed to write data to %s: %s" % (table_def, err))


@app.task(queue="normalize")
def task_normalize_block(data):
    try:
        norm_data = []
        for row in data:
            affil_id = row.affil_id
            affil_string = row.affil_string
            normstring = normalize.normalize_string(affstring)
            nd = [affil_id, normstring]
            norm_data.append(nd)
        if norm_data:
            task_write_block(affil_curation, norm_data)
        else:
            logger.warning("Normalize.normalize_block returned no data!")
    except Exception as err:
        logger.error("Normalize block failed! %s" % err)


def task_normalize_all():
    try:
        db.clear_table(app, affil_curation)
    except Exception as err:
        logger.error("Failed to clear affil_norm table: %s" % err)
    else:
        logger.debug("Affil_norm table has been cleared.")
        try:
            result = db.fetch_full_table(app, affil_data)
            logger.debug("Affil_data table has been fetched.")
            if result:
                blocksize = app.conf.get("BLOCKSIZE", 2000)
                total_rows = len(result)
                i = 0
                while i < total_rows:
                    logger.debug(
                        "Writing to db: %s of %s rows remaining" % 
                            (len(result) - i, total_rows)
                    )
                    processblock = result[i : (i + blocksize)]
                    for p in processblock:
                        print(p.affil_id)
                    task_normalize_block(processblock)
                    i += blocksize
        except Exception as err:
            logger.error("Failed to normalize affil_data table: %s" % err)
        else:
            logger.info("affil_data has been normalized in affil_norm")

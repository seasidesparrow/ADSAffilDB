# Specify where the affiliations database lives
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://user:password@localhost:5432/affildb"
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

CELERY_INCLUDE = ["adsaffildb.tasks"]
CELERY_BROKER = "pyamqp://user:password@localhost:6672/affildb"

PARENT_CHILD_FILE = "./data/country_parent_child.tsv"
MATCHED_AFFILS_FILE = "./data/affil_strings.txt"

# format string requires (_INDEXER_HOST, _INDEXER_PORT, collection_name, cursor_token)
SOLR_QUERY_ALL = "http://%s:%s/solr/%s/select?fl=bibcode,aff_id,aff&cursorMark=%s&q=*%3A*&rows=5000&sort=bibcode%20asc%2Cid%20asc&wt=json"

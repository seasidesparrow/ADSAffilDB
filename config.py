# Specify where the affiliations database lives
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://user:pwd@localhost:5432/affildb"
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

CELERY_INCLUDE = ['adsaffildb.tasks']
CELERY_BROKER = 'pyamqp://user:password@localhost:6672/affildb'

PARENT_CHILD_FILE = "./data/country_parent_child.tsv"
MATCHED_AFFILS_FILE = "./data/matched_affils.tsv"

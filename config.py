# Specify where the affiliations database lives
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg://user:pwd@localhost:5432/affildb"
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

PARENT_CHILD_FILE = "./data/country_parent_child.tsv"

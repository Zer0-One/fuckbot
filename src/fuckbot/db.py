#from sqlalchemy import create_engine
#
#from .config import Config
#
#config = Config()
#
#def db_init():
#    engine = create_engine("sqlite+pysqlite:///" + config["WORKING_DIR"] + "/" + config["SQLITE_DB"], future=True)
#
#    with engine.connect() as con:
#        res = con.execute(text("CREATE TABLE trigger"))
##    engine.connect()

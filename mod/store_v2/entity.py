from datetime import datetime
from sqlalchemy import MetaData, Table, Integer, SmallInteger, String, Column, DateTime

# solution 1
metadata = MetaData()
store_table = Table('tdar_store', metadata,
                    Column('id', Integer(), primary_key=True),
                    Column('name', String(100), nullable=False),
                    Column('address', String(100), nullable=False),
                    Column('ctime', DateTime(), default=datetime.now),
                    Column('mtime', DateTime(), default=datetime.now, onupdate=datetime.now),
                    Column('priority', Integer, default=100),
                    Column('comment', String(50)),
                    Column('is_active', SmallInteger, default=1),
                    Column('is_del', SmallInteger, default=0)
                    )


"""
# solution 2
store_table = Table('tdar_store', metadata, autoload_with=engine)
"""

"""
# solution 3: pass engine into MetaData, and let metadata get table information from the database
metadata = MetaData(engine)
db.MetaData.reflect(meta_data)
store_table = metadata.tables['tdar_store']
"""

"""
# make a mapping of Store class to a table
from sqlalchemy.orm import mapper
class Store(object):
    pass

mapper(Store, store_table)
"""
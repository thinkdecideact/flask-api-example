from sqlalchemy import create_engine
from sqlalchemy import select
from datetime import datetime
from sqlalchemy.sql.expression import desc
import redis
import MySQLdb as mdb


def get_db_engine(config):
    return create_engine(
        'mysql+mysqldb://%s:%s@%s:%s/%s' % (config['db_user'], config['db_pwd'], config['db_host'], config['db_port'], config['db_name']),
        connect_args={'charset': 'utf8'},
        encoding='utf-8',
        echo=True,
        future=True,
        pool_recycle=120
    )


def get_db_conn(config):
    return mdb.connect(
        host=config['db_host'],
        port=int(config['db_port']),
        database=config['db_name'],
        user=config['db_user'],
        password=config['db_pwd'],
        charset=config['db_charset'],
        autocommit=False
    )


def get_cache_conn(config):
    pool = redis.ConnectionPool(
        host=config['host'],
        port=int(config['port']),
        password=config['password'],
        db=config['db']
    )
    return redis.Redis(connection_pool=pool)


def get_many_by_page(conn, _table, **kwargs):
    kwargs['offset'] = kwargs['page_index'] * kwargs['row_count_per_page']
    stmt = select([_table]).where(kwargs['where']).order_by(desc(_table.c.id)).limit(kwargs['row_count_per_page']).offset(kwargs['offset'])
    result = conn.execute(stmt)
    return [dict(row) for row in result.all()]


def get_one(conn, _table, where):
    stmt = _table.select().where(where).limit(1)
    result = conn.execute(stmt)
    row = result.first()
    if row:
        return dict(row)
    return None


def get_one_by_pk(conn, _table, pk):
    return get_one(conn, _table, _table.c.id == pk)


def insert(conn, _table, **kwargs):
    result = conn.execute(_table.insert().values(kwargs))
    # return result.rowcount
    return result.inserted_primary_key


def update(conn, _table, pk, **kwargs):
    update_stmt = _table.update().where(_table.c.id == pk).values(kwargs)
    result = conn.execute(update_stmt)
    return result.rowcount


def raw_update(conn, update_stmt):
    result_proxy = conn.execute(update_stmt)
    return result_proxy.rowcount


def soft_delete(conn, _table, id):
    update_stmt = _table.update().values(
        is_del=1,
        mtime=datetime.now()
    ).where(_table.c.id == id)
    result = conn.execute(update_stmt)
    return result.rowcount


def delete(conn, _table, pk):
    delete_stmt = _table.delete().where(_table.c.id == pk)
    result = conn.execute(delete_stmt)
    return result.rowcount

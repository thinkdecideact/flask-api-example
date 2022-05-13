from sqlalchemy.sql.expression import desc
import sqlalchemy as sa


def get_count(conn, **kwargs):
    count_stmt = sa.select([sa.func.count('*')]).select_from(kwargs['entity']).where(kwargs['where'])
    count_result = conn.execute(count_stmt)
    # scalar() is used to the first column of the first row
    return count_result.scalar()


def get_many(conn, **kwargs):
    # Either select(kwargs['fields']) or select(*kwargs['fields']) can be used
    limit_stmt = sa.select(kwargs['fields']).where(kwargs['where']).order_by(desc(kwargs['entity'].mtime), desc(kwargs['entity'].id)).limit(kwargs['row_count_per_page']).offset(kwargs['offset'])
    limit_result = conn.execute(limit_stmt)
    return [dict(item) for item in limit_result]


def get_one(conn, **kwargs):
    stmt = sa.select(kwargs['fields']).where(kwargs['where'])
    result = conn.execute(stmt)
    row = result.first()
    if not row:
        raise Exception('Fail to find data.')
    return dict(row)


def insert(conn, **kwargs):
    insert_stmt = sa.insert(kwargs['entity']).values(kwargs['data'])
    result = conn.execute(insert_stmt)
    return result.rowcount, result.lastrowid


def soft_delete(conn, **kwargs):
    pass


def update(conn, **kwargs):
    update_stmt = sa.update(kwargs['entity']).where(kwargs['where']).values(kwargs['data'])
    update_result = conn.execute(update_stmt)
    return update_result.rowcount



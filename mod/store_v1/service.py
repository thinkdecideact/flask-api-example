from sqlalchemy import text
from datetime import datetime


def get_count(conn, **kwargs):
    count_result = conn.execute(
        text("SELECT COUNT(*) as row_count FROM tdar_store WHERE is_active=1 AND is_del=0")
    )
    # scalar() is used to get the first column of the first row
    row_count = count_result.scalar()
    # row_count = count_result.first()[0]
    # row_count = count_result.one()[0]
    # row_count = count_result.mappings().all()[0].row_count
    return row_count


def get_many(conn, **kwargs):
    limit_result = conn.execute(
        text(
            "SELECT * FROM tdar_store WHERE is_active=1 AND is_del=0 ORDER BY mtime DESC, id DESC LIMIT :offset,:row_count_per_page"),
        {'offset': kwargs['offset'], 'row_count_per_page': kwargs['row_count_per_page']}
    )
    # rows = list_result.mappings().all()
    return [dict(row) for row in limit_result]


def get_one(conn, **kwargs):
    result = conn.execute(
        text("SELECT * FROM tdar_store WHERE id=:pk AND is_active=:is_active AND is_del=:is_del"),
        {'pk': kwargs['pk'], 'is_active': kwargs['is_active'], 'is_del': kwargs['is_del']}
    )
    row = result.first()
    if not row:
        raise Exception('No record found')
    return dict(row)


def insert(conn, **kwargs):
    result = conn.execute(
        text("INSERT INTO tdar_store (name, address, ctime, mtime) VALUES (:name, :address, :ctime, :mtime)"),
        {'name': kwargs['name'], 'address': kwargs['address'], 'ctime': datetime.now(), 'mtime': datetime.now()}
    )
    return result.rowcount, result.lastrowid


def soft_delete(conn, **kwargs):
    delete_result = conn.execute(
        text("UPDATE tdar_store SET is_del=1, mtime=:mtime WHERE id=:pk AND is_del=0"),
        {'pk': kwargs['pk'], 'mtime': datetime.now()}
    )
    return delete_result.rowcount


def update(conn, **kwargs):
    update_result = conn.execute(
        text("UPDATE tdar_store SET name=:name, address=:address, mtime=:mtime WHERE id=:pk AND is_active=1 AND is_del=0"),
        {
            'pk': kwargs['pk'],
            'name': kwargs['name'],
            'address': kwargs['address'],
            'mtime': datetime.now()
        }
    )
    return update_result.rowcount



from flask import Blueprint
from flask import request
from flask_cors import cross_origin
from common.db_config import db_config_prod
from common.db_util import get_db_engine
from common.utils import api_success, api_failure, get_page_count
import mod.store_v1.service as store_service

store_bp = Blueprint('store_bp_v1', __name__)


engine = get_db_engine(db_config_prod)


@store_bp.route('/getList', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def get_list():
    """
    Get a list of records
    curl -X GET http://127.0.0.1:8080/api/v1/store/getList?pageIndex=0
    """
    # The first page starts at 0, not 1
    page_index = int(request.args.get('pageIndex', 0))
    row_count_per_page = int(request.args.get('rowCountPerPage', 2))
    offset = page_index * row_count_per_page

    with engine.connect() as conn:
        rows = store_service.get_many(conn, row_count_per_page=row_count_per_page, offset=offset)
        row_count = store_service.get_count(conn)
        page_count = get_page_count(row_count, row_count_per_page)

    output = {
        'page_index': page_index,
        'page_count': page_count,
        'row_count': row_count,
        'row_count_per_page': row_count_per_page,
        'offset': offset,
        'rows': rows,
    }
    return api_success(d=output)


@store_bp.route('/getDetail', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def get_detail():
    """
    Get one record
    curl -X GET 'http://127.0.0.1:8080/api/v1/store/getDetail?id=50'
    """
    try:
        pk = request.args.get('id', None)
        if not id:
            raise Exception('Invalid id')

        with engine.connect() as conn:
            row = store_service.get_one(conn, pk=pk, is_del=0, is_active=1)
        return api_success(d=row)
    except Exception as e:
        return api_failure(m=e.args[0])


@store_bp.route('/create', methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def create():
    """
    Create a record
    curl -X POST 'http://127.0.0.1:8080/api/v1/store/create' -F 'name=Panyu' -F 'address=Canton'
    curl -X POST 'http://127.0.0.1:8080/api/v1/store/create' -d 'name=Panyu&address=Canton'
    """
    try:
        name = request.form.get('name', '').strip()
        address = request.form.get('address', '').strip()
        if not name or not address:
            raise Exception('Invalid parameters')

        with engine.connect() as conn:
            rowcount, lastrowid = store_service.insert(conn, name=name, address=address)
            conn.commit()

        if lastrowid > 0:
            return api_success(m='Created successfully', d={'rowcount': rowcount, 'lastrowid': lastrowid})
        raise Exception('Failed to create a record')
    except Exception as e:
        return api_failure(m=e.args[0])


@store_bp.route('/update', methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def update():
    """
    Update fields of a record
    curl -X POST 'http://127.0.0.1:8080/api/v1/store/update' -d 'id=71&name=万顷沙&address=广州市南沙区'
    """
    try:
        pk = request.form.get('id', None)
        if not pk:
            raise Exception('Invalid id')
        name = request.form.get('name', '').strip()
        address = request.form.get('address', '').strip()
        if not name or not address:
            raise Exception('Invalid parameters')

        with engine.connect() as conn:
            store_service.get_one(conn, pk=pk, is_del=0, is_active=1)
            rowcount = store_service.update(conn, pk=pk, name=name, address=address)
            conn.commit()

        if rowcount > 0:
            return api_success(m='Updated successfully', d={'rowcount': rowcount})
        raise Exception('Failed to update')
    except Exception as e:
        return api_failure(m=e.args[0])


@store_bp.route('/delete', methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def delete():
    """
    Soft-delete a record
    curl -X POST 'http://127.0.0.1:8080/api/v1/store/delete' -d 'id=34'
    """
    try:
        pk = request.form.get('id', None)
        if not pk:
            raise Exception('Invalid id')

        with engine.connect() as conn:
            store_service.get_one(conn, pk=pk, is_del=0, is_active=1)
            rowcount = store_service.soft_delete(conn, pk=pk)
            conn.commit()

        if rowcount > 0:
            return api_success(m='Deleted successfully', d={'rowcount': rowcount})
        raise Exception('Failed to delete')
    except Exception as e:
        return api_failure(m=e.args[0])

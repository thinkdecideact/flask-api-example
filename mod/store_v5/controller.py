from flask import Blueprint
from flask import request
from flask_cors import cross_origin
from common.utils import api_success, api_failure, get_page_count
from common.db_config import db_config_prod
from common.db_util import get_db_conn
import mod.store_v5.service as store_service

store_bp = Blueprint('store_bp_v5', __name__)


@store_bp.route('/getList', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def get_list():
    """
    Get a list of records
    curl -X GET http://127.0.0.1:8080/api/v5/store/getList?pageIndex=0
    """
    # The first page starts at 0, not 1
    page_index = int(request.args.get('pageIndex', 0))
    row_count_per_page = int(request.args.get('rowCountPerPage', 2))
    offset = page_index * row_count_per_page

    conn = get_db_conn(db_config_prod)
    with conn:
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
    curl -X GET 'http://127.0.0.1:8080/api/v5/store/getDetail?id=83'
    """
    try:
        pk = request.args.get('id', None)
        if not pk:
            raise Exception('Invalid id')

        conn = get_db_conn(db_config_prod)
        with conn:
            row = store_service.get_one(conn, pk=pk)
        return api_success(d=row)
    except Exception as e:
        return api_failure(m=e.args[0])


@store_bp.route('/create', methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def create():
    """
    Create a record
    curl -X POST 'http://127.0.0.1:8080/api/v5/store/create' -F 'name=Panyu' -F 'address=Canton'
    curl -X POST 'http://127.0.0.1:8080/api/v5/store/create' -d 'name=Panyu&address=Canton'
    """
    try:
        name = request.form.get('name', '').strip()
        address = request.form.get('address', '').strip()
        if not name or not address:
            raise Exception('Invalid parameters')
        create_dict = {
            'name': name,
            'address': address,
        }

        conn = get_db_conn(db_config_prod)
        with conn:
            rowcount, lastrowid = store_service.insert(conn, **create_dict)
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
    curl -X POST 'http://127.0.0.1:8080/api/v5/store/update' -d 'id=71&name=abc&address=123'
    """
    try:
        pk = request.form.get('id', None)
        if not id:
            raise Exception('Invalid id')
        name = request.form.get('name', '').strip()
        address = request.form.get('address', '').strip()
        if not name or not address:
            raise Exception('Invalid parameters')

        conn = get_db_conn(db_config_prod)
        with conn:
            store_service.get_one(conn, pk=pk)
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
    curl -X POST 'http://127.0.0.1:8080/api/v5/store/delete' -d 'id=71'
    """
    try:
        pk = request.form.get('id', None)
        if not id:
            raise Exception('Invalid id')

        conn = get_db_conn(db_config_prod)
        with conn:
            store_service.get_one(conn, pk=pk)
            rowcount = store_service.soft_delete(conn, pk=pk)
            conn.commit()

        if rowcount > 0:
            return api_success(m='Deleted successfully', d={'rowcount': rowcount})
        raise Exception('Failed to delete')
    except Exception as e:
        return api_failure(m=e.args[0])

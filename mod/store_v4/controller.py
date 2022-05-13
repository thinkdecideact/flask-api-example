from flask import Blueprint
from flask import request
from flask_cors import cross_origin
from sqlalchemy.sql.expression import desc
from sqlalchemy.orm import sessionmaker
from common.db_config import db_config_prod
from common.db_util import get_db_engine
from common.utils import api_success, api_failure, get_page_count
from .entity import Store


store_bp = Blueprint('store_bp_v4', __name__)


engine = get_db_engine(db_config_prod)
DBSession = sessionmaker(bind=engine)
selected_fields = [Store.id, Store.name, Store.address, Store.ctime, Store.mtime]


@store_bp.route('/getList', methods=['GET'])
@cross_origin(origins='*', supports_credentials=True)
def _get_list():
    """
    Get a list of records
    curl -X GET http://127.0.0.1:8080/api/v4/store/getList?pageIndex=0
    """
    # The first page starts at 0, not 1
    page_index = int(request.args.get('pageIndex', 0))
    row_count_per_page = int(request.args.get('rowCountPerPage', 2))
    offset = page_index * row_count_per_page

    session = DBSession()

    # select..limit and select count share the following where
    where = (Store.is_del == 0) & (Store.is_active == 1)

    # Either select(selected_fields) or select(*selected_fields) can be used
    limit_result = session.query(*selected_fields).filter(where).order_by(desc(Store.mtime)).limit(row_count_per_page).offset(offset).all()
    rows = [dict(row) for row in limit_result]

    # Get row count
    row_count = session.query(Store).filter(where).count()

    # Get page count
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
def _get_detail():
    """
    Get one record
    curl -X GET 'http://127.0.0.1:8080/api/v4/store/getDetail?id=30'
    """
    try:
        pk = request.args.get('id', None)
        if not pk:
            raise Exception('Invalid id')

        session = DBSession()
        row = session.query(*selected_fields).filter(
            (Store.id == pk) &
            (Store.is_del == 0) &
            (Store.is_active == 1)
        ).first()
        if not row:
            raise Exception('Fail to find data.')
        row = dict(row)
        return api_success(d=row)
    except Exception as e:
        return api_failure(m=e.args[0])


@store_bp.route('/create', methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def _create():
    """
    Create a record
    curl -X POST 'http://127.0.0.1:8080/api/v4/store/create' -F 'name=Panyu' -F 'address=Canton'
    curl -X POST 'http://127.0.0.1:8080/api/v4/store/create' -d 'name=Panyu&address=Canton'
    """
    try:
        name = request.form.get('name', '').strip()
        address = request.form.get('address', '').strip()
        if not name or not address:
            raise Exception('Invalid parameters')

        with DBSession() as session:
            store_obj = Store(**{'name': name, 'address': address})
            session.add(store_obj)
            session.commit()
        return api_success(m='Created successfully')
    except Exception as e:
        return api_failure(m=e.args[0])


@store_bp.route('/update', methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def _update():
    """
    Update fields of a record
    curl -X POST 'http://127.0.0.1:8080/api/v4/store/update' -d 'id=82&name=123&address=abc'
    """
    try:
        pk = request.form.get('id', None)
        if not pk:
            raise Exception('Invalid id')
        name = request.form.get('name', '').strip()
        address = request.form.get('address', '').strip()
        if not name or not address:
            raise Exception('Invalid parameters')

        with DBSession() as session:
            store_obj = session.query(Store).get(pk)
            if not store_obj or store_obj.is_del == 1 or store_obj.is_active == 0:
                raise Exception('Fail to find data.')
            store_obj.name = name
            store_obj.address = address
            session.add(store_obj)
            session.commit()

        return api_success(m='Updated successfully')
    except Exception as e:
        return api_failure(m=e.args[0])


@store_bp.route('/delete', methods=['POST'])
@cross_origin(origins='*', supports_credentials=True)
def _delete():
    """
    Soft-delete a record
    curl -X POST 'http://127.0.0.1:8080/api/v4/store/delete' -d 'id=82'
    """
    try:
        pk = request.form.get('id', None)
        if not pk:
            raise Exception('Invalid id')

        with DBSession() as session:
            store_obj = session.query(Store).get(pk)
            if not store_obj or store_obj.is_del == 1:
                raise Exception('Fail to find data.')
            store_obj.is_del = 1
            session.add(store_obj)
            session.commit()
        return api_success(m='Deleted successfully')
    except Exception as e:
        return api_failure(m=e.args[0])

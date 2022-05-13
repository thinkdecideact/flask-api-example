import math
from flask import jsonify


def api_success(m='Successful operation', d='', c=0):
    return jsonify({'code': c, 'msg': m, 'data': d})


def api_failure(m='Errors occurred', d='', c=1):
    return jsonify({'code': c, 'msg': m, 'data': d})


def get_page_count(row_count, row_count_per_page):
    """
    calc how many pages there are
    """
    if (row_count % row_count_per_page) == 0:
        return int(row_count / row_count_per_page)
    else:
        return int(math.ceil(row_count / row_count_per_page))


def obj_to_dict(obj, fields):
    """
    convert an object to a dict
    Example:
        obj = Store()
        fields = ['id', 'name', 'address', 'ctime', 'mtime']
    """
    return {field: getattr(obj, field) for field in fields}

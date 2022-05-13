from flask.json import JSONEncoder
from datetime import datetime
from decimal import Decimal


class TdarCustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(obj, Decimal):
                return "%.2f" % obj
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


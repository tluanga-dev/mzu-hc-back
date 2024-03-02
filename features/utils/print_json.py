import json
import uuid
from json import JSONEncoder

class UUIDEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            # if the object is uuid, we simply return the value of uuid
            return str(obj)
        return super().default(obj)

def print_json_string(data):
    print(json.dumps(data, indent=4, cls=UUIDEncoder))
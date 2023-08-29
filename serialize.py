from __future__ import annotations
import dataclasses, json

from trail import Trail, TrailSplit, TrailSeries
from mountain import Mountain

# https://stackoverflow.com/questions/51286748/make-the-python-json-encoder-support-pythons-new-dataclasses
class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            res = dataclasses.asdict(o)
            self.remove_box(res)
            return res
        return super().default(o)

    def remove_box(self, obj):
        if isinstance(obj, dict):
            rm_keys = list(filter(lambda x: x.endswith("_box"), obj.keys()))
            for key in rm_keys:
                del obj[key]
            for key in obj.keys():
                self.remove_box(obj[key])
        if isinstance(obj, list):
            for o in obj:
                self.remove_box(o)

def serialize(trail):
    return json.dumps(trail, cls=EnhancedJSONEncoder)

def deserialize(obj):
    if obj["store"] is None:
        return Trail(None)
    if "mountain" in obj["store"]:
        inside = TrailSeries(
            Mountain(**obj["store"]["mountain"]),
            deserialize(obj["store"]["following"])
        )
    else:
        inside = TrailSplit(
            deserialize(obj["store"]["top"]),
            deserialize(obj["store"]["bottom"]),
            deserialize(obj["store"]["following"])
        )
    return Trail(inside)

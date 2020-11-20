import json

class Trace():
    '''class representing the trace object'''
    def __init__(self, raw_trace, interval_len):
        self.sprites = set(map(lambda x:x["sprite"]["name"], raw_trace))
        self.t2 = {x:
                        [y for y in raw_trace 
                        if y["sprite"]["name"] == x]
                    for x in self.sprites}
        self.traces = {x:
                        Trace.merge_to_interval([y for y in raw_trace 
                        if y["sprite"]["name"] == x], interval_len)
                    for x in self.sprites}
        

    @classmethod
    def from_json(cls, fp, interval_len):
        return cls(json.load(fp), interval_len)

    @staticmethod
    def merge_to_interval(trace, interval_len):
        merged_trace = []
        new_interval = True
        i = 0
        while True:
            # print(i)
            time_now = trace[i]["clockTime"]
            if new_interval:
                time_begin = trace[i]["clockTime"]
                new_interval = False
                touching = []
                keysDown = []
                continue
            touching = list(set(touching + trace[i]["sprite"]["touching"]))
            keysDown = list(set(keysDown + trace[i]["keysDown"]))
            if (time_now - time_begin >= interval_len) or (i+1 >= len(trace)):
                # print(time_now)
                # print(time_begin)
                interval_object = trace[i]
                interval_object["sprite"]["touch"] = touching
                interval_object["keysDown"] = keysDown
                merged_trace.append(interval_object)
                new_interval = True
            i = i + 1
            if i >= len(trace):
                break
        return merged_trace

class Event():
    '''class representing an event'''
    def __init__(self, id, attr=[]):
        self.id = id
        self.attr = attr

class Attr():
    '''class representing an attribute of an event'''
    def __init__(self, id, value=None):
        self.id = id
        self.value = value
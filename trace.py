import json
import pandas as pd

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
    def block_simplify(block):
        if "opcode" not in block:
            return block
        opcode = block['opcode']
        simple_field = ""
        if block['fields']:
            field = block['fields']
            field_key = list(field.keys())[0]
            value = field[field_key]['value']
            simple_field = "(" + field_key + ":" + str(value) + ")"
        if not block['inputs']:
            return opcode + simple_field
        else:
            sub_blocks = ""
            for input_block in block['inputs']:
                simple_sub_block = Trace.block_simplify(input_block)
                sub_blocks += simple_sub_block
            simple_block = opcode + simple_field + "{" + sub_blocks + "}"
            return simple_block

    @staticmethod
    def variable_simplify(variable, stage_var_dict):
        simple_variables = {}
        for v in variable.keys():
            if v not in stage_var_dict:
                stage_var_dict[v] = variable[v]['name']
            simple_variables[stage_var_dict[v]] = variable[v]['value']
        return simple_variables

    @staticmethod
    def merge_to_interval(trace, interval_len):
        # merged_trace = []
        merged_trace_df = pd.DataFrame(columns = ['clockTime', 'sprite', 'x', 'y', 'direction', 'touching', 'block', 'keysDown', 'variables', 'stageVariables'])
        new_interval = True
        stage_var_dict = {}
        for i, d in enumerate(trace):
            time_now = trace[i]["clockTime"]
            if new_interval:
                time_begin = trace[i]["clockTime"]
                new_interval = False
                touching = []
                keysDown = []
                continue
            touching = list(set(touching + trace[i]["sprite"]["touching"]))
            keysDown = list(set(keysDown + trace[i]["keysDown"]))
            direction = trace[i]["sprite"]["direction"]
            if (time_now - time_begin >= interval_len) or (i+1 >= len(trace)):
                # print('time_now：', time_now)
                # print('time_begin: ', time_begin)
                new_row = {
                    "clockTime": d['clockTime'],
                    'sprite': d['sprite']['name'],
                    'x': d["sprite"]['x'],
                    'y': d["sprite"]['y'],
                    'direction': d['sprite']['direction'],
                    'touching': touching,
                    'block': Trace.block_simplify(d['block']),
                    'keysDown': keysDown,
                    'variables': Trace.variable_simplify(d['sprite']['variables'], stage_var_dict),
                    'stageVariables': Trace.variable_simplify(d['stageVariables'], stage_var_dict)
                }
                merged_trace_df.loc[len(merged_trace_df)] = new_row
                new_interval = True
        merged_trace_df.to_csv("data/interval_trace.csv")
        return merged_trace_df

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
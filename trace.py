import json
import pandas as pd
from event import PredicateSequence
import os
from event import *
import pprint as pp

class Trace():
    '''class representing the trace object'''
    def get_predicate(self, interval_len = 0.25):
        for variation in ['1111', '1110', '1101', '1100', '1011', '1010', '1000', '0111', '0011', '0010']:
            for i in range(1,11):
                interval_len = 0.025
                try:
                    f = open(f"data/pong/json/{variation}/{variation}-{i}.json")
                except:
                    continue
                raw_trace = json.load(f)
                self.sprites = set(map(lambda x:x["sprite"]["name"], raw_trace))
                self.traces = {x:
                                Trace.merge_to_interval([y for y in raw_trace
                                if y["sprite"]["name"] == x], interval_len)
                            for x in self.sprites}
                dir = f"data/pong/trace/{variation}/{variation}-{i}/"
                if not os.path.exists(dir):
                    os.makedirs(dir)
                for sprite_name in self.traces:
                    # self.traces[sprite_name].to_csv(f"{dir}/interval_trace_{sprite_name}.csv")
                    all_seqs = self.mine_predicate_seq([is_moving, is_turning, is_touching])
                    print(all_seqs)
                    break
                break
            break



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
        sprite_name = trace[0]["sprite"]["name"]
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


        return merged_trace_df

    def mine_predicate_seq(self, predicates):
        all_seqs = {}
        for sprite in self.sprites:
            seq = []
            trace = self.traces[sprite]
            t_len = len(trace.index)
            for i in range(t_len):
                ps = set()
                for p in predicates:
                    if (p_res := p(trace[i:(min(i+2, t_len))])) is not None:
                        ps.add(p_res)
                seq.append(ps)
            all_seqs[sprite] = PredicateSequence(seq)
        return all_seqs



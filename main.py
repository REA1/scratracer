from trace import *
import pprint as pp

f = open("data/outputx.json")

interval_len = 0.025

t = Trace.from_json(f, 0.025)

# for item in t.traces["Stage"]:
#     pp.pprint(item)
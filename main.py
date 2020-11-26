from trace import *
from event import *
import pprint as pp

f = open("data/outputx.json")

interval_len = 0.025

t = Trace.from_json(f, interval_len)

res = t.mine_predicate_seq([is_moving, is_turning], 20)
pp.pprint(res["Bananas"].seq)
#for x in list(res["Bananas"].seq[0]):
#    print(x)
# for item in t.traces["Stage"]:
#     pp.pprint(item)
def is_moving(window):
    speed = get_speed(window)
    direction = get_direction(window)
    if True:
        return Predicate("Move", [speed, direction])
    else:
        return None

def is_turning(window):
    degree = get_degree(window)
    if True:
        return Predicate("Turn", [degree])
    else:
        return None

def get_direction(window):
    return Attr("Dir", 0)

def get_speed(window):
    return Attr("Speed", 0)

def get_degree(window):
    return Attr("Deg", 0)

class PredicateSequence():
    '''class representing sequences of predicates'''
    def __init__(self, seq=[]):
        self.seq = seq
    def __repr__(self):
        return str(self.seq)

class Predicate():
    '''class representing a predicate'''
    def __init__(self, id, attr=[]):
        self.id = id
        self.attr = attr
    
    def get_attr(self, id_str):
        return next(filter(lambda x: x.id == id_str, self.attr), None)

    def __repr__(self):
        return str(self.id) + " - [" + ", ".join(map(str, self.attr)) + "]"

class Attr():
    '''class representing an attribute part of a predicate'''
    def __init__(self, id, value=None):
        self.id = id
        self.value = value

    def __repr__(self):
        return str(self.id) + ":" + str(self.value)
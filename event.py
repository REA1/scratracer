def is_moving(window):
    # speed = get_speed(window)
    index_list = []
    for i in window.index:
        index_list.append(i)
    if len(index_list) < 2:
        return None

    i, j  = index_list[0], index_list[1]
    if window.at[i, 'x'] ==  window.at[j, 'x'] and window.at[i, 'y'] ==  window.at[j, 'y']:
        return None
    elif window.at[i, 'x'] !=  window.at[j, 'x'] and window.at[i, 'y'] !=  window.at[j, 'y']:
        return Predicate('Move')
    else:
        dir = None
        if window.at[i, 'x'] < window.at[j, 'x']:
            dir = "left"
        elif window.at[i, 'x'] > window.at[j, 'x']:
            dir = "right"
        direction = get_direction(dir)
        return Predicate("Move", [direction])


def is_turning(window):

    index_list = []
    for i in window.index:
        index_list.append(i)
    if len(index_list) < 2:
        return None

    i, j  = index_list[0], index_list[1]
    if window.at[i, 'direction'] ==  window.at[j, 'direction']:
        return None
    else:
        return Predicate("Turn")



def is_touching(window):

    index_list = []
    for i in window.index:
        index_list.append(i)
    if len(index_list) < 2:
        return None

    i, j  = index_list[0], index_list[1]
    if window.at[j, 'touching']:
        return Predicate("Touching", [get_touching_what(window.at[j, 'touching'][0])])
    else:
        return None


def get_direction(dir):
    return Attr("Dir")


def get_speed(window):
    return Attr("Speed", 0)

def get_degree(window):
    return Attr("Deg", 0)


def get_touching_what(name):
    return Attr("Item", name)

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
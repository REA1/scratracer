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
    elif (window.at[i, 'x'] !=  window.at[j, 'x'] and window.at[i, 'y'] !=  window.at[j, 'y']) or window.at[j, 'sprite'] == 'Ball':
        return Predicate('Move')
    else:
        mydir = ""
        if window.at[i, 'x'] < window.at[j, 'x']:
            mydir = "Right"
        elif window.at[i, 'x'] > window.at[j, 'x']:
            mydir = "Left"
        if mydir != "":
            direction = get_direction(mydir)
            return Predicate("Move", [direction])
        else:
            return Predicate("Move")


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

def is_keys_down(window):
    index_list = []
    for i in window.index:
        index_list.append(i)
    if len(index_list) < 2:
        return None
    i, j  = index_list[0], index_list[1]
    if window.at[j, 'keysDown'] and window.at[j, 'sprite'] == 'Paddle':
        keys_down = window.at[j, 'keysDown']
        return Predicate("KeysDown", [Attr("Keys", keys_down)])
    else:
        return None

def is_touching(window):

    index_list = []
    for i in window.index:
        index_list.append(i)
    if len(index_list) < 2:
        return None
    touching_what = []
    i, j  = index_list[0], index_list[1]
    if window.at[j, 'x'] > 210:
        touching_what.append('Edge')
        # touching_what.append('Right Edge')
    elif window.at[j, 'x'] < -210:
        # touching_what.append('Left Edge')
        touching_what.append('Edge')

    elif window.at[j, 'y'] > 170:
        # touching_what.append('Upper Edge')
        touching_what.append('Edge')
    elif window.at[j, 'y'] < -170:
        touching_what.append('Edge')
        # touching_what.append('Lower Edge')

    if window.at[j, 'touching']:
        touching_what.append(window.at[j, 'touching'][0])
    if touching_what:
        return Predicate("Touching", [Attr("Item", touching_what)])
    else:
        return None


def get_direction(dir):
    return Attr("Dir", dir)


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
        if self.attr != [] and self.attr is not None:
            return str(self.id) + " - [" + ", ".join(map(str, self.attr)) + "]"
        else:
            return str(self.id)

class Attr():
    '''class representing an attribute part of a predicate'''
    def __init__(self, id, value=None):
        self.id = id
        self.value = value

    def __repr__(self):
        return str(self.id) + ":" + str(self.value)
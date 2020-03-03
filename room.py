from ast import literal_eval

class Room:
    def __init__(self, x, y, desc=None):
        self.x = x
        self.y = y

        prop_check = lambda n, v=None: v if n not in desc else desc[n]

        self.room_id = prop_check("room_id")
        self.title = prop_check("title")
        self.description = prop_check("description")
        self.elevation = prop_check("elevation")
        self.terrain = prop_check("terrain")
        self.items = prop_check("items", [])
        self.messages = prop_check("messages", [])

        self.dirs = prop_check("dirs", [])
        self.n = None
        self.s = None
        self.e = None
        self.w = None

    def __repr__(self):
        result = {
            "room_id": self.room_id,
            "title": self.title,
            "description": self.description,
            "coordinates": self.get_coords(),
            "dirs": self.dirs,
            "exits": self.get_exits(),
            "elevation": self.elevation,
            "terrain": self.terrain,
            "items": self.items,
            "messages": self.messages
        }
        return str(result)
    def get_props(self):
        return literal_eval(str(self))
    def get_coords(self):
        return (self.x, self.y)
    def get_exits(self):
        dirs = ['n', 's', 'e', 'w']
        exits = {d: getattr(self, d).get_coords() for d in dirs if getattr(self, d) is not None}
        return exits
    def get_exits_string(self):
        return f"Exits: [{', '.join(self.get_exits().keys())}]"
    def exit_coords(self, direction):
        dirs_math = {
            'n': (0, 1),
            's': (0, -1),
            'e': (1, 0),
            'w': (-1, 0)
        }
        exit_x = dirs_math[direction][0]
        exit_y = dirs_math[direction][1]
        return (self.x + exit_x, self.y + exit_y)
    def get_direction(self, direction):
        return getattr(self, direction)
    def connect_rooms(self, direction, connecting_room):
        opp_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        if direction in opp_dirs:
            setattr(self, direction, connecting_room)
            setattr(connecting_room, opp_dirs[direction], self)
        else:
            print("INVALID ROOM CONNECTION")
            return None

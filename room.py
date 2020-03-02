class Room:
    def __init__(self, x=None, y=None, desc=None):
        self.x = x
        self.y = y
        self.room_id = None if "room_id" not in desc else desc["room_id"]
        self.title = None if "title" not in desc else desc["title"]
        self.description = None if "description" not in desc else desc["description"]
        self.elevation = None if "elevation" not in desc else desc["elevation"]
        self.terrain = None if "terrain" not in desc else desc["terrain"]
        self.n = None
        self.s = None
        self.e = None
        self.w = None
    def __repr__(self):
        dirs = ['n', 's', 'e', 'w']
        result = {
            "room_id": self.room_id,
            "title": self.title,
            "description": self.description,
            "coordinates": self.get_coords(),
            "exits": self.get_exits(),
            "elevation": self.elevation,
            "terrain": self.terrain
        }
        return str(result)
    def get_coords(self):
        return (self.x, self.y)
    def get_exits(self):
        dirs = ['n', 's', 'e', 'w']
        exits = {d: getattr(self, d).get_coords() for d in dirs if getattr(self, d) is not None}
        return exits
    def get_exits_string(self):
        return f"Exits: [{', '.join(self.get_exits().keys())}]"
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

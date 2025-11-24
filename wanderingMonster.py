# wanderingMonster.py
import random

# Colors for pygame (R,G,B)
MONSTER_COLORS = {
    "Killer Rabbit of Caerbannog": (200, 0, 0),   # red
    "Insulting Frenchman": (150, 0, 200),        # purple
    "Three-Headed Giant": (0, 200, 0),           # green
    "Slime": (0, 150, 50),
    "Zombie": (80, 200, 80),
}

_MONSTER_TEMPLATES = [
    {
        "name": "Killer Rabbit of Caerbannog",
        "description": "A deceptively cute but deadly rabbit with razor sharp teeth.",
        "health_range": (500, 1000),
        "power_range": (50, 80),
        "money_range": (200, 500),
    },
    {
        "name": "Insulting Frenchman",
        "description": "A castle guard who doesn't take kindly to you. Stay upwind of him!",
        "health_range": (50, 100),
        "power_range": (10, 20),
        "money_range": (100, 150),
    },
    {
        "name": "Three-Headed Giant",
        "description": "A giant with three heads that can't seem to agree with each other.",
        "health_range": (200, 300),
        "power_range": (30, 40),
        "money_range": (50, 100),
    },
]


class WanderingMonster:
    """Represents a single wandering monster on the grid."""

    def __init__(self, x=0, y=0, template=None):
        # choose template if not provided
        if template is None:
            template = random.choice(_MONSTER_TEMPLATES)

        self.x = int(x)
        self.y = int(y)
        self.name = template["name"]
        self.description = template["description"]
        self.health = random.randint(*template["health_range"])
        self.power = random.randint(*template["power_range"])
        self.money = random.randint(*template["money_range"])
        self.alive = True

        # color fallback
        self.color = MONSTER_COLORS.get(self.name, (200, 0, 0))

    def to_dict(self):
        """Return a serializable dict for storing in map_state."""
        return {
            "x": self.x,
            "y": self.y,
            "name": self.name,
            "description": self.description,
            "health": self.health,
            "power": self.power,
            "money": self.money,
            "alive": self.alive,
            "color": self.color,
        }

    @classmethod
    def from_dict(cls, d):
        """Create a WanderingMonster-like object from a dict (used to move/draw)."""
        inst = cls(d.get("x", 0), d.get("y", 0), template={
            "name": d.get("name"),
            "description": d.get("description"),
            "health_range": (d.get("health", 0), d.get("health", 0)),
            "power_range": (d.get("power", 0), d.get("power", 0)),
            "money_range": (d.get("money", 0), d.get("money", 0)),
        })
        # override fields with stored values (so we preserve randomized stats)
        inst.health = d.get("health", inst.health)
        inst.power = d.get("power", inst.power)
        inst.money = d.get("money", inst.money)
        inst.alive = d.get("alive", inst.alive)
        inst.color = tuple(d.get("color", inst.color))
        return inst

    @staticmethod
    def random_at(grid_size, town_pos, avoid_positions=None):
        """Create a random monster at a location that does not clash with town or avoid_positions."""
        if avoid_positions is None:
            avoid_positions = []

        # attempt random placements until valid
        attempts = 0
        while attempts < 200:
            x = random.randint(0, grid_size - 1)
            y = random.randint(0, grid_size - 1)
            if (x, y) == tuple(town_pos):
                attempts += 1
                continue
            if (x, y) in [tuple(p) for p in avoid_positions]:
                attempts += 1
                continue
            # build monster
            m = WanderingMonster(x, y)
            return m
        # fallback: place at bottom-right if nothing else
        return WanderingMonster(grid_size - 1, grid_size - 1)

    def move(self, grid_size, town_pos, player_pos, occupied_positions=None):
        """
        Attempt to move the monster one step in a random direction.
        Restrictions:
            - Stay within grid bounds
            - Do not move into town_pos
            - Optionally avoid occupied_positions (list of tuples)
        """
        if not self.alive:
            return

        if occupied_positions is None:
            occupied_positions = []

        directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx = self.x + dx
            ny = self.y + dy
            # check bounds
            if nx < 0 or ny < 0 or nx >= grid_size or ny >= grid_size:
                continue
            # don't move into town
            if (nx, ny) == tuple(town_pos):
                continue
            # optionally avoid colliding with other monsters when moving
            if (nx, ny) in occupied_positions and (nx, ny) != tuple(player_pos):
                # allow moving onto player_pos (triggers combat)
                continue
            # valid move
            self.x = nx
            self.y = ny
            return

    def as_encounter_dict(self):
        """Return a monster dict compatible with fight_monster() expectations."""
        return {
            "name": self.name,
            "description": self.description,
            "health": self.health,
            "power": self.power,
            "money": self.money,
        }

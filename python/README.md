# Python

Python basics: lists, dictionaries, importing from the standard library, and a small class hierarchy for practising object-oriented programming.

## What's here

| Path         | Covers                                                                              |
| ------------ | ----------------------------------------------------------------------------------- |
| `list.py`    | `pop(index)` vs `del`, `append`, slicing with `zoo[0:3]`                            |
| `dict.py`    | Iterating with `.items()`, `.copy()`, adding a key, `pop(key)` vs `del`             |
| `imports.py` | Importing a standard library module and using `random.choice`                       |
| `oop/`       | Classes, inheritance, encapsulation, composition, and polymorphism (enemies battle) |

### OOP (oop/)

```text
Enemy                    # base class: type, health, damage, weapon
├── Zombie(Enemy)        # special__attack: "bite"
└── Orge(Enemy)          # special__attack: "smash"

Weapon                   # type, damage; held by an Enemy (composition)
```

- **Encapsulation:** attributes are double-underscore "private" (`self.__health`) and read through getters (`get__health()`)
- **Inheritance:** `Zombie` and `Orge` call `super().__init__(...)` with their own type name
- **Overriding:** each subclass provides its own `special__attack(target)`
- **Composition:** an `Enemy` holds a `Weapon` and uses it in `weapon__attack()`
- **Polymorphism:** `arena()` makes every enemy fight every other one through the same `battle()` function, without knowing which subclass it has

`main.py` creates a zombie with a stick and an ogre with a hammer, then runs the arena:

```text
Type: Zombie, Health: 100, Damage: 5
Zombie attacks for 5 damage!
Zombie moves towards Orge!
Zombie attacks with Stick for 2 damage!
Zombie is trying to bite Orge!
Type: Orge, Health: 250, Damage: 15
...
```

## Running

No dependencies beyond the standard library. Last run on Python 3.14.

```bash
cd python
python list.py
python dict.py
python imports.py

python oop/main.py
```

`main.py` imports its siblings by bare name (`from enemy import *`), which works because Python puts the script's own directory on the import path. Importing `oop` as a package from elsewhere would need an `__init__.py` and relative imports.

## Other notes

- **Name mangling:** inside `class Enemy`, `self.__type` is stored as `self._Enemy__type`. That's why `zombie.__type` from outside raises `AttributeError` (the commented-out line in `main.py`). It's also why `move__towards` can read `target.__type`: inside the class body that compiles to `target._Enemy__type`, which every `Enemy` subclass has. Pass in a non-`Enemy` target and it fails.
- The double underscore in the middle of `get__type` or `move__towards` doesn't do anything. Mangling only applies to names that _start_ with `__`. Python convention is `get_type` / `move_towards`, or a `@property` instead of a getter.
- `Enemy.special__attack(self)` takes no `target`, but both subclasses define `special__attack(self, target)`, and `battle()` calls it with a target. A plain `Enemy` in the arena would raise `TypeError`. Giving the base method the same signature and `raise NotImplementedError` (or making `Enemy` an `abc.ABC` with an `@abstractmethod`) keeps them in line.
- `enemys: Enemy = [zombie, orge]` annotates a list as a single `Enemy`. It should be `list[Enemy]`. Python doesn't enforce annotations, so it runs anyway; a type checker would flag it.
- The parameter named `type` in both `__init__` methods shadows the built-in `type()` inside them.
- `from x import *` everywhere makes it hard to tell where a name came from. `from enemy import Enemy` is clearer.
- "Orge" is spelled that way throughout (file, class, output); the usual spelling is "Ogre".
- `dict.py` has make and model swapped: Ford is the make, Explorer the model.
- `pop()` returns the removed item, `del` doesn't. Neither file uses the return value, so both work the same here.

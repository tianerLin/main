from functools import partial
from typing import List

from primitives.effects import EventListener
from primitives.effects.RequirementsCheck import RequirementCheck


class ModifierEffect:
    # requirement function is: Callable[[Hero, Hero, Context], int]
    def __init__(self, requirement: partial[int] or None, modifier: dict):
        if requirement is None:
            requirement = lambda x, y, z: 1
        self.modifier = modifier
        self.requirement = requirement

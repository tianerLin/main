from __future__ import annotations
from typing import TYPE_CHECKING

from primitives.RequirementCheck.BuffRequirementChecks import BuffRequirementChecks
from primitives.RequirementCheck.CheckHelpers import _is_attacker
from primitives.RequirementCheck.LifeRequirementChecks import LifeRequirementChecks
from primitives.RequirementCheck.PositionRequirementChecks import PositionRequirementChecks

if TYPE_CHECKING:
    from primitives.Context import Context
    from primitives.hero.Hero import Hero
from primitives.hero.Element import get_elemental_relationship, ElementRelationships


class RequirementCheck:
    # TODO  should not include any function related to level2 modifier
    @staticmethod
    def battle_with_certain_hero(hero_temp_id: str, actor_hero: Hero, target_hero: Hero, context: Context) -> int:
        action = context.get_last_action()
        if action.is_in_battle:
            if target_hero.temp.id == hero_temp_id or actor_hero.temp.id == hero_temp_id:
                return 1
        return 0

    @staticmethod
    def move_less_or_equal_than(max_move: int, actor_hero: Hero, target_hero: Hero, context: Context):
        action = context.get_last_action()
        if actor_hero == action.actor:
            if action.moves <= max_move:
                return True
        return False

    @staticmethod
    def all_skills_in_cooldown(actor_hero: Hero, target_hero: Hero, context: Context) -> int:
        for skill in actor_hero.enabled_skills:
            if skill.current_cooldown > 0:
                return 0
        return 1

    @staticmethod
    def in_battle_with_non_flyable(actor_hero: Hero, target_hero: Hero, context: Context) -> int:
        action = context.get_last_action()
        if action.is_in_battle:
            if target_hero.temp.flyable:
                return 0
            else:
                return 1
        return 0

    @staticmethod
    def always_true() -> int:
        return 1

    @staticmethod
    def battle_with_no_element_advantage(actor_hero: Hero, target_hero: Hero, context: Context) -> int:
        action = context.get_last_action()
        if action.is_in_battle:
            actor_element = actor_hero.temp.element
            target_element = target_hero.temp.element
            if get_elemental_relationship(actor_element, target_element) == ElementRelationships.NEUTRAL:
                return 1
            else:
                return 0
        return 0

    @staticmethod
    def is_attacker(actor_hero: Hero, target_hero: Hero, context: Context) -> int:
        return _is_attacker(actor_hero, context)

    LifeChecks: LifeRequirementChecks
    PositionChecks: PositionRequirementChecks
    BuffChecks: BuffRequirementChecks

from random import random

from primitives.Action import Action
from primitives.hero.Element import get_elemental_multiplier
from calculation.attribute_calculator import *
from primitives import Context
from primitives.hero import HeroTemp, Hero

CRIT_MULTIPLIER = 1.3
LIEXING_DAMAGE_REDUCTION = 4
LIEXING_DAMAGE_INCREASE = 4


def apply_damage(action: Action, context: Context):
    targets = action.targets
    for target in targets:
        calculate_damage(action.actor, target, action, context)


def apply_counterattack_damage(counter_attacker: Hero, attacker: Hero, action: Action, context: Context):
    calculate_damage(counter_attacker, attacker, action, context)


def calculate_damage(attacker_instance: Hero, target_instance: Hero, action: Action, context):
    hero_id = attacker_instance.id
    is_attacker = action.is_attacker(hero_id)
    skill = action.skill
    is_magic = skill.is_magic
    attacker_elemental_multiplier = get_elemental_multiplier(attacker_instance.temp.element, target_instance.temp.element, is_attacker) + get_element_multiplier(is_attacker, context)
    defender_elemental_multiplier = get_elemental_multiplier(attacker_instance.temp.element, target_instance.temp.element,
                                                             not is_attacker) + get_element_multiplier(not is_attacker, context)

    # Calculating attack-defense difference
    attack_defense_difference = (
            get_attack(action, is_attacker, context) * attacker_elemental_multiplier
            - get_defense_with_penetration(attacker_instance, target_instance, is_magic,
                                           context) * defender_elemental_multiplier)

    # Calculating base damage
    actual_damage = (attack_defense_difference
                     * skill.damage_multiplier
                     * get_damage_modifier(attacker_instance, is_attacker, is_magic, context, skill)
                     * get_damage_reduction_modifier(target_instance, not is_attacker, is_magic, context))

    critical_probability = (get_critical_hit_probability(attacker_instance, is_attacker, context)
                            - get_critical_hit_resistance(target_instance, not is_attacker, context))

    critical_damage_multiplier = (CRIT_MULTIPLIER
                                  * get_critical_damage_modifier(attacker_instance, is_attacker, context)
                                  * get_critical_damage_reduction_modifier(target_instance, not is_attacker, context))

    if random() < critical_probability:
        # Critical hit occurs
        target_instance.take_harm(actual_damage * critical_damage_multiplier)
    else:
        # No critical hit
        target_instance.take_harm(actual_damage)


def calculate_fix_damage(damage, actor_instance: Hero, target_instance: Hero, context: Context):
    defender_fix_damage_reduction = get_fixed_damage_reduction_modifier(target_instance, actor_instance, context)
    target_instance.take_harm(damage * defender_fix_damage_reduction)


def calculate_magic_damage(damage: float, actor_instance: Hero, defender_instance: Hero, context: Context):
    actual_damage = (damage
                     * get_damage_reduction_modifier(defender_instance, actor_instance, True, context))
    defender_instance.take_harm(actual_damage)


def calculate_physical_damage(damage: float, actor_instance: Hero, defender_instance: Hero, context: Context):
    actual_damage = (damage
                     * get_damage_reduction_modifier(defender_instance, actor_instance, False, context))
    defender_instance.take_harm(actual_damage)

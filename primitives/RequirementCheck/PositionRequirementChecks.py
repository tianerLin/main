from __future__ import annotations
from typing import TYPE_CHECKING

from primitives.RequirementCheck.CheckHelpers import check_buff_in_range, _is_attacker

if TYPE_CHECKING:
    from primitives.Context import Context
    from primitives.hero.Hero import Hero
    from primitives.hero.Element import Elements
    from primitives.buff.Buff import Buff
from typing import List
from calculation.Range import calculate_if_targe_in_diamond_range
from primitives.buff.BuffTemp import BuffTypes


class PositionRequirementChecks:
    @staticmethod
    def in_range_of_enemy_caster(range_value: int, actor_hero: Hero, target_hero: Hero, context: Context,
                                 buff: Buff) -> int:
        caster_hero_id = buff.caster_id
        caster = context.get_hero_by_id(caster_hero_id)
        if caster.player_id != actor_hero.player_id:
            actor_position = actor_hero.position
            caster_position = caster.position
            if calculate_if_targe_in_diamond_range(actor_position, caster_position, range_value):
                return 1
        return 0

    @staticmethod
    def no_partners_in_range(range_value: int, actor_hero: Hero, target_hero: Hero, context: Context) -> int:
        actor_position = actor_hero.position
        for hero in context.heroes:
            if hero.id == actor_hero.id:
                continue
            if hero.player_id == actor_hero.player_id:
                if calculate_if_targe_in_diamond_range(actor_position, hero.position, range_value):
                    return 0
        return 1

    @staticmethod
    def no_partners_in_target_range(range_value: int, actor_hero: Hero, target_hero: Hero, context: Context) -> int:
        actor_position = target_hero.position
        for hero in context.heroes:
            if hero.id == actor_hero.id:
                continue
            if hero.player_id == target_hero.player_id:
                if calculate_if_targe_in_diamond_range(actor_position, hero.position, range_value):
                    return 0
        return 1

    @staticmethod
    def in_the_same_line(actor_hero: Hero, target_hero: Hero, context: Context) -> int:
        actor_position = actor_hero.position
        target_position = target_hero.position
        if actor_position[0] == target_position[0] or actor_position[1] == target_position[1]:
            return 1
        else:
            return 0

    @staticmethod
    def element_hero_in_range(elements: List[Elements], range_value: int, actor_hero: Hero, target_hero: Hero,
                              context: Context) -> int:
        actor_position = actor_hero.position
        count = 0
        for element in elements:
            for hero in context.heroes:
                if hero.id == actor_hero.id:
                    continue
                if hero.player_id == actor_hero.player_id:
                    if hero.temp.element == element:
                        if calculate_if_targe_in_diamond_range(actor_position, hero.position, range_value):
                            count += 1
                            break

        return 1 if count == len(elements) else 0

    @staticmethod
    def in_range(range_value: int, actor_hero: Hero, target_hero: Hero, context: Context) -> int:
        actor_position = actor_hero.position
        for hero in context.heroes:
            if hero.id == actor_hero.id:
                continue
            if calculate_if_targe_in_diamond_range(actor_position, hero.position, range_value):
                return 1
        return 0

    @staticmethod
    def has_partner_in_range(range_value, actor_hero: Hero, target_hero: Hero, context: Context) -> int:
        actor_position = actor_hero.position
        for hero in context.heroes:
            if hero.id == actor_hero.id:
                continue
            if hero.player_id == actor_hero.player_id:
                if calculate_if_targe_in_diamond_range(actor_position, hero.position, range_value):
                    return 1
        return 0

    @staticmethod
    def in_range_count_with_limit(range_value, maximum_count: int, actor_hero: Hero, target_hero: Hero,
                                  context: Context) -> int:
        actor_position = actor_hero.position
        count = 0
        for hero in context.heroes:
            if hero.id == actor_hero.id:
                continue
            if calculate_if_targe_in_diamond_range(actor_position, hero.position, range_value):
                count += 1
        return min(count, maximum_count)

    @staticmethod
    def enemy_in_range_count_bigger_than(range_value: int, count_requirement: int, actor_hero: Hero, target_hero: Hero,
                                         context: Context) -> int:
        actor_position = actor_hero.position
        enemy_count = 0
        for hero in context.heroes:
            if hero.id == actor_hero.id:
                continue
            if hero.player_id != actor_hero.player_id:
                if calculate_if_targe_in_diamond_range(actor_position, hero.position, range_value):
                    enemy_count += 1
        return 1 if enemy_count >= count_requirement else 0

    def attack_enemy_in_range_count_bigger_than_with_base_2(self, range_value: int, count_requirement: int,
                                                            actor_hero: Hero, target_hero: Hero,
                                                            context: Context) -> int:
        is_attacker = _is_attacker(actor_hero, context)
        if is_attacker:
            return 2 + self.enemy_in_range_count_bigger_than(range_value, count_requirement, actor_hero, target_hero,
                                                             context)
        else:
            return 2

    @staticmethod
    def has_harm_buff_partner_in_range(range_value: int, actor_hero: Hero, target_hero: Hero, context: Context) -> int:
        return check_buff_in_range(range_value, actor_hero, context, BuffTypes.Harm, True)

    @staticmethod
    def has_harm_buff_enemy_in_range(range_value: int, actor_hero: Hero, target_hero: Hero, context: Context) -> int:
        return check_buff_in_range(range_value, actor_hero, context, BuffTypes.Harm, False)

    @staticmethod
    def has_benefit_buff_partner_in_range(range_value: int, actor_hero: Hero, target_hero: Hero,
                                          context: Context) -> int:
        return check_buff_in_range(range_value, actor_hero, context, BuffTypes.Benefit, True)

    @staticmethod
    def has_benefit_buff_enemy_in_range(range_value: int, actor_hero: Hero, target_hero: Hero, context: Context) -> int:
        return check_buff_in_range(range_value, actor_hero, context, BuffTypes.Benefit, False)

    @staticmethod
    def life_not_full_in_range(range_value: int, actor_hero: Hero, target_hero: Hero, context: Context) -> int:
        actor_position = actor_hero.position
        for hero in context.heroes:
            if calculate_if_targe_in_diamond_range(actor_position, hero.position, range_value):
                if hero.current_life < hero.max_life:
                    return 1
        return 0

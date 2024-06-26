import os
import json
import pprint
import random

from app.classes.paladin import Paladin
from app.classes.target import Target, EnemyTarget
from app.classes.spells_auras import TyrsDeliveranceHeal
from app.classes.auras_buffs import DivinePurpose, BlessingOfDawn
from app.classes.spells_healing import DivineResonanceHolyShock, RisingSunlightHolyShock, DivineTollHolyShock

pp = pprint.PrettyPrinter(width=200)

def load_data_from_file(filename):
    with open(filename, "r") as file:
        return json.load(file)

path_to_character_data = os.path.join(os.path.dirname(__file__), "character_data", "character_data.json")
path_to_stats_data = os.path.join(os.path.dirname(__file__), "character_data", "stats_data.json")

path_to_talent_data = os.path.join(os.path.dirname(__file__), "character_data", "talent_data.json")
path_to_base_class_talents_data = os.path.join(os.path.dirname(__file__), "character_data", "base_class_talents")
path_to_base_spec_talents_data = os.path.join(os.path.dirname(__file__), "character_data", "base_spec_talents")
path_to_base_herald_of_the_sun_talents_data = os.path.join(os.path.dirname(__file__), "character_data", "base_herald_of_the_sun_talents")
path_to_base_lightsmith_talents_data = os.path.join(os.path.dirname(__file__), "character_data", "base_lightsmith_talents")

path_to_equipment_data = os.path.join(os.path.dirname(__file__), "character_data", "equipment_data.json")
path_to_updated_equipment_data = os.path.join(os.path.dirname(__file__), "character_data", "updated_equipment_data")

character_data = load_data_from_file(path_to_character_data)
stats_data = load_data_from_file(path_to_stats_data)

talent_data = load_data_from_file(path_to_talent_data)
base_class_talents_data = load_data_from_file(path_to_base_class_talents_data)
base_spec_talents_data = load_data_from_file(path_to_base_spec_talents_data)
base_herald_of_the_sun_talents_data = load_data_from_file(path_to_base_herald_of_the_sun_talents_data)
base_lightsmith_talents_data = load_data_from_file(path_to_base_lightsmith_talents_data)

equipment_data = load_data_from_file(path_to_equipment_data)
updated_equipment_data = load_data_from_file(path_to_updated_equipment_data)

def initialise_paladin():
    healing_targets = [Target(f"target{i + 1}") for i in range(20)]

    paladin = Paladin("paladin1", character_data, stats_data, talent_data, equipment_data, potential_healing_targets=healing_targets, version="ptr")
    
    return paladin

def apply_pre_buffs(paladin):
    paladin.apply_consumables()
    paladin.apply_item_effects()
    paladin.apply_buffs_on_encounter_start()
    
def set_up_paladin(paladin):
    paladin.update_equipment(updated_equipment_data)
    apply_pre_buffs(paladin)
    
    targets = paladin.potential_healing_targets
    glimmer_targets = [glimmer_target for glimmer_target in paladin.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
    
    paladin.mastery_effectiveness = 1
    paladin.set_bonuses = {"tww_season_1": 0, "tww_season_2": 0, "tww_season_3": 0, "dragonflight_season_1": 0, "dragonflight_season_2": 0, "dragonflight_season_3": 0}
    
    return targets, glimmer_targets

def reset_talents(paladin):
    paladin.update_character(class_talents=base_class_talents_data, spec_talents=base_spec_talents_data, herald_of_the_sun_talents=base_herald_of_the_sun_talents_data, lightsmith_talents=base_lightsmith_talents_data)
    paladin.update_equipment(updated_equipment_data)
    
def update_talents(paladin, class_talents={}, spec_talents={}, herald_of_the_sun_talents={}, lightsmith_talents={}):
    paladin.update_character(class_talents=class_talents, spec_talents=spec_talents, herald_of_the_sun_talents=herald_of_the_sun_talents, lightsmith_talents=lightsmith_talents)
    paladin.update_equipment(updated_equipment_data)

def set_crit_to_max(paladin):
    paladin.flat_crit = 100
    paladin.update_stat("crit", 0)
    

# heals
# 20% buff
def test_holy_shock():
    # no talents, no crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        paladin.crit = -10
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = 21576
        if i == 0:
            print(f"Holy Shock (no talents, no crit)")
            print(f"Expected Holy Shock: {expected_heal_amount}")
            print(f"Observed Holy Shock: {heal_amount}")
        assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Holy Shock (no talents, no crit) unexpected value"
        
def test_holy_shock_mastery_effectiveness():
    # no talents, no crit, no mastery effectiveness
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        paladin.crit = -10
        paladin.mastery_effectiveness = 0
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = 14260 * 1.2
        assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Holy Shock (no talents, no crit, no mastery effectiveness) unexpected value"
    
def test_holy_shock_reclamation():        
    # no talents, no crit, reclamation at 70%
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Reclamation": 1})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        paladin.crit = -10
        paladin.average_raid_health_percentage = 0.7
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = round(21576 * 1.15 / 10) * 10
        
        if i == 0:
            print(f"Holy Shock (no talents, no crit, Reclamation at 70%)")
            print(f"Expected Holy Shock: {expected_heal_amount}")
            print(f"Observed Holy Shock: {heal_amount}")
        
        assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Holy Shock (no talents, no crit, Reclamation at 70%) unexpected value"
    
def test_holy_shock_crit():
    # no talents - crit & infusion of light application
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        set_crit_to_max(paladin)
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = 21576 * 2
        
        if i == 0:
            print(f"Holy Shock (no talents, crit)")
            print(f"Expected Holy Shock: {expected_heal_amount}")
            print(f"Observed Holy Shock: {heal_amount}")
        
        assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Holy Shock (no talents, crit) unexpected value"
        assert "Infusion of Light" in paladin.active_auras
    
def test_holy_shock_awestruck():
    # awestruck - no crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Awestruck": 1})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        paladin.crit = -10
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = round(21576 / 10) * 10
        
        if i == 0:
            print(f"Holy Shock (awestruck, no crit)")
            print(f"Expected Holy Shock: {expected_heal_amount}")
            print(f"Observed Holy Shock: {heal_amount}")
        
        assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Holy Shock (Awestruck, no crit) unexpected value"
    
    # awestruck - crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Awestruck": 1})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        set_crit_to_max(paladin)
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = round((21576 * 2 * 1.1) / 10) * 10
        
        if i == 0:
            print(f"Holy Shock (awestruck, crit)")
            print(f"Expected Holy Shock: {expected_heal_amount}")
            print(f"Observed Holy Shock: {heal_amount}")
        
        assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Holy Shock (Awestruck, crit) unexpected value"
        
def test_holy_shock_tyrs_deliverance():   
    # tyr's deliverance, no crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Tyr's Deliverance": 1})
        
        tyrs_deliverance = TyrsDeliveranceHeal(paladin)
        holy_shock = paladin.abilities["Holy Shock"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, _ = tyrs_deliverance.cast_healing_spell(paladin, target, 0, True)
        paladin.global_cooldown = 0
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = round(21576 * 1.15 / 10) * 10
        
        if i == 0:
            print(f"Holy Shock (tyr's deliverance, no crit)")
            print(f"Expected Holy Shock: {expected_heal_amount}")
            print(f"Observed Holy Shock: {heal_amount}")
        
        assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Holy Shock (Tyr's Deliverance, no crit) unexpected value"
        
def test_holy_shock_tww_season_1_2pc():   
    # tww season 1 2pc, no crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        holy_shock = paladin.abilities["Holy Shock"]
        paladin.set_bonuses["tww_season_1"] = 2
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = round(17980 * 1.1 / 10) * 10
        
        if i == 0:
            print(f"Holy Shock (tww season 1 2pc, no crit)")
            print(f"Expected Holy Shock: {expected_heal_amount}")
            print(f"Observed Holy Shock: {heal_amount}")
        
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Shock (tww season 1 2pc, no crit) unexpected value"
        
def test_holy_shock_crit_chance():
    # no talents
    iterations = 10000
    crits = 0
    
    for i in range(iterations):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        target = [targets[0]]
        _, heal_crit, _, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        if heal_crit:
            crits += 1
            
    holy_shock_bonus_crit = 0.1
            
    expected_crit_rate = paladin.crit / 100 + holy_shock_bonus_crit
    observed_crit_rate = crits / iterations
    
    print(f"Expected crit rate: {expected_crit_rate}")
    print(f"Observed crit rate: {observed_crit_rate}")
    
    tolerance = 0.02
    assert abs(observed_crit_rate - expected_crit_rate) <= tolerance, "Observed crit rate does not match expected crit rate (no talents)"
    
    # divine glimpse
    iterations = 10000
    crits = 0
    
    for i in range(iterations):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Divine Glimpse": 1})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        target = [targets[0]]
        _, heal_crit, _, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        if heal_crit:
            crits += 1
            
    holy_shock_bonus_crit = 0.1
    divine_glimpse_bonus_crit = 0.08
            
    expected_crit_rate = paladin.crit / 100 + holy_shock_bonus_crit + divine_glimpse_bonus_crit
    observed_crit_rate = crits / iterations
    
    print(f"Expected crit rate: {expected_crit_rate}")
    print(f"Observed crit rate: {observed_crit_rate}")
    
    tolerance = 0.02
    assert abs(observed_crit_rate - expected_crit_rate) <= tolerance, "Observed crit rate does not match expected crit rate (divine glimpse)"
    
def test_divine_resonance_holy_shock():
    # no talents, no crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        divine_resonance_holy_shock = DivineResonanceHolyShock(paladin)
        
        paladin.crit = -10
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = divine_resonance_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = 21576
        
        if i == 0:
            print(f"Holy Shock Divine Resonance (no talents, no crit)")
            print(f"Expected Holy Shock: {expected_heal_amount}")
            print(f"Observed Holy Shock: {heal_amount}")
        
        assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Divine Resonance Holy Shock (no talents, no crit) unexpected value"
        
def test_divine_toll_holy_shock():
    # no talents, no crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        divine_resonance_toll = DivineTollHolyShock(paladin)
        
        paladin.crit = -10
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = divine_resonance_toll.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = 21576
        
        if i == 0:
            print(f"Holy Shock Divine Toll (no talents, no crit)")
            print(f"Expected Holy Shock: {expected_heal_amount}")
            print(f"Observed Holy Shock: {heal_amount}")
        
        assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Divine Toll Holy Shock (no talents, no crit) unexpected value"
        
def test_rising_sunlight_holy_shock():
    # no talents, no crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        rising_sunlight_holy_shock = RisingSunlightHolyShock(paladin)
        
        paladin.crit = -10
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = rising_sunlight_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = 21576
        
        if i == 0:
            print(f"Holy Shock Rising Sunlight (no talents, no crit)")
            print(f"Expected Holy Shock: {expected_heal_amount}")
            print(f"Observed Holy Shock: {heal_amount}")
        
        assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Rising Sunlight Holy Shock (no talents, no crit) unexpected value"
 
def test_holy_light():
    # no talents, no crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        holy_light = paladin.abilities["Holy Light"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(74615 / 10) * 10
        
        if i == 0:
            print(f"Holy Light (no talents, no crit)")
            print(f"Expected Holy Light: {expected_heal_amount}")
            print(f"Observed Holy Light: {heal_amount}")
        
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Light (no talents, no crit) unexpected value"
        
def test_holy_light_resplendent_light():
    # no talents, no crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Resplendent Light": 1})
        
        holy_light = paladin.abilities["Holy Light"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, heal_amount, resplendent_light_heal_amount, _ = holy_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(74615 * 0.08 / 10) * 10
        assert round(resplendent_light_heal_amount / 10) * 10 == expected_heal_amount, "Holy Light (no talents, no crit) unexpected value"
        
def test_holy_light_crit():        
    # no talents, crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        holy_light = paladin.abilities["Holy Light"]
        
        set_crit_to_max(paladin)
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(74615 * 2 / 10) * 10
        
        if i == 0:
            print(f"Holy Light (no talents, crit)")
            print(f"Expected Holy Light: {expected_heal_amount}")
            print(f"Observed Holy Light: {heal_amount}")
        
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Light (no talents, crit) unexpected value"
   
def test_holy_light_awestruck():     
    # awestruck, no crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        holy_light = paladin.abilities["Holy Light"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(74615 / 10) * 10
        
        if i == 0:
            print(f"Holy Light (awestruck, no crit)")
            print(f"Expected Holy Light: {expected_heal_amount}")
            print(f"Observed Holy Light: {heal_amount}")
        
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Light (Awestruck, no crit) unexpected value"
        
    # awestruck, crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Awestruck": 1})
        
        holy_light = paladin.abilities["Holy Light"]
        
        set_crit_to_max(paladin)
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(74615 * 2 * 1.1 / 10) * 10
        
        if i == 0:
            print(f"Holy Light (awestruck, crit)")
            print(f"Expected Holy Light: {expected_heal_amount}")
            print(f"Observed Holy Light: {heal_amount}")
        
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Light (Awestruck, no crit) unexpected value"
        
def test_holy_light_divine_favor():     
    # divine favour, no crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Divine Favor": 1})
        
        divine_favor = paladin.abilities["Divine Favor"]
        holy_light = paladin.abilities["Holy Light"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, _ = divine_favor.cast_healing_spell(paladin, target, 0, False)
        divine_favor_cast_time = holy_light.calculate_cast_time(paladin)
        _, _, heal_amount, _, _ = holy_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(74615 * 1.6 / 10) * 10
        expected_cast_time = 1.12
        
        if i == 0:
            print(f"Holy Light (divine favour, no crit)")
            print(f"Expected Holy Light: {expected_heal_amount}")
            print(f"Observed Holy Light: {heal_amount}")
        
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Light (Divine Favor, no crit) unexpected value"
        assert round(divine_favor_cast_time, 2) == expected_cast_time
        
def test_holy_light_hand_of_divinity():     
    # hand_of_divinity, no crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Hand of Divinity": 1})
        
        hand_of_divinity = paladin.abilities["Hand of Divinity"]
        holy_light = paladin.abilities["Holy Light"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, _ = hand_of_divinity.cast_healing_spell(paladin, target, 0, False)
        paladin.global_cooldown = 0
        hand_of_divinity_cast_time = holy_light.calculate_cast_time(paladin)
        _, _, heal_amount, _, _ = holy_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(74615 * 1.4 / 10) * 10
        expected_cast_time = 0
        
        if i == 0:
            print(f"Holy Light (hand of divinity, no crit)")
            print(f"Expected Holy Light: {expected_heal_amount}")
            print(f"Observed Holy Light: {heal_amount}")
        
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Light (Hand of Divinity, no crit) unexpected value"
        assert round(hand_of_divinity_cast_time, 2) == expected_cast_time
    
def test_holy_light_tyrs_deliverance():   
    # tyr's deliverance, no crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Tyr's Deliverance": 1})
        
        tyrs_deliverance = TyrsDeliveranceHeal(paladin)
        holy_light = paladin.abilities["Holy Light"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, _ = tyrs_deliverance.cast_healing_spell(paladin, target, 0, True)
        paladin.global_cooldown = 0
        _, _, heal_amount, _, _ = holy_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(74615 * 1.15 / 10) * 10
        
        if i == 0:
            print(f"Holy Light (tyr's deliverance, no crit)")
            print(f"Expected Holy Light: {expected_heal_amount}")
            print(f"Observed Holy Light: {heal_amount}")
        
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Light (Tyr's Deliverance, no crit) unexpected value" 
        
def test_flash_of_light():
    # no talents, no crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        flash_of_light = paladin.abilities["Flash of Light"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, heal_amount, _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(36968 / 10) * 10
        
        if i == 0:
            print(f"Flash of Light (no talents, no crit)")
            print(f"Expected Flash of Li36968ght: {expected_heal_amount}")
            print(f"Observed Flash of Light: {heal_amount}")
        
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Flash of Light (no talents, no crit) unexpected value"
        
def test_flash_of_light_crit():        
    # no talents, crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        flash_of_light = paladin.abilities["Flash of Light"]
        
        set_crit_to_max(paladin)
        
        target = [targets[0]]
        _, _, heal_amount, _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(36968 * 2 / 10) * 10
        
        if i == 0:
            print(f"Flash of Light (no talents, crit)")
            print(f"Expected Flash of Light: {expected_heal_amount}")
            print(f"Observed Flash of Light: {heal_amount}")
        
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Flash of Light (no talents, crit) unexpected value"
   
def test_flash_of_light_awestruck():     
    # awestruck, no crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        flash_of_light = paladin.abilities["Flash of Light"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, heal_amount, _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(36968 / 10) * 10
        
        if i == 0:
            print(f"Flash of Light (awestruck, no crit)")
            print(f"Expected Flash of Light: {expected_heal_amount}")
            print(f"Observed Flash of Light: {heal_amount}")
        
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Flash of Light (Awestruck, no crit) unexpected value"
        
    # awestruck, crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Awestruck": 1})
        
        flash_of_light = paladin.abilities["Flash of Light"]
        
        set_crit_to_max(paladin)
        
        target = [targets[0]]
        _, _, heal_amount, _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(36968 * 2 * 1.1 / 10) * 10

        if i == 0:
            print(f"Flash of Light (awestruck, crit)")
            print(f"Expected Flash of Light: {expected_heal_amount}")
            print(f"Observed Flash of Light: {heal_amount}")

        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Flash of Light (Awestruck, no crit) unexpected value"
        
def test_flash_of_light_divine_favor():     
    # divine favour, no crit & flash of light cast time
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Divine Favor": 1})
        
        divine_favor = paladin.abilities["Divine Favor"]
        flash_of_light = paladin.abilities["Flash of Light"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, _ = divine_favor.cast_healing_spell(paladin, target, 0, False)
        divine_favor_cast_time = flash_of_light.calculate_cast_time(paladin)
        _, _, heal_amount, _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(36968 * 1.6 / 10) * 10

        if i == 0:
            print(f"Flash of Light (divine favour, no crit)")
            print(f"Expected Flash of Light: {expected_heal_amount}")
            print(f"Observed Flash of Light: {heal_amount}")

        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Flash of Light (Divine Favor, no crit) unexpected value"
        assert round(divine_favor_cast_time / 0.01) * 0.01 == 0.84
    
def test_flash_of_light_tyrs_deliverance():   
    # tyr's deliverance, no crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Tyr's Deliverance": 1})
        
        tyrs_deliverance = TyrsDeliveranceHeal(paladin)
        flash_of_light = paladin.abilities["Flash of Light"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, _ = tyrs_deliverance.cast_healing_spell(paladin, target, 0, True)
        paladin.global_cooldown = 0
        _, _, heal_amount, _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(36968 * 1.15 / 10) * 10

        if i == 0:
            print(f"Flash of Light (tyr's deliverance, no crit)")
            print(f"Expected Flash of Light: {expected_heal_amount}")
            print(f"Observed Flash of Light: {heal_amount}")

        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Flash of Light (Tyr's Deliverance, no crit) unexpected value"
        
def test_flash_of_light_divine_revelations():
    # divine revelations, no crit
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Divine Revelations": 1})
    
    holy_shock = paladin.abilities["Holy Shock"]
    flash_of_light = paladin.abilities["Flash of Light"]
    
    set_crit_to_max(paladin)
    
    target = [targets[0]]
    _, _, _, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    paladin.global_cooldown = 0
    paladin.crit = -100
    _, _, heal_amount, _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(36968 * 1.2 / 10) * 10

    print(f"Flash of Light (divine revelations, no crit)")
    print(f"Expected Flash of Light: {expected_heal_amount}")
    print(f"Observed Flash of Light: {heal_amount}")

    assert round(heal_amount / 10) * 10 == expected_heal_amount, "Flash of Light (Divine Revelations, no crit) unexpected value"
    
def test_flash_of_light_moment_of_compassion():
    # moment of compassion, no crit
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Moment of Compassion": 1, "Beacon of Faith": 1})
    paladin.set_beacon_targets()
    
    flash_of_light = paladin.abilities["Flash of Light"]
    
    set_crit_to_max(paladin)
    target = [random.choice(paladin.beacon_targets)]
    paladin.crit = -100
    _, _, heal_amount, _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(36968 * 1.15 / 10) * 10

    print(f"Flash of Light (moment of compassion, no crit)")
    print(f"Expected Flash of Light: {expected_heal_amount}")
    print(f"Observed Flash of Light: {heal_amount}")

    assert round(heal_amount / 10) * 10 == expected_heal_amount, "Flash of Light (Moment of Compassion, no crit) unexpected value"
 
# 26% buff       
def test_word_of_glory():
    # no talents, no crit
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {})
    
    word_of_glory = paladin.abilities["Word of Glory"]
    
    target = [targets[0]]
    paladin.crit = -100
    paladin.holy_power = 3
    _, _, heal_amount, _, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(54101 / 10) * 10
    
    print(f"Word of Glory (no talents, no crit)")
    print(f"Expected Word of Glory: {expected_heal_amount}")
    print(f"Observed Word of Glory: {heal_amount}")

    assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Word of Glory (no talents, no crit) unexpected value"
    
def test_word_of_glory_crit_chance():
    # no talents
    iterations = 10000
    crits = 0
    
    for i in range(iterations):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        word_of_glory = paladin.abilities["Word of Glory"]
        
        target = [targets[0]]
        paladin.holy_power = 3
        _, heal_crit, _, _, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
        if heal_crit:
            crits += 1
            
    expected_crit_rate = paladin.crit / 100
    observed_crit_rate = crits / iterations
    
    print(f"Expected crit rate: {expected_crit_rate}")
    print(f"Observed crit rate: {observed_crit_rate}")
    
    tolerance = 0.02
    assert abs(observed_crit_rate - expected_crit_rate) <= tolerance, "Observed crit rate does not match expected crit rate (no talents)"
    
    # extrication
    iterations = 10000
    crits = 0
    
    for i in range(iterations):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Extrication": 1})
        
        word_of_glory = paladin.abilities["Word of Glory"]
        
        target = [targets[0]]
        paladin.holy_power = 3
        _, heal_crit, _, _, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
        if heal_crit:
            crits += 1
            
    bonus_crit = 0.09
    paladin.average_raid_health_percentage = 0.7
            
    expected_crit_rate = paladin.crit / 100 + bonus_crit
    observed_crit_rate = crits / iterations
    
    print(f"Expected crit rate: {expected_crit_rate}")
    print(f"Observed crit rate: {observed_crit_rate}")
    
    tolerance = 0.02
    assert abs(observed_crit_rate - expected_crit_rate) <= tolerance, "Observed crit rate does not match expected crit rate (extrication)"
    
def test_word_of_glory_divine_purpose():
    # divine purpose, no crit
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Divine Purpose": 1}, {})
    
    word_of_glory = paladin.abilities["Word of Glory"]
    
    target = [targets[0]]
    paladin.crit = -100
    paladin.holy_power = 3
    paladin.apply_buff_to_self(DivinePurpose(), 0)
    _, _, heal_amount, _, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(54101 * 1.15 / 10) * 10
    
    print(f"Word of Glory (divine purpose, no crit)")
    print(f"Expected Word of Glory: {expected_heal_amount}")
    print(f"Observed Word of Glory: {heal_amount}")

    assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Word of Glory (Divine Purpose, no crit) unexpected value"
    
def test_word_of_glory_blessing_of_dawn():
    # blessing of dawn, no crit
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Of Dusk and Dawn": 1}, {})
    
    word_of_glory = paladin.abilities["Word of Glory"]
    
    target = [targets[0]]
    paladin.crit = -100
    paladin.holy_power = 3
    paladin.apply_buff_to_self(BlessingOfDawn(), 0)
    _, _, heal_amount, _, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(54101 * 1.3 / 10) * 10
    
    print(f"Word of Glory (blessing of dawn, no crit)")
    print(f"Expected Word of Glory: {expected_heal_amount}")
    print(f"Observed Word of Glory: {heal_amount}")

    assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Word of Glory (Of Dusk and Dawn, no crit) unexpected value"
    
def test_word_of_glory_unending_light():
    # unending light, no crit
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Light of Dawn": 1, "Unending Light": 1})
    
    word_of_glory = paladin.abilities["Word of Glory"]
    light_of_dawn = paladin.abilities["Light of Dawn"]
    
    target = [targets[0]]
    paladin.crit = -100
    paladin.holy_power = 3
    _, _, heal_amount, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    paladin.holy_power = 3
    paladin.global_cooldown = 0
    _, _, heal_amount, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    paladin.holy_power = 3
    paladin.global_cooldown = 0
    _, _, heal_amount, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    paladin.holy_power = 3
    paladin.global_cooldown = 0
    _, _, heal_amount, _, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(54101 * 1.45 / 10) * 10
    
    print(f"Word of Glory (unending light, no crit)")
    print(f"Expected Word of Glory: {expected_heal_amount}")
    print(f"Observed Word of Glory: {heal_amount}")

    assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Word of Glory (Unending Light - 9 stacks, no crit) unexpected value"
    
def test_word_of_glory_healing_modifier_reset():
    # no talents, no crit
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Divine Purpose": 1, "Of Dusk and Dawn": 1}, {"Light of Dawn": 1, "Unending Light": 1})
    
    word_of_glory = paladin.abilities["Word of Glory"]
    light_of_dawn = paladin.abilities["Light of Dawn"]
    
    target = [targets[0]]
    paladin.crit = -100
    paladin.holy_power = 3
    _, _, heal_amount, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    paladin.holy_power = 3
    paladin.global_cooldown = 0
    _, _, heal_amount, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    paladin.holy_power = 3
    paladin.global_cooldown = 0
    _, _, heal_amount, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    paladin.holy_power = 3
    paladin.global_cooldown = 0
    paladin.apply_buff_to_self(DivinePurpose(), 0)
    paladin.apply_buff_to_self(BlessingOfDawn(), 0)
    _, _, heal_amount, _, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(54101 * 1.45 * 1.3 * 1.15 / 10) * 10
    
    print(f"Word of Glory (all buffs, no crit)")
    print(f"Expected Word of Glory: {expected_heal_amount}")
    print(f"Observed Word of Glory: {heal_amount}")

    assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Word of Glory (Unending Light - 9 stacks, Divine Purpose, Blessing of Dawn, no crit) unexpected value"
    
    # after resetting buffs
    if "Divine Purpose" in paladin.active_auras:
        del paladin.active_auras["Divine Purpose"]
    paladin.holy_power = 3
    paladin.global_cooldown = 0
    _, _, heal_amount, _, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(54101 / 10) * 10
    
    print(f"Word of Glory (after buffs reset, no crit)")
    print(f"Expected Word of Glory: {expected_heal_amount}")
    print(f"Observed Word of Glory: {heal_amount}")

    assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Word of Glory (Unending Light - 9 stacks, no crit) unexpected value"
   
# 20% buff 
def test_light_of_dawn():
    # no talents, no crit
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Light of Dawn": 1})
    
    light_of_dawn = paladin.abilities["Light of Dawn"]
    
    target = [targets[0]]
    paladin.crit = -100
    paladin.holy_power = 3
    _, _, heal_amount, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(11714 / 10) * 10
        
    print(f"Light of Dawn (no talents, no crit)")
    print(f"Expected Light of Dawn: {expected_heal_amount}")
    print(f"Observed Light of Dawn: {heal_amount}")

    assert round(heal_amount / 10) * 10 == expected_heal_amount, "Light of Dawn (no talents, no crit) unexpected value"
    
def test_light_of_dawn_crit_chance():
    # no talents
    iterations = 10000
    crits = 0
    
    for i in range(iterations):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Light of Dawn": 1})
        
        light_of_dawn = paladin.abilities["Light of Dawn"]
        
        target = [targets[0]]
        paladin.holy_power = 3
        _, heal_crit, heal_amount, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
        if heal_crit:
            crits += 1
            
    expected_crit_rate = paladin.crit / 100
    observed_crit_rate = crits / iterations
    
    print(f"Expected crit rate: {expected_crit_rate}")
    print(f"Observed crit rate: {observed_crit_rate}")
    
    tolerance = 0.02
    assert abs(observed_crit_rate - expected_crit_rate) <= tolerance, "Observed crit rate does not match expected crit rate (no talents)"
    
    # extrication
    iterations = 10000
    crits = 0
    
    for i in range(iterations):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Extrication": 1, "Light of Dawn": 1}, {"Luminosity": 1})
        
        light_of_dawn = paladin.abilities["Light of Dawn"]
        
        target = [targets[0]]
        paladin.holy_power = 3
        _, heal_crit, heal_amount, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
        if heal_crit:
            crits += 1
            
    bonus_crit = 0.19
    paladin.average_raid_health_percentage = 0.7
            
    expected_crit_rate = paladin.crit / 100 + bonus_crit
    observed_crit_rate = crits / iterations
    
    print(f"Expected crit rate: {expected_crit_rate}")
    print(f"Observed crit rate: {observed_crit_rate}")
    
    tolerance = 0.02
    assert abs(observed_crit_rate - expected_crit_rate) <= tolerance, "Observed crit rate does not match expected crit rate (extrication)"
    
def test_light_of_dawn_divine_purpose():
    # no talents, no crit
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Divine Purpose": 1}, {"Light of Dawn": 1})
    
    light_of_dawn = paladin.abilities["Light of Dawn"]
    
    target = [targets[0]]
    paladin.crit = -100
    paladin.holy_power = 3
    paladin.apply_buff_to_self(DivinePurpose(), 0)
    _, _, heal_amount, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(11714 * 1.15 / 100) * 100
            
    print(f"Light of Dawn (divine purpose, no crit)")
    print(f"Expected Light of Dawn: {expected_heal_amount}")
    print(f"Observed Light of Dawn: {heal_amount}")

    assert round(heal_amount / 100) * 100 == expected_heal_amount, "Light of Dawn (Divine Purpose, no crit) unexpected value"
    
def test_light_of_dawn_blessing_of_dawn():
    # no talents, no crit
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Of Dusk and Dawn": 1}, {"Light of Dawn": 1})
    
    light_of_dawn = paladin.abilities["Light of Dawn"]
    
    target = [targets[0]]
    paladin.crit = -100
    paladin.holy_power = 3
    paladin.apply_buff_to_self(BlessingOfDawn(), 0)
    _, _, heal_amount, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(11714 * 1.3 / 10) * 10
            
    print(f"Light of Dawn (blessing of dawn, no crit)")
    print(f"Expected Light of Dawn: {expected_heal_amount}")
    print(f"Observed Light of Dawn: {heal_amount}")

    assert round(heal_amount / 10) * 10 == expected_heal_amount, "Light of Dawn (Of Dusk and Dawn, no crit) unexpected value"
    
def test_light_of_dawn_empyrean_legacy():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Light of Dawn": 1, "Empyrean Legacy": 1})
    
    word_of_glory = paladin.abilities["Word of Glory"]
    judgment = paladin.abilities["Judgment"]
    enemy_target = EnemyTarget("enemyTarget1")
       
    target = [targets[0]]
    paladin.crit = -100
    _, _, _, _, _, _ = judgment.cast_damage_spell(paladin, [enemy_target], 0, targets)
    paladin.global_cooldown = 0
    paladin.holy_power = 3
    _, _, _, _, _, light_of_dawn_healing = word_of_glory.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = 73212
            
    print(f"Light of Dawn (empyrean legacy, no crit)")
    print(f"Expected Light of Dawn: {expected_heal_amount}")
    print(f"Observed Light of Dawn: {light_of_dawn_healing}")

    assert expected_heal_amount - 1000 <= round(light_of_dawn_healing / 10) * 10 <= expected_heal_amount + 1000, "Light of Dawn (Empyrean Legacy) unexpected value"
    
# 5% transfer nerf  
def test_barrier_of_faith_initial_absorb():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Barrier of Faith": 1})
    
    barrier_of_faith = paladin.abilities["Barrier of Faith"]
       
    paladin.crit = -100
    target = [targets[0]]
    _, _, barrier_of_faith_healing = barrier_of_faith.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = 58050
    assert expected_heal_amount - 100 <= round(barrier_of_faith_healing / 10) * 10 <= expected_heal_amount + 100, "Barrier of Light Initial Absorb unexpected value"
 
def test_barrier_of_faith_holy_shock():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Barrier of Faith": 1})
    
    barrier_of_faith = paladin.abilities["Barrier of Faith"]
    holy_shock = paladin.abilities["Holy Shock"]
    
    # regular holy shock
    paladin.crit = -100
    target = [targets[0]]
    _, _, _ = barrier_of_faith.cast_healing_spell(paladin, target, 0, True)
    paladin.global_cooldown = 0
    _, _, _, _, barrier_of_faith_holy_shock_healing = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
    expected_heal_amount = 17980 * 1.2 * 0.2
    assert expected_heal_amount - 100 <= round(barrier_of_faith_holy_shock_healing / 10) * 10 <= expected_heal_amount + 100, "Barrier of Light (Holy Shock) unexpected value"
    
    # divine resonance
    divine_resonance_holy_shock = DivineResonanceHolyShock(paladin)
    paladin.global_cooldown = 0
    _, _, _, _, barrier_of_faith_holy_shock_healing = divine_resonance_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
    expected_heal_amount = 17980 * 1.2 * 0.2
    assert expected_heal_amount - 100 <= round(barrier_of_faith_holy_shock_healing / 10) * 10 <= expected_heal_amount + 100, "Barrier of Light (Divine Resonance Holy Shock) unexpected value"
    
    # divine toll
    divine_toll_holy_shock = DivineTollHolyShock(paladin)
    paladin.global_cooldown = 0
    _, _, _, _, barrier_of_faith_holy_shock_healing = divine_toll_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
    expected_heal_amount = 17980 * 1.2 * 0.2
    assert expected_heal_amount - 100 <= round(barrier_of_faith_holy_shock_healing / 10) * 10 <= expected_heal_amount + 100, "Barrier of Light (Divine Toll Holy Shock) unexpected value"
    
    # rising sunlight
    rising_sunlight_holy_shock = RisingSunlightHolyShock(paladin)
    paladin.global_cooldown = 0
    _, _, _, _, barrier_of_faith_holy_shock_healing = rising_sunlight_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
    expected_heal_amount = 17980 * 1.2 * 0.2
    assert expected_heal_amount - 100 <= round(barrier_of_faith_holy_shock_healing / 10) * 10 <= expected_heal_amount + 100, "Barrier of Light (Rising Sunlight Holy Shock) unexpected value"
    
def test_barrier_of_faith_holy_light():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Barrier of Faith": 1})
    
    barrier_of_faith = paladin.abilities["Barrier of Faith"]
    holy_light = paladin.abilities["Holy Light"]
    
    paladin.crit = -100
    target = [targets[0]]
    _, _, _ = barrier_of_faith.cast_healing_spell(paladin, target, 0, True)
    paladin.global_cooldown = 0
    _, _, _, _, barrier_of_faith_holy_light_healing = holy_light.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = 59692 * 0.2
    assert expected_heal_amount - 100 <= round(barrier_of_faith_holy_light_healing / 10) * 10 <= expected_heal_amount + 100, "Barrier of Light (Holy Light) unexpected value"
    
def test_barrier_of_faith_flash_of_light():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Barrier of Faith": 1})
    
    barrier_of_faith = paladin.abilities["Barrier of Faith"]
    flash_of_light = paladin.abilities["Flash of Light"]
    
    paladin.crit = -100
    target = [targets[0]]
    _, _, _ = barrier_of_faith.cast_healing_spell(paladin, target, 0, True)
    paladin.global_cooldown = 0
    _, _, _, barrier_of_faith_flash_of_light_healing = flash_of_light.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = 46210 * 0.2
    assert expected_heal_amount - 100 <= round(barrier_of_faith_flash_of_light_healing / 10) * 10 <= expected_heal_amount + 100, "Barrier of Light (Flash of Light) unexpected value"
    
def test_holy_prism():
    # no talents, no crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Holy Prism": 1})
        
        holy_prism = paladin.abilities["Holy Prism"]
        
        paladin.crit = -10
        
        target = [targets[0]]
        _, _, heal_amount = holy_prism.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = 29850
        
        if i == 0:
            print(f"Holy Prism (no talents, no crit)")
            print(f"Expected Holy Prism: {expected_heal_amount}")
            print(f"Observed Holy Prism: {heal_amount}")
            
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Prism (no talents, no crit) unexpected value"
        
def test_tyrs_deliverance_heal():
    # no talents, no crit
    for i in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Tyr's Deliverance": 1})
        
        tyrs_deliverance = TyrsDeliveranceHeal(paladin)
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, heal_amount = tyrs_deliverance.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = 8410
        
        if i == 0:
            print(f"Tyr's Deliverance heal (no talents, no crit)")
            print(f"Expected Tyr's Deliverance heal: {expected_heal_amount}")
            print(f"Observed Tyr's Deliverance heal: {heal_amount}")
            
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Tyr's Deliverance (no talents, no crit) unexpected value"
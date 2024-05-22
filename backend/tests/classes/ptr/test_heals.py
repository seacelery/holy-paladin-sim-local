import os
import json
import pprint

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

path_to_equipment_data = os.path.join(os.path.dirname(__file__), "character_data", "equipment_data.json")
path_to_updated_equipment_data = os.path.join(os.path.dirname(__file__), "character_data", "updated_equipment_data")

character_data = load_data_from_file(path_to_character_data)
stats_data = load_data_from_file(path_to_stats_data)

talent_data = load_data_from_file(path_to_talent_data)
base_class_talents_data = load_data_from_file(path_to_base_class_talents_data)
base_spec_talents_data = load_data_from_file(path_to_base_spec_talents_data)

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
    paladin.set_bonuses = {"season_1": 0, "season_2": 0, "season_3": 0}
    
    return targets, glimmer_targets

def reset_talents(paladin):
    paladin.update_character(class_talents=base_class_talents_data, spec_talents=base_spec_talents_data)
    paladin.update_equipment(updated_equipment_data)
    
def update_talents(paladin, class_talents={}, spec_talents={}):
    paladin.update_character(class_talents=class_talents, spec_talents=spec_talents)
    paladin.update_equipment(updated_equipment_data)

def set_crit_to_max(paladin):
    paladin.flat_crit = 100
    paladin.update_stat("crit", 0)
    

# heals
# 20% buff
def test_holy_shock():
    # no talents, no crit
    print("a")
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        paladin.crit = -10
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = 17980 * 1.2
        assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Holy Shock (no talents, no crit) unexpected value"
        
def test_holy_shock_mastery_effectiveness():
    # no talents, no crit, no mastery effectiveness
    for _ in range(100):
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
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Reclamation": 1})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        paladin.crit = -10
        paladin.average_raid_health_percentage = 0.7
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = round(17980 * 1.15 * 1.2 / 10) * 10
        assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Holy Shock (no talents, no crit, Reclamation at 70%) unexpected value"
    
def test_holy_shock_crit():
    # no talents - crit & infusion of light application
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        set_crit_to_max(paladin)
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = 17980 * 2 * 1.2
        assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Holy Shock (no talents, crit) unexpected value"
        assert "Infusion of Light" in paladin.active_auras
    
def test_holy_shock_awestruck():
    # awestruck - no crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Awestruck": 1})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        paladin.crit = -10
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = round((17980 * 1.2) / 10) * 10
        assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Holy Shock (Awestruck, no crit) unexpected value"
    
    # awestruck - crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Awestruck": 1})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        set_crit_to_max(paladin)
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = round((17980 * 2 * 1.1 * 1.2) / 10) * 10
        assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Holy Shock (Awestruck, crit) unexpected value"
        
def test_holy_shock_tyrs_deliverance():   
    # tyr's deliverance, no crit
    for _ in range(100):
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
        
        expected_heal_amount = round(17980 * 1.15 * 1.2 / 10) * 10
        assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Holy Shock (Tyr's Deliverance, no crit) unexpected value"
        
# def test_holy_shock_crit_chance():
#     # no talents
#     iterations = 10000
#     crits = 0
    
#     for _ in range(iterations):
#         paladin = initialise_paladin()
#         targets, glimmer_targets = set_up_paladin(paladin)
        
#         reset_talents(paladin)
#         update_talents(paladin, {}, {})
        
#         holy_shock = paladin.abilities["Holy Shock"]
        
#         target = [targets[0]]
#         _, heal_crit, _, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
#         if heal_crit:
#             crits += 1
            
#     holy_shock_bonus_crit = 0.1
            
#     expected_crit_rate = paladin.crit / 100 + holy_shock_bonus_crit
#     observed_crit_rate = crits / iterations
    
#     print(f"Expected crit rate: {expected_crit_rate}")
#     print(f"Observed crit rate: {observed_crit_rate}")
    
#     tolerance = 0.02
#     assert abs(observed_crit_rate - expected_crit_rate) <= tolerance, "Observed crit rate does not match expected crit rate (no talents)"
    
#     # divine glimpse
#     iterations = 10000
#     crits = 0
    
#     for _ in range(iterations):
#         paladin = initialise_paladin()
#         targets, glimmer_targets = set_up_paladin(paladin)
        
#         reset_talents(paladin)
#         update_talents(paladin, {}, {"Divine Glimpse": 1})
        
#         holy_shock = paladin.abilities["Holy Shock"]
        
#         target = [targets[0]]
#         _, heal_crit, _, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
#         if heal_crit:
#             crits += 1
            
#     holy_shock_bonus_crit = 0.1
#     divine_glimpse_bonus_crit = 0.08
            
#     expected_crit_rate = paladin.crit / 100 + holy_shock_bonus_crit + divine_glimpse_bonus_crit
#     observed_crit_rate = crits / iterations
    
#     print(f"Expected crit rate: {expected_crit_rate}")
#     print(f"Observed crit rate: {observed_crit_rate}")
    
#     tolerance = 0.02
#     assert abs(observed_crit_rate - expected_crit_rate) <= tolerance, "Observed crit rate does not match expected crit rate (divine glimpse)"
    
def test_divine_resonance_holy_shock():
    # no talents, no crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        divine_resonance_holy_shock = DivineResonanceHolyShock(paladin)
        
        paladin.crit = -10
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = divine_resonance_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = 17980 * 1.2
        assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Divine Resonance Holy Shock (no talents, no crit) unexpected value"
        
def test_divine_toll_holy_shock():
    # no talents, no crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        divine_resonance_toll = DivineTollHolyShock(paladin)
        
        paladin.crit = -10
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = divine_resonance_toll.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = 17980 * 1.2
        assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Divine Toll Holy Shock (no talents, no crit) unexpected value"
        
def test_rising_sunlight_holy_shock():
    # no talents, no crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        rising_sunlight_holy_shock = RisingSunlightHolyShock(paladin)
        
        paladin.crit = -10
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = rising_sunlight_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = 17980 * 1.2
        assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Rising Sunlight Holy Shock (no talents, no crit) unexpected value"
 
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
    
    expected_heal_amount = round(40587 * 1.26 / 10) * 10
    assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Word of Glory (no talents, no crit) unexpected value"
    
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
    
    expected_heal_amount = round(40587 * 1.15 * 1.26 / 10) * 10
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
    
    expected_heal_amount = round(40587 * 1.3 * 1.26 / 10) * 10
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
    
    expected_heal_amount = round(40587 * 1.45 * 1.26 / 10) * 10
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
    
    expected_heal_amount = round(40587 * 1.45 * 1.3 * 1.15 * 1.26 / 10) * 10
    assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Word of Glory (Unending Light - 9 stacks, Divine Purpose, Blessing of Dawn, no crit) unexpected value"
    
    # after resetting buffs
    if "Divine Purpose" in paladin.active_auras:
        del paladin.active_auras["Divine Purpose"]
    paladin.holy_power = 3
    paladin.global_cooldown = 0
    _, _, heal_amount, _, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(40587 * 1.26 / 10) * 10
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
    
    expected_heal_amount = round(9760 * 1.2 / 10) * 10
    assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Light of Dawn (no talents, no crit) unexpected value"
    
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
    
    expected_heal_amount = round(9760 * 1.15 * 1.2 / 100) * 100
    assert expected_heal_amount - 200 <= round(heal_amount / 100) * 100 <= expected_heal_amount + 200, "Light of Dawn (Divine Purpose, no crit) unexpected value"
    
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
    
    expected_heal_amount = round(9760 * 1.3 * 1.2 / 10) * 10
    assert expected_heal_amount - 200 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 200, "Light of Dawn (Of Dusk and Dawn, no crit) unexpected value"
    
def test_light_of_dawn_empyrean_legacy():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Light of Dawn": 1, "Empyrean Legacy": 1})
    
    word_of_glory = paladin.abilities["Word of Glory"]
    judgment = paladin.abilities["Judgment"]
    enemy_target = EnemyTarget("enemyTarget1")
    light_of_dawn = paladin.abilities["Light of Dawn"]
       
    target = [targets[0]]
    paladin.crit = -100
    _, _, _, _, _, _ = judgment.cast_damage_spell(paladin, [enemy_target], 0, targets)
    paladin.global_cooldown = 0
    paladin.holy_power = 3
    _, _, _, _, _, light_of_dawn_healing = word_of_glory.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = 9760 * 5 * 1.25 * 1.2
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
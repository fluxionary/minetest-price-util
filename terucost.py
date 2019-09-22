import argparse
import collections
import math

# cost, in mg, of various raw materials
_COST_SCALE = 1
_DENOMINATOR = 172.20  # gold ore
_CRYSTAL_SCALE = 3

COSTS = dict(
    stone=1/99,
    gravel=1/99,
    sand=1/99,
    silver_sand=5/99,
    clay=1/99,
    dirt=5/99,
    tree=1/99,
    cotton=10/99,
    obsidian=1/99,
    flint=16 / 5,
    water=1,
    flower=1,
    sapling=1,

    # scaled by what comes out of the gravel sieve
    coal=(22.28/_DENOMINATOR)*_COST_SCALE,
    steel_ingot=(23.15/_DENOMINATOR)*_COST_SCALE,
    gold_ingot=(172.20/_DENOMINATOR)*_COST_SCALE,
    copper_ingot=(56.57/_DENOMINATOR)*_COST_SCALE,
    tin_ingot=(77.60/_DENOMINATOR)*_COST_SCALE,
    terumetal_ingot=(114.75/_DENOMINATOR)*_COST_SCALE,
    silver_ingot=(128.68/_DENOMINATOR)*_COST_SCALE,
    mithril_ingot=(523.34/_DENOMINATOR)*_COST_SCALE,

    quartz=(64.46/_DENOMINATOR)*_COST_SCALE*_CRYSTAL_SCALE,
    mese=(218.43/_DENOMINATOR)*_COST_SCALE*_CRYSTAL_SCALE,
    diamond=(341.10/_DENOMINATOR)*_COST_SCALE*_CRYSTAL_SCALE,
    titanium=(665.85/_DENOMINATOR)*_COST_SCALE*_CRYSTAL_SCALE,
)


class Components(collections.Counter):
    def __mul__(self, n: int):
        if not isinstance(n, int):
            return NotImplemented

        return type(self)({
            key: val * n
            for key, val in self.items()
        })

    def __truediv__(self, n: int):
        if not isinstance(n, int):
            return NotImplemented

        return type(self)({
            key: val / n
            for key, val in self.items()
        })

    def __add__(self, other):
        return type(self)(super().__add__(other))


def cost_of(c: Components, markup: float=1.0, round_up: float=None) -> float:
    s = sum(
        COSTS[key] * value * markup
        for key, value in c.items()
    )
    if round_up is None:
        return s

    else:
        return round_up * math.ceil(s / round_up)


def main(args):
    # crafting recipes
    # default materials
    stone = Components(stone=1)
    cobblestone = stone * 1
    tree = Components(tree=1)
    planks = tree / 4
    stick = planks / 4
    leaves = tree / 8  # from tubelib grinder
    water = Components(water=1)
    flint = Components(flint=1)
    sand = Components(sand=1)
    silver_sand = Components(silver_sand=1)
    glass = sand * 1
    cotton = Components(cotton=1)
    wool = cotton * 4
    string = cotton * 2
    flower = Components(flower=1)
    sapling = Components(sapling=1)
    dye = flower / 4
    dirt = Components(dirt=1)
    obsidian = Components(obsidian=1)
    obsidian_shard = obsidian / 9
    obsidian_grit = obsidian_shard
    obsidian_glass = obsidian_shard
    clay = Components(clay=1)
    papyrus = leaves * 1

    # metals and other ores
    steel_ingot = Components(steel_ingot=1)
    steel_block = steel_ingot * 9
    gold_ingot = Components(gold_ingot=1)
    gold_block = gold_ingot * 9
    copper_ingot = Components(copper_ingot=1)
    copper_block = copper_ingot * 9
    tin_ingot = Components(tin_ingot=1)
    tin_block = tin_ingot * 9
    terumetal_ingot = Components(terumetal_ingot=1)
    terumetal_block = terumetal_ingot * 9
    diamond = Components(diamond=1)
    diamond_block = diamond * 9
    mese = Components(mese=1)
    mese_block = mese * 9
    mese_fragment = mese / 9
    silver_ingot = Components(silver_ingot=1)
    silver_block = silver_ingot * 9
    mithril_ingot = Components(mithril_ingot=1)
    mithril_block = mithril_ingot * 9
    titanium = Components(titanium=1)
    titanium_block = titanium * 9
    coal = Components(coal=1)
    coal_block = coal * 9
    quartz = Components(quartz=1)
    quartz_block = quartz * 1
    brass_ingot = ((copper_ingot * 2) + silver_ingot) / 3
    brass_block = brass_ingot * 9
    bronze_ingot = ((copper_ingot * 8) + tin_ingot) / 9
    bronze_block = bronze_ingot * 9

    # basic craftables
    bucket = steel_ingot * 3
    water_bucket = bucket + water
    furnace = stone * 8
    chest = planks * 8
    torch = (coal + stick) / 4

    tube = (steel_ingot + tin_ingot + (planks * 3)) / 4

    # "basic materials" mod
    heating_element = ((copper_ingot * 2) + mese_fragment) / 2
    silicon = ((sand * 3) + steel_ingot) / 4
    simple_ic = ((silicon * 3) + copper_ingot) / 4
    copper_strip = copper_ingot / 6
    steel_strip = steel_ingot / 6
    chain_link_steel = steel_ingot / 2
    chain_steel = (chain_link_steel * 3) / 2
    chain_link_brass = brass_ingot / 2
    chain_brass = (chain_link_brass * 3) / 2
    steel_gear = ((steel_ingot * 4) + chain_link_steel) / 6
    oil_extract = leaves * 3
    steel_bar = steel_ingot / 2
    parafin = oil_extract
    plastic = parafin
    plastic_strip = plastic / 3
    empty_spool = (plastic * 7) / 3
    steel_spool = ((empty_spool * 2) + steel_ingot) / 2
    copper_spool = ((empty_spool * 2) + copper_ingot) / 2
    gold_spool = ((empty_spool * 2) + gold_ingot) / 2
    silver_spool = ((empty_spool * 2) + silver_ingot) / 2
    padlock = ((steel_ingot * 2) + steel_bar) / 2
    energy_crystal = (diamond * 2) + (mese_fragment * 2) + torch + gold_ingot
    motor = (mese_fragment * 2) + (copper_spool * 2) + (plastic * 2) + (steel_ingot * 2) + copper_ingot

    # terumet crystalized things
    iron_crystal = steel_ingot
    gold_crystal = gold_ingot
    tin_crystal = tin_ingot
    copper_crystal = copper_ingot
    terumetal_crystal = terumetal_ingot
    obsidian_crystal = obsidian
    diamond_crystal = diamond
    mese_crystal = mese

    flux = terumetal_ingot / 2
    terusteel_ingot = steel_ingot + (flux * 2)
    terucopper_ingot = copper_ingot + flux
    terucopper_block = terucopper_ingot * 9
    terutin_ingot = tin_ingot + flux
    terutin_block = terutin_ingot * 9
    terugold_ingot = gold_ingot + (flux * 3)
    coreglass_ingot = diamond + obsidian_shard + (flux * 5)
    teruchalchum_ingot = (bronze_ingot + (tin_ingot * 2) + (flux * 9)) / 3
    teruceramic = clay + (flux * 2)
    teruceramic_block = teruceramic * 9
    thermese = mese + (flux * 4)
    thermese_block = thermese * 9

    terumetal_coil = terumetal_ingot
    terucopper_coil = terucopper_ingot
    terugold_coil = terugold_ingot

    terumetal_heater = (heating_element * 2) + terumetal_coil
    thermese_element = ((terucopper_ingot * 2) + thermese) / 2
    thermese_heater = (thermese_element * 2) + terugold_coil
    thermese_array = thermese_heater * 6

    biomatter = leaves
    biomatter_block = biomatter * 9
    plant_glue = biomatter + water_bucket
    mulch = tree / 4
    pressed_wood = (plant_glue + (mulch * 8)) / 16

    # entropic_crystal = diamond_crystal + mul(mese_crystal, 4) + mul(obsidian_crystal, 4)
    entropic_crystal = diamond_crystal + (mese_crystal * 4) + (obsidian_grit * 4)
    entropic_matrix = (entropic_crystal * 8) + diamond_block
    heat_glass = (obsidian_glass + (tin_crystal * 2) + plant_glue + obsidian_grit) / 3
    heat_unit = obsidian_glass + (terugold_ingot * 2) + mese + (thermese * 2) + terugold_coil + (teruceramic * 2)

    crystal_growth_chamber = water_bucket + (teruchalchum_ingot * 2) + (obsidian_grit * 3) + (obsidian_glass * 3)
    expansion_press = (stone * 2) + terutin_block + (teruchalchum_ingot * 3) + (terutin_ingot * 3)

    upgrade_base = (terumetal_coil * 3) + (teruceramic * 2) + plant_glue
    max_heat_upgrade = upgrade_base + (thermese * 3)
    heat_gen_upgrade = upgrade_base + (thermese_heater * 3)
    heat_trans_upgrade = upgrade_base + (terugold_coil * 3)
    external_in_upgrade = upgrade_base + motor + (steel_gear * 2)
    external_out_upgrade = upgrade_base + (motor * 2) + steel_gear
    external_io_upgrade = external_in_upgrade + external_out_upgrade + plant_glue + thermese
    tubelib_upgrade = upgrade_base + (tube * 2) + plant_glue + thermese
    terumetal_upgrade = upgrade_base + thermese_heater + (crystal_growth_chamber * 2) + (terumetal_crystal * 3)
    crystal_upgrade = upgrade_base + thermese_array + (energy_crystal * 3) + (entropic_crystal * 3) + crystal_growth_chamber
    speed_upgrade = upgrade_base + thermese_array + (energy_crystal * 3) + (diamond_crystal * 3)

    terumetal_frame = terumetal_heater + (terumetal_ingot * 8)
    terusteel_frame = thermese_heater + (terusteel_ingot * 8)
    coreglass_frame = thermese_array + (coreglass_ingot * 8)

    heatline = ((terugold_coil * 3) + (teruceramic * 6)) / 6
    heatline_distributor = thermese_block + (terugold_coil * 4) + (teruceramic * 4)
    thermal_distributor = teruceramic_block + ((terumetal_coil + terucopper_coil) * 4)
    thermobox = teruceramic_block + ((thermese + terugold_coil) * 4)
    heat_emitter = coreglass_frame + heat_glass + (terugold_coil * 4) + (teruceramic * 2) + heat_unit
    heat_reflector = tin_ingot + ((terumetal_ingot + heat_glass) * 4)

    furnace_heater = terumetal_frame + furnace + copper_block + (terucopper_coil * 2) + (teruceramic * 2) + (copper_strip * 2)
    solar_heater = terusteel_frame + (heat_glass * 3) + (terugold_coil * 2) + (thermese * 2) + water_bucket
    eee_heater = coreglass_frame + heat_glass + (energy_crystal * 4) + (entropic_crystal * 2) + thermobox

    alloy_smelter = terumetal_frame + (terumetal_coil * 2) + (bucket * 2) + terumetal_heater + (copper_strip * 3)
    crusher = terumetal_frame + (terucopper_coil * 4) + (steel_strip * 2) + (expansion_press * 2)
    lava_melter = terumetal_frame + (terutin_ingot * 4) + (terumetal_heater * 4)

    ht_furnace = terusteel_frame + (thermese_heater * 2) + (teruceramic * 5) + copper_strip
    vulcanizer = terusteel_frame + (terugold_coil * 2) + (thermese * 2) + (teruceramic_block * 2) + crystal_growth_chamber + energy_crystal
    mese_garden = terusteel_frame + crystal_growth_chamber + (thermese * 2) + (teruceramic * 4) + energy_crystal
    reformer = terusteel_frame + bucket + (teruceramic * 4) + (terugold_coil * 2) + crystal_growth_chamber

    vacuum_oven = coreglass_frame + (motor * 2) + (teruchalchum_ingot * 2) + (thermese_array * 2) + (teruceramic_block * 2)

    tarball = coal / 4
    bio_tar = (tarball * 4) + biomatter
    rubber_bar = bio_tar

    ore_saw = (teruchalchum_ingot * 4) + (terusteel_ingot * 3)
    advanced_ore_saw = ore_saw + coreglass_ingot + (rubber_bar * 3) + (flux * 6)

    coreglass_pick = (coreglass_ingot * 3) + (stick * 2)

    # terutin_boots = (terutin_ingot * 4)
    # terutin_helm = (terutin_ingot * 5)
    # terutin_legs = (terutin_ingot * 7)
    # terutin_chest = (terutin_ingot * 8)

    rsuit_mat = rubber_bar + coreglass_ingot + teruceramic + (flux * 8)
    vulcan_boots = rsuit_mat * 4
    vulcan_helm = rsuit_mat * 5
    vulcan_legs = rsuit_mat * 7
    vulcan_chest = rsuit_mat * 8

    bracers = (terumetal_crystal * 5) + (terugold_coil * 4)
    bracer_base_element = steel_block / 2
    antigrav_element = bracer_base_element + entropic_crystal + (flux * 4)
    antigrav_bracers = bracers + (antigrav_element * 8)
    aqua_element = bracer_base_element + papyrus + (flux * 4)
    defense_element = bracer_base_element + rsuit_mat + (flux * 4)
    fireproof_element = bracer_base_element + obsidian_crystal + (flux * 4)
    heal_element = bracer_base_element + biomatter_block + (flux * 4)
    jump_element = bracer_base_element + mese_crystal + (flux * 4)
    speed_element = bracer_base_element + diamond_crystal + (flux * 4)

    copper_heat_battery = (terumetal_ingot * 6) + (copper_ingot * 3)
    thermese_heat_battery = (teruceramic * 6) + (thermese * 3)
    void_battery = (cobblestone * 2) + entropic_crystal

    print("furnace heater      ", cost_of(furnace_heater, args.markup, args.roundup))
    print("solar heater        ", cost_of(solar_heater, args.markup, args.roundup))
    print('eee heater          ', cost_of(eee_heater, args.markup, args.roundup))
    print('entropic_matrix     ', cost_of(entropic_matrix, args.markup, args.roundup))
    print()
    print("alloy smelter       ", cost_of(alloy_smelter, args.markup, args.roundup))
    print("crusher             ", cost_of(crusher, args.markup, args.roundup))
    print("lava_melter         ", cost_of(lava_melter, args.markup, args.roundup))
    print()
    print("ht furnace          ", cost_of(ht_furnace, args.markup, args.roundup))
    print("vulcanizer          ", cost_of(vulcanizer, args.markup, args.roundup))
    print("mese garden         ", cost_of(mese_garden, args.markup, args.roundup))
    print("reformer            ", cost_of(reformer, args.markup, args.roundup))
    print()
    print('vacuum_oven         ', cost_of(vacuum_oven, args.markup, args.roundup))
    print()
    print("thermal_distributor ", cost_of(thermal_distributor, args.markup, args.roundup))
    print("thermobox           ", cost_of(thermobox, args.markup, args.roundup))
    print('heat emitter        ', cost_of(heat_emitter, args.markup, args.roundup))
    print('heat reflector      ', cost_of(heat_reflector, args.markup, args.roundup))
    print('11*heatline         ', cost_of(heatline * 11, args.markup, args.roundup))
    print('heatline_distributor', cost_of(heatline_distributor, args.markup, args.roundup))
    print()
    print("crystal_upgrade     ", cost_of(crystal_upgrade, args.markup, args.roundup))
    print("speed_upgrade       ", cost_of(speed_upgrade, args.markup, args.roundup))
    print("max_heat_upgrade    ", cost_of(max_heat_upgrade, args.markup, args.roundup))
    print("heat_gen_upgrade    ", cost_of(heat_gen_upgrade, args.markup, args.roundup))
    print("heat_trans_upgrade  ", cost_of(heat_trans_upgrade, args.markup, args.roundup))
    print("external_in_upgrade ", cost_of(external_in_upgrade, args.markup, args.roundup))
    print("external_out_upgrade", cost_of(external_out_upgrade, args.markup, args.roundup))
    print('tubelib_upgrade     ', cost_of(tubelib_upgrade, args.markup, args.roundup))
    print()
    print('ore saw             ', cost_of(ore_saw, args.markup, args.roundup))
    print('advanced ore saw    ', cost_of(advanced_ore_saw, args.markup, args.roundup))
    print('coreglass pick      ', cost_of(coreglass_pick, args.markup, args.roundup))
    print('vulcan_boots        ', cost_of(vulcan_boots, args.markup, args.roundup))
    print('vulcan_helm         ', cost_of(vulcan_helm, args.markup, args.roundup))
    print('vulcan_legs         ', cost_of(vulcan_legs, args.markup, args.roundup))
    print('vulcan_chest        ', cost_of(vulcan_chest, args.markup, args.roundup))
    print('antigrav_bracers    ', cost_of(antigrav_bracers, args.markup, args.roundup))

    locked_chest = chest + steel_ingot
    iron_chest = locked_chest + (steel_ingot * 8)
    copper_chest = iron_chest + (copper_ingot * 8)
    silver_chest = copper_chest + (silver_ingot * 8)
    gold_chest = silver_chest + (gold_ingot * 8)
    mithril_chest = gold_chest + (mithril_ingot * 8)

    print()
    print('iron chest          ', cost_of(iron_chest, args.markup, args.roundup))
    print('copper chest        ', cost_of(copper_chest, args.markup, args.roundup))
    print('silver chest        ', cost_of(silver_chest, args.markup, args.roundup))
    print('gold chest          ', cost_of(gold_chest, args.markup, args.roundup))
    print('mithril chest       ', cost_of(mithril_chest, args.markup, args.roundup))

    elevator = titanium_block + (glass * 2) + (steel_ingot * 6)
    travelnet = (titanium_block * 2) + (mese_block * 3) + (glass * 4)

    print()
    print('elevator            ', cost_of(elevator, args.markup, args.roundup))
    print('travelnet           ', cost_of(travelnet, args.markup, args.roundup))

    print()
    print('99*quartz block     ', cost_of(quartz_block * 99, args.markup, args.roundup))

    wlan_chip = (mese + copper_ingot + gold_ingot + glass) / 8
    end_wrench = ((steel_ingot * 2) + tin_ingot) / 4

    tougher_titanium = titanium * 4
    titanium_tv = (tougher_titanium * 4) + (steel_ingot * 4) + glass

    mesecon = mese / 18

    sieve = diamond_block + (planks * 6)
    autosieve = sieve + (diamond_block * 5) + (mese_block * 3)

    pusher = ((planks * 4) + (wool * 2) + (tube * 2) + mese) / 2
    forceload_block = (planks * 4) + (energy_crystal * 2) + wlan_chip + titanium_tv
    tubelib_distributor = ((planks * 4) + (tube * 2) + (steel_ingot * 2) + mese) / 2
    black_hole = ((planks * 4) + (coal * 2) + tube) / 2
    teleporter = ((planks * 2) + (gold_ingot * 2) + (mese * 2) + tube) / 2
    protected_chest = chest + tube + steel_ingot
    hp_pusher = (pusher * 2) + tin_ingot + gold_ingot
    hp_distributor = (tubelib_distributor * 2) + tin_ingot + gold_ingot
    hp_chest = (protected_chest * 2) + tin_ingot + gold_ingot
    hp_pushing_chest = hp_pusher + protected_chest + tin_ingot + gold_ingot

    tubelib_lamp = ((wool * 3) + (planks * 2) + wlan_chip + coal) / 4
    tubelib_streetlamp = (tubelib_lamp + glass + steel_ingot) / 2
    tubelib_ceilinglamp = (tubelib_lamp + planks + glass) / 3
    invisible_lamp = ((torch * 4) + wlan_chip) / 2
    industrial_lamp = ((plastic_strip * 2) + glass + wlan_chip + dye + copper_ingot)
    industrial_lamp2 = ((glass * 2) + (steel_bar * 2) + wlan_chip + dye)

    tubelib_button = (planks * 2) + glass + wlan_chip
    tubelib_timer = (planks * 4) + wlan_chip + gold_ingot
    tubelib_sequencer = (planks * 4) + mese + wlan_chip
    tubelib_repeater = (planks * 2) + (wlan_chip * 2)
    tubelib_programmer = steel_ingot + wlan_chip + dye
    tubelib_msecons_converter = tubelib_button + mesecon
    tubelib_not = (planks * 2) + (wlan_chip * 2)
    tubelib_door = planks + wlan_chip
    tubelib_gate = planks + wlan_chip
    access_control = steel_block + wlan_chip
    tubelib_detector = (planks * 2) + (tube * 2) + wlan_chip

    fermenter = (steel_ingot * 4) + (tube * 2) + dirt + mese + planks
    reformer = (steel_ingot * 4) + (tube * 2) + clay + mese + planks
    quarry = (planks * 4) + (mese * 3) + tube + steel_ingot
    fast_pusher = pusher * 3
    liquid_sampler = (planks * 4) + (steel_ingot * 2) + mese + tube + bucket
    harvester = (planks * 2) + (mese * 3) + (steel_ingot * 3) + tube
    grinder = (planks * 4) + (tube * 2) + (tin_ingot * 2) + mese
    funnel = ((planks * 4) + steel_ingot + mese + tube) / 2
    autocrafter = (planks * 2) + (tube * 2) + (steel_ingot * 4) + mese
    biogas = leaves * 2
    biofuel = biogas * 4

    repair_kit = steel_gear + end_wrench + oil_extract


    print()
    print('tube * 33           ', cost_of(tube * 33, args.markup, 1))
    print('teleporter          ', cost_of(teleporter, args.markup, 1))
    print('black_hole          ', cost_of(black_hole, args.markup, 1))
    print('funnel              ', cost_of(funnel, args.markup, 1))
    print('biofuel * 99        ', cost_of(biofuel * 99, args.markup, 1))
    print('repair_kit * 11     ', cost_of(repair_kit * 11, args.markup, 1))

    print('pusher              ', cost_of(pusher, args.markup, 1))
    print('fast pusher         ', cost_of(fast_pusher, args.markup, 1))
    print('HP pusher           ', cost_of(hp_pusher, args.markup, 1))
    print('HP pushing chest    ', cost_of(hp_pushing_chest, args.markup, 1))

    print('distributor         ', cost_of(tubelib_distributor, args.markup, 1))
    print('HP distributor      ', cost_of(hp_distributor, args.markup, 1))

    print('protected chest     ', cost_of(protected_chest, args.markup, 1))
    print('HP chest            ', cost_of(hp_chest, args.markup, 1))

    print('autocrafter         ', cost_of(autocrafter, args.markup, 1))
    print('quarry              ', cost_of(quarry, args.markup, 1))
    print('harvester           ', cost_of(harvester, args.markup, 1))
    print('liquid sampler      ', cost_of(liquid_sampler, args.markup, 1))

    print('fermenter           ', cost_of(fermenter, args.markup, 1))
    print('reformer            ', cost_of(reformer, args.markup, 1))
    print('grinder             ', cost_of(grinder, args.markup, 1))
    print('autosieve           ', cost_of(autosieve, args.markup, args.roundup))

    print('forceload_block     ', cost_of(forceload_block, args.markup, args.roundup))

    print('tubelib_lamp        ', cost_of(tubelib_lamp, args.markup, 1))
    print('tubelib_streetlamp  ', cost_of(tubelib_streetlamp, args.markup, 1))
    print('tubelib_ceilinglamp ', cost_of(tubelib_ceilinglamp, args.markup, 1))
    print('invisible_lamp      ', cost_of(invisible_lamp, args.markup, 1))
    print('industrial_lamp     ', cost_of(industrial_lamp, args.markup, 1))
    print('industrial_lamp2    ', cost_of(industrial_lamp2, args.markup, 1))

    print('tubelib_button      ', cost_of(tubelib_button, args.markup, 1))
    print('access_control      ', cost_of(access_control, args.markup, 1))
    print('tubelib_detector    ', cost_of(tubelib_detector, args.markup, 1))
    print('tubelib_timer       ', cost_of(tubelib_timer, args.markup, 1))
    print('tubelib_sequencer   ', cost_of(tubelib_sequencer, args.markup, 1))
    print('tubelib_repeater    ', cost_of(tubelib_repeater, args.markup, 1))
    print('tubelib_programmer  ', cost_of(tubelib_programmer, args.markup, 1))
    print('msecons_converter   ', cost_of(tubelib_msecons_converter, args.markup, 1))
    print('tubelib_not         ', cost_of(tubelib_not, args.markup, 1))
    print('tubelib_door * 6    ', cost_of(tubelib_door * 6, args.markup, 1))
    print('tubelib_gate * 6    ', cost_of(tubelib_gate * 6, args.markup, 1))

    small_bag = (wool * 6) + cotton
    medium_bag =(small_bag * 2) + (cotton * 2)
    large_bag = (medium_bag * 2) + (cotton * 2)

    print()
    print('small bag           ', cost_of(small_bag, args.markup, 1))
    print('medium bag          ', cost_of(medium_bag, args.markup, 1))
    print('large bag           ', cost_of(large_bag, args.markup, 1))
    print('protection block    ', cost_of(steel_ingot * 10, args.markup, 1))

    glue = sapling / 2
    fiber = glue / 6
    insulated_mesecon = mesecon + (fiber * 2)
    digiline = ((insulated_mesecon * 2) + (fiber * 6) + gold_ingot) / 2

    luacontroller = ((silicon * 4) + (mesecon * 4)) / 2
    microcontroller = luacontroller
    player_detector = (steel_ingot * 7) + microcontroller + microcontroller
    mesecon_button = (mesecon + stone) / 2
    digiline_button = (mesecon_button + luacontroller + digiline)
    lightstone = (dye * 3) + torch + mesecon
    digiline_lcd = ((glass * 3) + (lightstone * 3) + (steel_ingot * 2) + digiline)

    print()
    print('mesecon * 22        ', cost_of(mesecon * 22, args.markup, 1))
    print('insulated_mesecon*11', cost_of(insulated_mesecon * 11, args.markup, 1))
    print('digiline * 11       ', cost_of(digiline * 11, args.markup, 1))
    print('luacontroller       ', cost_of(luacontroller, args.markup, 1))
    print('player_detector     ', cost_of(player_detector, args.markup, 1))
    print('mesecon_button      ', cost_of(mesecon_button, args.markup, 1))
    print('digiline_button     ', cost_of(digiline_button, args.markup, 1))
    print('digiline_lcd        ', cost_of(digiline_lcd, args.markup, 1))

    print()
    print('gold ingot * 99     ', cost_of(gold_ingot * 99, args.markup, 1))
    print('mese * 99           ', cost_of(mese * 99, args.markup, 1))
    print('steel block * 99    ', cost_of(steel_block * 99, args.markup, 1))

    tougher_titanium = titanium * 4
    titanium_plate = (titanium * 8 + tougher_titanium) / 9
    titanium_glass = (titanium * 4 + glass) / 3
    terumet_glass = ((glass * 4) + silver_sand + flux) / 4
    terumet_glow_glass = ((terumet_glass * 4) + mese + flux) / 4
    thermese_battery = (teruceramic * 6) + (thermese * 3)
    goggles = (titanium_plate * 5) + (titanium_glass * 2) + terumet_glow_glass + thermese_battery

    print()
    print('night vision goggles', cost_of(goggles, args.markup, 1))

    buy_at = 1/5
    # print()
    # print('buy steel ingot * 99      ', cost_of(steel_ingot * 99, args.markup * buy_at, .1))
    # print('buy diamond ore * 10      ', cost_of(diamond * 10 * 4, args.markup * buy_at, args.roundup))
    # print('buy iron lump * 99      ', cost_of(steel_ingot * 99 * 3, args.markup * buy_at, args.roundup))
    # print('buy copper lump * 99    ', cost_of(copper_ingot * 99 * 3, args.markup * buy_at, args.roundup))
    # print('buy tin lump * 99       ', cost_of(tin_ingot * 99 * 3, args.markup * buy_at, args.roundup))
    # print('buy gold lump * 99      ', cost_of(gold_ingot * 99 * 3, args.markup * buy_at, args.roundup))
    # print('buy terumetal lump * 99 ', cost_of(terumetal_ingot * 99 * 3, args.markup * buy_at, args.roundup))
    # print('buy silver lump * 99    ', cost_of(silver_ingot * 99 * 3, args.markup * buy_at, args.roundup))
    # print('buy mithril lump * 99   ', cost_of(mithril_ingot * 99 * 3, args.markup * buy_at, args.roundup))


def parse_args(argv=None, namespace=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--markup', '-m', type=float, default=(1/4), help='default: %(default)s')
    parser.add_argument('--roundup', '-r', type=float, default=1, help='default: %(default)s')
    return parser.parse_args(argv, namespace)


if __name__ == '__main__':
    main(parse_args())

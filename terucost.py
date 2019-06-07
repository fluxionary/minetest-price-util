import argparse
import collections
import math

# cost, in mg, of various raw materials
_COST_SCALE = 1
_DENOMINATOR = 173
_CRYSTAL_SCALE = 3

COSTS = dict(
    stone=1/99,
    gravel=1/99,
    sand=1/99,
    clay=1/99,
    dirt=5/99,
    tree=1/99,
    cotton=10/99,
    obsidian=5,
    flint=16 / 5,
    water=1,
    flower=1,
    sapling=1,

    quartz=(64.5/_DENOMINATOR)*_COST_SCALE*_CRYSTAL_SCALE,
    coal=(22.3/_DENOMINATOR)*_COST_SCALE,
    steel_ingot=(23.2/_DENOMINATOR)*_COST_SCALE,
    gold_ingot=(173/_DENOMINATOR)*_COST_SCALE,
    copper_ingot=(56.6/_DENOMINATOR)*_COST_SCALE,
    tin_ingot=(77.7/_DENOMINATOR)*_COST_SCALE,
    mese=(220/_DENOMINATOR)*_COST_SCALE,
    diamond=(345/_DENOMINATOR)*_COST_SCALE,
    terumetal_ingot=(111/_DENOMINATOR)*_COST_SCALE,
    silver_ingot=(129/_DENOMINATOR)*_COST_SCALE*_CRYSTAL_SCALE,
    mithril_ingot=(525/_DENOMINATOR)*_COST_SCALE*_CRYSTAL_SCALE,
    titanium=(694/_DENOMINATOR)*_COST_SCALE*_CRYSTAL_SCALE,
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
    stone = Components(stone=1)
    tree = Components(tree=1)
    planks = tree / 4
    stick = planks / 4
    leaves = tree / 8  # from tubelib grinder
    water = Components(water=1)
    flint = Components(flint=1)
    sand = Components(sand=1)
    glass = sand * 1
    cotton = Components(cotton=1)
    wool = cotton * 4
    string = cotton * 2
    flower = Components(flower=1)
    sapling = Components(sapling=1)
    dye = flower / 4
    dirt = Components(dirt=1)

    steel_ingot = Components(steel_ingot=1)
    steel_block = steel_ingot * 9
    gold_ingot = Components(gold_ingot=1)
    copper_ingot = Components(copper_ingot=1)
    copper_block = copper_ingot * 9
    tin_ingot = Components(tin_ingot=1)
    terumetal_ingot = Components(terumetal_ingot=1)
    bronze_ingot = ((copper_ingot * 8) + tin_ingot) / 9
    diamond = Components(diamond=1)
    diamond_block = diamond * 9
    mese = Components(mese=1)
    mese_block = mese * 9
    mese_fragment = mese / 9
    silver_ingot = Components(silver_ingot=1)
    mithril_ingot = Components(mithril_ingot=1)
    titanium = Components(titanium=1)
    titanium_block = titanium * 9
    coal = Components(coal=1)
    coal_block = coal * 9

    obsidian = Components(obsidian=1)
    obsidian_shard = obsidian / 9
    obsidian_grit = obsidian_shard
    obsidian_glass = obsidian_shard

    clay = Components(clay=1)

    bucket = steel_ingot * 3
    water_bucket = bucket + water
    furnace = stone * 8
    tube = (steel_ingot + tin_ingot + (planks * 3)) / 4
    chest = planks * 8

    iron_crystal = steel_ingot
    gold_crystal = gold_ingot
    tin_crystal = tin_ingot
    copper_crystal = copper_ingot
    terumetal_crystal = terumetal_ingot
    obsidian_crystal = obsidian
    diamond_crystal = diamond
    mese_crystal = mese

    terusteel_ingot = steel_ingot + terumetal_ingot * 2
    terucopper_ingot = copper_ingot + terumetal_ingot
    terucopper_block = terucopper_ingot * 9
    terutin_ingot = tin_ingot + terumetal_ingot
    terutin_block = terutin_ingot * 9
    terugold_ingot = gold_ingot + (terumetal_ingot * 3)
    coreglass_ingot = diamond + obsidian_shard + (terumetal_ingot * 5)
    teruchalchum_ingot = (bronze_ingot + (tin_ingot * 2) + (terumetal_ingot * 9)) / 3
    teruceramic = clay + (terumetal_ingot * 2)
    teruceramic_block = teruceramic * 9
    thermese = mese + (terumetal_ingot * 4)
    thermese_block = thermese * 9

    terumetal_coil = ((terumetal_ingot * 8) + stick) / 8
    terucopper_coil = ((terucopper_ingot * 8) + stick) / 8
    terugold_coil = ((terugold_ingot * 8) + stick) / 8

    biomatter = leaves
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
    max_heat_upgrade = upgrade_base + ((terusteel_ingot + thermese) * 4)
    crystal_upgrade = upgrade_base + ((diamond_crystal + entropic_crystal) * 4)
    speed_upgrade = upgrade_base + ((diamond_crystal + coreglass_ingot) * 4)
    heat_gen_upgrade = upgrade_base + ((mese_crystal + terugold_coil) * 4)
    heat_trans_upgrade = upgrade_base + ((gold_crystal + terugold_coil) * 4)
    external_in_upgrade = upgrade_base + (terucopper_coil * 7) + chest
    external_out_upgrade = upgrade_base + (terucopper_coil * 7) + chest
    tubelib_upgrade = upgrade_base + tube

    heatline = ((terugold_coil * 3) + (teruceramic * 6)) / 6
    heatline_distributor = thermese_block + (terugold_coil * 4) + (teruceramic * 4)

    thermobox = teruceramic_block + ((thermese + terugold_coil) * 4)
    thermal_distributor = teruceramic_block + ((terumetal_coil + terucopper_coil) * 4)
    heat_reflector = tin_ingot + ((terumetal_ingot + heat_glass) * 4)

    terumetal_frame = copper_block + (terumetal_ingot * 8)
    terusteel_frame = thermese + (terusteel_ingot * 8)
    coreglass_frame = thermobox + (coreglass_ingot * 8)

    furnace_heater = terumetal_frame + furnace + terucopper_block + (terucopper_coil * 4) + (teruceramic * 2)
    alloy_smelter = terumetal_frame + (terumetal_coil * 3) + (bucket * 2) + (furnace * 3)
    crusher = terumetal_frame + (terucopper_coil * 4) + (teruchalchum_ingot * 2) + (expansion_press * 2)
    lava_melter = terumetal_frame + furnace + (terumetal_coil * 3) + (terutin_ingot * 4)

    solar_heater = terusteel_frame + (heat_glass * 3) + (terugold_coil * 4) + water_bucket
    ht_furnace = terusteel_frame + (terucopper_coil * 3) + (teruceramic * 5)
    vulcanizer = terusteel_frame + (terugold_coil * 2) + (thermese * 2) + (teruceramic * 2) + teruceramic_block + crystal_growth_chamber
    mese_garden = terusteel_frame + terucopper_coil + crystal_growth_chamber + (thermese * 2) + (teruceramic * 4)
    reformer = terusteel_frame + bucket + (teruceramic * 3) + (terugold_coil * 4)

    eee_heater = coreglass_frame + heat_glass + (heat_gen_upgrade * 2) + (entropic_crystal * 3) + (teruceramic_block * 2)
    heat_emitter = coreglass_frame + heat_glass + (terugold_coil * 4) + (teruceramic * 2) + heat_unit

    ore_saw = (teruchalchum_ingot * 4) + (terusteel_ingot * 3)
    coreglass_pick = (coreglass_ingot * 3) + (stick * 2)
    terutin_boots = (terutin_ingot * 4)
    terutin_helm = (terutin_ingot * 5)
    terutin_legs = (terutin_ingot * 7)
    terutin_chest = (terutin_ingot * 8)

    bracers = (terumetal_crystal * 5) + (terugold_coil * 4)
    bracer_base_element = steel_block / 2
    antigrav_element = bracer_base_element + flint + (terumetal_ingot * 4)
    antigrav_bracers = bracers + (antigrav_element * 8)

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
    print('coreglass pick      ', cost_of(coreglass_pick, args.markup, args.roundup))
    print('terutin_boots       ', cost_of(terutin_boots, args.markup, args.roundup))
    print('terutin_helm        ', cost_of(terutin_helm, args.markup, args.roundup))
    print('terutin_legs        ', cost_of(terutin_legs, args.markup, args.roundup))
    print('terutin_chest       ', cost_of(terutin_chest, args.markup, args.roundup))
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

    quartz = Components(quartz=1)
    quartz_block = quartz * 1

    print()
    print('99*quartz block     ', cost_of(quartz_block * 99, args.markup, args.roundup))

    wlan_chip = (mese + copper_ingot + gold_ingot + glass) / 8
    chainlink_steel = steel_ingot / 2
    steel_gear = ((steel_ingot * 4) + chainlink_steel) / 6
    oil_extract = leaves * 3
    end_wrench = ((steel_ingot * 2) + tin_ingot) / 4
    steel_bar = steel_ingot / 2
    parafin = oil_extract
    plastic = parafin
    plastic_strip = plastic / 3

    tougher_titanium = titanium * 4
    titanium_tv = (tougher_titanium * 4) + (steel_ingot * 4) + glass
    torch = (coal + stick) / 4
    energy_crystal = (diamond * 2) + (mese_fragment * 2) + torch + gold_ingot

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

    silicon = ((sand * 3) + steel_ingot) / 4
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



def parse_args(argv=None, namespace=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--markup', '-m', type=float, default=1.2)
    parser.add_argument('--roundup', '-r', type=float, default=5)
    return parser.parse_args(argv, namespace)


if __name__ == '__main__':
    main(parse_args())

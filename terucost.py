import argparse
import collections
import math

# cost, in mg, of various raw materials
COSTS = dict(
    stone=1 / 99,
    tree=4 / 99,

    steel_ingot=(21/157)*(2/3),
    gold_ingot=(157/157)*(2/3),
    copper_ingot=(52/157)*(2/3),
    tin_ingot=(71/157)*(2/3),
    terumetal_ingot=(209/157)*(2/3),
    mese=(197/157)*(2/3),
    diamond=(303/157)*(2/3),

    obsidian=2,

    clay=1 / 99,
    flint=16 / 5,
    water=5,
)


def mul(c: collections.Counter, n: int) -> collections.Counter:
    return collections.Counter({
        key: n * val
        for key, val in c.items()
    })


def div(c: collections.Counter, n: int) -> collections.Counter:
    return collections.Counter({
        key: val / n
        for key, val in c.items()
    })


def cost_of(c: collections.Counter, markup:float=1.0, round_up: float=None) -> int:
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
    stone = collections.Counter(stone=1)
    tree = collections.Counter(tree=1)
    planks = div(tree, 4)
    stick = div(planks, 4)
    leaves = div(tree, 8)  # from tubelib grinder
    water = collections.Counter(water=1)
    flint = collections.Counter(flint=1)

    steel_ingot = collections.Counter(steel_ingot=1)
    steel_block = mul(steel_ingot, 9)
    gold_ingot = collections.Counter(gold_ingot=1)
    copper_ingot = collections.Counter(copper_ingot=1)
    copper_block = mul(copper_ingot, 9)
    tin_ingot = collections.Counter(tin_ingot=1)
    terumetal_ingot = collections.Counter(terumetal_ingot=1)
    bronze_ingot = div(mul(copper_ingot, 8) + tin_ingot, 9)
    diamond = collections.Counter(diamond=1)
    diamond_block = mul(diamond, 9)
    mese = collections.Counter(mese=1)

    obsidian = collections.Counter(obsidian=1)
    obsidian_shard = div(obsidian, 9)
    obsidian_grit = obsidian_shard
    obsidian_glass = obsidian_shard

    clay = collections.Counter(clay=1)

    bucket = mul(steel_ingot, 3)
    water_bucket = bucket + water
    furnace = mul(stone, 8)
    tube = div(steel_ingot + tin_ingot + mul(planks, 3), 4)
    chest = mul(planks, 8)

    iron_crystal = steel_ingot
    gold_crystal = gold_ingot
    tin_crystal = tin_ingot
    copper_crystal = copper_ingot
    terumetal_crystal = terumetal_ingot
    obsidian_crystal = obsidian
    diamond_crystal = diamond
    mese_crystal = mese

    terusteel_ingot = steel_ingot + mul(terumetal_ingot, 2)
    terucopper_ingot = copper_ingot + terumetal_ingot
    terucopper_block = mul(terucopper_ingot, 9)
    terutin_ingot = tin_ingot + terumetal_ingot
    terutin_block = mul(terutin_ingot, 9)
    terugold_ingot = gold_ingot + mul(terumetal_ingot, 3)
    coreglass_ingot = diamond + obsidian_shard + mul(terumetal_ingot, 5)
    teruchalchum_ingot = div(bronze_ingot + mul(tin_ingot, 2) + mul(terumetal_ingot, 9), 3)
    teruceramic = clay + mul(terumetal_ingot, 2)
    thermese = mese + mul(terumetal_ingot, 4)

    teruceramic_block = mul(teruceramic, 9)
    thermese_block = mul(thermese, 9)

    terumetal_coil = div(mul(terumetal_ingot, 8) + stick, 8)
    terucopper_coil = div(mul(terucopper_ingot, 8) + stick, 8)
    terugold_coil = div(mul(terugold_ingot, 8) + stick, 8)

    biomatter = leaves
    plant_glue = biomatter + water_bucket
    mulch = div(tree, 4)
    pressed_wood = div(plant_glue + mul(mulch, 8), 16)

    # entropic_crystal = diamond_crystal + mul(mese_crystal, 4) + mul(obsidian_crystal, 4)
    entropic_crystal = diamond_crystal + mul(mese_crystal, 4) + mul(obsidian_grit, 4)
    entropic_matrix = mul(entropic_crystal, 8) + diamond_block
    heat_glass = div(obsidian_glass + mul(tin_crystal, 2) + plant_glue + obsidian_grit, 3)
    heat_unit = obsidian_glass + mul(terugold_ingot, 2) + mese + mul(thermese, 2) + terugold_coil + mul(teruceramic, 2)

    crystal_growth_chamber = water_bucket + mul(teruchalchum_ingot, 2) + mul(obsidian_grit, 3) + mul(obsidian_glass, 3)
    expansion_press = mul(stone, 2) + terutin_block + mul(teruchalchum_ingot, 3) + mul(terutin_ingot, 3)

    upgrade_base = mul(terumetal_coil, 3) + mul(teruceramic, 2) + plant_glue
    max_heat_upgrade = upgrade_base + mul(terusteel_ingot + thermese, 4)
    crystal_upgrade = upgrade_base + mul(diamond_crystal + mese_crystal, 4)
    speed_upgrade = upgrade_base + mul(diamond_crystal + coreglass_ingot, 4)
    heat_gen_upgrade = upgrade_base + mul(mese_crystal + terugold_coil, 4)
    heat_trans_upgrade = upgrade_base + mul(gold_crystal + terugold_coil, 4)
    external_in_upgrade = upgrade_base + mul(terucopper_coil, 7) + chest
    external_out_upgrade = upgrade_base + mul(terucopper_coil, 7) + chest
    tubelib_upgrade = upgrade_base + tube

    heatline = div(mul(terugold_coil, 3) + mul(teruceramic, 6), 6)
    heatline_distributor = thermese_block + mul(terugold_coil, 4) + mul(teruceramic, 4)

    thermobox = teruceramic_block + mul(thermese + terugold_coil, 4)
    distributor = teruceramic_block + mul(terumetal_coil + terucopper_coil, 4)
    heat_reflector = tin_ingot + mul(terumetal_ingot + heat_glass, 4)

    terumetal_frame = copper_block + mul(terumetal_ingot, 8)
    terusteel_frame = thermese + mul(terusteel_ingot, 8)
    coreglass_frame = thermobox + mul(coreglass_ingot, 8)

    furnace_heater = terumetal_frame + furnace + terucopper_block + mul(terucopper_coil, 4) + mul(teruceramic, 2)
    alloy_smelter = terumetal_frame + mul(terumetal_coil, 3) + mul(bucket, 2) + mul(furnace, 3)
    crusher = terumetal_frame + mul(terucopper_coil, 4) + mul(teruchalchum_ingot, 2) + mul(expansion_press, 2)
    lava_melter = terumetal_frame + furnace + mul(terumetal_coil, 3) + mul(terutin_ingot, 4)

    solar_heater = terusteel_frame + mul(heat_glass, 3) + mul(terugold_coil, 4) + water_bucket
    ht_furnace = terusteel_frame + mul(terucopper_coil, 3) + mul(teruceramic, 5)
    vulcanizer = terusteel_frame + mul(terugold_coil, 2) + mul(thermese, 2) + mul(teruceramic, 2) + teruceramic_block + crystal_growth_chamber
    mese_garden = terusteel_frame + terucopper_coil + crystal_growth_chamber + mul(thermese, 2) + mul(teruceramic, 4)
    reformer = terusteel_frame + bucket + mul(teruceramic, 3) + mul(terugold_coil, 4)

    eee_heater = coreglass_frame + heat_glass + mul(heat_gen_upgrade, 2) + mul(entropic_crystal, 3) + mul(teruceramic_block, 2)
    heat_emitter = coreglass_frame + heat_glass + mul(terugold_coil, 4) + mul(teruceramic, 2) + heat_unit

    ore_saw = mul(teruchalchum_ingot, 4) + mul(terusteel_ingot, 3)
    coreglass_pick = mul(coreglass_ingot, 3) + mul(stick, 2)
    terutin_boots = mul(terutin_ingot, 4)
    terutin_helm = mul(terutin_ingot, 5)
    terutin_legs = mul(terutin_ingot, 7)
    terutin_chest = mul(terutin_ingot, 8)

    bracers = mul(terumetal_crystal, 5) + mul(terugold_coil, 4)
    bracer_base_element = div(steel_block, 2)
    antigrav_element = bracer_base_element + flint + mul(terumetal_ingot, 4)
    antigrav_bracers = bracers + mul(antigrav_element, 8)

    print("alloy smelter       ", cost_of(alloy_smelter, args.markup, args.roundup))
    print("ht furnace          ", cost_of(ht_furnace, args.markup, args.roundup))
    print("vulcanizer          ", cost_of(vulcanizer, args.markup, args.roundup))
    print("solar heater        ", cost_of(solar_heater, args.markup, args.roundup))
    print("thermobox           ", cost_of(thermobox, args.markup, args.roundup))
    print("distributor         ", cost_of(distributor, args.markup, args.roundup))
    print("max_heat_upgrade    ", cost_of(max_heat_upgrade, args.markup, args.roundup))
    print("crystal_upgrade     ", cost_of(crystal_upgrade, args.markup, args.roundup))
    print("speed_upgrade       ", cost_of(speed_upgrade, args.markup, args.roundup))
    print("heat_gen_upgrade    ", cost_of(heat_gen_upgrade, args.markup, args.roundup))
    print("heat_trans_upgrade  ", cost_of(heat_trans_upgrade, args.markup, args.roundup))
    print("external_in_upgrade ", cost_of(external_in_upgrade, args.markup, args.roundup))
    print("external_out_upgrade", cost_of(external_out_upgrade, args.markup, args.roundup))

    print('eee heater          ', cost_of(eee_heater, args.markup, args.roundup))
    print('heat emitter        ', cost_of(heat_emitter, args.markup, args.roundup))
    print('ore saw             ', cost_of(ore_saw, args.markup, args.roundup))
    print('coreglass pick      ', cost_of(coreglass_pick, args.markup, args.roundup))
    print('terutin_boots       ', cost_of(terutin_boots, args.markup, args.roundup))
    print('terutin_helm        ', cost_of(terutin_helm, args.markup, args.roundup))
    print('terutin_legs        ', cost_of(terutin_legs, args.markup, args.roundup))
    print('terutin_chest       ', cost_of(terutin_chest, args.markup, args.roundup))
    print('antigrav_bracers    ', cost_of(antigrav_bracers, args.markup, args.roundup))


def parse_args(argv=None, namespace=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--markup', '-m', type=float, default=3)
    parser.add_argument('--roundup', '-r', type=float, default=5)
    return parser.parse_args(argv, namespace)


if __name__ == '__main__':
    main(parse_args())

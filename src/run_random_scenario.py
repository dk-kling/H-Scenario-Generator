#!/usr/bin/env python3
from config import set_carla_api_path, start_server
set_carla_api_path()

import atexit
import time
from collections import deque

import executor
from config import Config, set_args, init, exit_handler
from seed import Seed
from states import State
from fuzz_utils import TestScenario


def main():
    conf = Config()
    arg_parser = set_args()
    args = arg_parser.parse_args()
    init(conf, args)
    atexit.register(exit_handler, [conf.sim_port])
    process = start_server(conf.sim_port, None)
    client, tm, world = executor.connect(conf)

    seed = Seed(deque(conf.enqueue_seed_scenarios()))
    seed.set_rgraph(client, conf)
    seed.rgraph_generate_scenario(conf)
    scenario = seed.pop()

    conf.cur_scenario = scenario
    test_scenario = TestScenario(conf)

    world = executor.switch_map(conf, test_scenario.town, client, world, seed)
    time.sleep(3)
    state = State()
    state.set_world(world)
    state.campaign_cnt = 0
    state.cycle_cnt = 0
    state.mutation = 0

    from object_generator import ObjectGenerator
    object_generator = ObjectGenerator(world, seed, test_scenario)
    for i in range(20):
        object_generator.add_static()
    for i in range(20):
        object_generator.add_linear_pedestrian()
    test_scenario = object_generator.update_pedestrians()

    ret = test_scenario.run_test(state, client, tm, world)

    score_list = []
    if ret is None:
        # failure
        pass

    elif ret == -1:
        print("Spawn / simulation failure")

    elif ret == 1:
        print("Found an error")
        # found an error - move on to next one in queue
        # test.quota = 0
        return True

    elif ret == 128:
        print("Exit by user request")
        exit(0)

    else:
        if ret == -1:
            print("[-] Fatal error occurred during test")
            exit(-1)

    score_list.append(test_scenario.driving_quality_score)


if __name__ == "__main__":
    main()

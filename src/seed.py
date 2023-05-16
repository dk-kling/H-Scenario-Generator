import random
import math
import os
import json

import executor
from config import Bcolors
from ScenaVRo.HDMap2RoadGraph.road_graph import RoadGraph


class Seed:
    def __init__(self, queue):
        self.seed_dict = dict()
        self.queue = queue
        self.scene_id = 0
        self.campaign_cnt = 0
        self.road_graph = None
        self.town_map = None
        self.way = list()

    def new_campaign(self):
        self.scene_id += 1
        self.campaign_cnt += 1
        print(f"{Bcolors.GREEN}\n{'=' * 10} Start Fuzzing Campaign #{self.campaign_cnt} {'=' * 10}{Bcolors.ENDC}")
        return self.campaign_cnt

    def pop(self):
        return self.queue.popleft()

    def set_seed_dict(self, town_map, sp, dp):
        self.seed_dict = {
            "map": town_map,
            "sp_x": sp.location.x,
            "sp_y": sp.location.y,
            "sp_z": sp.location.z,
            "pitch": sp.rotation.pitch,
            "yaw": sp.rotation.yaw,
            "roll": sp.rotation.roll,
            "wp_x": dp.location.x,
            "wp_y": dp.location.y,
            "wp_z": dp.location.z,
            "wp_yaw": dp.rotation.yaw
        }

    def set_rgraph(self, client, conf):
        if conf.user_defined_map is not None:
            self.town_map = conf.user_defined_map
            self.road_graph = RoadGraph(client, self.town_map, True)
        elif conf.town is not None:
            self.town_map = "Town0{}".format(conf.town)
            self.road_graph = RoadGraph(client, self.town_map)
        else:
            self.town_map = "Town0{}".format(random.randint(1, 5))
            self.road_graph = RoadGraph(client, self.town_map)

    def rgraph_generate_scenario(self, conf):
        sp, dp, self.way = self.road_graph.get_lane_route()
        self.set_seed_dict(self.town_map, sp, dp)

        scene_name = "scene-created{}.json".format(self.scene_id)
        with open(os.path.join(conf.seed_dir, scene_name), "w") as fp:
            json.dump(self.seed_dict, fp)
        self.queue.append(scene_name)

    def random_generate_scenario(self, conf):
        if conf.town is not None:
            town_map = "Town0{}".format(conf.town)
        else:
            town_map = "Town0{}".format(random.randint(1, 2))

        client, tm = executor.connect(conf)

        client.set_timeout(600)
        client.load_world(town_map)
        world = client.get_world()
        town = world.get_map()
        spawn_points = town.get_spawn_points()
        sp = random.choice(spawn_points)
        sp_x = sp.location.x
        sp_y = sp.location.y

        wp = random.choice(spawn_points)
        wp_x = wp.location.x
        wp_y = wp.location.y

        # restrict destinition to be within 200 meters
        while math.sqrt((sp_x - wp_x) ** 2 + (sp_y - wp_y) ** 2) > 100:
            wp = random.choice(spawn_points)
            wp_x = wp.location.x
            wp_y = wp.location.y

        self.set_seed_dict(town_map, sp, wp)

        scene_name = "scene-created{}.json".format(self.scene_id)
        with open(os.path.join(conf.seed_dir, scene_name), "w") as fp:
            json.dump(self.seed_dict, fp)
        self.queue.append(scene_name)

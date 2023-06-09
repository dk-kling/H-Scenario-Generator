import random
import constants as c


class ObjectGenerator:
    def __init__(self, world, seed, test_scenario):
        self.world = world
        self.map = world.get_map()
        self.static_lib = self.world.get_blueprint_library().filter("static.*")
        self.vehicle_lib = self.world.get_blueprint_library().filter("vehicle.*")
        self.walker_lib = self.world.get_blueprint_library().filter("walker.*")

        self.road_graph = seed.road_graph
        self.scenario_area = seed.scenario_area
        self.way = seed.way

        self.statics = list()
        self.vehicles = list()
        self.pedestrians = list()

        self.test_scenario = test_scenario

    def update_statics(self):
        for obj in self.statics:
            self.world.try_spawn_actor(obj["blueprint"], obj["transform"])

    def add_static(self):
        bp = random.choice(self.static_lib)
        spawn_point = self.scenario_area.get_static_location()
        obj_actor = None

        while obj_actor is None:
            obj_actor = self.world.try_spawn_actor(bp, spawn_point)

        self.statics.append({"actor": obj_actor, "blueprint": bp, "transform": spawn_point})
        print("Spawned Static Object Completely:", bp, spawn_point)

    def add_linear_pedestrian(self):
        bp = random.choice(self.walker_lib)
        spawn_point = self.scenario_area.get_npc_dynamic_linear_way()
        ped_actor = None
        speed = random.uniform(0, c.WALKER_MAX_SPEED)

        self.pedestrians.append({"actor": ped_actor, "blueprint": bp, "transform": spawn_point, "speed": speed})

    def update_pedestrians(self):
        for ped in self.pedestrians:
            # loc = (ped["transform"].location.x, ped["transform"].location.y, ped["transform"].location.z)
            # rot = (ped["transform"].rotation.pitch, ped["transform"].rotation.yaw, ped["transform"].rotation.roll)
            self.test_scenario.direct_add_actor(
                c.WALKER,
                c.LINEAR,
                ped["transform"],
                None,
                ped["speed"],
                ped["blueprint"]
            )
        return self.test_scenario

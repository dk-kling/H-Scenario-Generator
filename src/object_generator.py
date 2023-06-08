import random
import carla


class ObjectGenerator:
    def __init__(self, world, seed):
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

    def add_static(self):
        bp = random.choice(self.static_lib)
        spawn_point = self.scenario_area.get_static_location()
        obj_actor = None

        while obj_actor is None:
            obj_actor = self.world.try_spawn_actor(bp, spawn_point)

        self.statics.append({"actor": obj_actor, "blueprint": bp, "transform": spawn_point})
        print("Spawned Static Object Completely:", bp, spawn_point)


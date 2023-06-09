import random
import numpy
import math
import time


class EmptyObject:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        return str(self.__dict__)


class ScenarioArea:
    def __init__(self, road_graph):
        self.road_graph = road_graph
        sp, dp, ego_ways, main_junc = road_graph.get_lane_route()
        prev_ways, next_ways, adj_ways = self.road_graph.get_all_ways(main_junc)

        self.sp = sp
        self.dp = dp
        self.main_junc = main_junc
        self.ego_st = {"road_id": ego_ways[0], "lane_id": ego_ways[3]}
        self.ego_ed = {"road_id": ego_ways[1], "lane_id": ego_ways[4]}
        self.ego_md = {"road_id": ego_ways[2], "lane_id": ego_ways[5]}
        self.ego_ways = [self.ego_st, self.ego_md, self.ego_ed]
        self.prev_ways = prev_ways
        self.next_ways = next_ways
        self.adj_ways = adj_ways

        if self.ego_st in self.prev_ways:
            self.prev_ways.remove(self.ego_st)
        if self.ego_st in self.adj_ways:
            self.adj_ways.remove(self.ego_st)
        if self.ego_md in self.adj_ways:
            self.adj_ways.remove(self.ego_md)
        if self.ego_ed in self.adj_ways:
            self.adj_ways.remove(self.ego_ed)

    def get_sp(self):
        return self.sp

    def get_dp(self):
        return self.dp

    def get_npc_vehicle_way(self):
        sw = get_random_value(self.prev_ways)
        if sw in self.prev_ways:
            self.prev_ways.remove(sw)
        dw = get_random_value(self.next_ways)

        sp = self.road_graph.carla_map.get_waypoint_xodr(
            int(sw["road_id"]),
            int(sw["lane_id"]),
            self.road_graph.road_dict[sw["road_id"]].length * random.random()
        ).transform

        dp = self.road_graph.carla_map.get_waypoint_xodr(
            int(dw["road_id"]),
            int(dw["lane_id"]),
            self.road_graph.road_dict[dw["road_id"]].length * random.random()
        ).transform

        return sp, dp

    def get_npc_dynamic_linear_way(self):
        overlap_w = random.choice([self.ego_st, self.ego_ed])

        # try:
        length = self.road_graph.road_dict[overlap_w["road_id"]].length
        available = list(self.road_graph.road_dict[overlap_w["road_id"]].child.keys())

        # except KeyError:
        #     length = self.main_junc.find_road(overlap_w["road_id"]).length
        #     available = list(self.main_junc.find_road(overlap_w["road_id"]).child.keys())

        overlap_p = self.road_graph.carla_map.get_waypoint_xodr(
            int(overlap_w["road_id"]),
            int(overlap_w["lane_id"]),
            length * random.random()
        ).transform

        if overlap_w["lane_id"] in available:
            available.remove(overlap_w["lane_id"])

        sp = self.road_graph.carla_map.get_waypoint_xodr(
            int(overlap_w["road_id"]),
            int(random.choice(available)),
            length * random.random()
        ).transform

        radian_yaw = math.atan2(overlap_p.location.x - sp.location.x, overlap_p.location.y - sp.location.y)
        yaw = math.degrees(radian_yaw)
        sp.rotation.yaw = yaw
        sp.location.z += 2
        return sp

    def get_static_location(self):
        adj_w = get_random_value(self.adj_ways)

        adj_p = self.road_graph.carla_map.get_waypoint_xodr(
            int(adj_w["road_id"]),
            int(adj_w["lane_id"]),
            self.road_graph.road_dict[adj_w["road_id"]].length * random.random()
        ).transform

        return adj_p


def get_random_key(_dict):
    import random
    return random.choice(list(_dict.keys()))


def get_random_value(_list):
    import random
    return random.choice(_list)


class RoadGraph:

    def __init__(self, client, hd_map_name, user_defined=False):

        self.correct_spawn_locations_after_run = False
        self.lane_cov_list = []

        if user_defined is False:
            client.load_world(hd_map_name)
            time.sleep(3)
            world = client.get_world()
            self.carla_map = world.get_map()
            xodr = self.carla_map.to_opendrive()
            self.town_name = hd_map_name

        else:
            hd_map = open("ScenaVRo/HDMap2RoadGraph/HD-Map/" + hd_map_name, 'r')
            hd_map_str = hd_map.read()
            self.town_name = user_defined
            xodr = hd_map_str
            hd_map.close()
            client.generate_opendrive_world(xodr)
            time.sleep(3)
            world = client.get_world()
            self.carla_map = world.get_map()

        # Generate road graph
        self.map_str, self.road_dict, self.junction_dict = self.gen_obj(xodr)

        # while True:
        #     print("-")
        #     time.sleep(10)

    def gen_obj(self, hd_map_str):
        import xml.etree.ElementTree as ET

        sim_map_tree = ET.fromstring(hd_map_str)
        road_dict = dict()
        junction_dict = dict()

        # Junction
        for junction in sim_map_tree.findall("junction"):
            connection_list = list()
            for connection in junction.findall("connection"):
                for lane_link in connection.findall("laneLink"):
                    connection_list.append(self.Connection())
                    if connection.get("incomingRoad") is not None:
                        connection_list[-1].prev_road = connection.get("incomingRoad")
                        connection_list[-1].prev_lane = lane_link.get("from")
                    if connection.get("connectingRoad") is not None:
                        connection_list[-1].next_road = connection.get("connectingRoad")
                        connection_list[-1].next_lane = lane_link.get("to")

            junction_dict[junction.get("id")] = self.Junction(junction.get("id"), dict(), connection_list)

        # Simple Road
        for road in sim_map_tree.findall("road"):
            lane_dict = dict()
            if road.get("junction") == "-1":
                for lanes in road.findall("lanes"):
                    for lane_section in lanes.findall("laneSection"):

                        if lane_section.find("left") is not None:
                            for lane in lane_section.find("left").findall("lane"):
                                lane_dict[lane.get("id")] = self.Lane(lane.get("id"), lane.get("type"), road.get("id"))

                        if lane_section.find("right") is not None:
                            for lane in lane_section.find("right").findall("lane"):
                                lane_dict[lane.get("id")] = self.Lane(lane.get("id"), lane.get("type"), road.get("id"))

                road_dict[road.get("id")] = self.Road(road.get("id"),
                                                      float(road.get("length")),
                                                      lane_dict)

                if road.find("link") is not None:
                    link = road.find("link")
                    if link.find("predecessor") is not None:
                        road_dict[road.get("id")].set_prev(link.find("predecessor").get("elementType"),
                                                           link.find("predecessor").get("elementId"))

                    if link.find("successor") is not None:
                        road_dict[road.get("id")].set_next(link.find("successor").get("elementType"),
                                                           link.find("successor").get("elementId"))

            # Road in Junction
            else:
                for lanes in road.findall("lanes"):
                    for lane_section in lanes.findall("laneSection"):

                        if lane_section.find("left") is not None:
                            for lane in lane_section.find("left").findall("lane"):

                                if lane.find("link") is not None:
                                    link = lane.find("link")
                                    lane_dict[lane.get("id")] = self.JunctionLane(lane.get("id"),
                                                                                  lane.get("type"),
                                                                                  road.get("id"))
                                    if link.find("predecessor") is not None:
                                        lane_dict[lane.get("id")].set_prev(link.find("predecessor").get("id"))

                                    if link.find("successor") is not None:
                                        lane_dict[lane.get("id")].set_next(link.find("successor").get("id"))

                        if lane_section.find("right") is not None:
                            for lane in lane_section.find("right").findall("lane"):

                                if lane.find("link") is not None:
                                    link = lane.find("link")
                                    lane_dict[lane.get("id")] = self.JunctionLane(lane.get("id"),
                                                                                  lane.get("type"),
                                                                                  road.get("id"))
                                    if link.find("predecessor") is not None:
                                        lane_dict[lane.get("id")].set_prev(link.find("predecessor").get("id"))

                                    if link.find("successor") is not None:
                                        lane_dict[lane.get("id")].set_next(link.find("successor").get("id"))

                junction_dict[road.get("junction")].child[road.get("id")] = self.JunctionRoad(road.get("id"),
                                                                                              float(road.get("length")),
                                                                                              road.get("junction"),
                                                                                              lane_dict)

                if road.find("link") is not None:
                    link = road.find("link")
                    if link.find("predecessor") is not None:
                        pred = link.find("predecessor")
                        try:
                            road_dict[road.get("id")].set_prev(pred.get("elementType"), pred.get("elementId"))
                        except KeyError:
                            junction_dict[road.get("junction")].child[road.get("id")].set_prev(pred.get("elementType"),
                                                                                               pred.get("elementId"))

                    if link.find("successor") is not None:
                        succ = link.find("successor")
                        try:
                            road_dict[road.get("id")].set_next(succ.get("elementType"), succ.get("elementId"))
                        except KeyError:
                            junction_dict[road.get("junction")].child[road.get("id")].set_next(succ.get("elementType"),
                                                                                               succ.get("elementId"))

        return hd_map_str, road_dict, junction_dict

    def get_junction(self, junction_id):
        return self.junction_dict.get(junction_id)

    def get_road(self, road_id):
        return self.road_dict.get(road_id)

    def get_junctions(self):
        return self.junction_dict

    def get_roads(self):
        return self.road_dict

    def select_random_junction_id(self):
        return get_random_key(self.junction_dict)

    def select_random_road_id(self):
        return get_random_key(self.road_dict)

    def get_lane_route(self):
        while True:
            d_road_id = self.select_random_road_id()
            d_road = self.road_dict[d_road_id]
            random_access = get_random_value([True, False])
            if random_access:
                d_junc_id = d_road.prev_id
                m_junc_id = d_road.next_id
            else:
                d_junc_id = d_road.next_id
                m_junc_id = d_road.prev_id

            try:
                m_junc = self.junction_dict[m_junc_id]
                d_junc = self.junction_dict[d_junc_id]
            except KeyError:
                continue

            d_lane_id = d_junc.find_prev_lane(d_road_id)

            if d_lane_id is None:
                continue
            if d_road.child[d_lane_id].type != "driving":
                continue

            elif int(d_lane_id) > 0:
                dp_loc = self.road_dict[d_road_id].length * 0.1
            else:
                dp_loc = self.road_dict[d_road_id].length * 0.9

            while True:
                conn = m_junc.select_random_connection()
                if conn.prev_road == d_road_id:
                    continue
                if self.road_dict[conn.prev_road].child[conn.prev_lane].type != "driving":
                    continue
                if int(conn.prev_lane) > 0:
                    sp_loc = self.road_dict[conn.prev_road].length * 0.9
                    break
                else:
                    sp_loc = self.road_dict[conn.prev_road].length * 0.1
                    break

            sp = self.carla_map.get_waypoint_xodr(int(conn.prev_road), int(conn.prev_lane), sp_loc).transform
            dp = self.carla_map.get_waypoint_xodr(int(d_road_id), int(d_lane_id), dp_loc).transform
            break
        return sp, dp, [conn.prev_road, d_road_id, conn.next_road, conn.prev_lane, d_lane_id, conn.next_lane], m_junc

    def get_all_ways(self, junc):
        connected_roads, prev_ways = junc.get_all_prev_ways()
        all_ways = list()
        adj_ways = list()
        for road_id in connected_roads:
            road = self.get_road(road_id)
            lanes = road.child.values()
            for lane in lanes:
                adj_ways.append({"road_id": lane.parent, "lane_id": lane.id})
                if lane.type == "driving":
                    all_ways.append({"road_id": lane.parent, "lane_id": lane.id})
        next_ways = [way for way in all_ways if way not in prev_ways]
        return prev_ways, next_ways, adj_ways

    class Junction:
        def __init__(self, j_id, child_road_dict, conn_list):
            self.id = j_id
            self.child = child_road_dict
            self.connection = conn_list

        def find_road(self, road_id):
            return self.child[road_id]

        def find_prev_lane(self, road_id):
            for conn in self.connection:
                if conn.prev_road == road_id:
                    return conn.prev_lane
            return None

        def select_random_connection(self):
            return get_random_value(self.connection)

        def get_all_prev_ways(self):
            prev_ways = list()
            connected_roads = list()
            for c in self.connection:
                prev_ways.append({"road_id": c.prev_road, "lane_id": c.prev_lane})
                if c.prev_road not in connected_roads:
                    connected_roads.append(c.prev_road)
            return connected_roads, prev_ways

    class Connection:
        def __init__(self):
            self.prev_road = None
            self.prev_lane = None
            self.next_road = None
            self.next_lane = None

    class Road:
        def __init__(self, r_id, length, lane_dict, prev_type=None, prev_id=None, next_type=None, next_id=None):
            self.id = r_id
            self.length = length
            self.child = lane_dict
            self.prev_type = prev_type
            self.prev_id = prev_id
            self.next_type = next_type
            self.next_id = next_id

        def set_prev(self, _type, _id):
            self.prev_type = _type
            self.prev_id = _id

        def set_next(self, _type, _id):
            self.next_type = _type
            self.next_id = _id

    class JunctionRoad:
        def __init__(self, r_id, length, junction_id, lane_dict, prev_type=None, prev_id=None, next_type=None,
                     next_id=None):
            self.id = r_id
            self.length = length
            self.parent = junction_id
            self.child = lane_dict
            self.prev_type = prev_type
            self.prev_id = prev_id
            self.next_type = next_type
            self.next_id = next_id

        def set_prev(self, _type, _id):
            self.prev_type = _type
            self.prev_id = _id

        def set_next(self, _type, _id):
            self.next_type = _type
            self.next_id = _id

    class Lane:
        def __init__(self, l_id, l_type, road_id):
            self.id = l_id
            self.type = l_type
            self.parent = road_id

    class JunctionLane:
        def __init__(self, l_id, l_type, road_id, prev_lane_id=None, next_lane_id=None):
            self.id = l_id
            self.type = l_type
            self.parent = road_id
            self.prev = prev_lane_id
            self.next = next_lane_id

        def set_prev(self, prev_id):
            self.prev = prev_id

        def set_next(self, next_id):
            self.next = next_id

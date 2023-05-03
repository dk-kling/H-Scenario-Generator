import glob
import argparse
import os
import sys
import time
import random
import shlex
import socket
import subprocess
from datetime import datetime

import constants as c


def get_proj_root():
    config_path = os.path.abspath(__file__)
    src_dir = os.path.dirname(config_path)
    proj_root = os.path.dirname(src_dir)

    return proj_root


def set_carla_api_path():
    proj_root = get_proj_root()

    dist_path = os.path.join(proj_root, "carla/PythonAPI/carla/dist")
    glob_path = os.path.join(dist_path, "carla-*%d.%d-%s.egg" % (
        sys.version_info.major,
        sys.version_info.minor,
        "win-amd64" if os.name == "nt" else "linux-x86_64"
    ))

    try:
        api_path = glob.glob(glob_path)[0]
    except IndexError:
        print("Couldn't set Carla API path.")
        exit(-1)

    if api_path not in sys.path:
        sys.path.append(api_path)
        print(f"API: {api_path}")


def handler(signum, frame):
    raise Exception("HANG")


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", int(port))) == 0


def start_server(port, prev_process):
    cmd_list = shlex.split(
        "sh " + "./run_carla_display_10.1.sh"
    )
    while is_port_in_use(int(port)):
        try:
            if prev_process is not None:
                prev_process.terminate()
                while prev_process.poll() is None:
                    time.sleep(0.1)
                print(f"{Bcolors.WARNING}[*] previous process kill server at port {port}{Bcolors.ENDC}")
                subprocess.run(['fuser', '-k', str(port) + '/tcp'])
                print(f"{Bcolors.FAIL}\n[-] previous process kill server at port {port}{Bcolors.ENDC}")
                time.sleep(2)
            else:
                subprocess.run(['fuser', '-k', str(port) + '/tcp'])
                print(f"{Bcolors.FAIL}\n[-] kill server at port {port}{Bcolors.ENDC}")
                time.sleep(2)
        except:
            import traceback
            traceback.print_exc()
            continue

    process = subprocess.Popen(cmd_list)
    print(f"{Bcolors.BLUE}[+] start server at port {port}{Bcolors.ENDC}")
    time.sleep(3)
    return process


def exit_handler(ports):
    for port in ports:
        while is_port_in_use(port):
            try:
                subprocess.run("kill -9 $(lsof -t -i :" + str(port) + ")", shell=True)
            except:
                continue


def set_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-o", "--out-dir", default="out-artifact", type=str,
                            help="Directory to save fuzzing logs")
    arg_parser.add_argument("-s", "--seed-dir", default="seed", type=str,
                            help="Seed directory")
    arg_parser.add_argument("-c", "--max-cycles", default=10, type=int,
                            help="Maximum number of loops")
    arg_parser.add_argument("-m", "--max-mutations", default=8, type=int,
                            help="Size of the mutated population per cycle")
    arg_parser.add_argument("-d", "--determ-seed", type=float,
                            help="Set seed num for deterministic mutation (e.g., for replaying)")
    arg_parser.add_argument("-v", "--verbose", action="store_true",
                            default=False, help="enable debug mode")
    arg_parser.add_argument("-u", "--sim-host", default="localhost", type=str,
                            help="Hostname of Carla simulation server")
    arg_parser.add_argument("-p", "--sim-port", default=2000, type=int,
                            help="RPC port of Carla simulation server")
    arg_parser.add_argument("-t", "--target", default="behavior", type=str,
                            help="Target autonomous driving system (basic/behavior)")
    arg_parser.add_argument("-f", "--function", default="general", type=str,
                            choices=["general", "collision", "traction", "eval-os", "eval-us",
                                     "figure", "sens1", "sens2", "lat", "rear"],
                            help="Functionality to test (general / collision / traction)")
    arg_parser.add_argument("--strategy", default="all", type=str,
                            help="Input mutation strategy (all / congestion / entropy / instability / trajectory)")
    arg_parser.add_argument("--town", default=None, type=int,
                            help="Test on a specific town (e.g., '--town 3' forces Town03)")
    arg_parser.add_argument("-x", "--user-defined-map", default=None, type=str,
                            help="User defined xodr map name in directory, 'src/ScenaVRo/HDMap2RoadGraph/HD-Map'")
    arg_parser.add_argument("--timeout", default="20", type=int,
                            help="Seconds to timeout if vehicle is not moving")
    arg_parser.add_argument("--no-speed-check", action="store_true")
    arg_parser.add_argument("--no-lane-check", action="store_true")
    arg_parser.add_argument("--no-crash-check", action="store_true")
    arg_parser.add_argument("--no-stuck-check", action="store_true")
    arg_parser.add_argument("--no-red-check", action="store_true")
    arg_parser.add_argument("--no-other-check", action="store_true")

    return arg_parser


def init(conf, args):
    """
    Set
    :param conf: fuzzing configuration
    :param args: arguments
    :return: void
    """

    """
    Set Random Seed
    """
    conf.cur_time = time.time()
    if args.determ_seed:
        conf.determ_seed = args.determ_seed
    else:
        conf.determ_seed = conf.cur_time
    random.seed(conf.determ_seed)
    print(f"{Bcolors.WARNING}[info] determ seed set to: {conf.determ_seed}{Bcolors.ENDC}")

    """
    Make Directory for output files
    """
    now = datetime.now()
    time_str = now.strftime("%Y_%m_%d_%H_%M_%S")
    conf.out_dir = args.out_dir + "/" + time_str

    try:
        os.mkdir(conf.out_dir)
    except Exception as e:
        estr = f"{Bcolors.WARNING}Output directory {conf.out_dir} already exists. Remove with " \
               f"caution; it might contain data from previous runs.{Bcolors.ENDC}"
        print(estr)
        sys.exit(-1)

    """
    Make Directory for Seed Scenario
    """
    seed_dir = conf.out_dir + "/" + args.seed_dir
    args.seed_dir = seed_dir
    conf.seed_dir = args.seed_dir
    try:
        os.mkdir(seed_dir)
    except Exception as e:
        estr = f"{Bcolors.WARNING}Seed directory {args.seed_dir} already exists. Remove with " \
               f"caution; it might contain data from previous runs.{Bcolors.ENDC}"
        print(estr)
        sys.exit(-1)

    if args.verbose:
        conf.debug = True
    else:
        conf.debug = False

    conf.set_paths()

    with open(conf.meta_file, "w") as f:
        f.write(" ".join(sys.argv) + "\n")
        f.write("start: " + str(int(conf.cur_time)) + "\n")

    try:
        os.mkdir(conf.queue_dir)
        os.mkdir(conf.error_dir)
        os.mkdir(conf.cov_dir)
        os.mkdir(conf.rosbag_dir)
        os.mkdir(conf.cam_dir)
        os.mkdir(conf.score_dir)
        os.mkdir(conf.color_feedback_dir)
        os.mkdir(conf.measure_dir)
    except Exception as e:
        print(e)
        sys.exit(-1)

    """
    Set conf using args
    """

    conf.sim_host = args.sim_host
    conf.sim_port = args.sim_port

    conf.max_cycles = args.max_cycles
    conf.max_mutations = args.max_mutations

    conf.timeout = args.timeout

    conf.function = args.function

    if args.target.lower() == "basic":
        conf.agent_type = c.BASIC
    elif args.target.lower() == "behavior":
        conf.agent_type = c.BEHAVIOR
    else:
        print(f"{Bcolors.FAIL}[-] Unknown target: {args.target}{Bcolors.ENDC}")
        sys.exit(-1)

    conf.town = args.town
    conf.user_defined_map = args.user_defined_map

    if args.no_speed_check:
        conf.check_dict["speed"] = False
    if args.no_crash_check:
        conf.check_dict["crash"] = False
    if args.no_lane_check:
        conf.check_dict["lane"] = False
    if args.no_stuck_check:
        conf.check_dict["stuck"] = False
    if args.no_red_check:
        conf.check_dict["red"] = False
    if args.no_other_check:
        conf.check_dict["other"] = False

    if args.strategy == "all":
        conf.strategy = c.ALL
    elif args.strategy == "congestion":
        conf.strategy = c.CONGESTION
    elif args.strategy == "entropy":
        conf.strategy = c.ENTROPY
    elif args.strategy == "instability":
        conf.strategy = c.INSTABILITY
    elif args.strategy == "trajectory":
        conf.strategy = c.TRAJECTORY
    else:
        print(f"{Bcolors.FAIL}[-] Please specify a strategy{Bcolors.ENDC}")
        exit(-1)


class Config:
    """
    A class defining fuzzing configuration and helper methods.
    An instance of this class should be created by the main module (fuzzer.py)
    and then be shared across other modules as a context handler.
    """

    def __init__(self):
        self.debug = False

        # simulator config
        self.sim_host = "localhost"
        self.sim_port = 2000
        self.sim_tm_port = 8000

        # Fuzzer config
        self.max_cycles = 0
        self.max_mutation = 0
        self.num_dry_runs = 1
        self.num_param_mutations = 1
        # self.initial_quota = 10

        # Fuzzing metadata
        self.cur_time = None
        self.determ_seed = 13
        self.out_dir = None
        self.seed_dir = None

        # Target config
        self.agent_type = c.BEHAVIOR

        # Enable/disable Various Checks
        self.check_dict = {
            "speed": True,
            "lane": False,
            "crash": True,
            "stuck": True,
            "red": False,
            "other": True,
        }

        # Functional testing
        self.function = "general"

        # Sim-debug settings
        self.view = c.BIRDSEYE

    def set_paths(self):
        self.queue_dir = os.path.join(self.out_dir, "queue")
        self.error_dir = os.path.join(self.out_dir, "errors")
        self.cov_dir = os.path.join(self.out_dir, "cov")
        self.meta_file = os.path.join(self.out_dir, "meta")
        self.cam_dir = os.path.join(self.out_dir, "camera")
        self.rosbag_dir = os.path.join(self.out_dir, "rosbags")
        self.score_dir = os.path.join(self.out_dir, "scores")
        self.color_feedback_dir = os.path.join(self.out_dir, "color_feedback")
        self.measure_dir = os.path.join(self.out_dir, "measurements")

    def enqueue_seed_scenarios(self):
        try:
            seed_scenarios = os.listdir(self.seed_dir)
        except:
            print(f"{Bcolors.FAIL}[-] Error - cannot find seed directory ({self.seed_dir}){Bcolors.ENDC}")
            sys.exit(-1)

        queue = [seed for seed in seed_scenarios if not seed.startswith(".")
                 and seed.endswith(".json")]

        return queue


class Bcolors:
    VIOLET = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
import carla

EGO_SCENARIO = {
    "map": "Town01",
    "sp_x": 86.0,
    "sp_y": 145.0,
    "sp_z": 0.29999998211860657,
    "pitch": 0.0,
    "yaw": 90.0,
    "roll": 0.0,
    "wp_x": 182.91,
    "wp_y": 198.76,
    "wp_z": 0.29999998211860657,
    "wp_yaw": 179.999755859375
}

CARLA_WEATHER = carla.WeatherParameters(
    # 구름의 양 [0-100]
    cloudiness=carla.WeatherParameters.ClearNoon.cloudiness,
    # 강수량 [0-100]
    precipitation=carla.WeatherParameters.ClearNoon.precipitation,
    # 강수 퇴적물 (물 웅덩이) [0-100]
    precipitation_deposits=carla.WeatherParameters.ClearNoon.precipitation_deposits,
    # 바람 세기 (빗방울 방향) [0-100]
    wind_intensity=carla.WeatherParameters.ClearNoon.wind_intensity,
    # 태양 방위각 [0-360]
    sun_azimuth_angle=carla.WeatherParameters.ClearNoon.sun_azimuth_angle,
    # 태양 고도각 [-90-90]
    sun_altitude_angle=carla.WeatherParameters.ClearNoon.sun_altitude_angle,
    # 안개 밀도 [-90-90]
    fog_density=carla.WeatherParameters.ClearNoon.fog_density,
    # 안개 거리 [0-infinite]
    fog_distance=carla.WeatherParameters.ClearNoon.fog_distance,
    # 젖음 정도 (RGB 카메라 센서에만 영향을 줌)[0-100]
    wetness=carla.WeatherParameters.ClearNoon.wetness,
    # 안개 높이 [0 - 100]
    fog_falloff=carla.WeatherParameters.ClearNoon.fog_falloff,
    # 빛이 안개에 기여하는 정도 [0-infinite]
    scattering_intensity=carla.WeatherParameters.ClearNoon.scattering_intensity,
    # 꽃가루나 대기오염과 같은 입자 [0-infinite]
    mie_scattering_scale=carla.WeatherParameters.ClearNoon.mie_scattering_scale,
    # 공기 분자와 같은 작은 입자와 빛의 상호 작용을 제어합니다.
    # 빛의 파장에 따라 낮에는 푸른 하늘이, 저녁에는 붉은 하늘이 된다.
    rayleigh_scattering_scale=0.0331
)


PEDESTRIAN_TYPES = ['walker.pedestrian.00'+f'{i:02d}' for i in range(1, 14)]

VEHICLE_TYPES = [
        'vehicle.audi.a2',
        'vehicle.audi.etron',
        'vehicle.audi.tt,'
        'vehicle.bmw.grandtourer',
        'vehicle.chevrolet.impala',
        'vehicle.citroen.c3',
        'vehicle.dodge.charger_2020',
        'vehicle.dodge.charger_police',
        'vehicle.dodge.charger_police_2020',
        'vehicle.ford.ambulance',
        'vehicle.ford.crown',
        'vehicle.ford.mustang',
        'vehicle.jeep.wrangler_rubicon',
        'vehicle.lincoln.mkz_2017',
        'vehicle.lincoln.mkz_2020',
        'vehicle.mercedes.coupe',
        'vehicle.mercedes.coupe_2020',
        'vehicle.mercedes.sprinter',
        'vehicle.micro.microlino',
        'vehicle.mini.cooper_s',
        'vehicle.mini.cooper_s_2021',
        'vehicle.nissan.micra',
        'vehicle.nissan.patrol',
        'vehicle.nissan.patrol_2021',
        'vehicle.seat.leon',
        'vehicle.tesla.cybertruck',
        'vehicle.tesla.model3',
        'vehicle.toyota.prius',
        'vehicle.vespa.zx125',
        'vehicle.volkswagen.t2',
        'vehicle.volkswagen.t2_2021'
]

LARGE_VEHICLE_TYPES = [
        'vehicle.carlamotors.carlacola',
        'vehicle.carlamotors.firetruck',
]

# motorcycle
MOTORCYCLE_TYPES = [
        'vehicle.yamaha.yzf',
        'vehicle.harley-davidson.low_rider',
        'vehicle.kawasaki.ninja'
]

# cyclist
CYCLIST_TYPES = [
        'vehicle.bh.crossbike',
        'vehicle.gazelle.omafiets',
        'vehicle.diamondback.century'
]

# Static
STATIC_TYPES = [
        "static.prop.advertisement",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.atm",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.barbeque",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.barrel",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.bench01",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.bench02",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.bench03",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.bike helmet",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.bin",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.box01",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.box02",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.box03",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.briefcase",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.brokentile01",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.brokentile02",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.brokentile03"
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.brokentile04",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.busstop",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.busstoplb",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.calibrator",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.chainbarrier",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.chainbarrierend",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.clothcontainer",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.clothesline",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.colacan",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.constructioncone",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.container",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.creasedbox01",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.creasedbox02",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.creasedbox03",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.dirtdebris01",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.dirtdebris02",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.dirtdebris03",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.doghouse",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.foodcart",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.fountain"
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.garbage01",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.garbage02",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.garbage03",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.garbage04",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.garbage05",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.garbage06",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.gardenlamp",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.glasscontainer",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.gnome",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.guitarcase",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.haybale",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.haybalelb",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.ironplank",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.kiosk_01",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.mailbox",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.maptable",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.mesh",
        # Attributes:
        # mass (Float) - Modifiable
        # mesh_path (String) - Modifiable
        # role_name (String) - Modifiable
        # scale (Float) - Modifiable
        "static.prop.mobile",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.motorhelmet",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.pergola",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.plantpot01",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.plantpot02",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.plantpot03",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.plantpot04",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.plantpot05",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.plantpot06",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.plantpot07",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.plantpot08",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.plasticbag",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.plasticchair",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.plastictable",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.platformgarbage01",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.purse",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.shoppingbag",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.shoppingcart",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.shoppingtrolley",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.slide",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.streetbarrier",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.streetfountain",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.streetsign",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.streetsign01",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.streetsign04",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.swing",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.swingcouch",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.table",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.trafficcone01",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.trafficcone02",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.trafficwarning",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.trampoline",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.trashbag",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.trashcan01",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.trashcan02",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.trashcan03",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.trashcan04",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.trashcan05",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.travelcase",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.vendingmachine",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.warningaccident",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.warningconstruction",
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
        "static.prop.wateringcan"
        # Attributes:
        # role_name (String) - Modifiable
        # size (String)
]

"""A collection of guns, projectiles, mediums, and unit conversions."""
import math

from ballistics.guns import SimpleGun
from ballistics.mediums import Fluid
from ballistics.mediums import Gas
from ballistics.mediums import Medium
from ballistics.projectiles import GolfBall
from ballistics.projectiles import Sphere

# Basic unit conversions
YARD_TO_M = 0.9144
LB_TO_KG = 0.45359237
DEG_TO_RAD = math.pi / 180

# Weightless void
void = Medium(density=0, g=0, speed_of_sound=0)
# Vaccum on Earth
vaccum = Medium(density=0, g=9.8, speed_of_sound=0)
# The moon
moon = Medium(density=0, g=1.62, speed_of_sound=0)
# Air at 20c without gravity
air_20c_weightless = Gas(density=1.204, gravity=0, speed_of_sound=343, viscosity=0.00001825)
# Normal air at 20c
air_20c = Gas(density=1.204, gravity=9.8, speed_of_sound=343, viscosity=0.00001825)
# Air used in the Airsoft Tracjetory Project
air_atp = Gas(density=1.28, gravity=9.8, speed_of_sound=343, viscosity=0.0000174)
# Water at 20c
water_20c = Fluid(density=998.21, g=9.8, speed_of_sound=1481, viscosity=0.001002)

# Sample gun configurations
gun_list = {"airsoftgun": SimpleGun(1.9),
            "airsoftsniper": SimpleGun(3),
            "68calmarker": SimpleGun(10.8),
            "50calmarker": SimpleGun(1.89),
            "gelblaster": SimpleGun(.851),
            "megablaster": SimpleGun(.674),
            "rivalblaster": SimpleGun(.824),
            "357sim": SimpleGun(3.93),
            "9x19mmsim": SimpleGun(3.65),
            "556x45mmsim": SimpleGun(4.15),
            "762x51mmsim": SimpleGun(5.78),
            "bbgun": SimpleGun(1.75),
            "driver": SimpleGun(57.4, .429, 14.7 * DEG_TO_RAD),
            "testbbgun": SimpleGun(477),
            "testgun": SimpleGun(227000)}

# Sample projectile list
projectile_list = {"68calpaint": Sphere(.003, .01725),
                   "50calpaint": Sphere(.00125, .0127),
                   "gelball": Sphere(.00021, .0075),
                   "rivalball": GolfBall(.00183, .0222, .4),
                   "177bb": Sphere(.00035, .0044),
                   "golfball": GolfBall(.04593, .04273),
                   "golfball_smooth": Sphere(.04593, .04273, .3),
                   "6mm0.12": Sphere(.00032, .00595),
                   "6mm0.20": Sphere(.00032, .00595),
                   "6mm0.25": Sphere(.00032, .00595),
                   "6mm0.28": Sphere(.00032, .00595),
                   "6mm0.30": Sphere(.00032, .00595),
                   "6mm0.32": Sphere(.00032, .00595),
                   "6mm0.36": Sphere(.00032, .00595),
                   "6mm0.40": Sphere(.00032, .00595),
                   "6mm0.45": Sphere(.00032, .00595),
                   "6mm0.48": Sphere(.00032, .00595),
                   "6mm0.69": Sphere(.00032, .00595),
                   "6mm0.90": Sphere(.00032, .00595)}

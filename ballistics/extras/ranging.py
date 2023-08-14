import copy
import inspect
from typing import Callable

from ballistics.extras import config
from ballistics.guns import Gun
from ballistics.mediums import Medium
from ballistics.projectiles import Projectile


def sim(projectile: Projectile, medium: Medium, condition_t: Callable | None = None, 
        condition_f: Callable | None = None, time_step=0.001, 
        *args: str) -> dict[str, list[float]]:
    """Simulate the flight of a projectile in a medium until stop.
    
    Returns a dictionary of projectile properties to list of values, as 
    specified in the args. By default results will include the 
    distance (x), drop (y), and time.
    
    projectile - to be simulated

    medium - to be used

    condition_t - condition at which to exit and return the results

    condition_f - condition to exit and return no results

    time_step - time step at which to evaluate physics

    args - projectile properties to record at each time step
    """
    time = 0
    results = {"dist":[0.0], "drop":[0.0], "time":[0.0]}
    params = [arg for arg in args if arg not in results]
    for arg in params:
        if callable(getattr(projectile, arg)):
            if len(inspect.signature(getattr(projectile, arg)).parameters) > 0:
                results[arg] = [getattr(projectile, arg)(medium)]
            else:
                results[arg] = [getattr(projectile, arg)()]
        else:
            results[arg] = [getattr(projectile, arg)]

    while True:
        if condition_t and condition_t(results):
            return results
        if condition_f and condition_f(results):
            return {}
        x, y = projectile.tick(medium, time_step)
        time += time_step

        results["dist"].append(results["dist"][-1] + x)
        results["drop"].append(results["drop"][-1] + y)
        results["time"].append(time)

        for arg in params:
            if callable(getattr(projectile, arg)):
                if len(inspect.signature(getattr(projectile, arg)).parameters) > 0:
                    results[arg].append(getattr(projectile, arg)(medium))
                else:
                    results[arg].append(getattr(projectile, arg)())
            else:
                results[arg].append(getattr(projectile, arg))


def get_spin(projectile: Projectile, gun: Gun, medium: Medium, drop: float, rise: float, time_step=0.001) -> float:
    """Find the max spin that will extend the range of the projectile."""
    projectile = copy.deepcopy(projectile)
    gun = copy.deepcopy(gun)
    for spin in range(int(gun.vel(projectile) / projectile.diameter), 0, -int(gun.vel(projectile) / projectile.diameter / 1000)):
        gun.set_spin(spin, projectile)
        gun.shoot(projectile)
        res = sim(projectile, medium, lambda r: r["drop"][-1] < -drop, lambda r: r["drop"][-1] > rise, time_step)
        if res:
            print(spin)
            return spin
    return -1

def max_range(projectile: Projectile, gun: Gun, medium: Medium, drop: float, time_step=0.001) -> float:
    """Find the max range of a projectile, firing at a max angle."""
    projectile = copy.deepcopy(projectile)
    gun = copy.deepcopy(gun)
    og_angle = gun.angle
    gun.angle = 45 * config.DEG_TO_RAD
    max_range = 0
    range = sim(projectile, medium, lambda r: r["drop"][-1] < -drop, time_step=time_step)["dist"][-1]
    while range > max_range:
        max_range = range
        gun.angle -= 1 * config.DEG_TO_RAD
        gun.shoot(projectile)
        range = sim(projectile, medium, lambda r: r["drop"][-1] < -drop, time_step=time_step)["dist"][-1]
    gun.angle = og_angle
    return max_range

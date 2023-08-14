import copy
from matplotlib import pyplot

from ballistics.guns import Gun
from ballistics.mediums import Medium
from ballistics.projectiles import Projectile
from ballistics.extras import ranging

def plot_bb(projectile: Projectile, gun: Gun, medium: Medium, zero_dist: float, target_dist: float, height: float, target_height: float, projectile_name: str, gun_name: str, x_unit: float, y_units: list[float], x_label: str, y_labels: list[str], rise: float):
    projectile = copy.deepcopy(projectile)
    gun = copy.deepcopy(gun)
    gun.set_spin(ranging.get_spin(projectile, gun, medium, height, rise, .0001), projectile)
    plot_bullet(projectile, gun, medium, zero_dist, target_dist, height, target_height, projectile_name, gun_name, x_unit, y_units, x_label, y_labels)

def plot_bullet(projectile: Projectile, gun: Gun, medium: Medium, zero_dist: float, target_dist: float, height: float, target_height: float, projectile_name: str, gun_name: str, x_unit: float, y_units: list[float], x_label: str, y_labels: list[str]):
    projectile = copy.deepcopy(projectile)
    gun = copy.deepcopy(gun)
    gun.aim(target_dist, target_height - height)
    gun.shoot(projectile)
    r = ranging.sim(projectile, medium, lambda r: r["drop"][-1] < -height, lambda _: False, .0001, x_label, *y_labels)
    for y_label, y_unit in tuple(zip(y_labels, y_units)):
        pyplot.plot([x * x_unit for x in r[x_label]], [y * y_unit for y in r[y_label]], label = gun_name + " " + projectile_name + " " + y_label)

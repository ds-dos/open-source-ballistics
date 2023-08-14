import math

from ballistics import projectiles


class Gun:
    """A gun that fires a projectile."""

    def __init__(self, angle: float = 0):
        self.angle = angle

    def vel(self, projectile: "projectiles.Projectile") -> float:
        """In m/s."""
        return 0

    def set_vel(self, v: float, projecitle: "projectiles.Projectile"):
        pass

    def spin(self, projectile: "projectiles.Projectile") -> float:
        """In rad/s."""
        return 0

    def set_spin(self, w: float, projectile: "projectiles.Projectile"):
        pass

    def shoot(self, projectile: "projectiles.Projectile"):
        projectile.velocity = self.vel(projectile)
        projectile.angular_velocity = self.spin(projectile)
        projectile.angle = self.angle

    def aim(self, x: float, y: float):
        self.angle = math.atan(y / x)


class SimpleGun(Gun):
    """A gun that fires a projectile with a fixed energy."""

    def __init__(self, k: float, wk: float = 0, angle: float = 0):
        """
        k - linear kinetic energy in Joules
        wk - angular kinetic energy in Joules
        """
        super().__init__(angle)
        self._k = k
        self._wk = wk

    def vel(self, projectile: "projectiles.Projectile"):
        return (self._k / projectile.mass * 2)**.5

    def set_vel(self, v: float, projectile: "projectiles.Projectile"):
        self._k = projectile.mass * v**2 / 2

    def spin(self, projectile: "projectiles.Projectile"):
        if projectile.mofinertia == 0:
            return 0
        return (self._wk / projectile.mofinertia * 2)**.5

    def set_spin(self, w: float, projectile: "projectiles.Projectile"):
        self._wk = projectile.mofinertia * w**2 / 2

import math

from ballistics import mediums


class Projectile:
    """A projectile that's launched and travels through the air."""

    def __init__(self, mass: float, diameter: float, i_mod=0.0):
        """
        mass - in kg
        diameter - in m
        i_mod - constant k for moment of intertia = k * mr^2
        """
        self.mass = mass
        self.diameter = diameter
        self.i_mod = i_mod
        self.velocity = 0
        self.angular_velocity = 0
        self.angle = 0

    def tick(self, medium: "mediums.Medium", time=0.0, dist=0.0) -> tuple[float, float]:
        """Progress time, apply forces return x/y distances traveled."""
        # Time for this tick
        if time:
            dist = time * self.velocity
        else:
            time = dist / self.velocity
        
        old_angle = self.angle

        # Directional force
        force_dir = -medium.drag(self)
        force_dir -= medium.crush(self)

        # Perpendicular lift force
        force_perp = medium.lift(self)

        # Vertical gravitational force
        force_y = -medium.gravity(self)
        force_y += medium.buoyant(self)

        # Apply linear forces
        # print("drag", force_dir)
        # print("lift", force_perp)
        # print("grav", force_y)
        vel_x = self.vel_x + (force_dir * math.cos(self.angle) + force_perp * math.sin(self.angle)) / self.mass * time
        vel_y = self.vel_y + (force_y + force_dir * math.sin(self.angle) + force_perp * math.cos(self.angle)) / self.mass * time

        if vel_x < 0:
            vel_x = 0.000000000001
        self.velocity = (vel_x**2 + vel_y**2)**0.5
        self.angle = math.atan(vel_y / vel_x)

        # Spin decay
        if self.angular_velocity != 0:
            self.angular_velocity -= medium.torque(self) / self.mofinertia * time
            # Golf balls lose ~3-4% of their spin per second
            # self.angular_velocity *= .967**time
        
        # Total distance traveled
        return dist * math.cos(old_angle), dist * math.sin(old_angle)

    @property
    def k(self) -> float:
        """Linear kinetic energy in J."""
        return self.mass * self.velocity**2 / 2
    
    @property
    def wk(self) -> float:
        """Angular kinetic energy in J."""
        return self.mofinertia * self.angular_velocity**2 / 2

    @property
    def vel_x(self) -> float:
        """X (forwards) velocity in m/s."""
        return math.cos(self.angle) * self.velocity
    
    @property
    def vel_y(self) -> float:
        """Y (vertical) velocity in m/s"""
        return math.sin(self.angle) * self.velocity
    
    @property
    def w(self) -> float:
        """Velocity of a point on the projectile's surface in m/s."""
        return self.angular_velocity * self.diameter / 2
    
    @property
    def area(self) -> float:
        """Frontal area in m^2."""
        return 0
    
    @property
    def volume(self) -> float:
        """Volume in m^3."""
        return 0

    @property
    def mofinertia(self) -> float:
        """Moment of inertia in kgm^2."""
        return 0
    
    def cd(self, medium: "mediums.Fluid") -> float:
        """Dimensionless drag coefficient."""
        return 0
    
    def cl(self, medium: "mediums.Fluid") -> float:
        """Dimensionless lift coefficient."""
        return 0
    
    def ct(self, medium: "mediums.Fluid") -> float:
        """Dimensionless torque coefficient."""
        return 0
    
    def re(self, medium: "mediums.Fluid") -> float:
        """Dimensionless Reynold's number."""
        return medium.density * self.velocity * self.diameter / medium.viscosity
    
    def rew(self, medium: "mediums.Fluid") -> float:
        """Dimensionless angular Reynold's number."""
        return medium.density * self.diameter / 2 * abs(self.w) / medium.viscosity


class Sphere(Projectile):
    """A smooth sphere."""
    def __init__(self, mass: float, diameter: float, i_mod: float = .4):
        super().__init__(mass, diameter, i_mod)

    @property
    def area(self) -> float:
        return math.pi * self.diameter**2 / 4

    @property
    def volume(self) -> float:
        return 4 / 3 * math.pi * self.diameter**3 / 8
    
    @property
    def mofinertia(self) -> float:
        return self.i_mod * self.mass * self.diameter**2 / 4
    
    def cd(self, medium: "mediums.Fluid") -> float:
        if self.re(medium) < 9000:
            cd0 = 24 / self.re(medium) + 4 / self.re(medium)**.5 + .4
        else:
            cd0 = (0.4274794 + 0.000001146254 * self.re(medium) - 7.559635 * 10**-12 * self.re(medium)**2 - 3.817309 * 10**-18 * self.re(medium)**3 + 2.389417 * 10**-23 * self.re(medium)**4) / (1 - 0.000002120623 * self.re(medium) + 2.952772 * 10**-11* self.re(medium)**2 - 1.914687 * 10**-16 * self.re(medium)**3 +  3.125996 * 10**-22 * self.re(medium)**4)
        if self.angular_velocity > 0:
            vu = self.w / self.velocity
            cd0 = (cd0 + 2.2132291 * vu - 10.345178 * vu**2 + 16.157030 * vu**3 - 5.27306480 * vu**4) / (1 + 3.1077276 * vu - 13.6598678 * vu**2 + 24.00539887 * vu**3 - 8.340493152 * vu**4 + 0.07910093 * vu**5)
        return cd0

    def cl(self, medium: "mediums.Fluid") -> float:
        vu = self.w / self.velocity
        if vu == 0:
            return 0
        return (-0.0020907 - 0.208056226 * vu + 0.768791456 * vu**2 - 0.84865215 * vu**3 + 0.75365982 * vu**4) / (1 - 4.82629033 * vu + 9.95459464 * vu**2 - 7.85649742 * vu**3 + 3.273765328 * vu**4)

    def ct(self, medium: "mediums.Fluid") -> float:
        if self.rew(medium) > 0:
            return 6.45 / self.rew(medium)**.5 + 32.1 / self.rew(medium)
        else:
            return 0


class GolfBall(Sphere):
    """A golf ball (dimpled sphere)."""
    def __init__(self, mass: float, diameter: float, i_mod: float = .3):
        super().__init__(mass, diameter, i_mod)
    
    @property
    def mofinertia(self) -> float:
        return self.i_mod * self.mass * self.diameter**2 / 4
    
    def cd(self, medium: "mediums.Fluid") -> float:
        if self.re(medium) < 9000:
            return 24 / self.re(medium) + 4 / self.re(medium)**.5 + .4
        elif self.re(medium) < 50000:
            return .5
        elif self.re(medium) < 100000:
            return 1.29 * 10**-10 * self.re(medium)**2 - 2.59 * 10**-5 * self.re(medium) + 1.5
        elif self.re(medium) < 200000:
            return 1.91 * 10**-11 * self.re(medium)**2 - 5.4 * 10**-6 * self.re(medium) + .56
        else:
            return .4
    
    def cl(self, medium: "mediums.Fluid") -> float:
        vu = self.w / self.velocity
        if vu > .3:
            return .3
        if vu == 0:
            return 0
        return -3.25 * vu**2 + 1.99 * vu
    
    def ct(self, medium: "mediums.Fluid") -> float:
        # Formula from the Airsoft Trajectory Project. This needs to be 
        # verified by some other source though. Otherwise a constant of 
        # 1 seems to be fairly accurate.
        return 6.45 / self.rew(medium)**.5 + 32.1 / self.rew(medium)

from ballistics import projectiles


# Abstract, don't use
class Medium:
    """A physical medium a projectile can travel through."""

    def __init__(self, density: float, g: float, speed_of_sound: float):
        """
        density - in kg/m^3
        g - graviational acceleration in m/s
        speed_of_sound - in m/s, for wave drag (not implemented)
        """
        self.density = density
        self.g = g
        self.speed_of_sound = speed_of_sound
    
    def drag(self, projectile: "projectiles.Projectile") -> float:
        """The drag force exerted on the given projectile in N."""
        return 0
    
    def lift(self, projectile: "projectiles.Projectile") -> float:
        """The lift force exerted on the given projectile in N."""
        return 0
    
    def crush(self, projectile: "projectiles.Projectile") -> float:
        """The material resistance exerted in a solid in N."""
        return 0
    
    def buoyant(self, projectile: "projectiles.Projectile") -> float:
        """The bouyant force exerted on the given projectile in N."""
        return 0
    
    def gravity(self, projectile: "projectiles.Projectile") -> float:
        """The gravitational force exerted on the given projectile."""
        return self.g * projectile.mass
    
    def torque(self, projectile: "projectiles.Projectile") -> float:
        """The torque exerted on the given projectile in Nm."""
        return 0


class Solid(Medium):
    """A solid medium with a material strength."""

    def __init__(self, density: float, g: float, speed_of_sound: float, hardness: float):
        """
        density - in kg/m^3
        g - graviational acceleration in m/s
        speed_of_sound - in m/s, for wave drag (not implemented)
        hardness - material strength in N/m
        """
        super().__init__(density, g, speed_of_sound)
        self.hardness = hardness
    
    def crush(self, projectile: "projectiles.Projectile") -> float:
        return projectile.area * self.hardness


class Fluid(Medium):
    """A mon-compressible, viscous fluid medium."""

    def __init__(self, density: float, g: float, speed_of_sound: float, viscosity: float):
        """
        density - in kg/m^3
        g - graviational acceleration in m/s
        speed_of_sound - in m/s, for wave drag (not implemented)
        viscosity - in kg  /
        """
        super().__init__(density, g, speed_of_sound)
        self.viscosity = viscosity
    
    def drag(self, projectile: "projectiles.Projectile") -> float:
        return self.density * projectile.area * projectile.velocity**2 * projectile.cd(self) / 2
    
    def lift(self, projectile: "projectiles.Projectile") -> float:
        return projectile.cl(self) * self.density * projectile.velocity**2 * projectile.area / 2
    
    def buoyant(self, projectile: "projectiles.Projectile") -> float:
        return self.density * projectile.volume * self.g
    
    def torque(self, projectile: "projectiles.Projectile") -> float:
        # I only have a torque equation for Spheres
        if issubclass(type(projectile), projectiles.Sphere):
            # Working formula, needs to be verified. Is torque 
            # proportional to velocity or velocity squared? I think 
            # this is fine. At least the units are correct.
            return .5 * projectile.ct(self) * self.density * projectile.diameter**3 * projectile.w**2
            # return 6 * pi * self.viscosity * projectile.diameter / 2 * projectile.w**2
            # return 8 / 3 * pi * projectile.diameter**3 / 8 * self.viscosity * projectile.angular_velocity
            # k = .0000000000075 / .006 ** 2
            # return k * self.density * projectile.diameter**5 * projectile.angular_velocity**2
        return 0


class Gas(Fluid):
    """A compressible, viscous gas medium."""

    def __init__(self, density: float, gravity: float, speed_of_sound: float, viscosity: float):
        """
        density - in kg/m^3
        g - graviational acceleration in m/s
        speed_of_sound - in m/s, for wave drag (not implemented)
        viscosity - in kg  /
        """
        super().__init__(density, gravity, speed_of_sound, viscosity)

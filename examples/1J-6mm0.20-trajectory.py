import matplotlib.pyplot as plt
from ballistics.extras.config import air_atp
from ballistics import SimpleGun
from ballistics.extras.config import projectile_list
from ballistics.extras.plotting import plot_bb


if __name__ == "__main__":
    """! Trajectory of a 6mm 0.20g airsoft BB fired from a 1J airsoft gun.

    The sping of the projectile is calculated to allow for a 0.1 m
    rise above the muzzle whilst achieving maximum range.
    """
    fig = plot_bb(
        projectile=projectile_list["6mm0.20"],
        gun=SimpleGun(1.0),  # 1 Joule
        medium=air_atp,
        zero_dist=0,
        target_dist=50,  # 50 m target
        height=1.5,  # Avg shoulder height.
        target_height=1.5,  # Avg target center off mass height.
        projectile_name="6mm0.20",
        gun_name="airsoftgun",
        x_unit=1,  # No scaling.
        y_units=[1],  # No scaling.
        x_label="dist",  # Horizontal distance.
        y_labels=["drop"],  # Vertical drop.
        rise=0.1,  # Allow for 0.1 m rise above muzzle.
    )
    plt.show()

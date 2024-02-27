# Open Source Ballistics

An open-source ballistics calculator library written in Python. Mainly intended
for calculating trajectories of airsoft BBs and other spherical projectiles in
SI units. Inspired on
[The Airsoft Trajectory Project](https://web.archive.org/web/20200621112354/http://mackila.com/airsoft/atp/index.htm)
and aimed at answering more complex questions than even those originally posed
in a pursie of bringing grounded science into the sport.


<!----------------------------------------------------------------------------->
## Getting Started
<!----------------------------------------------------------------------------->

### Quick setup and test

If you just want to test Open Source Ballistics, create a virtual environment
and run any of the included examples. The following steps simulate a 0.20 g BB
shot form a 1 J airsoft rifle and, if everything works as intended, creates a
plot of said trajectory.

1. Clone this repository and `cd` into it.
2. Create a python virtual environemnt, `python -m venv ./.venv`.
3. Activate the virtual environment.
    - `source .venv/bin/activate` on Unix/macOS.
    - `.venv\Scripts\activate` on Windows.
4. Install this project locally, `pip install --editable .`
5. Run the example script, `python examples/1J-6mm0.20-trajectory.py`.

### Installation

[Work in progress]

### Usage

[Work in progress]

<!----------------------------------------------------------------------------->
## Overview
<!----------------------------------------------------------------------------->

- `ballistics.guns.Gun`
    A gun that fires a projectile.

- `ballistics.guns.SimpleGun`
    A gun that fires a projectile with a fixed energy.

- `ballistics.mediums.Medium`
    A physical medium a projectile can travel through.

- `ballistics.mediums.Solid`
    A solid medium with a material strength.

- `ballistics.mediums.Fluid`
    A non-compressible, viscous fluid medium.

- `ballistics.mediums.Gas`
    A compressible, viscous gas medium.

- `ballistics.projectiles.Projectile`
    A projectile that's launched and travels through the air.

- `ballistics.projectiles.Sphere`
    A smooth sphere.

- `ballistics.projectiles.GolfBall`
    A golf ball (dimpled sphere).

<!----------------------------------------------------------------------------->
## Contributing
<!----------------------------------------------------------------------------->

We welcome contributions! Please consider:

- Write clear and concise commit messages.
- Follow the PEP 8 style guide for Python code.
- Submit a pull request with a brief description of your changes, and when
  applicable, explain how to test them.

Otherwise, found a bug, or Encountered an issue? Create a new issue and describe
the problem clearly. For question outside the scope of an issue, feel free to
reach out to us. You can find a detailed list of everyone involved in the
development in [AUTHORS.md](AUTHORS.md). Thanks to all of you!

<!----------------------------------------------------------------------------->
## License
<!----------------------------------------------------------------------------->

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).
See the [LICENSE](./LICENSE) file for details.




"""
An open-source ballisics calculator library. Mainly intended for calculating trajectories of airsoft BBs and other spherical projectiles. All units are SI.

Distributed under the GNU GPL 3 license.

This is very much a WORK IN PROGRESS. Nothing here is final.

Feel free to email me at stuff255@outlook.com
"""

__package__ = "ballistics"

from ballistics.guns import *  # noqa F401
from ballistics.mediums import *  # noqa F401
from ballistics.projectiles import *  # noqa F401
from ballistics.extras import *  # noqa F401

__all__ = [
    "Gun",
    "Medium",
    "Projectile",
    "ranging",
    "config",
    "plotting",
    "extras",
]

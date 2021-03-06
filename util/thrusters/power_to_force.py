# -*- coding: utf-8 -*-
"""Functions related to power to force conversion."""

from sys import exit
from pymarcyb.util.enumerations import ThrusterType


def imca_p2f(thruster_type, max_power_positive, max_power_negative):
    """Return the maximum force a thruster can apply, in kN, given the maximum power it can deliver,
    according to the IMCA power-to-force relationship (see IMCA M 140).

    Includes thruster losses.

    Args:
        - thruster_type (ThrusterType enum)  -- type of thruster
        - max_power_positive (float)         -- maximum power, positive direction, in kW
        - max_power_negative (float)         -- maximum power, negative direction, in kW

    Returns:
        - max_force_positive (float)        -- maximum force, positive direction, in kN
        - max_force_negative (float)        -- maximum force, negative direction, in kN
    """

    grav = 9.81
    hp_per_Kw = 1.36332     # metric horsepower

    if thruster_type is ThrusterType.tunnel:
        conversion_factor_positive =  11.0 * 10**-3 * hp_per_Kw * grav
        conversion_factor_negative = -11.0 * 10**-3 * hp_per_Kw * grav
    elif thruster_type is ThrusterType.azimuth:
        conversion_factor_positive =  13.0 * 10**-3 * hp_per_Kw * grav
        conversion_factor_negative =  -8.0 * 10**-3 * hp_per_Kw * grav
    elif thruster_type is ThrusterType.propeller:
        conversion_factor_positive = 13.0 * 10**-3 * hp_per_Kw * grav
        conversion_factor_negative = -0.7 * conversion_factor_positive
    elif thruster_type is ThrusterType.waterjet:
        conversion_factor_positive = 8.0 * 10**-3 * hp_per_Kw * grav
        conversion_factor_negative = 0.0
    else:
        print("Illegal thruster type.")
        exit(2)

    max_force_positive = conversion_factor_positive * max_power_positive
    max_force_negative = conversion_factor_negative * max_power_negative

    return max_force_positive, max_force_negative


def abs_p2f(max_power_positive, max_power_negative, diameter, ducted):
    """Return the maximum force a thruster can apply, in kN, given the maximum power it can deliver,
    according to the ABS power-to-force relationship (see ABS Guide For Dynamic Positioning Systems).

    Excludes thruster losses.

    Args:
        - max_power_positive (float)         -- maximum power, positive direction, in kW
        - max_power_negative (float)         -- maximum power, negative direction, in kW
        - diameter (float)                   -- diameter of the thruster, in m
        - ducted (bool)                      -- true if the thruster is ducted

    Returns:
        - max_force_positive (float)        -- maximum force, positive direction, in kN
        - max_force_negative (float)        -- maximum force, negative direction, in kN
    """

    if ducted == False:
        K = 848.0
    else:
        K = 1250.0

    max_force_positive = (K * (max_power_positive * diameter)**(2.0/3.0)) / 1000.0
    max_force_negative = (K * (max_power_negative * diameter)**(2.0/3.0)) / 1000.0

    return max_force_positive, max_force_negative

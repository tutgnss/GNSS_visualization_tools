# Tampere University of Technology
#
# DESCRIPTION
# Create the matrix of parameters that we want to set in the Spectracom
#
# AUTHOR
# Anne-Marie Tobie

import configparser


def read_scen(filename):
    # It's a matrix with nb_sections boxes, each of them contain nb_options boxes
    # scenario = [[LAT, LONG, ALT, Duration, Heading, Speed, Acceleration, Rate heading,
    # Turn rate, turn radius, C/N0, Propagation, antenna, tropospheric model, Ionospheric model,
    # Keep altitude, signal type, ...][LAT, LONG, ...]]
    config = configparser.ConfigParser()
    config.read(filename)
    nb_sections = len(config.sections())
    nb_option = []
    for i in range(nb_sections):
        section = config.sections()[i]
        nb_option.append(len(config.options(section)))

    scenario = [[[] for _ in range(max(nb_option))] for _ in range(nb_sections)]
    for i in range(nb_sections):
        section = config.sections()[i]
        for j in range(nb_option[i]):
            option = config.options(section)
            scenario[i][j] = config.get(section, option[j])
    return scenario

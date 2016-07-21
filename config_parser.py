# Tampere University of Technology
#
# DESCRIPTION
# Create the matrix of parameters that we want to set in the Spectracom
#
# AUTHOR
# Anne-Marie Tobie

import configparser

filename = 'test_1.ini'

Config = configparser.ConfigParser()
read = Config.read(filename)
nb_sections = len(Config.sections())
nb_option = []
for i in range(nb_sections):
    section = Config.sections()[i]
    nb_option.append(len(Config.options(section)))


def read_scen():
    # It's a matrix with nb_sections boxes, each of them contain nb_options boxes
    # scenario = [[LAT, LONG, ALT, Duration, Heading, Speed, Acceleration, Rate heading,
    # Turn rate, turn radius, C/N0, Propagation, antenna, tropospheric model, Ionospheric model,
    # Keep altitude, signal type][LAT, LONG, ...]]
    scenario = [[[] for _ in range(max(nb_option))] for _ in range(nb_sections)]
    for i in range(nb_sections):
        section = Config.sections()[i]
        for j in range(nb_option[i]):
            option = Config.options(section)
            scenario[i][j] = Config.get(section, option[j])
    return scenario
scenario = read_scen()


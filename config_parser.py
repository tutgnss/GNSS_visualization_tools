__author__ = 'tobie'

import configparser

filename = 'test_3.ini'

Config = configparser.ConfigParser()
read = Config.read(filename)
nb_sections = len(Config.sections())
nb_option = []
for i in range(nb_sections):
    section = Config.sections()[i]
    nb_option.append(len(Config.options(section)))


def read_scen():
    # c'est une matrice de nb_sections cases contenant chacune nb_options case
    # scenario = [[LAT, LONG, ALT, Duration, Heading, Speed][LAT, LONG, ...]]
    scenario = [[[] for _ in range(max(nb_option))] for _ in range (nb_sections)]
    for i in range(nb_sections):
        section = Config.sections()[i]
        for j in range(nb_option[i]):
            option = Config.options(section)
            scenario[i][j] = Config.get(section, option[j])
    return(scenario)

#print(read_scen())


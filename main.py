from terminal import *
from tqdm import tqdm



file = file()
term_dic = file.csv2dict('term_info_test1.csv')
term_series = file.csv2dict('die_SN_test1.csv')
machinesList = file.csv2machinesList('machines.csv')
file.generate_folders()
machine = "maq 1"

for terminal, values in tqdm(term_dic.items()):
    DieObj = die(terminal, values)
    series = term_series[terminal]
    for i in range(len(series)):
        serial = series[i]
        sigma_cch = DieObj.random_cch_sigma(7, 3, 2)
        sigma_tension = DieObj.random_tension_sigma(9, 4)
        cch_data = DieObj.normalCCH_rndmData(100)
        tension_data = DieObj.normalTension_rndmData(100, 2)
        file.outFile(terminal, serial, machine)
        file.write_csv(cch_data, tension_data)










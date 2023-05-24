import sys
from terminal import *



file = file()
term_dic = file.csv2dict('term_info_test1.csv')
term_series = file.csv2dict('die_SN_test1.csv')
machinesList = file.csv2machinesList('machines.csv')
file.generate_folders()
machine = file.get_MachineName()

for terminal, values in term_dic.items():
    DieObj = die(terminal, values)
    series = term_series[terminal]
    for i in range(len(series)):
        serial = series[i]
        sigma_cch = DieObj.random_cch_sigma(8, 5, 2)
        sigma_tension = DieObj.random_tension_sigma(13, 9)
        cch_data = DieObj.normalCCH_rndmData(100)
        tension_data = DieObj.normalTension_rndmData(100, 2)
        DieObj.print_estimates(serial)
        file.outFile(terminal, DieObj.cs_area, serial, machine)
        file.write_csv(cch_data, tension_data)
print()
prompt = input("Quit? ")
if prompt == "y":
    sys.exit("Goodbye")











import numpy as np
import csv
import os
import random


def main():
    # get info from csv files and convert it into dictionaries
    term_dic = csv_into_dict("term_info_test1.csv")
    SN_dict = csv_into_dict("die_SN_test1.csv")
    machines_list = csv_into_list_mchn("machines.csv") 
    #Create folders from machines and terminals list and select the machine where the capability studies are going to be created
    generate_folders(machines_list)  
    mchn_index = get_mchn_name(machines_list)
    currpath = os.path.join(os.getcwd(), "machines", machines_list[mchn_index])
    generate_term_folders(term_dic.keys(), machines_list[mchn_index])

    # loops over the keys that are the terminal PN
    for terminal in term_dic.keys():
        term_data = term_dic[terminal]
        SN_data = SN_dict[terminal]
        for i in range(len(SN_data)):
            SN = SN_data[i]  
            term_data = [float(x) for x in term_data]  
            CCH_sigma, tension_sigma = rndm_sigma(term_data[1])
            CCH_list = getCCH_rndm_data(term_data[0], CCH_sigma, term_data[1])
            tension_list = get_tension_rndm_data(tension_sigma, term_data[2])
            filename = f"{terminal}_{SN}.csv" 
            header = f"{terminal} {SN} {machines_list[mchn_index]}"
            write_csv(currpath, filename, CCH_list, tension_list, header, terminal) 


def getCCH_rndm_data(nominal_value, sigma, cs_area): #Function to generate 100 CCH normal random values, where the nominal value is the central value or mu
    if 0 < cs_area <= 0.35:
        upper_limit = nominal_value + 0.03
        lowest_limit = nominal_value - 0.03
    elif 0.35 < cs_area <= 8:
        upper_limit = nominal_value + 0.05
        lowest_limit = nominal_value - 0.05
    else:
        upper_limit = nominal_value + 0.1
        lowest_limit = nominal_value - 0.1

    rand_nums = np.random.normal(nominal_value, sigma, 100)
    rand_nums_rounded = np.round(rand_nums, 3)
    rounded_list = [
        num for num in rand_nums_rounded if lowest_limit <= num <= upper_limit
    ]
    return rounded_list


def get_tension_rndm_data(sigma, tension): #Function to generate 100 tension random values, where mu is always bigger than the nominal value (25%-35%)
    min_tension = tension
    upper_limit = min_tension * 1.35
    lowest_limit = min_tension * 1.25
    mu = (upper_limit - lowest_limit) + lowest_limit

    rand_nums = np.random.normal(mu, sigma, 100)
    rand_nums_rounded = np.round(rand_nums, 1)
    return rand_nums_rounded.tolist()


def csv_into_list_mchn(file): #Function that takes a csv file that has a list of machines, the function reads only one column
    with open(file, "r") as file:
        reader = csv.reader(file)
        machine = []
        for row in reader:
            machine.append(row[0])
        return machine


def csv_into_dict(file): #Function that takes a csv file and get its first row element and it will be the key of the dictionary, the remain values are a list[CCH,cs area,tension]
    with open(file, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        data = {}
        for row in csv_reader:
            key = row[0]
            values = row[1:]
            data[key] = values

    return data


def generate_folders(machine_list): #Function that creates machine's folders 
    path = os.path.join(os.getcwd(), "machines")
    for folder_name in machine_list:
        folder_path = os.path.join(path, folder_name)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
            print(f"Created folder: {folder_path}")
        else:
            print(f"Folder {folder_path} already exists")


def write_csv(currpath, filename, cch_list, tension_list, header, terminal): #Function that writes a csv file with the random data, it has a header and save the dies in its folder
    path = os.path.join(currpath, terminal, filename)
    with open(path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([header])
        writer.writerow(["CCH", "tension"])
        for row in zip(cch_list, tension_list):
            writer.writerow(row)


def rndm_sigma(cs_area): #function thath chooses a randon value of sigma, it depends of the CCH's tolerance, the more tolerances are tight sigma gets low 
    cch_lwrsigma = 4
    cch_uprsigma = 7
    tn_lwrsigma = 5
    tn_uprsigma = 10
    cch_factor = 2
    tn_factor = 4
    if 8 <= cs_area <= 10:
        cch_lwrsigma = cch_lwrsigma * cch_factor
        cch_uprsigma = cch_uprsigma * cch_factor
        tn_lwrsigma = tn_lwrsigma * tn_factor
        tn_uprsigma = tn_uprsigma * tn_factor
    elif cs_area <= 0.35:
        cch_lwrsigma = 4
        cch_uprsigma = 5
        tn_lwrsigma = 1
        tn_uprsigma = 3

    cch_sigma_list = []
    tension_sigma_list = []
    for i in range(cch_lwrsigma, cch_uprsigma, 1):
        cch_sigma_list.append(i / 1000)

    for i in range(tn_lwrsigma, tn_uprsigma, 1):
        tension_sigma_list.append(i)

    rndm_cchsigma = random.choice(cch_sigma_list)
    rndm_tensigma = random.choice(tension_sigma_list)
    return rndm_cchsigma, rndm_tensigma


def generate_term_folders(terminals, machine): #Function tha generate folders inside the machines folder, are a list of dies
    for terminal in terminals:
        path = os.path.join(os.getcwd(), "machines", machine, terminal)
        if not os.path.exists(path):
            os.mkdir(path)
            print(f"Created folder: {path}")
        else:
            print(f"Folder {path} already exists")

def get_mchn_name(mchn_list):
    while True:
        try:
            machine = input("Machine: ")
            mchn_index = mchn_list.index(machine)
            return mchn_index
        except ValueError:
            print("The machines is not in the list, the names must match")


main()

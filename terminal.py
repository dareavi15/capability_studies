
import numpy as np
import csv
import os
import random
from scipy.stats import ttest_1samp
from scipy import stats


class die():
    def __init__(self, terminal, term_info):
        self.terminal = terminal
        self.nominal_cch = float(term_info[0])
        self.minTension = float(term_info[2])
        self.cs_area = float(term_info[1])
        self.cch_data = []
        self.tension_data = []
        self.cch_sigma = 0
        self.tension_sigma = 0
     

    def normalCCH_rndmData(self, samples):
        pvalue = 0
        ad_test = 1
        while pvalue <= 0.06 or ad_test > 0.75:
            rand_nums = np.random.normal(self.nominal_cch, self.cch_sigma, samples)
            rand_nums_rounded = np.round(rand_nums, 3)
            rounded_list = rand_nums_rounded.tolist()
            ad_test = stats.anderson(rounded_list, dist="norm").statistic
            _, pvalue = ttest_1samp(rounded_list, self.nominal_cch)
            
        self.cch_data = rounded_list
        return rand_nums_rounded.tolist()

    def normalTension_rndmData(self, samples, factor):
        pvalue = 0
        ad_test = 1
        while pvalue <= 0.06 or ad_test > 0.75:
            rand_nums = np.random.normal(self.minTension * factor, self.tension_sigma, samples)
            rand_nums_rounded = np.round(rand_nums, 1)
            rounded_list = rand_nums_rounded.tolist()
            ad_test = stats.anderson(rounded_list, dist="norm").statistic
            _, pvalue = ttest_1samp(rounded_list, self.minTension * factor)

        self.tension_data = rounded_list
        return rand_nums_rounded.tolist()

    def random_cch_sigma(self, max_sigma, min_sigma, factor):
        lwrsigma = min_sigma
        uprsigma = max_sigma
        if 8 <= self.cs_area <= 10:
            lwrsigma = min_sigma * factor
            uprsigma = max_sigma * factor

        cch_sigma_list = []
        for i in range(lwrsigma, uprsigma, 1):
            cch_sigma_list.append(i / 1000)

        self.cch_sigma = random.choice(cch_sigma_list)
        return random.choice(cch_sigma_list)

        
    def random_tension_sigma(self, max_sigma, min_sigma):
        cch_sigma_list = []
        for i in range(min_sigma, max_sigma, 1):
            cch_sigma_list.append(i)
            
        self.tension_sigma = random.choice(cch_sigma_list)
        return random.choice(cch_sigma_list)

        

    def cpk_ppk(self, tol_type, data):
        x_bar = np.mean(data)
        s = np.std(data, ddof=1)
        if tol_type != "ten":
            LSL = self.nominal_cch - 0.05
            USL = self.nominal_cch + 0.05
            if self.cs_area <= 0.35:
                LSL = self.nominal_cch - 0.03
                USL = self.nominal_cch + 0.03
            if self.cs_area > 8:
                LSL = self.nominal_cch - 0.1
                USL = self.nominal_cch + 0.1
            cpk = min((USL - x_bar) / (3 * s), (x_bar - LSL) / (3 * s))
        else:
            LSL = self.minTension
            cpk = (x_bar - LSL) / (3 * s)

        return round(cpk, 3)




class machine():
    def __init__(self, serial):
        self.serial = serial


class file():
    def __init__(self):
        self.machines_list = []
        self.header = None
        self.machine = None
        self.filename = None
        self.path = None
        self.terminal = None


    def csv2dict(self, filename):
        while True:
            try:
                with open(filename, "r") as csv_file:
                    csv_reader = csv.reader(csv_file)
                    data = {}
                    for row in csv_reader:
                        key = row[0]
                        values = row[1:]
                        data[key] = values
                return data
            except FileNotFoundError:
                filename = input(
                    "Couldn't find terminal/die information please input the file name including the extension: ")
    
    def csv2machinesList(self, machine_csv):
        with open(machine_csv, "r") as file:
            reader = csv.reader(file)
            machines = []
            for row in reader:
                machines.append(row[0])
                
            self.machines_list = machines
            return machines
        
    def generate_folders(self):
        path = os.path.join(os.getcwd(), "machines")
        for folder_name in self.machines_list:
            folder_path = os.path.join(path, folder_name)
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
                print(f"Created folder: {folder_path}")
            else:
                print(f"Folder {folder_path} already exists")
    
    def outFile(self, terminal, serie, machine):
        self.filename = f"{terminal}_{serie}.csv"
        self.header = f"{terminal} {serie} {machine}"
        self.path = os.path.join(os.getcwd(), "machines", machine, terminal)
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            print(f"Created folder: {self.path}")
        self.terminal = terminal

    def write_csv(self, cch_list, tension_list):
        path = os.path.join(self.path, self.filename)
        with open(path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.header])
            writer.writerow(["CCH", "tension"])
            for row in zip(cch_list, tension_list):
                writer.writerow(row)
        
        
        
        
        
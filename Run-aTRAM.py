#!/usr/bin/env python3

# Load modules
import glob
import os
import os.path
from os.path import exists
import subprocess




def atram(directory):
    '''
    This function runs both aTRAM_preprocessor and aTRAM
    '''
    R1 = glob.glob("*R1.trimmed.fastq.gz")[0]
    R2 = glob.glob("*R2.trimmed.fastq.gz")[0]
    db = directory.split("/")[0]+".db"
    command1 = ["atram_preprocessor.py", "-b", db, "--gzip", "--fastq", "--end-1", R1, "--end-2", R2]
    command2 = ["atram.py", "-b", db, "-Q", "../PetromyzonExonReferences/PetromyzonFishLife.fa", "-o", "./aTRAM_output/trinity", "--cpus", "10", "-a", "trinity"]
    subprocess.run(command1)
    subprocess.run(command2)
    


home = os.getcwd()

for directory in glob.glob("*DDB*/"):
    if os.path.exists(directory+directory.split("/")[0]+".db.atram_preprocessor.log") == False:
        os.chdir(directory)
        os.mkdir("aTRAM_output/")
        atram(directory)
        os.chdir(home)
        output = open(directory.split("/")[0]+".step2.aTRAM.txt", "w")
        output.write(directory+" processed with aTRAM.")
        output.close()


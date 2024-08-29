#!/usr/bin/env python3

# import subprocess module
import subprocess


# Function to run cd-hit-est
def cdhitest(fasta,cvalue):
    ''' 
    Run CD-HIT-EST on a fasta file with a given -c value.
    CD-HIT must be in your path.
    '''
    outfile = fasta+".cdhit"
    command = ["cd-hit-est", "-i", fasta, "-o", outfile, "-c", cvalue]
    res = subprocess.run(command)
    return res

### Running CD-HIT for all aTRAM output

# Load glob module
import glob

# Run CD-HIT on filtered_contigs.fasta aTRAM output
for file in glob.glob("*.filtered_contigs.fasta"):
    cdhitest(file,"1")

# Function to run exonerate
def exonerate(contigs,query):
    '''
    Run exonerate coding2genome on the output from CD-HIT-EST based on a set of reference sequences.
    '''
    command = ["exonerate", "--model", "coding2genome", "-t", contigs, "-q", query, "--ryo", ">%ti\\t%qab-%qae\n%tas", "--showcigar", "F", "--showvulgar", "F", "--showalignment", "F", "--showsugar", "F", "--showquerygff", "F", "--showtargetgff", "F", "--bestn", "2" ]
    res = subprocess.run(command, capture_output=True)
    stdout = res.stdout
    stdoutstr = stdout.decode()  # converts a bytes obj to str
    n = len(stdoutstr.split("\n")) - 2 # need to drop the first three and last two lines of the exonerate output if you split by \n
    nout = stdoutstr.split("\n")[3:n]
    outfile = contigs+".exonerate.fa"
    output = open(outfile, "w")
    for item in nout:
        output.write(item+"\n")
    output.close()
    return "sequences written to " + outfile
    
### Running exonerate for all exons

# Make a list of reference sequences
refs = []
for file in glob.glob("../../PetromyzonExonReferences/*.fasta"):
    refs.append(file)

# Run exonerate
for ref in refs:
    locus = ref.split("/")[3].split(".")[0]
    contigs = glob.glob("*"+locus+"*.cdhit")
    if len(contigs) == 1:
        exonerate(contigs[0],ref)
        print("exonerate completed for " + contigs[0])
        
### Second Filter with CD-HIT on the exonerate output

# c-value reduced to 0.99 for potential allelic variation
for file in glob.glob("*.exonerate.fa"):
    cdhitest(file,"0.99")

### Final filter for contigs, if there is more than one contig remaining after the previous step, they are passed to ".failed"


# Load biopython modules
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


def formatfasta(fas, name):
    '''
    Replace Trinity fasta header with taxon name for files that passed filters. Reverse complements sequences if necessary.
    '''
    infas = list(SeqIO.parse(fas, "fasta"))
    aligned = infas[0].description.split("\t")[1]
    start = aligned.split("-")[0]
    end = aligned.split("-")[1]
    if int(start) < int(end):
        outfas = SeqRecord(infas[0].seq, id=name, description='')
        outfile = SeqIO.write(outfas, fas+".final_contig.fa", "fasta")
    else:
        rcseq = infas[0].seq.reverse_complement()
        outfas = SeqRecord(rcseq, id=name, description='')
        outfile = SeqIO.write(outfas, fas+".final_contig.fa", "fasta")


# Count the number of files that passed
passed = 0

for file in glob.glob("*.exonerate.fa.cdhit"):
    datafile = open(file, "r")
    data = datafile.read()
    contigs = data.count(">")
    datafile.close()
    if contigs == 1:
        taxon = file.split(".")[1]
        formatfasta(file, taxon)  # The function above will create the final_contig.fa file
        passed = passed + 1
        
summary = open("filtering_summary.txt", "w")
summary.write(str(passed)+" loci passed all filters")    
summary.close()



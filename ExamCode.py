#!/usr/bin/python3

#PROGRAM TO MAKE BLAST DATABASES AND DO BLAST ANALYSES
##WARNING: CURRENTLY ONLY BLASTP IMPLEMENTED, SO PROGRAM WILL ONLY PROPERLY WORK WITH PROTEIN/PROTEIN INPUTS. BEWARE OF THAT!

#Import modules needed
import os
import subprocess
import pandas as pd

#Set user workspace
chdir = ("cd /localdisk/home/$USER")
subprocess.check_output(chdir, shell=True)

#Create a new directory to store the results
Directory = input("Type in a name for the directory that will be created in your workspace: ")
os.mkdir(Directory)
os.chdir(Directory)

#Create source directory to keep results tidy
os.mkdir("src")
os.chdir("src")

##Some options for the user
yes = {'yes','y', 'ye', 'YES', 'Yes'}
no = {'no','n', 'No', 'NO'}

#Function to get the desired sequences using ESEARCH against NCBI databases
def ESEARCH_get(user_orgn, user_seq, type ):
	print("Then, the program will guide you to find and download your desired query sequence(s) from the NCBI databases. ")
	GeneralES = 'esearch -db protein -query "{}[Organism] AND {}[{}]" | efetch -db protein -format fasta > {}.fasta'.format(user_orgn, user_seq, type, user_orgn)
	GeneralESout = subprocess.check_output(GeneralES, shell=True)
	return(GeneralESout)

##Loop that allows the user to decide to use their own sequence files or fetch them from NCBI databases
#Option of getting DNA or protein sequences
i = 0
while (i == 0):
	user_query_input = input("Do you have your own DNA or protein file that you would like to use as a QUERY? :")
	user_db_input = input("Do you have your own DNA or protein file that you would like to use as a DATABASE? :")
	##GET QUERY SEQUENCE(S)
	if user_query_input in yes:
		i=1
		user_query_file = input("Please type in the name of your file (the full path, please! I don't know where you store your things ;) ) ")
		query = open(user_query_file).read()
		print(query)
	if user_query_input in no:
		i=1
		print("Then, the program will guide you to find and download your desired query sequence(s) from the NCBI databases. ")
		user_query_orgn = input("Please type in the name of your organism of interest for your QUERY: ")
		##IMPROVEMENT: Need to implement error trap here in case user does not say protein or gene
		search = input("Do you want your query to be made of proteins or DNA sequences? Type protein or gene: ")
		seq = input("Please type in the sequence that you are interested in (name of a protein: ")
		query = ESEARCH_get(user_query_orgn, seq, search)
		user_query_file = "{}.fasta".format(user_query_orgn)
	else:
		print("Please answer yes or no!")
	##GET DB SEQUENCES
	if  user_db_input in yes:
		i=1
		user_db_file = input("Please type in the name of the file you want to use for your DATABASE (the full path, please!) : ")
		DB = open(user_db_file).read()
		
	if user_db_input in no:
		i=1
		search = input("Do you want your database to be made of proteins or DNA sequences? Type protein or gene: ")
		user_db_orgn = input("Please type in the name of your organism/taxon of interest for your DATABASE: ")
		seq_db = input("Please type in the name of the protein/gene that you are interested in (name of a protein): ")
		DB = ESEARCH_get(user_db_orgn, seq_db, search)
		user_db_file = "{}.fasta".format(user_db_orgn)
	else:
		print("Please answer yes or no!")

##CREATE FUNCTION THAT GENERATES A BLAST DATABASE AND RUNS BLAT FROM PYTHON

#Improvement: choose correct BLAST flavour depending on user input. Currently only BLASTP implemented.

def BLASTP(seq, db): 
	BlastDB = "makeblastdb -in {} -dbtype prot".format(db)
	BlastP = "blastp -query {} -db {} -num_threads 10 -outfmt 7 -out blastout.txt".format(seq, db)
	BlastDBOut = subprocess.check_output(BlastDB, shell=True)
	print("Database created")
	BlastPOut = subprocess.check_output(BlastP, shell=True)
	print("BLAST analysis performed")



##RUN BLAST FOR THE DIFFERENT INPUTS

BLASTP(user_query_file, user_db_file)


#Sort BLAST results by similarity using Pandas
def SortBLAST_similarity(BLASTout): 
        df = pd.read_csv(BLASTout,sep='\t', skiprows=(0,1,2,3,4), header=None)
        df.columns = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
        pd.concat([pd.DataFrame(df.columns), df], ignore_index=True)
        ##Column 3 contains the similarity values
        dfsorted = df.sort_values('3', ascending = False)
        print("Sorted by similarity")
        return dfsorted

dfsorted = SortBLAST_similarity("blastout.txt")
print(dfsorted)

import csv
from Bio import SeqIO
import pandas as pd
import numpy as np
import pickle
import argparse

import warnings
def warn(*args, **kwargs): pass
warnings.warn = warn


parser = argparse.ArgumentParser(description="Prediction of TMD's affinity to EMC")
parser.add_argument('fasta_file', type=str, help='Name of the fasta file to be parsed')
args = parser.parse_args()


features = dict()
f = open("significant_features.csv", "r")
t = csv.reader(f, delimiter = "\t")
for row in t:
	feature = row[0]
	pos = row[1]
	corr = float(row[2])
	if feature not in features:
		features[feature] = []
	features[feature].append(pos)
f.close()


f = open("aaindex1")
aaindex = dict()
values = []
order = 0
for line in f.readlines():
	line = line[:-1]
	if line.startswith("H"):
		feature = line.split("H ")[1]
	if line.startswith("I"):
		order = 1
	if line.startswith(" ") and order == 1:
		for x in line.split(" "):
			if x != '':
				if x != 'NA':
					x = float(x)
				values.append(x)
	if line.startswith("//"):
		aaindex[feature] = values
		values = []
		order = 0

AAs = 'ARNDCQEGHILKMFPSTWYV'

aaindex_AA = dict()
for key in aaindex:
	aaindex_AA[key] = dict()
	for i in range(len(aaindex[key])):
		aaindex_AA[key][AAs[i]] = aaindex[key][i]
		
f.close()


def split(s, n):
	a = list(s)
	k, m = divmod(len(a), n)
	r = []
	for i in range(n):
		rp = a[i*k+min(i, m):(i+1)*k+min(i+1, m)]
		r.append("".join(rp))
	return r


indeces = [1,2,4,5,6]

columns = []
for feature in features:
	for ind in indeces: 
		columns.append(feature+"_"+str(ind))
columns.append("TMD")
df = pd.DataFrame(columns=columns)

for record in SeqIO.parse(args.fasta_file, "fasta"):
	s = str(record.seq)
	d = record.description
	if len(s) >= 9:
		s_parts = split(s, 9)
		s_parts = [s_parts[index] for index in indeces]
		row = []
		for feature in features:
			for prt in s_parts: 
				values = []
				for letter in prt:
					value = aaindex_AA[feature][letter]
					values.append(value)
				extr = np.mean(values)
				row.append(extr)
		row.append(d)
		df.loc[len(df)] = row
	else:
		print("Sequence " + d + " will be skipped as it is less than 9 residues" +"\n")


model_pkl_file = "regr.pkl"
with open(model_pkl_file, 'rb') as file:  
    regr = pickle.load(file)

X_unknown = df.iloc[:, :-1].values
sequences = df.iloc[:, -1].values

predictions_unknown = regr.predict(X_unknown)

f = open("predicted_affinity.csv", "w")
f.write("TMD"+"\t"+"Affinity to EMC"+"\n")
for i in range(len(predictions_unknown)):
	aff = predictions_unknown[i]
	s = sequences[i]
	f.write(s+"\t"+str(aff)+"\n")
f.close()

print("Prediction is done. Please check predicted_affinity.csv")

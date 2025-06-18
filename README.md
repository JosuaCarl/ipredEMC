# ipredEMC
ipredEMC - intramembrane binding predictor for the EMC protein complex

The script "prediction.py" predicts the transmembrane domain's (TMD) affinity to endoplasmic reticulum membrane complex (EMC) based on the given fasta file containing protein sequences of TMDs.

Dependencies

    Python 3.x
    Biopython 1.80
    pandas 1.5.3
    numpy 1.23.5
    pickle 4.0
    argparse 1.1
    warnings

Usage

    Run the script by providing the fasta file name as a command-line argument. For example 
    
    	python3 prediction.py TMDs_example.fasta
    
    The script will parse the fasta file and extract sequences with 9 or more residues. The predicted affinity of TMD to EMC will be saved in a file named "predicted_affinity.csv". 
    
    For the correct prediction provide the sequences of the TMD from "exo" part to "cyto" part, regardless C- or N- terminus. 
    
Other files

    "significant_features.csv": Contains the list of significant features used for prediction.
    "aaindex1": Contains the Amino Acid Index data used for feature calculation.
    "regr.pkl": Pre-trained model for prediction.
    "predicted_affinity.csv": Output file with predicted affinities for TMD sequences.
    "TMDs_example.fasta": example of fasta file with sequences of TMDs

Contact
     
     mar.ark.parr - at - gmail.com

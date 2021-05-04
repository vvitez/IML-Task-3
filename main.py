""" 
Ok here we go. Let's acquire the bread of this task.
"""
import numpy as np 
import pandas as pd 



amino_category = {#already ordered by chemical closeness and chain length/van-der-waals/hydrogen bonds
#positively charged:
    'K' : 0,#Lysine
    'R' : 0,#Arginine
    'H' : 0,#Histidine
#negatively charged:
    'D' : 1,#Aspartic Acid
    'E' : 1,#Glutamic Acid
#uncharged:
    'T' : 2,#Threonine
    'S' : 2,#Serine
    'N' : 2,#Asparagine
    'Q' : 2,#Glutamine
#special cases:
    'G' : 3,#Glycine
    'C' : 3,#Cysteine
    'U' : 3,#Selenocysteine
    'P' : 3,#Proline
#Hydrophobic:
    'A' : 4,#Alanine
    'V' : 4,#Valine
    'I' : 4,#Isoleucine
    'L' : 4,#Leucine
    'M' : 4,#Methionine
    'F' : 4,#Phenylalanine
    'W' : 4,#Tryptophan
    'Y' : 4 #Tyrosine
}

amino_order = {#this time i start at 1 for nn reasons
    'K' : 1,#Lysine
    'D' : 1,#Aspartic Acid
    'T' : 1,#Threonine
    'G' : 1,#Glycine
    'A' : 1,#Alanine
    'R' : 2,#Arginine
    'E' : 2,#GluIsoleucine
    'Q' : 4,#Glutamine
    'P' : 4,#Proline
    'L' : 4,#Leucine
    'M' : 5,#Methionine
    'F' : 6,#Phenylalanine
    'W' : 7,#Tryptophan
    'Y' : 8 #Tyrosine
}

data = pd.read_csv(filepath_or_buffer="train.csv", nrows = 10)
data["Sequence"].apply(lambda x: pd.Series(list(x)))
data["amino_ord_0"] = np.nan
data["amino_ord_1"] = np.nan
data["amino_ord_2"] = np.nan
data["amino_ord_3"] = np.nan

#for pos,seq in enumerate(data[Sequence]):
#    data["amino_cat_0"][pos] = seq[0]
data[0] = ""
data[0][0] = "hello"
print(data["Sequence"][0])
print(data.head(5))
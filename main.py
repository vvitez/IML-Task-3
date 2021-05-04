""" 
Ok here we go. Let's acquire the bread of this task.
"""
import numpy as np 
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import f1_score
#f1_score(y_true, y_predicted)

from util import Logger, Timer


logger: Logger = Logger()
script_timer = Timer()

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
    'E' : 2,#Glutamic Acid
    'S' : 2,#Serine
    'C' : 2,#Cysteine
    'V' : 2,#Valine
    'H' : 3,#Histidine
    'N' : 3,#Asparagine
    'U' : 3,#Selenocysteine
    'I' : 3,#Isoleucine
    'Q' : 4,#Glutamine
    'P' : 4,#Proline
    'L' : 4,#Leucine
    'M' : 5,#Methionine
    'F' : 6,#Phenylalanine
    'W' : 7,#Tryptophan
    'Y' : 8 #Tyrosine
}


def read_data(filename) -> pd.DataFrame:
	"""
		Read the data of a csv file into a pandas DataFrame
		
		Parameters:
			filename: The filename to read from
		
		Returns:
			Pandas DataFrame containing the data from the csv file
		
		Authors:
			linvogel
	"""
	return pd.read_csv(filename)

def split_data(data: pd.DataFrame, a_cols: list[str], b_cols: list[str]) -> (pd.DataFrame, pd.DataFrame):
	"""
		Splits the given pandas DataFrame into two collections of columns. This can be used to split features and labels provided in a single csv file.csv
		
		Parameters:
			data: The pandas DataFrame containing the data
			a_cols: List of column names that should be in the left side of the split
			b_cols: List of column names that should be in the right side of the split
		
		Returns:
			A tuple of two pandas DataFrames containing the left and right side of the split
		
		Authors:
			linvogel
	"""
	features: pd.DataFrame = data.drop(b_cols, axis=1) # drop the columns named in b_cols, aka the features
	labels: pd.DataFrame = data.drop(a_cols, axis=1) # drop the columns named in b_cols, aka the labels
	return features, labels


logger.info_begin("Reading data...")
read_timer = Timer()
data = read_data("train.csv")
#data = pd.read_csv(filepath_or_buffer="train.csv",nrows= 5000)
pSequence, pActive = split_data(data, a_cols=['Sequence'], b_cols=['Active'])

#test_features = read_data("test.csv"), TODO: do that later
logger.info_end("Done in " + str(read_timer))

ndSequence = pSequence.values.T[0]
ndActive = pActive.values.T[0]


logger.info_begin("Preprocessing...")
proc_timer = Timer()


features = np.zeros(shape = (len(ndActive), 25), dtype= np.int64,)#0-0, .., 0-4, ..., 3-4, 0_ord, ..., 3_ord, bias

for pos, seq in enumerate(ndSequence):
    if pos % 1000 == 0: logger.info_update("%d" %pos)
    for i in range(4):
        features[pos,i*5 + amino_category[seq[i]]] = 1
        features[pos, 20 + i] = amino_order[seq[i]]
    features[pos, 24] = 1 #bias
logger.info_end("Done in " + str(proc_timer))

x_train, x_test, y_train, y_test = train_test_split(features, ndActive, test_size = 0.1, random_state = 42, shuffle = True)

#logger.info_begin("Training Classifier...")
train_timer = Timer()
classifier = MLPClassifier(hidden_layer_sizes = (100), activation = "relu", solver = "adam", alpha = 0.0001, batch_size = 200, learning_rate = "constant", learning_rate_init = 0.001, max_iter = 1000, shuffle = False, tol = 1e-4, verbose = True, warm_start = False, beta_1 = 0.9, beta_2 = 0.999, epsilon = 1e-8, n_iter_no_change = 100)
# ah yes big chungus.
classifier.fit(x_train, y_train)
#logger.info_end("Done in " + str(train_timer))

y_pred = classifier.predict(x_test)

score = f1_score(y_test, y_pred)
print("Test F1 score: %f" %score)

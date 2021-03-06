# -*- coding: utf-8 -*-
"""tdalkilic_23994_cs412hw1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15b3xggJuThpVrrQHydim08cwC-W-pCjp

# Load the dataset
"""

from google.colab import drive
drive.mount('/content/drive')

# You can find the data under https://drive.google.com/drive/folders/1e550az93U3_kfRBbVY5PZnMKYwGYmHqi?usp=sharing

import pandas as pd
import numpy as np

train_data = pd.read_csv("/content/drive/My Drive/Colab Notebooks/train_data.csv") 
train_label = pd.read_csv("/content/drive/My Drive/Colab Notebooks/train_label.csv") 

test_data = pd.read_csv("/content/drive/My Drive/Colab Notebooks/test_data.csv")
test_label = pd.read_csv("/content/drive/My Drive/Colab Notebooks/test_label.csv")

# show random samples from the training data

train_data.sample(n=5)

"""# Train Decision Tree with default parameters"""

from sklearn.tree import DecisionTreeClassifier

# Train decision tree using the whole training data with **entropy** criteria

dt = DecisionTreeClassifier(criterion="entropy")
dt.fit(train_data,train_label)


# Estimate the prediction of test data
test_pred = dt.predict(test_data)

# Calculate accuracy of test data
from sklearn.metrics import accuracy_score
TestAcc = accuracy_score(test_label,test_pred)

print("Testing Accuracy = %.5f%%" % (TestAcc * 100))

"""# FineTune Decision Tree parameters

1- Spliting dataset into train and validation
"""

# Split training data to 70% training and 30% validation
from sklearn.model_selection import train_test_split
x_train, x_val, y_train, y_val = train_test_split(train_data,train_label,test_size=0.3)

"""2- FineTune minimum sample split"""

min_samples_splits = range(2, 100)

train_results = []
val_results = []
for min_samples_split in min_samples_splits:
  
  # Fit the tree using the 70% portion of the training data
  dtsecond = DecisionTreeClassifier(criterion="entropy",min_samples_split= min_samples_split)
  dtsecond.fit(x_train, y_train)
  
  # Evaluate on Training set
  train_pred = dtsecond.predict(x_train)
  train_acc = accuracy_score(y_train, train_pred)
  train_results.append(train_acc)
   
  # Evaluate on Validation set
  val_pred = dtsecond.predict(x_val)
  val_acc = accuracy_score(y_val, val_pred)
  val_results.append(val_acc)
  
# Ploting
import matplotlib.pyplot as plt

plt.plot(min_samples_splits, train_results, 'b')
plt.plot(min_samples_splits, val_results,'r')
plt.show()

# Choose the best minimum split sample based on the plot
Best_minSampl = 50

# Train decision tree using the full training data and the best minimum split sample
ms= DecisionTreeClassifier(criterion="entropy",min_samples_split= Best_minSampl)
ms = ms.fit(train_data, train_label)

# Estimate the prediction of the test data
test_pred = ms.predict(test_data)

# Calculate accuracy of test data
TestAcc = accuracy_score(test_label, test_pred)
print("Testing Accuracy = %.5f%%" % (TestAcc * 100))

"""# Now, apply the same procedure but using KNN instead of decision tree 

# For finetuning, find the best value of K to use with this dataset.
"""

# Write your code here

from sklearn.neighbors import KNeighborsClassifier

# initialize the values of k to be a list of odd numbers between 1 and 30
kVals = range(1, 30, 2)

# Save the accuracies of each value of kVal in [accuracies] variable
# hint: you can use accuracies.append(...) function inside the loop
accuracies = []

# loop over values of k for the k-Nearest Neighbor classifier
for k in kVals:
  model = KNeighborsClassifier(n_neighbors=k)
  model.fit(x_train,y_train.values.ravel())
  score = model.score(x_val,y_val)
  accuracies.append(score)  
  print("For k = %d, validation accuracy = %.5f%%" % (k, score * 100))

# Train KNN using the full training data with the best K that you found
max_index = np.argmax(accuracies)  
model2 = KNeighborsClassifier(n_neighbors=kVals[max_index])
model2.fit(train_data, train_label.values.ravel())

# Testing
predict2= model2.predict(test_data)
TestAcc2 = accuracy_score(test_label, predict2)
print("Testing Accuracy = %.5f%%" % (TestAcc2* 100))

"""# Bonus

# Apply gridsearch using decision tree on any hyperparameter(s) of your choice, you have to beat your previous obtained accuracies to get the bonus
"""

# Write your code here
from sklearn.model_selection import GridSearchCV

grid_tree_model= DecisionTreeClassifier()
param_grid = {'max_depth': np.arange(3, 10),'max_leaf_nodes': list(range(2, 20))}
grid = GridSearchCV(grid_tree_model, param_grid)

grid.fit(train_data,train_label)


test_pred_grid = grid.predict(test_data)
TestAcc3 = accuracy_score(test_label, test_pred_grid)
print("Testing Accuracy in grid search is = %.5f%%" % (TestAcc3* 100))

"""# Report: Write a summary of your approach to this problem; this should be like an abstract of a paper or the executive summary (you aim for clarity and passing on information, not going to details about known facts such as what decision trees are, assuming they are known to people in your research area).

Must include statements such as:


*   Include the problem definition: 1-2 lines
*   Talk about train/val/test sets, size and how split.
*   State what your test results are with the chosen method, parameters: e.g. "We have obtained the best results with the ….. classifier (parameters=....) , giving classification accuracy of …% on test data…."
*   Comment on the speed of the algorithms and anything else that you deem important/interesting (e.g. confusion matrix)

# Write your report in this cell
In this assignment, how accurate prediction of data is choosen by changing hyperparameters and seperating data are studied.Without seperating training data,with default parameters accuracy was measured in 68.12 percent.After that, training data was seperated into 70 percent as training and 30 percent as validation. As minimum split sample, at nearly sample size 50, training and validation results get closer.The accuracy by dividing 70 and 30 (training and validation respectively) was resulted as 71.98 percent when 50 is choosen as best minimum sample size.

In KNN part, between 1 and 30 as k value, all k-nearest validation accuracy increases mostly as k increases.The best K , 15 in my trials, was choosen as testing accuracy parameter to measure accuracy.KNN accuracy was measured as 71.01 percent.

In grid search, by adding restrictions as max depth and max leaf nodes, the accuracy increased to 73.42 percent.Before adding max_leaf parameter, all methods (default parameter, splitting 70 and 30, KNN and grid) was working under 1 seconds. After i add max_leaf constraint, grid method working time increased to 7-8 seconds.
..

..

..

# New Section
"""
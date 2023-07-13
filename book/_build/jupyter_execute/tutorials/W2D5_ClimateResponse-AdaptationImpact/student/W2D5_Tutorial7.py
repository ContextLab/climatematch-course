#!/usr/bin/env python
# coding: utf-8

# # Tutorial 7:  Logisitc Regression on Crops Dataset
# 
# **Week 2, Day 5: Climate Response: adaptation and impact**
# 
# **By Climatematch Academy**
# 
# __Content creators:__ Deepak Mewada, Grace Lindsay
# 
# __Content reviewers:__ Name Surname, Name Surname
# 
# __Content editors:__ Name Surname, Name Surname
# 
# __Production editors:__ Name Surname, Name Surname

# ___
# # **Tutorial Objectives**
# 
# *Estimated timing of tutorial: 10 minutes*
# 
# Welcome to tutorial 7 of a series focused on understanding the role of data science and machine learning in addressing the impact of climate change and adapting to it.
# 
# In this tutorial, we will explore how to train a logistic regression model on a crops dataset. By the end of this tutorial, you should be able to:
# 
# 1. Load and preprocess the dataset
# 2. Fit a logistic regression model on the preprocessed data
# 3. Evaluate the model performance using scikit-learn
# 4. Understand and reflect on different performance metrics
# 5. Compare and evaluate different feature importance methods
# 
# 
# ---

# ##  Tutorial slides
# 

#  These are the slides for the videos in all tutorials today
# 

# In[ ]:


# @title Tutorial slides

# @markdown These are the slides for the videos in all tutorials today
from IPython.display import IFrame
IFrame(src=f"https://mfr.ca-1.osf.io/render?url=https://osf.io/kaq2x/?direct%26mode=render%26action=download%26mode=render", width=854, height=480)


# 
# 
# ---
# # **Setup**

# ##  Import necessary libraries:
# 

# In[ ]:


#@title Import necessary libraries:

import numpy as np
# Import the LogisticRegression class from the sklearn.linear_model module
from sklearn.linear_model import LogisticRegression
import sklearn.metrics as skm
import matplotlib.pyplot as plt


# <details>
# <summary> <font color='Red'>Click here if you are running on local machine or you encounter any error while importing   </font></summary>
# **NOTE :**  Please note that if you are running this code on a local machine and encounter an error while importing a library, make sure to install the library via pip. For example, if you receive a "`ModuleNotFoundError: No module named 'library name'`" error , please run "`pip install 'library name'`" to install the required module.

# ##  Plotting functions
# 

#  Run this cell to define all plotting function we will be suing in this tutorial
# 

# In[ ]:


# @title Plotting functions
#@markdown Run this cell to define all plotting function we will be suing in this tutorial
def plot_feature_performance(missing_feature_performance, only_feature_performance):
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Plot missing feature performance
    ax1.bar(range(12), missing_feature_performance)
    ax1.set_xticks(range(12))
    ax1.set_xticklabels([f"Without Feature {i}" for i in range(1, 13)], rotation=90)
    ax1.set_ylabel("Performance")
    ax1.set_title("Impact of Missing Features on Model Performance")
    ax1.yaxis.grid(True)

    # Plot only one feature performance
    ax2.bar(range(12), only_feature_performance)
    ax2.set_xticks(range(12))
    ax2.set_xticklabels([f"Feature {i+1}" for i in range(12)], rotation=90)
    ax2.set_ylabel("Performance")
    ax2.set_title("Impact of Single Features on Model Performance")
    ax2.yaxis.grid(True)

    # Adjust spacing between subplots
    plt.subplots_adjust(wspace=0.4)

    plt.show()


def plot_permutation_feature_importance(perm_feat_imp, X_test):
    """
    Plots feature importance using the permutation importance method.

    Args:
        perm_feat_imp (dict): A dictionary containing feature importance scores and statistics.
        X_test (ndarray): The testing data.
    """
    # create a figure and axis object using subplots
    fig, ax = plt.subplots()

    # create a bar plot for feature importance
    # set the x-axis to be the feature index
    # set the y-axis to be the mean importance score
    # set the error bar to be the standard deviation of importance scores
    ax.bar(np.arange(X_test.shape[1]), perm_feat_imp['importances_mean'],
           yerr=perm_feat_imp['importances_std'])

    # set the x-tick labels to be the feature names
    ax.set_xticks(np.arange(X_test.shape[1]))
    #ax.set_xticklabels(feature_names, rotation=90)

    # set the x and y axis labels and title
    ax.set_xlabel('Feature index')
    ax.set_ylabel('feature Importance')
    ax.set_title('Feature Importance using Permutation Importance Method')

    # display the plot
    plt.show()


# --- 
# # **Section 1: Training a Logisitic Regression Model on Crops Data**
# ---
# 
# 
# 
# 

# ##  Video 1: Video 1 Name
# 

# In[ ]:


# @title Video 1: Video 1 Name
from ipywidgets import widgets
from IPython.display import display, IFrame, YouTubeVideo

out2 = widgets.Output()
with out2:
  class BiliVideo(IFrame):
    def __init__(self, id, page=1, width=400, height=300, **kwargs):
      self.id=id
      src = 'https://player.bilibili.com/player.html?bvid={0}&page={1}'.format(id, page)
      super(BiliVideo, self).__init__(src, width, height, **kwargs)

  video = BiliVideo(id="", width=730, height=410, fs=1)
  print(f'Video available at https://www.bilibili.com/video/{video.id}')
  display(video)

out1 = widgets.Output()
with out1:
  video = YouTubeVideo(id="", width=730, height=410, fs=1, rel=0)
  print(f'Video available at https://youtube.com/watch?v={video.id}')
  display(video)

out = widgets.Tab([out1, out2])
out.set_title(0, 'Youtube')
out.set_title(1, 'Bilibili')

display(out)


# Now that we understand our remote sensing data set we can train a model to classify each point as either containing or not containing crops. The data is already separated into training and test sets. Use what you've learned to train a logistic regression model on the training data. Evaluate the model separately on both the training set and test set according to the overall classification accuracy. 

# 
# ---
# ## Section 1.1:  Dataset loading and Preprocessing
# ---
# 
# 
# 

# In[ ]:


#Load the data from the specified file path
import os, pooch
fname = 'togo_crops_data.npz'
if not os.path.exists(fname):
    url = "https://osf.io/4tqhe/download"
    fname = pooch.retrieve(url, known_hash=None)
data = np.load(fname)

# The following lines extract the training and test data arrays from the loaded dataset
X_train = data['arr_0']
y_train = data['arr_1']
X_test = data['arr_2']
y_test = data['arr_3']


# 
# 
# ---
# 
# 
# ## Section 1.2: Model Fitting on Data
# 
# ---
# 
# 

# ### Coding Exercise 1.2: Fitting a Logistic Regression Model and Evaluation using scikit-learn
# In this exercise, you will use `LogisticRegression` from scikit-learn to train a logistic regression model on the Togo crops dataset. First, fit the model to the training data, and then evaluate its accuracy on both the training and test data using the `.score()` method. Finally, print the training and test accuracy scores.

# In[ ]:


def evaluate_model(X_train, y_train, X_test, y_test):
    """
    Fits a logistic regression model to the training data and evaluates its accuracy on the training and test sets.

    Parameters:
    X_train (numpy.ndarray): The feature data for the training set.
    y_train (numpy.ndarray): The target data for the training set.
    X_test (numpy.ndarray): The feature data for the test set.
    y_test (numpy.ndarray): The target data for the test set.

    Returns:
    tuple: A tuple containing the training accuracy and test accuracy of the trained model.
    """

    #################################################
    ## TODO for students: Fits a logistic regression model to the training data and evaluates its accuracy on the training and test sets ##
    # Fill out function and remove
    raise NotImplementedError("Student exercise: Fill in the code in empty places to remove this error")
    #################################################

    # Create an instance of the LogisticRegression class and fit it to the training data
    trained_model = ... #todo

    # Calculate the training and test accuracy of the trained model
    train_accuracy = ... #todo
    test_accuracy = ... #todo

    # Return the trained_model, training and test accuracy of the trained model
    return trained_model,train_accuracy, test_accuracy

## Uncomment the code below to test your function
#trained_model, train_acc, test_acc = evaluate_model(X_train, y_train, X_test, y_test)
#print('Training Accuracy: ', train_acc)
#print('Test Accuracy: ', test_acc)


# 
# 
# 
# 
# ```
# The result should look like: 
# Training Accuracy:  0.7511627906976744  
# Test Accuracy:  0.7352941176470589
# ```
# 
# 

# [*Click for solution*](https://github.com/NeuromatchAcademy/course-content/tree/main//tutorials/W2D5_ClimateResponse-AdaptationImpact/solutions/W2D5_Tutorial7_Solution_0fa7ad53.py)
# 
# 

# 
# 
# ---
# 
# ## Section 1.3:  Further Evaluation of Performance
# ---
# 
# As discussed in the video,in some cases, overall accuracy of a machine learning model can be misleading, as it may not reveal how the model is performing in different areas. **Precision** and **recall** are two important metrics that can help evaluate the performance of a model in terms of its ability to correctly identify positive cases (precision) and to identify all positive cases (recall).
# 
# In this section, we will calculate precision and recall on the test set of our model using scikit-learn's built-in evaluation functions: `precision_score()` and `recall_score()`. For more information on these functions, please refer to their documentation : [precision](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html) and [recall](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html)
# 
# 
# 
# 

# ### Coding Exercise 1.3:  Evaluating Performance with Precision and Recall
# In this exercise, you will evaluate the performance of a machine learning model using precision and recall metrics. We will provide you with a trained model, a test set X_test and its corresponding labels y_test. Your task is to use scikit-learn's built-in evaluation functions, precision_score() and recall_score(), to calculate the precision and recall on the test set. Then, you will print the results.
# 
# To complete this exercise, you will need to:
#  
# - Use the trained model to make predictions on the test set.  
# - Calculate the recall score and precision score on the test set using scikit-learn's recall_score() and precision_score() functions, respectively.  
# 

# In[ ]:


def evaluate_model_performance(trained_model, X_test, y_test):
    """
    Evaluate the performance of a trained model on a given test set suing recall and precision

    Parameters:
    trained_model (sklearn estimator): A trained scikit-learn estimator.
    X_test (array-like): Test input data.
    y_test (array-like): True labels for the test data.

    Returns:
    test_recall (float): The recall score on the test set.
    test_precision (float): The precision score on the test set.
    """

    #################################################
    ## TODO for students:Fill in the blank to use recall and precision.##
    # Fill out function and remove
    raise NotImplementedError("Student exercise: Fill in the code in empty places to remove this error")
    #################################################

    # Use the trained model to make predictions on the test set hint: use predict
    pred_test = ...

    # Calculate the recall and precision scores on the test set
    # test_recall = skm. .... #hint: call recall suing skm
    # test_precision = skm.   #hint: call preicision using skm


    # Return the recall and precision scores
    return ..., ...

# Evaluate the performance of the trained model on the test set
## Uncomment the code below to test your function
#test_recall, test_precision = evaluate_model_performance(trained_model, X_test, y_test)
# Print the results
#print('Test Recall: ', test_recall)
#print('Test Precision: ', test_precision)


# [*Click for solution*](https://github.com/NeuromatchAcademy/course-content/tree/main//tutorials/W2D5_ClimateResponse-AdaptationImpact/solutions/W2D5_Tutorial7_Solution_5513184a.py)
# 
# 

# ### Think! 1.3: Reflecting on performance metrics 
# 
# Looking at the results on the test data, which is your model better at: catching true crops that exist or not labeling non-crops as crops? 

# ---
# ## Section 1.4:  Another feature importance method
# ---
# 
# 
# 
# 
# Create a series of new datasets, each of which contains only 11 out of the 12 indepedent variables. Train and evaluate the accuracy of models using these different reduced datasets. Comparing the performances of these different models is one way of trying to understand which input features are most important for correct classification. Try also training a series of models that only use one feature at a time. According to these results, are there any features that seem especially useful for performance?

# In[ ]:


def calculate_performance(X_train, X_test, y_train, y_test):
    """
    Calculates performance with missing one features and only one feature using logistic regression.

    Args:
        X_train (ndarray): The training data.
        X_test (ndarray): The testing data.
        y_train (ndarray): The training labels.
        y_test (ndarray): The testing labels.

    Returns:
        missing_feature_performance (list): A list of performance scores for each missing feature.
        only_feature_performance (list): A list of performance scores for each individual feature.
    """

    #################################################
    ## TODO for students:Fill in the blank with appropriate code ##
    # Fill out function and remove the line below
    # raise NotImplementedError("Student exercise: Fill in the code in empty places to remove this error")
    #################################################

    missing_feature_performance = []  # Create empty list to store performance scores for each missing feature
    only_feature_performance = []  # Create empty list to store performance scores for each individual feature

    for feature in range(X_train.shape[1]):  # Iterate through each feature in the dataset
        # Remove the feature from both the training and test set
        X_train_reduced = np.delete(X_train, feature, 1)  # Remove feature from training set
        X_test_reduced = np.delete(X_test, feature, 1)  # Remove feature from test set
        reduced_trained_model = LogisticRegression().fit(..., ...)  # Train a logistic regression model on the reduced training set
        # missing_feature_performance.append(reduced_trained_model.score(..., ....))  # Calculate the score on the reduced test set and append to list

        # Select only the feature from both the training and test set
        X_train_reduced = X_train[:, feature].reshape(-1, 1)  # Select only feature from training set
        X_test_reduced = X_test[:, feature].reshape(-1, 1)  # Select only feature from test set
        # reduced_trained_model = LogisticRegression().fit(..., ....)  # Train a logistic regression model on the reduced training set
        only_feature_performance.append(reduced_trained_model.score(..., ...))  # Calculate the score on the reduced test set and append to list

    return missing_feature_performance, only_feature_performance

## Uncomment the code below to test your function
#missing_feature_performance, only_feature_performance = calculate_performance(X_train, X_test, y_train, y_test) # Call calculate_performance() function with the training and testing data and the corresponding labels
#plot_feature_performance(missing_feature_performance, only_feature_performance) # Plot the performance scores for each missing feature and each individual feature


# *Example output:*
# 
# ![image.png](data:image/png;base64,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d3eNRuPv7z9//nz5NxIXsW/fvuDgYGtr65o1a3777bd6q/f9998X95Dq1atHRETcvXtXfCsnJ2fSpEm1atXSaDTe3t5jx46VLxdlWYVqay5evPjKK6/o/S/t7u4uvTZr67Bly5YWLVrY2dk5ODh06tTp9OnTTytpmIHD+NWrV4cPH16nTh0bG5sqVaq8/fbbUpu4dOnSt99+WxCENm3aiGtY7CBeMGZ54yJu7r179w4fPtzd3b169epFfhcD7XJBu3btEutxdnZ+4403zpw5I71V5PovVHh4+JYtW6S94ujRo+fPny/YlFy6dOntt9+uXLmyra3tq6++umnTJvm7169f79atm52dnbu7+/vvv1/waGZgExSXvCnRarWJiYn169e3trb28PAYOnSo/JdVsBVQqVS7d+8+ffq0fINmZWWNGTPG29tbo9HUqVPniy++0Ol0UiVid9YVK1aIP6KtW7eKm3jfvn0jR450c3NzdnYeOnRobm7ugwcPIiIiXFxcXFxcxo4dK6/kiy++aNq0aZUqVWxsbIKCgtauXSv/RuIifv755wYNGmg0mvr162/dulVe4MaNGwMHDhQPEb6+vu+++25ubq741oMHD0aPHi0GX6tWrenTp2u12iLXoTLO0+fn53fo0KFly5aff/75ihUroqOj7ezsPvnkk759+7711ltJSUkRERFNmjTx9fWVPhIdHe3s7BwXF3fu3Ln58+dfvXpVbPgFQVi6dKm9vX1MTIy9vf2uXbsmTpyYkZExY8YM8YM7duzo3Lmzp6fnqFGjqlateubMmY0bN44aNWro0KE3b97csWPH8uXLDYQaFxcXHx8fGhr67rvvios+evTo/v37LS0tExMTv/32259++km82NSoUaOnVdKyZcvq1auvXLly8uTJgiCsWrXK3t6+U6dOBpbbvXv306dPv/feez4+Prdv396xY8e1a9fE1+3bt3dzcxs3bpyzs/OVK1cMd+To2bOnr69vQkLC8ePHv/nmG3d39+nTp4tv9e/ff/Xq1f369Xv11Vf37t1rOB5Rdna2lOsIguDk5GRpaXn69OlmzZp5eXmNGzfOzs5u9erV3bp1+/HHH998801BEC5duvTzzz+//fbbvr6+aWlpCxYsaNWq1d9//12tWrV69epNnjx54sSJQ4YMadGihSAITZs2LTIG0ZQpU6ysrD744IOcnBwrK6tdu3Z16NAhKCho0qRJarVazPB+++234OBgQRCGDRu2du3a6Ohof3//e/fu7du378yZMy+//HLBak+fPt2iRQtHR8exY8daWlouWLCgdevWe/fuDQkJkcq89957Li4ukyZNunLlSmJiYnR09KpVqwyEaszWf/ToUevWrS9cuBAdHe3r67tmzZr+/fs/ePBg1KhRgiDodLo33nhj3759w4YNq1ev3k8//RQZGakXtoFNUFwXL14UBKFKlSqCIEydOnXChAk9e/YcNGjQnTt35syZ07JlyxMnTkinT+7du9ehQ4fevXu/8847Hh4ejRs3Xrhw4ZEjR7755hvhfxt00KBBy5Yt69Gjx5gxYw4fPpyQkHDmzJmffvpJWuK5c+f69OkzdOjQwYMH16lTR5yZkJBgY2Mzbty4CxcuzJkzx9LSUq1W379/Py4u7tChQ0uXLvX19Z04caJYeP78+fXr1+/atWulSpU2bNgwfPhwrVY7YsQIaREXLlzo0aPHwIEDIyMjk5OT+/fvHxQUVL9+fUEQMjMzW7RocebMmQEDBrz88st3795dv3799evXXV1dtVpt165d9+3bN2TIkHr16v3111+zZ8/+559/fv755xKsWDx/FaetqVGjRkpKyvXr16XctEimah2WL18eGRkZFhY2ffr07Ozs+fPnN2/e/MSJEwa6wTx8+FDelFSuXFmtVhs+jB89evTAgQO9e/euXr36lStX5s+f37p167///tvW1rZly5YjR4786quvPv7443r16gmCIP41xvDhw93c3CZOnJiVlVXkd3lau1yw2p07d3bo0KFmzZpxcXGPHj2aM2dOs2bNjh8/Li9sYP0X6q233ho2bNi6devEE3krV66sW7euXkOWlpbWtGnT7OzskSNHVqlSZdmyZV27dl27dq3YFjx69Kht27bXrl0bOXJktWrVli9fvmvXLvnHDW+C4pI3JUOHDl26dGlUVNTIkSMvX7789ddfnzhxQty9xcLyVqB69erLly+fOnVqZmZmQkKCIAj16tXT6XRdu3bdvXv3wIEDAwMDt23b9uGHH964cUPeOWfXrl2rV6+Ojo52dXX18fERb9V77733qlatGh8ff+jQoYULFzo7Ox84cOCFF16YNm3a5s2bZ8yY0aBBg4iICLGGL7/8smvXrn379s3Nzf3hhx/efvvtjRs3yvf/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SH5osriPN6Db01tYWAQFBR05cmTYsGGEEP7m1+nTpzd85EcffbR06dIDBw706tWLakkAAMA0EWd1EjEmdrI4rwzJDCUzVzCSH5r8YM2e1Ul97k10dPSYMWN69eoVHBycmJhYUVHBf1oaGRnp6ekZHx9PCPnwww9jYmK2bdvm4+NTUFBACLG1tbW1taVdGwAAPPYeMKuTiDGxk8V5ZUhmKJm5gpH80OQHa/asTuo9/YgRI4qKimJiYgoKCrp3775//37+4sq1a9eUyr9X0kxKSqqurn7llVcMf2rhwoWxsbG0awMAAOaIOKuTiDGxk8V5ZUhmKJm5gpH80GRxH28gxT2y06dPbzjfJjU11XB85coVCcoAAIDHAGZ1AgA0ZFrr3gAAADwUZnUCANSDnh4AABiDWZ0AAPWgpwcAAPZgVicAgDFlSxcAAAAAAACCoKcHAAAAAGAbenoAAAAAALahpwcAAAAAYBt6egAAAAAAtqGnBwAAAABgG3p6AAAAAAC2oacHAAAAAGAbenoAAAAAALahpwcAAAAAYBt6egAAAAAAtqGnBwAAAABgG3p6AAAAAAC2oacHAAAAAGAbenoAAAAAALahpwcAAAAAYBt6egAAAAAAtqGnBwAAAABgG3p6AAAAAAC2oacHAAAAAGAbenoAAAAAALahpwcAAAAAYBt6egAAAAAAtqGnBwAAAABgG3p6AAAAAAC2oacHAAAAAGAbenoAAAAAALahpwcAAAAAYBt6egAAAAAAtqGnBwAAAABgG3p6AAAAAAC2oacHAAAAAGAbenoAAAAAALahpwcAAAAAYBt6egAAAAAAtlHv6T/99FMfHx+1Wh0SEvLzzz83fMDFixdffvllHx8fhUKRmJhIux4AAAAAgMcM3Z7+66+/jo6OXrhwYVpaWrdu3SIiIv766696j9HpdH5+fgkJCR4eHlSLAQCAxwYuGAEAGKPb069atWrSpEnjxo0LDAxct26dtbV1cnJyvcf07t17+fLlr732mqWlJdViAADg8YALRgAA9ZjRi66urj537ty8efP4L5VKZXh4+I8//ti8tKqqqqqqKv747t27hJCampqamppHCrFUcc179noaPq+JJzNXMJJZT2au4EaTafwREIXhghEhZN26dT/88ENycvLcuXONH9O7d+/evXsTQuqNAwA8lij29Ldu3dLr9e7u7oYR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T59Lly5lZWVptdpXXnlFSPKLL7748ssvl5eXV1dXv/3224bPW3/66SeBL4ySkpLBgwcrFAonJ6eOHTt27NjRyclJqVQ+++yzt2/fbnZsv379Gp0UJHzuzYQJE8aPH19v8Pr16wEBASZyKQUeb0OHDl2wYEHDceFnlt69e2/atKne4LRp0zQajcDXdteuXfft28cfnz9/vqamhj8+fvy4r6+vkGReWVlZZGRk165dz58/b25uLtbJpUuXLj169LC1td21a5dh/NixY56enkKSb9y44ePj079//+joaCsrqyeffHLSpEn9+/e3sLCod2Z/1IIbPbPU1dUJ/BB4/vz5rq6uEydO9PX1nTt3rre3d1JS0rp167y8vATetPDWW2917tx53759KSkpYWFhAwYM4Mf379/v7+8vJHnBggWOjo6rVq3KzMwsKCgoKCjIzMxctWqVk5PTwoULhSQPGjRo8eLFDceF/wB26dLF+JXGcVxNTc2wYcO8vb1N5OQi655+/fr1q1evbjheUFBgmEDWPDNmzGjYot29ezckJETgP/yUKVM2bNjQcDw+Pv65554TkszT6XRTpkxp166dSqUS5W1Xq9UaplEaV7548WKtVisw/PTp03369DH+fM3T01Pg9HHu/u+8whUUFDzzzDO2trYRERF37tyZPn264a6pP/74Q0hyTk6Ov7+/mZmZubm5RqPhb/DiOO6LL74QeN8C79KlS8nJycuWLVu2bFlycjI/60mIpUuXNvpTdu3atbFjxwpJvnLlyv79+xuO37hx48svvxSSDNAUx48fN/THxsrLy1NTU4UkL1u27Nlnn204HhUVJbBZSUpK+v777xuOz5s3b8KECUKSjW3fvt3d3V2pVIpycok1YvwjP3v27Ndee01g+O3bt997773AwEC1Wm1hYdG2bdvXX3+90VmITefj4yPWrVn16PX6pUuX/utf/1q2bFldXd327du9vLycnZ3Hjh1bXl4uJLmsrGz48OFmZmYKhaJfv36Gm48PHDiwc+dOgWUnJCS0atXKMAtaoVC0atVK4CU5juP27NmzefPmhuMlJSUCTwHvvvtuw7n+NTU1zz//vIn09AqO41r6o4LH0O3bt2/evPnEE0/UGy8rK0tLS9NqtaI/Y15enlqtNv78UYhvv/326NGj8+bNE/ix3QPk5uZaWFi0adNGeFRRUVFu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)

# [*Click for solution*](https://github.com/NeuromatchAcademy/course-content/tree/main//tutorials/W2D5_ClimateResponse-AdaptationImpact/solutions/W2D5_Tutorial7_Solution_15925f81.py)
# 
# 

# 
# 
# ---
# 
# 
# ## (Bonus) Section 1.5: Compare to Permutation Feature importance
# 
# ---
# 
# 
# 
# 
# Use what you learned to also implement the permutation method of estimating feature importance on this model. 

# ### Coding Exercise : Evaluate and plot feature importance with the permutation method
# For this exercise, you have to evaluate and plot feature importance with the permutation method using the `permutation_importance` function from [sklearn.inspection](https://scikit-learn.org/stable/modules/generated/sklearn.inspection.permutation_importance.html).
# 
# Here are the steps to follow:
# 
# 1. Import `permutation_importance` from `sklearn.inspection`.
# 2. Calculate the permutation feature importance using trained_model, X_test, and y_test.
# 3. Set the number of repeats to 10 and random state to 0.

# In[ ]:


#################################################
## TODO for students:
# Fill in the code in empty places to remove this error
# raise NotImplementedError("Student exercise: Fill in the code in empty places to remove this error")
#################################################

# Evaluate and plot feature importance with the permutation method

# import permutation_importance from sklearn.inspection
from sklearn.inspection import permutation_importance

# calculate the permutation feature importance using trained_model, X_test and y_test
# set n_repeats to 10 and random_state to 0
# perm_feat_imp = permutation_importance(..., ..., ...,
                                    #    n_repeats=.., random_state=...)

#### Uncomment the code below to test your solution
#plot_permutation_feature_importance(perm_feat_imp, X_test)


# [*Click for solution*](https://github.com/NeuromatchAcademy/course-content/tree/main//tutorials/W2D5_ClimateResponse-AdaptationImpact/solutions/W2D5_Tutorial7_Solution_5348d632.py)
# 
# 

# <details>
# <summary> <font color='yellow'>Click here for description of code  </font></summary>
# The code is performing feature importance analysis using the permutation importance method. This method is used to determine the importance of features in a machine learning model by shuffling the values of each feature and measuring the effect on the model's performance.
# 
# The first step is to import the necessary libraries including `sklearn` for the permutation importance method. Then the permutation importance is computed using the `permutation_importance()` function, which takes the trained model, test data, and number of repeats as input.
# 
# The results of the permutation importance are stored in the `perm_feat_imp` variable.
# 
# Finally, a bar plot is generated using Matplotlib to visualize the feature importance values. 

# <details>
# <summary> <font color='yellow'>Click here for interpretation of plot  </font><font color=' red'>(first try to understand by yourself)  </font></summary>
# The plot generated shows the feature importance scores using the permutation importance method. Each bar represents the importance of a feature, with the height of the bar indicating the mean importance score across all permutations and the error bar indicating the standard deviation.
# 
# Features with higher importance scores are considered more important in predicting the target variable than those with lower scores. You can use this information to identify the most important features in your dataset and potentially reduce the dimensionality of your model by removing the least important features.
# 
# In this particular plot, the x-axis represents the feature index (or feature number), and the y-axis represents the feature importance score. The feature names are also included on the x-axis for better readability.

# 
# 
# ---
# 
# 
# # Section 2 : Reflection 
# 
# ---
# 
# 

# ### Think! 2: Comparing importance measures 
# 
# Do these two methods return similar results as to what features are most important? If not, why might they not? 

# 
# 
# ---
# 
# 
# # **Summary**
# 
# Estimated timing of tutorial: 
# 
# In this tutorial, we learned how to train a logistic regression model on a crops datase, and evaluate the performance of the model using various metrics such as accuracy, precision, and recall. We also learned about feature importance and explored two methods for determining feature importance: missing features-only one feature method and permutation importance. We implemented the permutation importance method using scikit-learn's permutation_importance function and visualized the results using a bar plot. Finally, we reflected on the performance of the model and the importance measures and discussed their implications.Remember to practice what you learned and experiment with different datasets and performance metrics.
# 
# ---
# 
# 

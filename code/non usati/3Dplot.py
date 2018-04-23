#-*- coding: utf-8 -*-

import json
import matplotlib.pyplot as plt
# Though the following import is not directly being used, it is required
# for 3D projection to work
from mpl_toolkits.mplot3d import Axes3D

from sklearn.cluster import KMeans



asin = 'B01AXOCCG2'
rev_scores = json.load(open('analisi_'+asin+'.json'))  

# range per la classificazione
target = []

final_score = []
variance, ver_purchase, rev_date, rev_user, rev_help = [], [], [], [], []

for rev in rev_scores:
    final_score.append(rev_scores[rev]['final_score'])

    # variance    
    variance.append(rev_scores[rev]['details']['variance'])
    
    # verified_purchase
    ver_purchase.append(rev_scores[rev]['details']['verified_purchase'])
    
    # review_date
    rev_date.append(rev_scores[rev]['details']['review_date'])
    
    # review_by_user
    rev_user.append(rev_scores[rev]['details']['review_by_user'])
    
    # review_helpfulness
    rev_help.append(rev_scores[rev]['details']['review_helpfulness'])
    

k = KMeans(n_clusters=3)
for i in range(0, 3):
    fig = plt.figure(i+1, figsize=(7, 6))
    
    #if i==0: el, az =45, 130    
    #elif i==1: el, az = 0, 130
    #else: el, az = 90, 0
        
    ax = Axes3D(fig, rect=[0, 0, 1, 1], elev=45, azim=130)
    X = zip(variance, ver_purchase, rev_date, rev_user, rev_help)
    pred = k.fit_predict(X)

    if i==0: x_axis, y_axis, z_axis = variance, ver_purchase, rev_date    
    elif i==1: x_axis, y_axis, z_axis = variance, rev_help, rev_date
    else: x_axis, y_axis, z_axis = rev_help, ver_purchase, rev_date    
    ax.scatter(x_axis, y_axis, z_axis, c=pred, edgecolor='k')
    
    #ax.w_xaxis.set_ticklabels([])
    #ax.w_yaxis.set_ticklabels([])
    #ax.w_zaxis.set_ticklabels([])
   
    if i==0:     
        ax.set_xlabel('\nvariance')
        ax.set_ylabel('\nver_purchase')
        ax.set_zlabel('\nrev_date')
        ax.set_title('variance - ver_purchase - rev_date')
    elif i==1: 
        ax.set_xlabel('\nvariance')
        ax.set_ylabel('\nrev_help')
        ax.set_zlabel('\nrev_date')
        ax.set_title('variance - review_helpfulness - rev_date')
    else:  
        ax.set_xlabel('\nrev_help')
        ax.set_ylabel('\nver_purchase')
        ax.set_zlabel('\nrev_date')
        ax.set_title('review_helpfulness - ver_purchase - rev_date')
        ax.dist = 12

'''
for name, label in [('Fake', 0),
                    ('Warning', 1),
                    ('Trustable', 2)]:
    ax.text3D(X[y == label, 1].mean(),
              X[y == label, 0].mean(),
              X[y == label, 2].mean() + 2, name,
              horizontalalignment='center',
              bbox=dict(alpha=.2, edgecolor='w', facecolor='w'))
# Reorder the labels to have colors matching the cluster results
ax.scatter(X[:, 3], X[:, 0], X[:, 2], c=y, edgecolor='k')
'''


fig.show()
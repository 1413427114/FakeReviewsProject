# -*- coding: utf-8 -*-

import json
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans

asin = 'B01AXOCCG2'
rev_scores = json.load(open('analisi_'+asin+'.json'))  

final_score = []
variance, ver_purchase, rev_date, rev_user, rev_help = [], [], [], [], []


for rev in rev_scores:
    final_score.append(rev_scores[rev]['final_score'])
    variance.append(rev_scores[rev]['details']['variance'])
    
    ver_purchase.append(rev_scores[rev]['details']['verified_purchase'])
    
    rev_date.append(rev_scores[rev]['details']['review_date'])
    
    rev_user.append(rev_scores[rev]['details']['review_by_user'])
    
    rev_help.append(rev_scores[rev]['details']['review_helpfulness'])



plt.figure(figsize=(10, 30))

# Final score PER Variance
y_pred = KMeans(n_clusters=2).fit_predict(zip(final_score, variance))

plt.subplot(511)
plt.scatter(variance, final_score, c=y_pred)
#plt.scatter(final_x_variance[:, 0], final_x_variance[:, 1], c=y_pred)
plt.title("Final score PER Variance")


# Final score PER Verified purchase
y_pred = KMeans(n_clusters=2).fit_predict(zip(final_score, ver_purchase))

plt.subplot(512)
plt.scatter(ver_purchase, final_score, c=y_pred)
plt.title("Final score PER Verified purchase")

# Final score PER Review date
y_pred = KMeans(n_clusters=2,).fit_predict(zip(final_score, rev_date))

plt.subplot(513)
plt.scatter(rev_date, final_score, c=y_pred)
plt.title("Final score PER Review date")

# Final score PER Review by user
y_pred = KMeans(n_clusters=2).fit_predict(zip(final_score, rev_user))

plt.subplot(514)
plt.scatter(rev_user, final_score, c=y_pred)
plt.title("Final score PER Review by user")

# Final score PER Review helpfulness
y_pred = KMeans(n_clusters=2).fit_predict(zip(final_score, rev_help))

plt.subplot(515)
plt.scatter(rev_help, final_score, c=y_pred)
plt.title("Final score PER Review helpfulness")


plt.show()

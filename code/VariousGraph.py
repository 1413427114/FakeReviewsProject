# -*- coding: utf-8 -*-
import json
import numpy as np
import datetime as dt
from dateutil import parser as dp
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import Counter

def parseDate(date_to_parse):
    string_of_date = date_to_parse
    string_of_date = string_of_date.replace('gen', 'jan')
    string_of_date = string_of_date.replace('feb', 'feb')
    string_of_date = string_of_date.replace('mar', 'mar')
    string_of_date = string_of_date.replace('apr', 'apr')
    string_of_date = string_of_date.replace('mag', 'may')
    string_of_date = string_of_date.replace('giu', 'jun')
    string_of_date = string_of_date.replace('lug', 'jul')
    string_of_date = string_of_date.replace('ago', 'aug')
    string_of_date = string_of_date.replace('set', 'sep')
    string_of_date = string_of_date.replace('ott', 'oct')
    string_of_date = string_of_date.replace('nov', 'nov')
    string_of_date = string_of_date.replace('dic', 'dec')
    try:       
        return dp.parse(string_of_date).strftime('%d %m %Y')
    except:
        return date_to_parse
        
def reviewsPerDay(reviews_data):
    all_days = []
    for review in reviews_data:
        review_date = reviews_data[review]['reviewPostedDate']
        all_days.append(review_date)
    return all_days
       
def reviewsPerUser(reviews_data):
    all_users = []
    for review in reviews_data:
        review_author = reviews_data[review]['reviewAuthor']['code']
        all_users.append(review_author)
    return all_users

def trigramsPerRev(trigrams_data):
    trigrams_per_rev = []
    for review in trigrams_data:
        repeated_trigrams = trigrams_data[review]['numberOfRepeatedTrigrams']
        trigrams_per_rev.append(repeated_trigrams)
    return trigrams_per_rev

def plotRevPerDay(all_days, fig, axis):
    rpd_d = []
    for d in all_days:
        try: 
            #d = dp.parse(d).strftime('%d %m %Y')
            d = parseDate(d)
            data = dt.datetime.strptime(d, "%d %m %Y").date()
            rpd_d.append(data)
        except: None
    
    mpl_data = mdates.date2num(np.array(rpd_d))
       
    axis.hist(mpl_data, bins=100, color='lightblue')
    axis.xaxis.set_major_locator(mdates.MonthLocator())
    axis.xaxis.set_major_formatter(mdates.DateFormatter('%m.%y'))
    axis.set_title("Frequenza recensioni per periodi")     
    #axis.set_xlabel('Mesi', fontsize = 9)
    #axis.set_ylabel('Frequenza', fontsize = 9)
    plt.show()
    
def plotRevPerUser(all_users, fig, axis):    
    l, v = zip(*Counter(all_users).items()) 
    labels, values = zip(*Counter(v).items())   
    
    indexes = np.arange(len(labels))
    width = 0.07    
    
    axis.set_title("Numero Recensioni x Numero Utenti")
    #axis.set_xlabel('Numero Recensioni', fontsize = 9)
    #axis.set_ylabel('Numero Utenti', fontsize = 9)
    plt.sca(axis)
    plt.bar(indexes, values, width, color='lightblue')
    plt.xticks(indexes + width * 0.5, labels)
    plt.show()

def plotTrigramsPerRep(trigrams_per_rev, fig, axis):
    labels, values = zip(*Counter(trigrams_per_rev).items()) 

    indexes = np.arange(len(labels))
    width = 0.25    
    
    axis.set_title("Numero Trigrammi Ripetuti x Numero Recensioni")
    #axis.set_xlabel('Numero Trigrammi ripetuti', fontsize = 9)
    #axis.set_ylabel('Numero Recensioni', fontsize = 9)
    plt.sca(axis)
    plt.bar(indexes, values, width, color='lightblue')
    plt.xticks(indexes + width * 0.5, labels)
    plt.show()
    
    
if __name__ == '__main__':    
    asin = 'B00P73B1E4' #'B00PVDMTIC', 'B01LZ1Y47Q', 'B01MY98XEN', 'B01AXOCCG2', 'B01GPEA1QC', 'B00P73B1E4'
    
    review_data = json.load(open('json/'+asin+'/sommario_'+asin+'.json'))
    reviews_data = review_data[asin]['reviews']
    trigrams_data = review_data[asin]['trigrams']
    all_days = reviewsPerDay(reviews_data)
    all_users = reviewsPerUser(reviews_data)
    trigrams_per_rev = trigramsPerRev(trigrams_data)
    
    #rest comprende anche le recensioni con 0 trigrammi ripetuti
    rest = []
    for i in range(0,(len(all_days)-len(trigrams_per_rev))): rest.append(0)
    rest += trigrams_per_rev
    
    fig, ax = plt.subplots(3,1)
    plotRevPerDay(all_days, fig, axis=ax[0])
    plotRevPerUser(all_users, fig, axis=ax[1])   
    plotTrigramsPerRep(trigrams_per_rev, fig, axis=ax[2])
    #plotTrigramsPerRep(rest, fig, axis=ax[2])
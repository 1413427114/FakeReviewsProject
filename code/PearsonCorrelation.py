# -*- coding: utf-8 -*-

from scipy import stats
import json
import pandas as pd
import numpy as np


asin = 'B01GPEA1QC' #'B00PVDMTIC', 'B01LZ1Y47Q', 'B01MY98XEN', 'B01AXOCCG2', 'B01GPEA1QC', 'B00P73B1E4'
json_data = json.load(open('json/'+asin+'/analisi_'+asin+'.json'))  

vp, rbu, rh, rt, v, rd, sr, rl, vine = [], [], [], [], [], [], [], [], []
a_r, a_eg, a_otr, a_rr = [], [], [], []
for rev in json_data:
    vp.append(json_data[rev]['scoreDetails']['verifiedPurchase'])
    rbu.append(json_data[rev]['scoreDetails']['reviewByUser'])
    rh.append(json_data[rev]['scoreDetails']['reviewHelpfulness'])
    rt.append(json_data[rev]['scoreDetails']['repeatedTrigrams'])
    v.append(json_data[rev]['scoreDetails']['variance'])
    rd.append(json_data[rev]['scoreDetails']['reviewDate'])
    sr.append(json_data[rev]['scoreDetails']['shortAndRepetitive'])
    rl.append(json_data[rev]['scoreDetails']['reviewLength'])
    vine.append(json_data[rev]['scoreDetails']['vineReview'])
    a_r.append(json_data[rev]['scoreDetails']['authorReliability']['rank'])
    a_eg.append(json_data[rev]['scoreDetails']['authorReliability']['easyGrader'])
    a_otr.append(json_data[rev]['scoreDetails']['authorReliability']['oneTimeReviewer'])
    a_rr.append(json_data[rev]['scoreDetails']['authorReliability']['repetitiveReviewer'])

#restituisce due valori, il primo è il coefficiente di correlazione di pearson 
#viene calcolato tra le recensioni sui due valori considerati
    #IMPORTANTE: stats.pearsonr(A, B) = stats.pearsonr(B, A)
#il valore può essere compreso tra -1<pc<1
    #pc=0, indica la non correlazione tra gli elementi
    #-0,3<pc<0,3 con 0 escluso, indica una debole correlazione diretta (>0) o inversa (<0)
    #-0,7<pc<0,7 con -0,3<pc<0,3 escluso, indica una media correlazione diretta (>0) o inversa (<0)
    #-1<pc<1 con -0,7<pc<0,7 escluso, indica una forte correlazione diretta (>0) o inversa (<0)
'''
pc = stats.pearsonr(v, rh)
print pc[0]
print pc==stats.pearsonr(rh, v)

print ("------------------------")
'''
aaa = [vp, rbu, rh, rt, v, rd, sr, rl, vine, a_r, a_eg, a_otr, a_rr]
#coefficienti di correlazione vari
mat = [[asin, "vp", "rbu", "rh", "rt", "v", "rd", "sr", "rl", "vine", "a_r", "a_eg", "a_otr", "a_rr"],
       ["vp"] + [round(stats.pearsonr(aaa[0], el)[0],3) for el in aaa],
       ["rbu"] + [round(stats.pearsonr(aaa[1], el)[0],3) for el in aaa],
       ["rh"] + [round(stats.pearsonr(aaa[2], el)[0],3) for el in aaa],
       ["rt"] + [round(stats.pearsonr(aaa[3], el)[0],3) for el in aaa],
       ["v"] + [round(stats.pearsonr(aaa[4], el)[0],3) for el in aaa],
       ["rd"] + [round(stats.pearsonr(aaa[5], el)[0],3) for el in aaa],
       ["sr"] + [round(stats.pearsonr(aaa[6], el)[0],3) for el in aaa],
       ["rl"] + [round(stats.pearsonr(aaa[7], el)[0],3) for el in aaa],
       ["vine"] + [round(stats.pearsonr(aaa[8], el)[0],3) for el in aaa],
       ["a_r"] + [round(stats.pearsonr(aaa[9], el)[0],3) for el in aaa],
       ["a_eg"] + [round(stats.pearsonr(aaa[10], el)[0],3) for el in aaa],
       ["a_otr"] + [round(stats.pearsonr(aaa[11], el)[0],3) for el in aaa],
       ["a_rr"] + [round(stats.pearsonr(aaa[12], el)[0],3) for el in aaa]]
npmat = np.array(mat)
#print npmat

## convert your array into a dataframe
df = pd.DataFrame (npmat)
## save to xlsx file
filepath = 'xls/pearson_'+asin+'.xls'
df.to_excel(filepath, index=False)
    
    
#una sorta di anomaly detection può essere quello di calcolare tutti i vari coefficienti di pearson possibili
#si può poi confrontare la correlazione tra le due feature della singola recensione con quello generale
#ma come calolare la correlazione tra due feature della singola recensione??????


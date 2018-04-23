# -*- coding: utf-8 -*-

from scipy import stats
import json
import pandas as pd
import numpy as np


asin = 'B00PVDMTIC' #'B00PVDMTIC' 'B01AXOCCG2' 'B01LZ1Y47Q'
json_data = json.load(open('json'+asin+'/analisi_'+asin+'.json'))  

vp, rbu, rh, rt, v, rd, sr, rl, vine= [], [], [], [], [], [], [], [], []
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

#restituisce due valori, il primo è il coefficiente di correlazione di pearson 
#viene calcolato tra le recensioni sui due valori considerati
    #IMPORTANTE: stats.pearsonr(A, B) = stats.pearsonr(B, A)
#il valore può essere compreso tra -1<pc<1
    #pc=0, indica la non correlazione tra gli elementi
    #-0,3<pc<0,3 con 0 escluso, indica una debole correlazione diretta (>0) o inversa (<0)
    #-0,7<pc<0,7 con -0,3<pc<0,3 escluso, indica una media correlazione diretta (>0) o inversa (<0)
    #-1<pc<1 con -0,7<pc<0,7 escluso, indica una forte correlazione diretta (>0) o inversa (<0)
pc = stats.pearsonr(v, rh)
print pc[0]
print pc==stats.pearsonr(rh, v)

print ("------------------------")

aaa = [vp, rbu, rh, rt, v, rd, sr, rl, vine]
#mette in correlazione tra loro tutti i singoli elementi della matrice
#nel nostro caso gli passiamo una matrice di 6 righe e di N colonne (N=numero recensioni)
#restituisce una matrice NxN (da 0 a N-1) che dice il fattore di correlazione tra i singoli elementi
    #l'elemento (10,15) della matrice rappresenta la correlazione tra la recensione 10 e la 15
    #la diagonale è ovviamente tutta pari a 1 poichè gli elementi correlati con se stessi danno valore 1
coeffs = pd.DataFrame(aaa).corr()
print coeffs[0][1]

print ("------------------------")

#coefficienti di correlazione vari
mat = [["/", "vp", "rbu", "rh", "rt", "v", "rd", "sr", "rl", "vine"],
       ["vp", round(stats.pearsonr(vp, vp)[0],3), round(stats.pearsonr(vp, rbu)[0],3), round(stats.pearsonr(vp, rh)[0],3), round(stats.pearsonr(vp, rt)[0],3), round(stats.pearsonr(vp, v)[0],3), round(stats.pearsonr(vp, rd)[0],3), round(stats.pearsonr(vp, sr)[0],3), round(stats.pearsonr(vp, rl)[0],3), round(stats.pearsonr(vp, vine)[0],3)],
       ["rbu", round(stats.pearsonr(rbu, vp)[0],3), round(stats.pearsonr(rbu, rbu)[0],3), round(stats.pearsonr(rbu, rh)[0],3), round(stats.pearsonr(rbu, rt)[0],3), round(stats.pearsonr(rbu, v)[0],3), round(stats.pearsonr(rbu, rd)[0],3), round(stats.pearsonr(rbu, sr)[0],3), round(stats.pearsonr(rbu, rl)[0],3), round(stats.pearsonr(rbu, vine)[0],3)],
       ["rh", round(stats.pearsonr(rh, vp)[0],3), round(stats.pearsonr(rh, rbu)[0],3), round(stats.pearsonr(rh, rh)[0],3), round(stats.pearsonr(rh, rt)[0],3), round(stats.pearsonr(rh, v)[0],3), round(stats.pearsonr(rh, rd)[0],3), round(stats.pearsonr(rh, sr)[0],3), round(stats.pearsonr(rh, rl)[0],3), round(stats.pearsonr(rh, vine)[0],3)],
       ["rt", round(stats.pearsonr(rt, vp)[0],3), round(stats.pearsonr(rt, rbu)[0],3), round(stats.pearsonr(rt, rh)[0],3), round(stats.pearsonr(rt, rt)[0],3), round(stats.pearsonr(rt, v)[0],3), round(stats.pearsonr(rt, rd)[0],3), round(stats.pearsonr(rt, sr)[0],3), round(stats.pearsonr(rt, rl)[0],3), round(stats.pearsonr(rt, vine)[0],3)],
       ["v", round(stats.pearsonr(v, vp)[0],3), round(stats.pearsonr(v, rbu)[0],3), round(stats.pearsonr(v, rh)[0],3), round(stats.pearsonr(v, rt)[0],3), round(stats.pearsonr(v, v)[0],3), round(stats.pearsonr(v, rd)[0],3), round(stats.pearsonr(v, sr)[0],3), round(stats.pearsonr(v, rl)[0],3), round(stats.pearsonr(v, vine)[0],3)],
       ["rd", round(stats.pearsonr(rd, vp)[0],3), round(stats.pearsonr(rd, rbu)[0],3), round(stats.pearsonr(rd, rh)[0],3), round(stats.pearsonr(rd, rt)[0],3), round(stats.pearsonr(rd, v)[0],3), round(stats.pearsonr(rd, rd)[0],3), round(stats.pearsonr(rd, sr)[0],3), round(stats.pearsonr(rd, rl)[0],3), round(stats.pearsonr(rd, vine)[0],3)],
       ["sr", round(stats.pearsonr(sr, vp)[0],3), round(stats.pearsonr(sr, rbu)[0],3), round(stats.pearsonr(sr, rh)[0],3), round(stats.pearsonr(sr, rt)[0],3), round(stats.pearsonr(sr, v)[0],3), round(stats.pearsonr(sr, rd)[0],3), round(stats.pearsonr(sr, sr)[0],3), round(stats.pearsonr(sr, rl)[0],3), round(stats.pearsonr(sr, vine)[0],3)],
       ["rl", round(stats.pearsonr(rl, vp)[0],3), round(stats.pearsonr(rl, rbu)[0],3), round(stats.pearsonr(rl, rh)[0],3), round(stats.pearsonr(rl, rt)[0],3), round(stats.pearsonr(rl, v)[0],3), round(stats.pearsonr(rl, rd)[0],3), round(stats.pearsonr(rl, sr)[0],3), round(stats.pearsonr(rl, rl)[0],3), round(stats.pearsonr(rl, vine)[0],3)],
       ["vine", round(stats.pearsonr(vine, vp)[0],3), round(stats.pearsonr(vine, rbu)[0],3), round(stats.pearsonr(vine, rh)[0],3), round(stats.pearsonr(vine, rt)[0],3), round(stats.pearsonr(vine, v)[0],3), round(stats.pearsonr(vine, rd)[0],3), round(stats.pearsonr(vine, sr)[0],3), round(stats.pearsonr(vine, rl)[0],3), round(stats.pearsonr(vine, vine)[0],3)]]

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


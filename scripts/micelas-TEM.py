# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 13:40:08 2026
@author: NOELIA
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import os

filepath = '../data/E384.5.txt'

# el txt a veces trae cabecera y a veces no, así que miro la primera fila
with open(filepath, 'r') as f:
    fila1 = f.readline().strip().split()
try:
    float(fila1[1])
    header = None
except ValueError:
    header = 0

df = pd.read_csv(filepath, sep=r'\s+', header=header, engine='python')
bin_starts = df.iloc[:,1].astype(float).values
counts = df.iloc[:,2].astype(float).astype(int).values

bin_width = bin_starts[1]-bin_starts[0]
bin_centers = bin_starts + bin_width/2


datos = np.repeat(bin_centers, counts.astype(int))
media = np.mean(datos)
sigma = np.std(datos) # poblacional, N grande así que da igual ddof
print("media:", round(media,2), "nm")
print("sigma:", round(sigma,2), "nm")

def lognormal(x,A,mu,sigma):
    return (A/(x*sigma))*np.exp(-0.5*((np.log(x)-mu)/sigma)**2)

p0 = [counts.max()*bin_centers[counts.argmax()]*0.5,
      np.log(bin_centers[counts.argmax()]),
      0.5]

try:
    popt,_ = curve_fit(lognormal, bin_centers, counts, p0=p0, maxfev=20000)
except RuntimeError:
    popt = p0
    print('no convergió, uso p0')

margen = bin_width*4
x_fit = np.linspace(max(0.1,bin_starts[0]-margen), bin_starts[-1]+bin_width+margen, 800)
y_fit = lognormal(x_fit,*popt)

fig,ax = plt.subplots(figsize=(6,4.5))
ax.bar(bin_starts, counts, width=bin_width, align='edge',
       color='lavender', edgecolor='black', linewidth=0.5, zorder=2)
ax.plot(x_fit, y_fit, color='black', linewidth=0.8, zorder=3)

ax.set_xlabel('Diámetro (nm)', fontsize=21)
ax.set_ylabel('Número de micelas', fontsize=21)
ax.set_xlim(bin_starts[0]-bin_width*0.5, bin_starts[-1]+bin_width*1.5)
ax.set_ylim(0, counts.max()*1.15)
ax.tick_params(axis='both', direction='in', top=True, right=True, labelsize=15)
ax.spines[['top','right']].set_visible(True)
ax.text(0.95,0.95,'h)', transform=ax.transAxes, ha='right', va='top', fontsize=15)

#plt.title('E$_{38}$S$_{10}$E$_{38}$ en tampón fosfato pH 7,4', fontsize=15)
plt.tight_layout()
plt.savefig('../figuras/histograma_micelas.png', dpi=150, bbox_inches='tight')
plt.show()

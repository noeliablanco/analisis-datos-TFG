# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 17:27:09 2026
@author: NOELIA
"""

import matplotlib.pyplot as plt
import pandas as pd

# el txt viene con tab y coma decimal (exportado del Zetasizer)
name = "fibrinogeno_PBS_37C_10µM_2"
d = pd.read_csv(name + ".txt", sep="\t", decimal=",")
d.columns = d.columns.str.strip()  # venían con espacios raros al final

x = d["X Intensity"]
r1 = d["Record 193: fibrinogeno PBS pH 7.4 37C 10µM 1"]
r2 = d["Record 194: fibrinogeno PBS pH 7.4 37C 10µM 2"]
r3 = d["Record 195: fibrinogeno PBS pH 7.4 37C 10µM 3"]
r4 = d["Record 196: fibrinogeno PBS pH 7.4 37C 10µM 4"]

plt.figure(figsize=(8,4))
plt.plot(x, r1, label="Medida 1", color="cadetblue")
plt.plot(x, r2, label="Medida 2", color="gold")
plt.plot(x, r3, label="Medida 3", color="yellowgreen")
plt.plot(x, r4, label="Medida 4", color="tomato")

plt.xscale("log")
plt.xlim(0.1, 10000)
plt.ylim(0, 40)
plt.xlabel("Tamaño (d.nm)")
plt.ylabel("Intensidad (%)")
plt.title("Fibrinógeno en PBS pH=7.4 10µM a T=37C")
plt.grid(True, which="both", linestyle="--", linewidth=0.25)
plt.legend()

# tamaño medio del pico 1, calculado aparte (ver notas TFG)
plt.text(0.13, 35, "Tamaño medio pico 1: (31.1$\pm$1.1) nm",
          bbox=dict(facecolor='white', alpha=0.5))

plt.tight_layout()
plt.show()
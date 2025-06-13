jsonfile = 'SPP.json'

import json
import numpy as np
import matplotlib.pyplot as plt

projects = json.load(open(jsonfile))['projects']

digits = np.arange(1,10)
counts = np.zeros((len(digits), len(projects)))

for ip,project in enumerate(projects):
  for i in range(len(digits)):
    for app_nr in project['applications']:
      counts[i,ip] += app_nr.count(str(i+1))
      counts[i,ip] += project['abstract'].count(str(i+1))

freq = counts/counts.sum(axis=0).reshape((1,-1))
std = np.std(freq, axis=1)
cdigits = np.linspace(digits[0],digits[-1],64)

# plot it
plt.figure()
plt.xlabel('digit')
plt.ylabel('frequency')
plt.errorbar(digits, freq.mean(axis=1), std, fmt='o', capsize=5)
plt.plot(cdigits, np.log10(cdigits+1) - np.log10(cdigits), '-', label='Benford\'s law')
plt.legend()
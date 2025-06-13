jsonfile = 'SPP.json'

import json
import numpy as np
import matplotlib.pyplot as plt

projects = json.load(open(jsonfile))['projects']

def stats(prop):
  values = []
  for project in projects:
    values += list(project[prop])
  values = sorted(set(values))
  counts = [0]*len(values)
  for i,val in enumerate(values):
    for project in projects:
      counts[i] += list(project[prop]).count(val)

  # prop's values and their frequencies
  return (np.array(values), np.array(counts))

def word_count(word):
  counts = [project['abstract'].lower().count(word) for project in projects]
  for i, count in enumerate(counts):
    nr = projects[i]['lfd-nr']
    print(f'{i:2d} SPP-2451-{nr:<2d}\t{count}')
  print(f'total:\t{sum(counts)}')

  return counts



participants, participant_frequency = stats('names')
locations, location_frequency = stats('locations')
# print(participants, participant_frequency) #DEBUG
# print(locations, location_frequency) #DEBUG


# print all people associated with the SPP
people = []
for project in projects:
  for name in project['names']:
    print(name) 
    people.append(name)
people = set(people)
print(f'total: {len(people)} from {len(locations)} cities combined into {len(projects)} projects')

# which projects require the most attention from me?
# for project in projects:
#   cities = set(project['locations'])
#   if len(cities) <= 1: continue
#   print(project['lfd-nr'], ':', project['title'])
#   print(cities)

# export city stats to a file
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="MyApp")
with open('cities.dat', 'w') as output:
  output.write('city\tlongitude\tlatitude\tcount\n')
  for city,count in zip(locations, location_frequency):
    loc = geolocator.geocode(city)
    output.write(f'{city}\t{loc.longitude}\t{loc.latitude}\t{count}\n')



# plot city distribution (bar diagram)
fig_bar = plt.figure()
plt.grid(False)
plt.bar(locations,location_frequency)
plt.xticks(rotation=70)
plt.ylabel('count')
plt.tight_layout()
fig_bar.savefig('cities_bar.png', dpi=500)


# plot city distribution (cake diagram)
idcs = np.argsort(location_frequency)
explode = [0]*len(locations)
explode[-1] = 0.1
fig_pie, ax = plt.subplots()
ax.pie(location_frequency[idcs], labels=locations[idcs], explode=explode, autopct='%1.1f%%')#, shadow={'ox': -0.02, 'edgecolor': 'none', 'shade': 0.3})
plt.tight_layout()
fig_pie.savefig('cities_pie.png', dpi=500)
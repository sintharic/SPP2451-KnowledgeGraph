import os
import json

SRC = 'Antragsübersicht bewilligte Anträge.csv'
DST = '..{os.sep}SPP.json'
nheader = 2
colheader = 1


current = 0
projects = []
info = ''
with open(SRC) as file:
  line = ''
  for _ in range(nheader): line = file.readline()
  info = line.split(';')[0]

  for line in file.readlines()[colheader:]:
    
    split = line.split(';')
    try: 
      num = int(split[0])
    except: 
      projects[-1]['abstract'] += line
      #projects[-1]['abstract'] += f'\n{line}'
      continue
 
    # append to current project info
    if num==current: 
      projects[-1]['applications'].append(split[1])
      projects[-1]['names'].append(split[2])
      projects[-1]['locations'].append(split[4])
      continue

    # start of new project info
    current = num
    projects.append(dict())
    projects[-1]['lfd-nr'] = num
    projects[-1]['applications'] = [split[1]]
    projects[-1]['names'] = [split[2]]
    projects[-1]['title'] = split[3]
    projects[-1]['locations'] = [split[4]]
    projects[-1]['collaborators'] = split[5]
    projects[-1]['abstract'] = split[6]


# clean up abstracts
for project in projects:
  if len(project['abstract']) < 3: continue
  if project['abstract'][-1]=='\n': project['abstract'] = project['abstract'][:-1]
  if project['abstract'][-1]=='"': project['abstract'] = project['abstract'][:-1]
  if project['abstract'][0]=='"': project['abstract'] = project['abstract'][1:]


# create json file 
data = dict()
for item in info.split(','):
  key, value = item.split(':')
  while key[0]==' ': key = key[1:]
  while value[0]==' ': value = value[1:]
  while key[-1]==' ': key = key[:-1]
  while value[-1]==' ': value = value[:-1]
  data[key] = value
data['projects'] = projects

json.dump(data, open(DST,'w'), separators=(',',' : '), indent=2, ensure_ascii=False)
import os
import yaml, json
from glob import glob

SRC_YRR = f'YRR{os.sep}*.yaml'
SRC_projects = f'..{os.sep}converted_data{os.sep}projects'

files = glob(SRC_YRR)
methods = dict()
documentation_media = dict()
for file in files:
  with open(file, 'r') as fid:
    project = file.split('_')[0].split(os.sep)[-1]
    params = yaml.safe_load(fid)
    
    # parse documentation media
    doc_given = [p.lower() for p in params['documentation_media'] if isinstance(p, str)]
    doc_detect = []
    print(file)
    print(doc_given)
    for doc in doc_given:
      if not isinstance(doc, str): continue
      if 'elab' in doc: doc_detect.append('ELN - eLabFTW')
      if 'rspace' in doc: doc_detect.append('ELN - RSpace')
      if 'obsidian' in doc: doc_detect.append('Markdown - Obsidian')
      if 'excel' in doc: doc_detect.append('Excel')
      if ('powerpoint' in doc) or ('power point' in doc): doc_detect.append('PowerPoint')
      if 'goodnotes' in doc: doc_detect.append('GoodNotes')
      if 'benchling' in doc: doc_detect.append('Benchling')
      if 'notion' in doc: doc_detect.append('Notion')
      if 'basecamp' in doc: doc_detect.append('Basecamp')

      if ('paper' in doc) or ('physical' in doc): doc_detect.append('Paper')
      if doc=='notebook': doc_detect.append('Paper')
    if ('eln' in doc_given) and ('ELN - eLabFTW' not in doc_detect) and ('ELN - RSpace' not in doc_detect):
      doc_detect.append('ELN - ?')
    print(doc_detect)
    documentation_media[project] = doc_detect

    # parse methods
    if 'methods' not in params.keys(): params['methods'] = []
    methods_given = [m.lower() for m in params['methods']]
    if project not in methods.keys(): methods[project] = []
    for method in methods_given:
      if 'hplc' in method: methods[project].append('HPLC')
      if 'bright field' in method: methods[project].append('Optical BF imaging')
      if 'confocal' in method: methods[project].append('Confocal LSM imaging')
      if 'clsm' in method: methods[project].append('Confocal LSM imaging')
      if 'imagej' in method: methods[project].append('ImageJ')
      if 'rheolog' in method: methods[project].append('Rheology')
      if 'flow cytometry' in method: methods[project].append('Flow Cytometry')
      if 'optical density' in method: methods[project].append('OD')
      if ('uv vis' in method) or ('uv-vis' in method): methods[project].append('UV vis spectroscopy')
      if 'sem microscopy' in method: methods[project].append('SEM imaging')
      if 'tem microscopy' in method: methods[project].append('TEM imaging')
      if 'afm microscopy' in method: methods[project].append('AFM imaging')
      if 'afm stiffness' in method: methods[project].append('AFM stiffness measurement')
      if 'ph measurement' in method: methods[project].append('pH measurement')
      if 'thermogravimetric' in method: methods[project].append('TGA')
      if 'dynamic light scattering' in method: methods[project].append('DLS')
      if 'dsc' in method: methods[project].append('DSC')
      if 'nmr' in method: methods[project].append('NMR')
      if 'gpc' in method: methods[project].append('GPC')
      if 'rt-qpcr' in method: methods[project].append('RT-qPCR')
      if 'assay' in method: methods[project].append(f'Assay - {method}')
    print(methods_given)
  print()

projects = methods.keys()
for key in projects:
  filename = f'{SRC_projects}{os.sep}{key}.json'
  params = json.load(open(filename, 'r'))
  methods[key] = list(set(methods[key]))
  # print(key, ':', methods[key])
  params['documentation_media'] = documentation_media[key]
  params['methods'] = methods[key]
  json.dump(params, open(filename, 'w'), indent='  ')
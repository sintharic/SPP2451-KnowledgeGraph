# SPP2451-KnowledgeGraph

[SPP-2451](https://spp2451.de) is a resarch focus program on the field of Engineered Living Materials with Adaptive Functions.
It is funded by the German Research Foundation (DFG) and comprises 15 projects spread across all of Germany.

One of the goals of the SPP is the standardization of research data management (RDM), especially with respect to metadata.
For this purpose, a small RDM demonstrator was developed for the Kick-Off meeting in September of 2024, which has now been published as a GitHub repository for further exchange and development.

## What is this Repository?

The Metadata used for this Knowledge Base had to be collected from various places and was then converted into the machine-readable JSON format.
The Python codes in this repository have two functions: 
1. Convert the metadata in `raw_data` to JSON
2. Use the now readable metadata for statistics and plotting in the subdirectory `analysis`

## The Research Institutes 

![Alt text](analysis/cities_pie.png?raw=true "The cities visualized on the map of Germany")

## The Research Topics

In order to identify the different topics that each of the projects are working on and how they overlap, the abstracts in the metadata were processed automatically.
Arguably the simplest version of natural language processing is the simple detection of keywords. 
For this purpose, certain topics have been defined in `ontology.json` and keywords associated with each topic in `keywords.json`.
This information is then used to automatically create a Knowledge Graph of the entire SPP.

## The Knowledge Graph

Based on the JSON metadata, the file `make_graph.py` generates an Obsidian Vault, which allows the visualization of the projects and the topics they are working on in an interactive graph view.
To interact with the graph, you need to install [Obsidian](https://obsidian.md), download the directory `SPP-KG` and open it as an Obsidian Vault.
Have fun!

![Alt text](obsidianKG.png?raw=true "The Knowledge Graph view in Obsidian")
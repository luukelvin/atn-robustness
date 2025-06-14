# Air Traffic Network Robustness

Code and data used for the Math 168 final project entitled "What Happens When Airports Fail? Analyzing the Resilience of the Global Air Network" by Johan Chua, Farrel Gomargana, Seeun Lim, Kelvin Luu, Felix Su, and Ethan Tran.

## Description

The Kaggle dataset [1] that we used for this project is present in this repository under `kaggle_data`.

The Python packages needed to run the code in this repository is listed in the `requirements.txt` file.

The `1_preliminary.ipynb` Python notebook explores the dataset and computes the centrality measures of the network representation we obtain from the data. We also do some preliminary examination and visualization of the network as nodes are removed according to closeness and betweenness centrality. 

The `2_communities.py` Python file computes and plots the communities for the network. We also examine the communities after removing one node from the network.

The `4_airline_structures.ipynb` Python notebook contains the analysis and visualizations of various US airlines' operational structures.

The final `5_clustering.ipynb` notebook computes clustering coefficients and transitivity for our network. The results of this code were only mentioned in passing in our paper.

## Sources
[1] T Woebkenberg, Global air transportation network (2023) <https://www.kaggle.com/datasets/thedevastator/global-air-transportation-network-mapping-the-wo>.

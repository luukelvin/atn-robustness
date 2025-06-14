import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import seaborn as sns
from itertools import cycle

# data
airports = pd.read_csv("kaggle_data/airports.csv")
routes = pd.read_csv("kaggle_data/routes.csv")

# cleanign up and building 
routes = routes[routes['Airline ID'] != '\\N']
routes = routes[routes['Source airport'].notna() & routes['Destination airport'].notna()]
routes = routes[routes['Source airport'] != routes['Destination airport']]

# Keep routes served by 5+ airlines
route_counts = routes.groupby(['Source airport', 'Destination airport']).size().reset_index(name='count')
route_counts = route_counts[route_counts['count'] >= 5]

# Build graph
G = nx.DiGraph()
G.add_edges_from(route_counts[['Source airport', 'Destination airport']].values)
airport_locs = airports.set_index('IATA')[['Latitude', 'Longitude']].dropna()
pos = {iata: (lon, lat) for iata, (lat, lon) in airport_locs.iterrows()}
G = G.subgraph(set(pos.keys()))

# this part gives communities consistent colors 
palette = sns.color_palette("Set2", 8)
default_colors = cycle(palette)
community_color_map = {}

def assign_colors(communities):
    community_color_map.clear()
    for idx, comm in enumerate(communities):
        color = palette[idx % len(palette)]
        for node in comm:
            community_color_map[node] = color

# plotting community
def plot_communities(G, pos, communities, removed_airport=None, title="", filename="plot.png"):
    assign_colors(communities)

    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([-180, 180, -60, 80], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.set_title(title, fontsize=16)

    for u, v in G.edges():
        if u in pos and v in pos:
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            ax.plot([x0, x1], [y0, y1], color='gray', alpha=0.02, transform=ccrs.PlateCarree())

    for node in G.nodes():
        if node in pos:
            x, y = pos[node]
            ax.plot(x, y, 'o', color=community_color_map.get(node, 'black'), markersize=3, transform=ccrs.PlateCarree())

    if removed_airport and removed_airport in pos:
        x, y = pos[removed_airport]
        ax.plot(x, y, 'X', color='red', markersize=8, label=f"Removed: {removed_airport}", transform=ccrs.PlateCarree())
        ax.legend(loc="lower left")

    plt.savefig(filename, dpi=300)
    plt.show()
    plt.close()

# exolainign colors 
def plot_community_color_legend():
    fig, ax = plt.subplots(figsize=(10, 2))
    for i, color in enumerate(palette):
        ax.plot(i, 1, 'o', markersize=12, color=color)
        ax.text(i, 0.8, f"Community {i+1}", ha='center', va='top')
    ax.set_xlim(-1, len(palette))
    ax.axis('off')
    plt.title("Community Color Legend")
    plt.savefig("color_legend.png", dpi=300)
    plt.close()

plot_community_color_legend()

# centrality leaders 
G_base = G.to_undirected()
leaders = {
    "Degree (ATL)": "ATL",
    "Eigenvector (XIY)": "XIY",
    "Closeness (ORD)": "ORD"
}

for label, airport_code in leaders.items():
    G_full = G_base.copy()
    communities_before = list(greedy_modularity_communities(G_full))
    plot_communities(
        G_full, pos, communities_before,
        removed_airport=airport_code,
        title=f"Community Structure with {airport_code} ({label})",
        filename=f"community_{airport_code}_before.png"
    )

    G_cut = G_full.copy()
    if airport_code in G_cut:
        G_cut.remove_node(airport_code)
    communities_after = list(greedy_modularity_communities(G_cut))
    plot_communities(
        G_cut, pos, communities_after,
        removed_airport=None,
        title=f"Community Structure After Removing {airport_code} ({label})",
        filename=f"community_{airport_code}_after.png"
    )

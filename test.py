import matplotlib.pyplot as plt
import numpy as np

# Sample data: Price Change % for products across different cities
products = [
    "Air Max 270", "Revolution 6", "Zoom Fly 5", "Dunk Low", "Air Force 1",
    "Ultraboost 22", "Superstar", "Stan Smith", "Adizero Pro", "NMD_R1"
]

cities = ["Bangkok", "Jakarta", "Kuala Lumpur", "Manila", "Ho Chi Minh City"]

# Simulated price change percentages (in %)
price_changes_matrix = np.array([
    [-10,  0,   5, -15, -5],
    [  0, -5,   0,   3,  0],
    [ 10,  5,  -5,   0,  8],
    [-10, -8, -10, -5, -12],
    [  0,  0,   0,   0,  0],
    [-10, -5,  -8, -3, -7],
    [  0,  0,   0,   0,  0],
    [-8,  -5,  -4,  0, -6],
    [ 10,  8,  12, 15,  9],
    [-5,  -6,  -3, -4, -2]
])

# Create color map manually
def get_color(value):
    if value < 0:
        return 'green'
    elif value > 0:
        return 'red'
    else:
        return 'gray'

colors = np.vectorize(get_color)(price_changes_matrix)

fig, ax = plt.subplots(figsize=(10, 6))

# Draw the heatmap cells manually using colored rectangles
for i in range(len(products)):
    for j in range(len(cities)):
        rect = plt.Rectangle([j, i], 1, 1, facecolor=colors[i, j])
        ax.add_patch(rect)
        ax.text(j + 0.5, i + 0.5, f"{price_changes_matrix[i, j]:+.0f}%", 
                ha='center', va='center', color='white', fontsize=9)

# Set ticks and labels
ax.set_xlim(0, len(cities))
ax.set_ylim(0, len(products))
ax.set_xticks(np.arange(len(cities)) + 0.5)
ax.set_xticklabels(cities)
ax.set_yticks(np.arange(len(products)) + 0.5)
ax.set_yticklabels(products)
ax.invert_yaxis()
ax.set_title("Price Change % Heatmap (1–8 June 2025)")

# Hide spines and ticks
for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(left=False, bottom=False)

plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt

# Example brand data: [quality, cost]
brands = {
    "Brand 1": [0.8, 0.9],
    "Brand 2": [0.4, 0.9],
    "Brand 3": [0.6, 0.7],
    "Brand 4": [0.8, 0.8],
    "Brand 5": [0.3, 0.3],
    "XYZ Co. (old)": [0.6, 0.8],
    "XYZ Co. (new)": [0.9, 0.5],
}

# Separate data for plotting
labels = list(brands.keys())
x = [brands[label][0] for label in labels]  # Quality
y = [brands[label][1] for label in labels]  # Cost

# Create plot
fig, ax = plt.subplots(figsize=(8, 8))

# Draw vertical and horizontal center lines
ax.axhline(0.5, color='gray', linestyle='--')
ax.axvline(0.5, color='gray', linestyle='--')

# Scatter plot
for i, label in enumerate(labels):
    ax.scatter(x[i], y[i], s=100)  # s = marker size
    ax.text(x[i] + 0.01, y[i], label, fontsize=9)

# Example movement arrow for XYZ Co.
ax.annotate("", xy=(0.9, 0.5), xytext=(0.6, 0.8),
            arrowprops=dict(arrowstyle="->", color='blue', lw=2))

# Axis labels
ax.set_xlabel('Perceived Quality')
ax.set_ylabel('Perceived Cost')

# Set limits
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

ax.set_title('Perceptual Map for Competitive Analysis')
plt.grid(True, which='both', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.show()

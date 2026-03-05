import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

STATES = ["Home", "Explore", "Feat A", "Feat B", "Feat C", "Subscribe", "Churn"]
COLORS = ["#60a5fa", "#a78bfa", "#34d399", "#f59e0b", "#fb923c", "#10b981", "#ef4444"]

SUBSCRIBE_WEEKLY_CHURN = 1 - (0.95 ** (1/4))
SUBSCRIBE_PROB = 0.01  # 1% chance per step from any free state

P = np.array([
#  Home   Expl   FtA    FtB    FtC    Sub    Churn
  [0.10,  0.45,  0.15,  0.10,  0.08,  0.01,  0.11],  # Home
  [0.15,  0.25,  0.25,  0.15,  0.09,  0.01,  0.10],  # Explore
  [0.08,  0.15,  0.35,  0.18,  0.15,  0.01,  0.08],  # Feat A
  [0.06,  0.10,  0.18,  0.38,  0.21,  0.01,  0.06],  # Feat B
  [0.05,  0.08,  0.15,  0.20,  0.46,  0.01,  0.05],  # Feat C
  [0.00,  0.00,  0.00,  0.00,  0.00,  1 - SUBSCRIBE_WEEKLY_CHURN, SUBSCRIBE_WEEKLY_CHURN],  # Subscribe
  [0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  1.00],  # Churn (absorbing)
])

# Sanity check rows sum to 1
assert np.allclose(P.sum(axis=1), 1.0), "Rows must sum to 1"

N_USERS = 1000
N_STEPS = 52  # 52 weeks

def simulate_user():
    path = [0]  # start at Home
    state = 0
    for _ in range(N_STEPS):
        state = np.random.choice(len(STATES), p=P[state])
        path.append(state)
        if state == 6:  # Churn absorbing
            break
    return path

all_paths = [simulate_user() for _ in range(N_USERS)]

# Build distribution matrix: (weeks x states)
dist = np.zeros((N_STEPS + 1, len(STATES)))
for path in all_paths:
    for t, s in enumerate(path):
        dist[t, s] += 1
dist /= N_USERS

# --- Plot ---
fig, axes = plt.subplots(2, 1, figsize=(13, 9))
fig.patch.set_facecolor("#0a0f1e")

# ── Top: stacked area ──
ax = axes[0]
ax.set_facecolor("#0a0f1e")
x = np.arange(N_STEPS + 1)
ax.stackplot(x, dist.T, colors=COLORS, alpha=0.88)
ax.axvline(4,  color="#ffffff", linewidth=0.6, linestyle="--", alpha=0.3)
ax.axvline(52, color="#ffffff", linewidth=0.6, linestyle="--", alpha=0.3)
ax.text(4.5,  0.92, "Wk 4\n66% retained", color="#94a3b8", fontsize=7.5)
ax.text(44,   0.92, "Wk 52\n33% retained", color="#94a3b8", fontsize=7.5)
ax.set_xlim(0, N_STEPS)
ax.set_ylim(0, 1)
ax.set_ylabel("Share of Users", color="#94a3b8")
ax.set_title("52-Week User Journey  ·  1 000 simulated users", color="#e2e8f0", fontsize=13)
ax.tick_params(colors="#64748b")
for sp in ax.spines.values(): sp.set_edgecolor("#1e293b")
patches = [mpatches.Patch(color=COLORS[i], label=STATES[i]) for i in range(len(STATES))]
ax.legend(handles=patches, loc="lower left", framealpha=0.15, labelcolor="#e2e8f0", facecolor="#0a0f1e", fontsize=8)

# ── Bottom: Subscribe vs Churn lines ──
ax2 = axes[1]
ax2.set_facecolor("#0a0f1e")
ax2.plot(x, dist[:, 5], color="#10b981", linewidth=2,   label="Subscribe (cumulative)")
ax2.plot(x, dist[:, 6], color="#ef4444", linewidth=2,   label="Churn (cumulative)")
ax2.plot(x, dist[:, 0] + dist[:, 1] + dist[:, 2] + dist[:, 3] + dist[:, 4],
         color="#60a5fa", linewidth=1.5, linestyle="--", label="Still active (free)")
ax2.set_xlim(0, N_STEPS)
ax2.set_ylim(0, 1)
ax2.set_xlabel("Week", color="#94a3b8")
ax2.set_ylabel("Share of Users", color="#94a3b8")
ax2.set_title("Subscribe · Churn · Active Free  over 52 weeks", color="#e2e8f0", fontsize=11)
ax2.tick_params(colors="#64748b")
for sp in ax2.spines.values(): sp.set_edgecolor("#1e293b")
ax2.legend(framealpha=0.15, labelcolor="#e2e8f0", facecolor="#0a0f1e", fontsize=8)

plt.tight_layout(pad=2.5)
plt.savefig("journey_52w.png", dpi=150, bbox_inches="tight", facecolor="#0a0f1e")
plt.show()

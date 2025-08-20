# analysis.py
# Marimo-style interactive notebook (script form with cell markers).
# Author/verification email: 23f1001029@ds.study.iitm.ac.in
#
# This script is written to behave like an interactive notebook when run in Jupyter or VS Code (use the "# %%"
# cell markers). It includes:
# - At least two cells with variable dependencies
# - An interactive slider widget (ipywidgets)
# - Dynamic markdown output that updates based on widget state
# - Comments documenting the data flow between cells
#
# Data flow summary (comments below show dependencies):
# Cell 1: Generate synthetic dataset -> produces `df` (depends on no other cell)
# Cell 2: Create interactive widget `threshold_slider` and display function -> depends on `df`
# Cell 3: Derived computation and dynamic markdown output -> depends on `threshold_slider` and `df`

# %%
# CELL 1: Data generation and initial variables
# Produces `df` which downstream cells will use.
import pandas as pd
import numpy as np

# Email included as a comment for verification
# 23f1001029@ds.study.iitm.ac.in

np.random.seed(0)
n = 200
df = pd.DataFrame({
    "feature_a": np.random.normal(loc=50, scale=10, size=n),
    "feature_b": np.random.normal(loc=30, scale=5, size=n),
    "group": np.random.choice(["A", "B", "C"], size=n, p=[0.4, 0.35, 0.25])
})

# Derived column dependent on feature_a and feature_b; demonstrates variable dependency within this cell
df["score"] = 0.6 * df["feature_a"] + 0.4 * df["feature_b"]

# Explain data flow for readers:
# - `df` is the canonical dataset produced here.
# - `score` is computed from `feature_a` and `feature_b` and will be used by the interactive cell below.

print("Cell 1 complete: generated df with columns:", df.columns.tolist())

# %%
# CELL 2: Interactive slider widget and reactive display function
# This cell depends on `df` created in Cell 1.
from IPython.display import display, Markdown, clear_output
import ipywidgets as widgets

# Create an interactive slider to set a score threshold.
threshold_slider = widgets.FloatSlider(
    value=df["score"].mean(),
    min=float(df["score"].min() - 5),
    max=float(df["score"].max() + 5),
    step=0.1,
    description='Score threshold:',
    continuous_update=True,
    layout=widgets.Layout(width='80%')
)

# This output area will contain dynamic markdown and a small table snapshot
out = widgets.Output()

def update_display(change=None):
    # This function depends on current slider value and on `df`.
    thresh = threshold_slider.value
    subset = df[df["score"] >= thresh].copy()
    counts_by_group = subset["group"].value_counts().sort_index()
    mean_scores = subset.groupby("group")["score"].mean().round(2)

    # Documenting data flow:
    # - Input: `threshold_slider.value` (user-controlled)
    # - Data source: `df` from Cell 1
    # - Outputs: dynamic markdown summary and counts table, shown in `out`
    with out:
        clear_output(wait=True)
        md = f\"\"\"### Interactive Summary (threshold = **{thresh:.2f}**)

- **Total rows ≥ threshold:** {len(subset)} out of {len(df)}
- **Counts by group (A / B / C):** {', '.join(str(counts_by_group.get(g,0)) for g in ['A','B','C'])}
- **Mean score by group (for subset):** {', '.join(f'{g}:{mean_scores.get(g, float('nan'))}' for g in ['A','B','C'])}

> Note: The subset is recalculated whenever the slider moves. This demo shows how downstream analysis updates reactively based on widget state.
\"\"\"
        display(Markdown(md))
        # Show a small DataFrame head for context
        display(subset.head(10))

# Wire the slider to the update function
threshold_slider.observe(update_display, names='value')

# Initial display
display(threshold_slider)
display(out)
# Trigger initial render
update_display()

# %%
# CELL 3: Additional dependent cell demonstrating further computations
# This cell also depends on the slider and df; it illustrates chaining behavior.
# It computes the proportion of high-scorers per group and prints a short interpretation.
def compute_proportions(threshold):
    # Data dependency: df from Cell 1
    subset = df[df["score"] >= threshold]
    prop = subset["group"].value_counts(normalize=True).reindex(["A","B","C"]).fillna(0).round(3)
    return prop

# Expose a small utility widget-based inspector for proportions
prop_button = widgets.Button(description="Show group proportions (in out area)")
def on_prop_clicked(b):
    with out:
        display(Markdown("#### Group proportions (for current threshold)"))
        display(compute_proportions(threshold_slider.value))

prop_button.on_click(on_prop_clicked)
display(prop_button)

# Comments on data flow:
# - The compute_proportions function depends on `df` (Cell 1) and `threshold_slider.value` (Cell 2).
# - This demonstrates how a Marimo notebook can have multiple interactive cells with clear dependencies.

# End of notebook script

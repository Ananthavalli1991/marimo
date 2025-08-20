# 23f1001029@ds.study.iitm.ac.in

import marimo

__generated_with = "0.8.0"
app = marimo.App()


# Cell 1: Import and create dataset
@app.cell
def cell1():
    import pandas as pd
    import numpy as np

    # Generate synthetic dataset
    np.random.seed(42)
    df = pd.DataFrame({
        "x": np.linspace(0, 10, 100),
        "y": np.linspace(0, 10, 100) + np.random.normal(0, 1, 100)
    })
    df.head()
    return df


# Cell 2: Interactive slider widget
@app.cell
def cell2(mo):
    # Slider to control number of points displayed
    slider = mo.ui.slider(start=10, stop=100, step=10, value=50, label="Number of points")
    slider
    return slider


# Cell 3: Variable dependency (df depends on slider value)
@app.cell
def cell3(df, slider):
    subset = df.head(slider.value)
    subset.describe()
    return subset


# Cell 4: Dynamic Markdown output based on widget
@app.cell
def cell4(mo, slider):
    mo.md(f"""
    ### Data Story
    You selected **{slider.value} points** from the dataset.  
    Increasing the slider value shows more of the linear relationship between `x` and `y`.
    """)
    return


if __name__ == "__main__":
    app.run()

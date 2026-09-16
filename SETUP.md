# Running the TTM4105 Assignment 1 Notebook

1. **Open a terminal in the assignment folder** — the one containing
   `Assignment1_TTM4105_2026.ipynb`, `scripts/` and `audio/`.

2. **Create a virtual environment:**

   ```bash
   python3 -m venv .venv
   ```

   On Windows: `py -m venv .venv`, and read `.venv\Scripts\` for `.venv/bin/` below.

3. **Install the packages:**

   ```bash
   .venv/bin/pip install numpy scipy matplotlib librosa ipykernel notebook
   ```

4. **Register it as a Jupyter kernel:**

   ```bash
   .venv/bin/python -m ipykernel install --user --name ttm4105 --display-name "Python (TTM4105)"
   ```

5. **Select the kernel:** open the notebook, click the kernel picker at the
   top-right, and choose **Python (TTM4105)** (or `.venv` under _Python Environments_).

6. **Set your seed and run:** in cell 2, set `seed = ` to your group number + 10000
   (group 18 → `10018`).

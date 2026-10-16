
# N-Queens Solver Benchmark

This project implements and compares five exact approaches for the
N-Queens problem:

- SAT using PySAT
- CP-SAT using Google OR-Tools
- CPLEX Mixed-Integer Programming (MIP)
- Gurobi Mixed-Integer Programming
- CPLEX Constraint Programming (CP)

## Requirements

- Python 3.13
- Dependencies listed in `requirements.txt`
- IBM ILOG CPLEX Optimization Studio for CPLEX CP
- Valid solver licenses or applicable community editions

The CPLEX CP executable path must match the local installation.

## Setup

Create a virtual environment and install the Python packages:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run an individual solver

```powershell
python .\nqueens_sat.py 8
python .\nqueens_cpsat.py 8
python .\nqueens_cplex_mip.py 8
python .\nqueens_gurobi.py 8
python .\nqueens_cplex_cp.py 8
```

## Run tests

```powershell
python .\test_nqueens.py
```

## Run benchmarks

```powershell
python .\benchmark.py
python .\plot_results_5solvers.py
```

For larger board sizes:

```powershell
python .\benchmark_large.py
python .\plot_large_results.py
```

Benchmark scripts overwrite their corresponding output CSV files.
Review and preserve previous results before rerunning experiments.

## Experimental data

- `benchmark_5solvers.csv`: repeated runs for smaller board sizes
- `benchmark_large.csv`: large-board experiments, including solver errors
- `benchmark_medians.csv`: summary for the five-solver benchmark
- `benchmark_large_medians.csv`: summary for large-board experiments
- PNG files: generated runtime comparison plots

Failed runs and license restrictions are recorded rather than
replaced with estimated runtimes.

## Data Availability

Source code, benchmark results, and visualizations:

https://github.com/transonnn/nqueens-sat

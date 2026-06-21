
# Strong Bridge Propagation for the Circuit Constraint in Pumpkin

This repository contains an extension of the Pumpkin solver that enhances **circuit constraint propagation** using **strong bridges from graph theory**.

In addition to the solver modification, this project provides a full experimental framework for:
- Instance generation
- Experiment execution
- Result collection and analysis
- Validation against a reference solver



## Contribution

We extend the Pumpkin solver by introducing a new propagation mechanism for the circuit constraint based on **strong bridges**.

### Key Ideas
- Represent circuit constraints as directed graphs
- Identify **strong bridges** in these graphs
- Use strong bridges to derive additional propagation
- Improve pruning compared to standard approaches


### Solver Modes

The solver supports two propagation modes:

- `base` → standard circuit propagation
- `strong-bridges` → enhanced propagation using strong bridges (this work)

Internally, these are invoked with a flag `--circuit-propagation=strong-bridges` (if not specified, `base` is used)



## Repository Structure

- `experiments/` — generated experiment outputs; instances, data and generated graphs can be found here.
- `pumpkin/` — fork of the Pumpkin solver (as a git submodule)
- `scripts/` — Python scripts for experiments, including:
  - `generate.py` — instance generation
  - `run_experiments.py` — full experiment pipeline
  - `validate_solutions.py` — correctness checking
  - supporting scripts:
    - `analyze.py` and `merged_data.py` for generating graphs and tables based on data
    - `generator.py` for the generation logic and `minizinc_io.py` for compiling instances
- `models/` — MiniZinc models used for compiling instances:
    - `circuit_model_satisfy.mzn` for satisfaction problem
    - `circuit_model_minimize.mzn` for optimization problem (minimizing total length of cycle)



## Setup

### Requirements
- Python 3.x
- Rust (for building Pumpkin)
- MiniZinc

### Build Pumpkin
You can build the project yourself by running the following commands; `run_experiments.py` does this for you as well.
```bash
cd pumpkin
cargo build --release -p pumpkin-solver
```

## Instance Generation

Generate a single instance:

```bash
cd scripts
python generate.py <n> <k> [seed]

```
This saves the generated instance in a folder called `manual_instances` and prints out the command you could use to run it individually.
## Running Experiments
Run a full experiment:

```bash
python run_experiments.py <seed>
```
This script will:

1. Generate instances based on configuration and seed
2. Run both solver variants (`base` and `strong-bridges`)
3. Execute runs in parallel (depending on amount of workers)
4. Collect statistics into CSV files
5. Run analysis scripts

### Experiment Configuration

Experiment parameters are defined inside `run_experiments.py`, at the bottom of the script.
You can change the parameters for both `sat` (satisfaction) and `opt` (optimization):
- `n_values`: different graph sizes that should be generated
- `k_values`: different densities which should be used for generation
- `instance_amount`: number of instances for each combination of (n, k)
- `timeout`: per-instance time limit; should generally not exceed 30 minutes
- `excluded_combinations`: combinations to skip; list of tuples which represent the (n,k) combinations to not use

You can also change the `MAX_WORKERS` at the top to align with the capabilities of the processor in use; set it to 1 for sequential solving.
### Output

Results are stored in in `experiments/experiment<seed>`. Running another experiment with the same seed will overwrite the existing results. Each experiment produces an optimization and satisfaction folder with:
- `instances` folder containing all generated instances (gitignored)
- `results_base_seed<seed>.csv` and `results_sb_seed<seed>.csv` containing the measured statistics, which include:
    - solving time
    - number of conflicts
    - number of propagations
    - strong bridge propagation counts
    - SCC propagation counts
    - average nogood length
    - average LBD size
    - and more
- `analysis` folder which contains all graphs and tables generated for analysis and comparison

The `experiment<seed>` folder also contains `merged_analysis`, which are tables that use information from both the satisfaction and the optimization setting.


## Validation

To verify correctness against a reference solver (Gecode):

```bash
python validate_solutions.py
```
What this does:
- Generates test instances based on what is configured in the script
- Runs:
  - Pumpkin (strong-bridges)
  - Gecode (reference solver)
- Compares **all solutions** and returns whether they matched or not

In `validate_solutions.py`, you can define:
- `N_VALUES` for different graph sizes to be generated
- `K_VALUES` for different densities to be generated
- `INSTANCE_AMOUNT` to define how many instances are generated for every (n, k) combination

For validating, it is recommended to not go much higher than `k = 5` and `n = 15`, as the amount of possible solutions explodes with higher parameters.
## Reproducibility
All experiments are deterministic given a seed:

```bash
python run_experiments.py <seed>
```
The seed controls instance generation and ensures that satisfaction and optimization instances with the same (n,k) will have the same instances generated.

## Notes

- This repository contains a **research extension** and is not part of the official Pumpkin project
- Performance improvements depend on instance size and parameter choices. The goal of this project was to show the effect strong bridges can have in regards of **search effort**, not necessarily runtime.
- statistics collected when performing strong bridge propagation may introduce measuring overhead, resulting slower runtimes

## Summary
This project provides:
- A novel **strong-bridge-based propagation technique**
- Integration into a modern constraint solver (Pumpkin)
- A complete **experimental pipeline**
- Validation against a reference solver

## Credits
This extension has been developed for CSE3000 Research Project.

- Student: Martijn van Leest
- Responsible Professor: Emir Demirović
- Supervisor: Imko Marijnissen
- Thesis committee: Emir Demirović, Imko Marijnissen, Andreea Costea

An electronic version of this thesis is available at https://repository.tudelft.nl/

Reported results in the thesis have been collected using seed: **420**
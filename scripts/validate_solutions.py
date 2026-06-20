import subprocess
import os
import random
from generate import generate_dzn_file

MODEL = "../models/circuit_model_satisfy.mzn"
SOLVER_SB = "pumpkin-strong-bridge"
SOLVER_REF = "gecode"
N_VALUES = [10, 13, 15]
K_VALUES = [2,3,4]
INSTANCE_AMOUNT = 5
OUTPUT_DIR = "../validation_instances"
DZN_FILES = []
os.makedirs(OUTPUT_DIR, exist_ok=True)


def run_minizinc(model, solver, dzn_file):
    cmd = [
        "minizinc",
        "--solver", solver,
        model,
        dzn_file,
        "-a"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error running {solver} on {dzn_file}")
        print(result.stderr)
        return None

    return result.stdout


def normalize_output(output):
    lines = output.splitlines()

    # Remove MiniZinc separators
    cleaned = [
        line.strip()
        for line in lines
        if line.strip() and not set(line.strip()) <= set("-=")
    ]

    # Sort solutions
    cleaned.sort()

    return cleaned


def compare_outputs(out1, out2):
    return out1 == out2


def validate_instance(dzn_file):
    print(f"Checking {dzn_file}...")

    sb_output = run_minizinc(MODEL, SOLVER_SB, dzn_file)
    ref_output = run_minizinc(MODEL, SOLVER_REF, dzn_file)

    if sb_output is None or ref_output is None:
        return False

    sb_norm = normalize_output(sb_output)
    ref_norm = normalize_output(ref_output)
    print(len(sb_norm), len(ref_norm))

    if sb_norm == ref_norm:
        print(f"MATCH: {dzn_file}")
        return True
    else:
        print(f"MISMATCH: {dzn_file}")
        print(f"SB solutions:  {len(sb_norm)}")
        print(f"REF solutions: {len(ref_norm)}")
        return False
    

def get_seeds_for_pair(n, k, amount):
    pair_rng = random.Random()
    return [pair_rng.randint(0, 10**9) for _ in range(amount)]

def generate_instances():
    for n in N_VALUES:
        for k in K_VALUES:
            print(f"generating {INSTANCE_AMOUNT} instances for n = {n} and k = {k}...")
            seeds_for_pair = get_seeds_for_pair(n, k, INSTANCE_AMOUNT)

            for seed in seeds_for_pair:
                folder = OUTPUT_DIR
                dzn_file_name = os.path.join(f"n{n}k{k}seed{seed}")

                generate_dzn_file(n, k, seed, folder, dzn_file_name)
                DZN_FILES.append(f"{dzn_file_name}.dzn")


def delete_unlisted_files():
    # Convert allowed_names to a set for faster lookup
    allowed_set = set(DZN_FILES)

    for filename in os.listdir(OUTPUT_DIR):
        file_path = os.path.join(OUTPUT_DIR, filename)

        # Only process files (skip directories)
        if os.path.isfile(file_path):
            if filename not in allowed_set:
                os.remove(file_path)

def main():
    generate_instances()

    delete_unlisted_files()

    files = [
        os.path.join(OUTPUT_DIR, f)
        for f in os.listdir(OUTPUT_DIR)
        if f.endswith(".dzn")
    ]

    total = len(files)
    correct = 0

    for dzn in files:
        if validate_instance(dzn):
            correct += 1

    print("\n============================")
    print(f"{correct}/{total} instances match")
    print("============================")


if __name__ == "__main__":
    main()




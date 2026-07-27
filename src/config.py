# ==========================================
# Project Paths
# ==========================================

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = PROJECT_ROOT / "data" / "raw"

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

MODEL_DIR = PROJECT_ROOT / "models"

OUTPUT_DIR = PROJECT_ROOT / "outputs"

# ==========================================
# Training
# ==========================================

RANDOM_STATE = 42

TEST_SIZE = 0.20

# ==========================================
# Dataset
# ==========================================

FILES = {
    "comp0": {
        "pridb": RAW_DIR / "comp0.pridb",
        "mts": RAW_DIR / "comp0_mts.csv",
        "damage_mode": "Fiber_Failure"
    },

    "comp90": {
        "pridb": RAW_DIR / "comp90.pridb",
        "mts": RAW_DIR / "comp90_mts.csv",
        "damage_mode": "Matrix_Cracking"
    },

    "compteflon": {
        "pridb": RAW_DIR / "compteflon.pridb",
        "mts": RAW_DIR / "compteflon_mts.csv",
        "damage_mode": "Delamination"
    },

    "CAI-spec1": {
        "pridb": RAW_DIR / "CAI-spec1.pridb",
        "mts": RAW_DIR / "CAIspec1_mts.csv",
        "damage_mode": "Mixed_Damage"
    },

    "CAI-spec2": {
        "pridb": RAW_DIR / "CAI-spec2.pridb",
        "mts": RAW_DIR / "CAIspec2_mts.csv",
        "damage_mode": "Mixed_Damage"
    },

    "CAI-spec3": {
        "pridb": RAW_DIR / "CAI-spec3.pridb",
        "mts": RAW_DIR / "CAIspec3_mts.csv",
        "damage_mode": "Mixed_Damage"
    }
}

# Tables to skip when reading PRIDB databases
SKIP_TABLES = ["acq_setup", "waveform", "setup"]




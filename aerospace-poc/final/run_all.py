"""
run_all.py — Master runner for the aerospace synthetic data analysis pipeline.

Executes all downstream analysis scripts in sequence after synthetic data generation.
Each script is run as a subprocess. If a script fails, the error is logged and
execution continues with the next script. A final summary is printed at the end.

Pipeline order:
    1. full_validation_pipeline.py
    2. feature_engineering.py
    3. predictive_models.py
    4. class_balancing.py
    5. edge_case_analysis.py
    6. build_data_analysis_report.py
"""

import subprocess
import sys
import logging
import time
from pathlib import Path

from tqdm import tqdm

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "full_validation_pipeline.py",
    "feature_engineering.py",
    "predictive_models.py",
    "class_balancing.py",
    "edge_case_analysis.py",
    "build_data_analysis_report.py",
]

LOG_FILE = BASE_DIR / "run_all.log"

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(str(LOG_FILE), mode="w", encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_script(script_name: str) -> tuple[bool, float, str]:
    """
    Run a single Python script as a subprocess.

    Parameters
    ----------
    script_name : str
        Filename of the script to run (relative to BASE_DIR).

    Returns
    -------
    success : bool
        True if the script exited with return code 0.
    elapsed : float
        Wall-clock time in seconds.
    error_message : str
        Empty string on success; stderr + stdout tail on failure.
    """
    script_path = BASE_DIR / script_name

    if not script_path.exists():
        return False, 0.0, f"Script not found: {script_path}"

    start = time.monotonic()
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=str(BASE_DIR),
        )
        elapsed = time.monotonic() - start

        if result.returncode == 0:
            return True, elapsed, ""
        else:
            # Collect the last 20 lines of stdout + all of stderr for the error message
            stdout_tail = "\n".join(result.stdout.strip().splitlines()[-20:])
            stderr_body = result.stderr.strip()
            error_message = ""
            if stdout_tail:
                error_message += f"[stdout tail]\n{stdout_tail}\n"
            if stderr_body:
                error_message += f"[stderr]\n{stderr_body}"
            return False, elapsed, error_message.strip()

    except Exception as exc:
        elapsed = time.monotonic() - start
        return False, elapsed, f"Unexpected exception: {exc}"


def main() -> None:
    logger.info("=" * 70)
    logger.info("Aerospace Synthetic Data — Master Analysis Pipeline")
    logger.info(f"Base directory : {BASE_DIR}")
    logger.info(f"Log file       : {LOG_FILE}")
    logger.info(f"Scripts to run : {len(SCRIPTS)}")
    logger.info("=" * 70)

    results: dict[str, dict] = {}

    with tqdm(
        total=len(SCRIPTS),
        desc="Pipeline progress",
        unit="script",
        ncols=80,
        file=sys.stdout,
        leave=True,
    ) as progress_bar:

        for script_name in SCRIPTS:
            progress_bar.set_description(f"Running {script_name}")
            logger.info("-" * 70)
            logger.info(f"Starting : {script_name}")

            success, elapsed, error_message = run_script(script_name)

            if success:
                logger.info(
                    f"Finished : {script_name}  [{elapsed:.1f}s]  STATUS=OK"
                )
                results[script_name] = {
                    "status": "SUCCESS",
                    "elapsed": elapsed,
                    "error": "",
                }
            else:
                logger.error(
                    f"Failed   : {script_name}  [{elapsed:.1f}s]  STATUS=ERROR"
                )
                if error_message:
                    # Log each line of the error at ERROR level
                    for line in error_message.splitlines():
                        logger.error(f"  {line}")
                results[script_name] = {
                    "status": "FAILED",
                    "elapsed": elapsed,
                    "error": error_message,
                }

            progress_bar.update(1)

    # -----------------------------------------------------------------------
    # Final summary
    # -----------------------------------------------------------------------

    succeeded = [name for name, r in results.items() if r["status"] == "SUCCESS"]
    failed = [name for name, r in results.items() if r["status"] == "FAILED"]
    total_time = sum(r["elapsed"] for r in results.values())

    logger.info("=" * 70)
    logger.info("PIPELINE COMPLETE — FINAL SUMMARY")
    logger.info("=" * 70)
    logger.info(
        f"Total scripts : {len(SCRIPTS)}  |  "
        f"Succeeded : {len(succeeded)}  |  "
        f"Failed : {len(failed)}  |  "
        f"Wall time : {total_time:.1f}s"
    )
    logger.info("")

    if succeeded:
        logger.info("Succeeded:")
        for name in succeeded:
            elapsed = results[name]["elapsed"]
            logger.info(f"    OK   {name:<45}  ({elapsed:.1f}s)")

    if failed:
        logger.info("")
        logger.info("Failed:")
        for name in failed:
            elapsed = results[name]["elapsed"]
            logger.error(f"    ERR  {name:<45}  ({elapsed:.1f}s)")
        logger.info("")
        logger.info(
            "Review run_all.log for detailed error output from failed scripts."
        )

    logger.info("=" * 70)

    # Exit with non-zero code if any script failed, so CI/CD pipelines can detect failures.
    if failed:
        sys.exit(1)


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()

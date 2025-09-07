import errno

def setup_module8_test_dir(modname: str, shell_vars: dict, overwrite: bool = False) -> str:
    """
    Create a share/module8 test directory for the given module.
    Layout (relative to the repository root that contains 'install/'):
      share/module8/<pkg>/<ver>/
        ├── test.qsub
        ├── run_test.sh
        └── README.md

    - If overwrite=False and files exist, they are left untouched.
    - Returns the absolute path to the created test directory.
    """
    # Figure out repo root next to 'install/'
    install_dir = module_env.get_install_directory(modname, shell_vars)
    inst_start = install_dir.find('install')
    repo_root = install_dir[:inst_start] if inst_start != -1 else os.path.dirname(install_dir)

    # Split modname into pkg and version
    if '/' in modname:
        pkg, ver = modname.split('/', 1)
    else:
        pkg, ver = modname, 'unknown'

    test_dir = os.path.join(repo_root, 'share', 'module8', pkg, ver)
    os.makedirs(test_dir, exist_ok=True)

    # ===== File contents (safe defaults) =====
    test_qsub_path = os.path.join(test_dir, 'test.qsub')
    run_sh_path   = os.path.join(test_dir, 'run_test.sh')
    readme_path   = os.path.join(test_dir, 'README.md')

    # test.qsub — DO NOT include the placeholder 'module load xyz/0.0.0'
    test_qsub = f"""#!/bin/bash
#PBS -N {pkg}-{ver}-test
#PBS -l select=1:ncpus=1:mem=2gb
#PBS -l walltime=00:10:00
#PBS -j oe

# Load the module under test
module purge
module load {modname}

echo "Running smoke test for {modname} on $(hostname)"
which python >/dev/null 2>&1 && python -V || true
which {pkg} >/dev/null 2>&1 && {pkg} --version || true

echo "OK"
"""

    # run_test.sh — convenience wrapper
    run_sh = """#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QSUB_SCRIPT="${SCRIPT_DIR}/test.qsub"

if command -v qsub >/dev/null 2>&1; then
  echo "Submitting test with qsub..."
  qsub "${QSUB_SCRIPT}"
else
  echo "qsub not found; running directly."
  bash "${QSUB_SCRIPT}"
fi
"""

    # README.md — brief instructions
    readme = f"""# Module8 Tests for `{modname}`

This directory contains a minimal test harness for the module.

## Files
- `test.qsub`: PBS script that loads `{modname}` and runs a smoke test.
- `run_test.sh`: Submits with `qsub` if available, otherwise runs directly.
- `README.md`: You are here.

## Notes
- Replace/extend the smoke commands to actually validate the package.
- Do **not** include the placeholder string `module load xyz/0.0.0` anywhere.
"""

    def _write(filepath: str, content: str, executable: bool = False):
        if not overwrite and os.path.exists(filepath):
            return
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        if executable:
            st = os.stat(filepath)
            os.chmod(filepath, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    _write(test_qsub_path, test_qsub, executable=False)
    _write(run_sh_path, run_sh, executable=True)
    _write(readme_path, readme, executable=False)

    return test_dir







# def main():
#     modname = command_line.parse()
#     check_module_loadable(modname)
#     shell_vars = check_module_env(modname)
#     check_files_dirs(shell_vars)
#     check_long_description_and_license(modname, shell_vars)
#     check_test_qsub_placeholder(modname, shell_vars)  # your earlier check
#     # Create/refresh the module8 test dir (set overwrite=True to regenerate files)
#     test_dir = setup_module8_test_dir(modname, shell_vars, overwrite=False)
#     print(f"Module8 test directory ready at: {test_dir}")
#     check_permissions(modname, shell_vars)




"""The function will not overwrite existing files unless you pass overwrite=True.

It intentionally avoids the module load xyz/0.0.0 placeholder in test.qsub to keep your placeholder check happy.

run_test.sh is marked executable automatically."""
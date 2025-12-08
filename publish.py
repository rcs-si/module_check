import subprocess

def test_publish_module(modname: str, shell_vars: dict, overwrite: bool = False):
    """
    Perform a test-publish of the given module:
    1. Make a /share/module.8/test/<pkg>/ directory
    2. Symlink the real modulefile.lua into that dir as <ver>.lua
    3. cd into the module's test dir
    4. Run 'module use /share/module.8/test'
    5. Submit 'test.qsub' with qsub -V
    """
    install_dir = module_env.get_install_directory(modname, shell_vars)
    inst_start = install_dir.find('install')
    repo_root = install_dir[:inst_start] if inst_start != -1 else os.path.dirname(install_dir)

    if '/' in modname:
        pkg, ver = modname.split('/', 1)
    else:
        pkg, ver = modname, 'unknown'

    # Paths
    modulefile_real = os.path.join(repo_root, 'share', 'pkg.8', pkg, ver, 'modulefile.lua')
    test_dir_root   = os.path.join(repo_root, 'share', 'module.8', 'test', pkg)
    os.makedirs(test_dir_root, exist_ok=True)

    # Link as <ver>.lua
    link_target = os.path.join(test_dir_root, f"{ver}.lua")
    if overwrite and os.path.islink(link_target):
        os.unlink(link_target)
    if not os.path.exists(link_target):
        os.symlink(modulefile_real, link_target)

    # Path to test.qsub
    qsub_dir = os.path.join(repo_root, 'share', 'pkg.8', pkg, ver, 'test')
    qsub_path = os.path.join(qsub_dir, 'test.qsub')

    if not os.path.exists(qsub_path):
        raise Exception(f"No test.qsub found at {qsub_path}")

    # Run the commands in sequence
    try:
        # Extend MODULEPATH temporarily
        subprocess.run(["module", "use", os.path.join(repo_root, "share", "module.8", "test")],
                       check=True)

        # Submit job
        subprocess.run(["qsub", "-V", qsub_path], cwd=qsub_dir, check=True)

        print(f"Passes all checks, auto test-publish and submitted {qsub_path}")

    except subprocess.CalledProcessError as e:
        raise Exception(f"Test publish failed: {e}")

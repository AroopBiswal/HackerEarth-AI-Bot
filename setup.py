import os
import shutil
import subprocess

# Navigate to frontend directory and install dependencies
os.chdir('frontend')
subprocess.run(['npm', 'install'])
subprocess.run(['npm', 'run', 'build'])

# Move back to the root directory
os.chdir('..')

# Copy build files to backend static directory
build_dir = 'frontend/build'
static_dir = 'backend/static'

if os.path.exists(static_dir):
    shutil.rmtree(static_dir)

shutil.copytree(build_dir, static_dir)

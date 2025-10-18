from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
import os
import sys
import subprocess


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        self.configure_macro()

    def configure_macro(self):
        """Configure ChemStation macro after installation."""
        try:
            # Run the configuration script
            script_path = os.path.join(os.path.dirname(__file__), 'configure_macro.py')
            if os.path.exists(script_path):
                subprocess.check_call([sys.executable, script_path])
            else:
                # If script not found, try importing and running configure function
                try:
                    from ChemstationAPI import configure
                    configure()
                except Exception as e:
                    print(f"\nWarning: Could not auto-configure macro: {e}")
                    print("You can manually configure it later by running:")
                    print("  python -m ChemstationAPI.configure")
                    print("or")
                    print("  python -c 'from ChemstationAPI import configure; configure()'\n")
        except Exception as e:
            print(f"\nWarning: Post-install configuration failed: {e}")
            print("Run manually: python -c 'from ChemstationAPI import configure; configure()'\n")


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        self.configure_macro()

    def configure_macro(self):
        """Configure ChemStation macro after development installation."""
        try:
            script_path = os.path.join(os.path.dirname(__file__), 'configure_macro.py')
            if os.path.exists(script_path):
                subprocess.check_call([sys.executable, script_path])
            else:
                try:
                    from ChemstationAPI import configure
                    configure()
                except Exception as e:
                    print(f"\nWarning: Could not auto-configure macro: {e}")
                    print("Run manually: python -c 'from ChemstationAPI import configure; configure()'\n")
        except Exception as e:
            print(f"\nWarning: Post-install configuration failed: {e}")
            print("Run manually: python -c 'from ChemstationAPI import configure; configure()'\n")


# Get absolute path to this file
here = os.path.abspath(os.path.dirname(__file__))

# Read README for long description (optional)
readme_path = os.path.join(here, 'README.md')
if os.path.exists(readme_path):
    with open(readme_path, encoding='utf-8') as f:
        long_description = f.read()
else:
    long_description = ""

setup(
    name="sia-ce-control",
    version="0.1.0",
    author="Richard Maršala",
    author_email="risaniusl@gmail.com",
    description="Combined API for ChemStation CE and SIA control",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Xixaus/SI-CE",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "pyserial>=3.5",
        "tqdm>=4.60.0",
        "pandas>=1.2.0",
        "pywin32>=300; platform_system=='Windows'",
        "openpyxl>=3.1.5"
    ],

    package_data={
        'ChemstationAPI': [
            'controllers/macros/*.mac',
            'core/*.mac',
            'py.typed',
        ],
        'SIA_API': [
            'py.typed',
        ],
    },
    include_package_data=True,
    cmdclass={
        'install': PostInstallCommand,
        'develop': PostDevelopCommand,
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
    ],
)

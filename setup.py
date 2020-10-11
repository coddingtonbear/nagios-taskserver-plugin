from setuptools import setup, find_packages

from nagios_taskserver_plugin import __version__ as version_string


setup(
    name="nagios-taskserver-plugin",
    version=version_string,
    url="https://github.com/coddingtonbear/nagios-taskserver-plugin",
    description=("Monitor taskserver (taskd) using Nagios."),
    author="Adam Coddington",
    author_email="me@adamcoddington.net",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    install_requires=["argparse",],
    include_package_data=True,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "nagios_taskserver_plugin = " "nagios_taskserver_plugin.cmdline:cmdline"
        ],
    },
)

# pylint: disable=missing-docstring
from distutils.core import setup

import os

files = []
for directory in ["mediapanel_beta/static", "mediapanel_beta/templates"]:
    for path, dirs, filenames in os.walk(directory):
        files.append(os.path.join("..", path, "*"))

print(files)

setup(
    name='mediapanel_beta',
    version='0.1-dev',
    packages=['mediapanel_beta'],
    package_data={
        "mediapanel_beta": files,
    },
    extras_require={
        "postgres": "psycopg2-binary",
        "mysql": "pymysql",
    },
    install_requires=['flask', 'flask_sqlalchemy', 'gigaspoon'])

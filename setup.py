from setuptools import setup

setup(
    name='flibusta-dl',
    version='0.1',
    py_modules=['flibusta-dl'],
    install_requires=[
        'requests',
        'pyquery',
        'humanize',
        'click',
        'tqdm',
    ],
    entry_points='''
        [console_scripts]
        flibusta-dl=flibusta_dl.flibusta_dl:cli
    ''',
)

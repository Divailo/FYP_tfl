from setuptools import setup, find_packages


setup(
    name='ivaylo-tfl',
    version='0.3.2',
    packages=find_packages(),
    install_requires=['pywin32'],
    entry_points={
        'console_scripts' : [
            'extract_data_vissim = ivaylotfl.main_extract_data:main',
            'apply_changes_vissim = ivaylotfl.main_apply_changes:main'
        ]
    },
    author='Ivaylo Hristov',
    author_email='ivaylokhr@gmail.com',
    license='MIT',
    py_modules = [
        'ivaylotfl.main_apply_changes',
        'ivaylotfl.main_extract_data',
        'ivaylotfl.dialoghelper',
        'ivaylotfl.jsonhelper',
        'ivaylotfl.pddlhelper',
        'ivaylotfl.puahelper',
        'ivaylotfl.stringhelper',
        'ivaylotfl.vaphelper',
        'ivaylotfl.vissimhelper'
    ]
)

from setuptools import setup, find_packages


setup(
    name='ivaylotfl',
    version='1.0',
    packages=find_packages(),
    install_requires=['pywin32'],
    entry_points={
        'console_scripts' : [
            'extract_data_vissim = ivaylotfl.__main_extract_data:main',
            'apply_changes_vissim = ivaylotfl.__main_apply_changes:main'
        ]
    },
    author='Ivaylo Hristov',
    author_email='ivaylokhr@gmail.com',
    license='MIT',
    py_modules = [
        'ivaylotfl.main_apply_changes',
        'ivaylotfl.main_extract_data',
        'ivaylotfl.__dialoghelper',
        'ivaylotfl.__jsonhelper',
        'ivaylotfl.pddlhelper',
        'ivaylotfl.puahelper',
        'ivaylotfl.stringhelper',
        'ivaylotfl.vaphelper',
        'ivaylotfl.vissimhelper'
    ]
)

from setuptools import setup
setup(
    name='ivaylo-tfl-1',
    version='0.1',
    scripts=['main_extract_data'],
    author='Ivaylo Hristov',
    py_modules = ['dialoghelper',
                  'jsonhelper',
                  'pddlhelper',
                  'puahelper',
                  'stringhelper',
                  'vaphelper',
                  'vissimhelper']
)
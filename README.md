# FYP_tfl

A project which creates an interface between [Vissim](http://vision-traffic.ptvgroup.com/en-us/products/ptv-vissim/) and a [traffic PDDL+ planner](https://pdfs.semanticscholar.org/913e/89b74189b7b5221386671db8bb96916effc6.pdf). The classes of the project could also be used as an external library to extract properties of VAP signal controllers.

### External libraries

[PyWin32](https://sourceforge.net/projects/pywin32) : to enable communicating with COM.

# Install
Before you install you need to make sure that:

* Running <b>Windows</b>, because COM works only on Windows.

* <b>Python</b> is isntalled in your machine.

* <b>Pip</b> is added to your PATH system variable.

* If you want to run the scripts <b>Vissim</b> will be needed.

To install the project all you have to do is run this command in terminal:

```
pip install ivaylotfl
```

# Usage

There are two use cases of the project. You can either:

1. Used the built scripts , or
2. Use the project as an external library for personal projects.

### Run built-in scripts

#### Gather Signal Controller Data in JSON and Construct PDDL file

Run in terminal:

```
extract_data_vissim
```
First you will have to choose a network to run the script for. A JSON file will be created in the same folder as the chosen network with all the data it has gathered. Then you will be asked where to save the newly-generated PDDL problem file. The file will be populated with all the data available from the JSON file.

#### Apply PDDL Results to Network

Run in terminal:

```
extract_data_vissim
```
First you will have to choose PDDL results file and then you will be asked for the network you want to edit. <b>Make sure that the network you've chosen is the same the PDDL results are made for.</b>

### Use as external libraries

Some classes with sample usage and sample output for [those files]()

Vissimhelper

___

```python
from ivaylotfl import vissimhelper
import win32com.client as com

# start the program
vissim = initialise_vissim(com)
# load network
load_vissim_network(vissim, path_to_network)
# bring to front
bring_vissim_to_front(vissim)

# get_signal_controllers(vissim)
>>> Collection of signal controllers 
```

Puahelper

___

```python
from ivaylotfl import puahelper

read_and_map_signalgroups_from_pua(pua_filepath)
>>> {'A' : 1, 'B' : 2, 'C' : 3}

get_phases_in_stages_from_pua(pua_filepath)
>>> { 1 : [1,3], 2 : [2], 3 : [3] }

get_starting_stage_from_pua(pua_filepath)
>>> 1

get_max_stage_from_pua(pua_helper)
>>> 3
```

Vaphelper

___

```python
from ivaylotfl import vaphelper

get_cycle_length_from_vap(vap_filepath)
>>> 15

get_stage_lenghts_from_vap(vap_filepath)
>>> [10,25,45]
```

##### You can get the JSON keys from jsonhelper

# Contribute

To contribute to this project you can fork the project and submit a pull request. Make sure that all unit tests pass before submitting the merge request.

# Future work

- Handle no such file I guess

- := used when declaring VAP variables -> not supported

- Non-VAP SCs not supported

- If original VAP file has no PLAN[x,y] = [];, then it won't work

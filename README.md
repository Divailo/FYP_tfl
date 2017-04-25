# FYP_tfl

A project which creates an interface between [Vissim](http://vision-traffic.ptvgroup.com/en-us/products/ptv-vissim/) and a [traffic PDDL+ planner](https://pdfs.semanticscholar.org/913e/89b74189b7b5221386671db8bb96916effc6.pdf). The classes of the project could also be used as an external library to extract properties of VAP signal controllers.

### External libraries

[PyWin32](https://sourceforge.net/projects/pywin32) : to enable communicating with COM.

# Install
Before you install you need to make sure that:

* Running <b>Windows</b>, because COM works only on Windows.

* <b>Python</b> is isntalled in your machine.

* <b>Pip</b> is added to your PATH system variable.

To install the project all you have to do is run this command in terminal:

```
pip install ivaylotfl
```

# Usage

There are two use cases of the project. You can either:

1. Used the built scripts , or
2. Use the project as an external library

### Run built-in scripts

### Use as external libraries

Puahelper

___

```python
from ivaylotfl import puahelper

read_and_map_signalgroups_from_pua(pua_filepath)
>>> {'V1' : 1, 'V2' : 2}

get_phases_in_stages_from_pua(pua_filepath)
>>> { 1 : [1,3], 2 : [2] }

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

# Contribute

# Future work

- Handle no such file I guess

- := used when declaring VAP variables -> not supported

- Non-VAP SCs not supported

- If original VAP file has no PLAN[x,y] = [];, then it won't work

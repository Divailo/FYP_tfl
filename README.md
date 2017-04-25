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
$ pip install ivaylotfl
```

# Usage

There are two use cases of the project. You can either:

1. Used the built scripts , or
2. Use the project as external libraries

# Contribute

# Stuff to do

- Handle no such file I guess

- := used when declaring VAP variables -> not supported

- Non-VAP SCs not supported

- If original VAP file has no PLAN[x,y] = [];, then it won't work

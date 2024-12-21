# graph_visualizer

## What is it?
Graph_visualizer is a cmd tool for visualizing a dependency graph. Dependencies are defined by the name of the python package (pip). The PlantUML representation is used to describe the dependency graph. The visualizer displays the result on the screen in the form of a code.


## Example

```
python visualizer.py --package requests --output deps.txt --depth 1
```
or
```
python visualizer.py --package scipy --output deps.txt --depth 1
```


## If you don't have pip installed
If you don't have pip installed, follow the steps below:

**Download PIP get-pip.py**
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```
**Installing PIP on Windows**
```
python get-pip.py
```
**Verify Installation**
```
python -m pip help
```

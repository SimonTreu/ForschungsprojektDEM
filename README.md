# ForschungsprojektDEM
Documentation of a research project, applying the Discrete Element Method in a geoscientific context. 

## /docker

here you find a dockerfile which installs all necessary dependencies to install (and compile)
yade on ubuntu. But yade is not yet compiled in this dockerfile.

I use it as Python Interpreter in the PyCharm IDE. Then I have all necessary dependencies to import
yade in pure Python Code.

## /pure_python

this folder contains python code that imports yade. To import yade you will need all necessary python
dependencies. To achieve that I use a docker container as Python Interpreter. The scripts here
are tested with pytest.

## /pure_yade

this folder contains scripts that will run with the ```yade my_script.py``` command.
Pytest will not work here, so I test the python code in the /pure_python folder.

### /official_examples

contains examples from the official yade homepage.

## /documentation

contains some other documentation files and official
yade documentation.
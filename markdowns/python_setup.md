# Set up Python Environment
<hr>
0. use Linux or OSX systems.
1. install [Anaconda](https://anaconda.org/), choose `python 3.6`.
2. `pip install <package-name>` to install packages.

List of packages that you `always` need
    
* **numpy**: basic array operations.
* **scipy**: scientific toolkit based on numpy, where you start your scientific programming.
* **matplotlib**: scientific plots.
* **ipython**: to use notebooks.

List of packages that you `may` need

* **pytorch**: neural network package, install following [installation guide](http://pytorch.org/).

    * select CUDA 8 if you have an Nvidia GPU with properly configured driver
    * select CUDA None if your don’t

* **tensorflow**: alternative to pytorch.
* **viznet**: neural network/tensor network/quantum circuit visualization toolkit.
* **qutip**: toolkit for at time depedant quantum simulation, especially for time dependant qubit systems.
* **fire**: user friendly command line tool.
* **ProjectQ**: quantum circuit simulation, visit github repo to install [https://github.com/ProjectQ-Framework/ProjectQ](https://github.com/ProjectQ-Framework/ProjectQ)

3. read a jupyter notebook to get a feeling of scientific programming, e.g. this repository https://github.com/GiggleLiu/marburg/
4. read a decent python library, learn the **project setup**, **PEP8 coding style**, **google style documentation** and **unit testing**.
e.g. this one [https://github.com/ProjectQ-Framework/ProjectQ](https://github.com/ProjectQ-Framework/ProjectQ)

### How to learn python
Remember, **learn by use**.

To learn python, I suggest you to solve the tasks in notebooks (**step 3**),
or build some quantum circuit in Neilson's quantum computation book using **ProjectQ**.

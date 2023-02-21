# Tuberculosis Transmission Predictor

This Python program predicts the transmission of tuberculosis by clustering reported infected cases by their geographic location. The program uses the k-means or hierarchical algorithm for clustering.

## Installation

To install the necessary packages, first clone the repository:

```
git clone https://github.com/digmouse233/tuberculosis-transmission-predictor.git
cd tuberculosis-transmission-predictor
```

Then, create a virtual environment and activate it:

```
python -m venv venv
source venv/bin/activate   # for Linux/Mac OS
venv\Scripts\activate.bat  # for Windows
```

Finally, install the required packages with pip:

```
pip install -r requirements.txt
```

This will install all the necessary dependencies for the project.

## Usage

To run the program, use the `visualization.py` script.

```shell
python visualization.py
```

The script creates a subdirectory in the `output` directory for each location in the `data` directory, saves the cluster assignments to a .csv file in the corresponding location subdirectory, and generates a map visualization of the clustered data, which is also saved in the corresponding location subdirectory.

## Description

### Directories

- `data/`: This directory contains .csv files with the geographic coordinates of reported tuberculosis cases.
- `output/`: This directory contains the output of the program, including cluster assignments and map visualizations. The program creates a subdirectory in this directory for each location in the `data` directory.
- `venv/`: This directory contains the virtual environment used to run the project.

### Clustering

- `cluster.py`: This file contains the `Cluster` class, which represents a cluster of buildings.
- `hierarchical.py`: This file contains the `HierarchicalCluster` class, which performs hierarchical clustering.
- `k_means.py`: This file contains the `KMeansCluster` class, which performs k-means clustering.

### Data Processing

- `building.py`: This file contains the `Building` class, which represents a building and its location.
- `io_operations.py`: This file contains functions for loading and saving data to and from .csv files.
- `statistics.py`: This file contains functions for calculating statistics on clusters.

### Visualization

- `visualization.py`: This file is the main program file, which loads tuberculosis data from each .csv file in the `data` directory, clusters the data using the k-means or hierarchical algorithm, and saves the results to a subdirectory named after the location in the `output` directory.
- `border.py`: This file contains the `get_border()` function, which is used to calculate the border of a cluster.
- `colors.py`: This file contains functions to generate color values for use in visualizations.
- `scale.py`: This file contains functions for scaling points, moving the border of a cluster, and other related functions.
- `intersects.py`: This file contains the `is_intersects()` function, which is used to determine whether two clusters intersect.

### Other

- `__init__.py`: An empty initialize file.
- `requirements.txt`: A text file listing the required packages to run this project.

## Contributing

If you're interested in contributing to this project, please feel free to submit a pull request. You can also reach out to me at [digmouse233@gmail.com](mailto:digmouse233@gmail.com) if you have any questions or suggestions.

## License

This program is released under the MIT license. See the `LICENSE` file for more.

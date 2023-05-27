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

To run the program, use the `main.py` script.

```shell
python main.py
```

The script creates a subdirectory in the `output` directory for each location in the `data` directory, saves the cluster assignments to a .csv file in the corresponding location subdirectory, and generates a map visualization of the clustered data, which is also saved in the corresponding location subdirectory.

## Contributing

If you're interested in contributing to this project, please feel free to submit a pull request. You can also reach out to me at [digmouse233@gmail.com](mailto:digmouse233@gmail.com) if you have any questions or suggestions.

## License

This program is released under the MIT license. See the `LICENSE` file for more.

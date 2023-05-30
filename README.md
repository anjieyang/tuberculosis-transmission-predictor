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

Running this script will generate two .csv files with time-sequence data within the `sir` folder for each location specified in the `data` directory. These files record the state of the SIR model over time.

A visualization of the model's progression can be accessed locally by running the Dash application, available at `http://127.0.0.1:8050` in your web browser after the script execution.

## License

This program is released under the MIT license. See the `LICENSE` file for more.

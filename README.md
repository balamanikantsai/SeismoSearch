# SeismoSearch

SeismoSearch is a web application for processing and analyzing seismic data. It allows users to upload `.mseed` files, process them, and visualize the results.

## Features

- Upload `.mseed` files for processing
- Visualize seismic data and characteristic functions
- Download processed data as CSV

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/SeismoSearch.git
    cd SeismoSearch
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:
    ```sh
    python app.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000/`.

3. Use the web interface to upload `.mseed` files and view the results.

## How to Use the Application

1. **Home Page**: Navigate to the home page to get an overview of the application.
2. **Upload File**: Go to the "Prediction" page and upload your `.mseed` file.
3. **View Results**: After uploading, the application will process the file and display the detected seismic events and a plot of the characteristic function.
4. **Download CSV**: You can download the processed data as a CSV file for further analysis.

## Algorithm Explanation

The algorithm used in `app.py` for analyzing seismic data involves the following steps:

1. **Reading the Data**: The `.mseed` file is read using the `obspy` library to extract the seismic trace data.
2. **Filtering**: The seismic data is filtered using a bandpass filter to isolate the frequency range of interest.
3. **Spectrogram**: A spectrogram is generated to visualize the frequency content of the filtered data over time.
4. **STA/LTA Calculation**: The Short-Term Average/Long-Term Average (STA/LTA) algorithm is applied to detect seismic events. This involves calculating the ratio of the short-term average to the long-term average of the signal amplitude.
5. **Trigger Detection**: The STA/LTA characteristic function is used to identify potential seismic events based on predefined thresholds.
6. **Result Compilation**: The detected events are compiled into a DataFrame, and the results are plotted and displayed.

### What We Analyze For

The primary goal of the analysis is to detect seismic events within the uploaded `.mseed` file. The analysis focuses on:

- **Seismic Event Detection**: Identifying the times at which seismic events occur based on the STA/LTA characteristic function.
- **Frequency Content**: Visualizing the frequency content of the seismic data using a spectrogram.
- **Characteristic Function**: Plotting the STA/LTA characteristic function to highlight periods of increased seismic activity.

## Project Structure

- `app.py`: Main application file
- `templates/`: HTML templates for the web interface
- `static/`: Static files (CSS, JavaScript, images)
- `uploads/`: Directory for uploaded files

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

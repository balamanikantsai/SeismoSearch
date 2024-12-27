import os
from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from obspy import read
from obspy import signal
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from obspy import read
from scipy import signal
from datetime import timedelta, datetime
from matplotlib import cm
from obspy.signal.invsim import cosine_taper
from obspy.signal.filter import highpass
from obspy.signal.trigger import classic_sta_lta, plot_trigger, trigger_onset




app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

# Function to process the .mseed file using obspy
def process_mseed(mseed_path):
    # Read the mseed file
    st = read(mseed_path)

    # Get the trace
    tr = st.traces[0].copy()
    tr_times = tr.times()
    tr_data = tr.data

    # Start time of trace
    starttime = tr.stats.starttime.datetime

    # Initialize figure for trace
    fig, ax = plt.subplots(1, 1, figsize=(10, 3))

    # Plot trace
    ax.plot(tr_times, tr_data)

    # Set the minimum frequency
    minfreq = 0.5
    maxfreq = 1.0

    # Create a separate trace for the filter data
    st_filt = st.copy()
    st_filt.filter('bandpass', freqmin=minfreq, freqmax=maxfreq)
    tr_filt = st_filt.traces[0].copy()
    tr_times_filt = tr_filt.times()
    tr_data_filt = tr_filt.data

    f, t, sxx = signal.spectrogram(tr_data_filt, tr_filt.stats.sampling_rate)

    # Define sampling frequency
    df = tr.stats.sampling_rate

    # STA and LTA parameters
    sta_len = 120  # seconds
    lta_len = 600  # seconds

    # Run Obspy's STA/LTA
    cft = classic_sta_lta(tr_data, int(sta_len * df), int(lta_len * df))

    # Plot characteristic function
    fig, ax = plt.subplots(1, 1, figsize=(12, 3))
    ax.plot(tr_times, cft)
    ax.set_xlim([min(tr_times), max(tr_times)])
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Characteristic function')

    # Trigger thresholds
    thr_on = 4
    thr_off = 1.5
    on_off = np.array(trigger_onset(cft, thr_on, thr_off))

    # Compile detection times
    detection_times = []
    fnames = []

    for i in np.arange(0, len(on_off)):
        triggers = on_off[i]
        on_time = starttime + timedelta(seconds=tr_times[triggers[0]])
        on_time_str = datetime.strftime(on_time, '%Y-%m-%dT%H:%M:%S.%f')
        detection_times.append(on_time_str)
        fnames.append(mseed_path.split('/')[-1])  # Get filename from path

    # Compile DataFrame of detections
    detect_df = pd.DataFrame(data={'filename': fnames, 
                                    'time_abs(%Y-%m-%dT%H:%M:%S.%f)': detection_times, 
                                    'time_rel(sec)': tr_times[triggers[0]]})

    return detect_df, fig  # Return the DataFrame and the last figure

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        if 'file' not in request.files or request.files['file'].filename == '':
            return redirect(request.url)

        file = request.files['file']
        # Ensure the upload folder exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Process the uploaded .mseed file
        detection_df, fig = process_mseed(file_path)

        # Convert DataFrame to CSV
        output_csv = io.StringIO()
        detection_df.to_csv(output_csv, index=False)
        output_csv.seek(0)

        # Convert plot to PNG
        fig_io = io.BytesIO()
        FigureCanvas(fig).print_png(fig_io)
        fig_io.seek(0)

        return render_template('result.html', csv_data=output_csv.getvalue(), figure=fig_io.getvalue().decode('latin1'))

    return render_template('prediction.html')

@app.route('/download_csv')
def download_csv():
    csv_data = request.args.get('csv_data')
    output = io.StringIO(csv_data)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='Seismic_Signals_Report.csv')

if __name__ == '__main__':
    app.run(debug=True)

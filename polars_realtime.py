




import polars as pl
import plotly.graph_objects as go
import numpy as np
import time

# Define the sampling rate and the duration of the signal
sampling_rate = 44100  # Hz
duration = 1.0  # In seconds

# Generate the time axis for the signal
t = np.linspace(0, duration, int(sampling_rate * duration), False)

# Generate a sine wave
f = 440  # Frequency of the sine wave in Hz
signal = np.sin(f * 2 * np.pi * t)

# Create a Polars DataFrame to hold the data
df = pl.DataFrame({
    'Time': t,
    'Signal': signal
})

# Create a Plotly figure
fig = go.Figure()

# Add a scatter trace for the signal
fig.add_trace(go.Scatter(x=df['Time'], y=df['Signal'], mode='lines'))

# Set the title and labels
fig.update_layout(
    title='Real-time Sine Wave',
    xaxis_title='Time (seconds)',
    yaxis_title='Amplitude'
)

# Function to update the figure with new data
def update_figure(fig, df):
    fig.data[0].x = df['Time']
    fig.data[0].y = df['Signal']
    fig.update_layout()

while True:
    # Shift the time axis by the duration
    df = df.with_column(pl.col('Time') + duration).rename('Time')

    # Generate a new sine wave
    signal = np.sin(f * 2 * np.pi * (df['Time'] % (1 / f)))

    # Update the signal in the DataFrame
    df = df.with_column(pl.col('Signal').set(signal)).rename('Signal')

    # Update the figure
    update_figure(fig, df)

    # Pause for a while
    time.sleep(0.1)
fig.show()

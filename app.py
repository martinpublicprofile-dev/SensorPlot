import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from io import StringIO
import pickle
import os

# Set page configuration
st.set_page_config(
    page_title="Sensor Data Visualization",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'sensor_data' not in st.session_state:
    st.session_state.sensor_data = {}
if 'sensor_names' not in st.session_state:
    st.session_state.sensor_names = {}

# Pastel colors for different sensors
PASTEL_COLORS = [
    "#FF9999",  # Light red
    "#99CCFF",  # Light blue
    "#99FF99",  # Light green
    "#FFCC99"   # Light orange
]

# File paths for persistent storage
SENSOR_DATA_FILE = "sensor_data.pkl"
SENSOR_NAMES_FILE = "sensor_names.pkl"

def save_sensor_data():
    """Save sensor data to disk for persistence"""
    try:
        with open(SENSOR_DATA_FILE, 'wb') as f:
            pickle.dump(st.session_state.sensor_data, f)
        with open(SENSOR_NAMES_FILE, 'wb') as f:
            pickle.dump(st.session_state.sensor_names, f)
    except Exception as e:
        # Silent fail - don't disrupt the app if saving fails
        pass

def load_sensor_data():
    """Load sensor data from disk if it exists"""
    try:
        if os.path.exists(SENSOR_DATA_FILE) and os.path.exists(SENSOR_NAMES_FILE):
            with open(SENSOR_DATA_FILE, 'rb') as f:
                sensor_data = pickle.load(f)
            with open(SENSOR_NAMES_FILE, 'rb') as f:
                sensor_names = pickle.load(f)
            return sensor_data, sensor_names
    except Exception as e:
        # Silent fail - return empty data if loading fails
        pass
    return {}, {}

def darken_color(hex_color, factor=0.2):
    """Darken a hex color by the given factor (0.0 to 1.0)"""
    # Remove the '#' if present
    hex_color = hex_color.lstrip('#')
    
    # Convert to RGB
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # Darken by reducing each RGB component
    darkened_rgb = tuple(int(component * (1 - factor)) for component in rgb)
    
    # Convert back to hex
    return "#{:02x}{:02x}{:02x}".format(*darkened_rgb)

def validate_csv_structure(df):
    """Validate that the CSV has the required columns"""
    required_columns = 5
    if len(df.columns) < required_columns:
        return False, f"CSV must have at least {required_columns} columns"

    # Check if first column can be parsed as datetime with the expected format
    try:
        pd.to_datetime(df.iloc[:, 0], format='%Y/%m/%d %H:%M:%S', errors='raise')
    except:
        return False, "First column must contain valid date/time values in format YYYY/MM/DD HH:MM:SS"

    # Check if temperature and humidity columns are numeric
    try:
        pd.to_numeric(df.iloc[:, 1], errors='raise')
        pd.to_numeric(df.iloc[:, 3], errors='raise')
    except:
        return False, "Temperature (column 2) and humidity (column 4) must be numeric"

    return True, "Valid CSV structure"

def process_csv_data(uploaded_file, sensor_id):
    """Process uploaded CSV file and return cleaned data"""
    try:
        # Read CSV with header row
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        df = pd.read_csv(stringio, header=0)

        # Validate structure
        is_valid, message = validate_csv_structure(df)
        if not is_valid:
            return None, message

        # Assign column names (use first 5 columns)
        new_columns = ['datetime', 'temperature', 'temp_comfort', 'humidity', 'humidity_comfort']
        if len(df.columns) > 5:
            new_columns.extend([f'extra_{i}' for i in range(5, len(df.columns))])
        df.columns = new_columns[:len(df.columns)]

        # Convert datetime with specific format
        df['datetime'] = pd.to_datetime(df['datetime'], format='%Y/%m/%d %H:%M:%S', errors='coerce')

        # Convert numeric columns
        df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
        df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')

        # Remove rows with invalid data
        df = df.dropna(subset=['datetime', 'temperature', 'humidity'])

        # Sort by datetime
        df = df.sort_values('datetime')

        # Add sensor ID
        df['sensor_id'] = sensor_id

        return df, "Successfully processed CSV data"

    except Exception as e:
        return None, f"Error processing CSV: {str(e)}"

def create_dual_axis_chart(data_dict, visible_series, time_range):
    """Create dual-axis chart with temperature and humidity data"""

    # Create subplot with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Filter data by time range if specified
    filtered_data = {}
    for sensor_id, df in data_dict.items():
        if time_range:
            mask = (df['datetime'] >= time_range[0]) & (df['datetime'] <= time_range[1])
            filtered_data[sensor_id] = df[mask]
        else:
            filtered_data[sensor_id] = df

    # Add temperature traces (left axis)
    for i, (sensor_id, df) in enumerate(filtered_data.items()):
        sensor_name = st.session_state.sensor_names.get(sensor_id, f"Sensor {sensor_id}")
        color = PASTEL_COLORS[i % len(PASTEL_COLORS)]

        # Temperature line
        temp_visible = visible_series.get(f"{sensor_id}_temp", True)
        fig.add_trace(
            go.Scatter(
                x=df['datetime'],
                y=df['temperature'],
                name=f"{sensor_name} - Temperature",
                line=dict(color=color, width=2),
                visible=temp_visible,
                hovertemplate="<b>" + f"{sensor_name} - Temperature" + "</b><br>" +
                             "Time: %{x|%H:%M}<br>" +
                             "Temperature: %{y:.1f}°C<br>" +
                             "<extra></extra>"
            ),
            secondary_y=False
        )

        # Humidity line
        humidity_visible = visible_series.get(f"{sensor_id}_humidity", True)
        humidity_color = darken_color(color, 0.2)
        fig.add_trace(
            go.Scatter(
                x=df['datetime'],
                y=df['humidity'],
                name=f"{sensor_name} - Humidity",
                line=dict(color=humidity_color, width=2),
                visible=humidity_visible,
                hovertemplate="<b>" + f"{sensor_name} - Humidity" + "</b><br>" +
                             "Time: %{x|%H:%M}<br>" +
                             "Humidity: %{y:.1f}%<br>" +
                             "<extra></extra>"
            ),
            secondary_y=True
        )

    # Update layout for minimalist design
    fig.update_layout(
        title=None,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=0, r=0, t=40, b=0),
        height=600,
        hovermode='x unified'
    )

    # Update x-axis with day separators
    fig.update_xaxes(
        showgrid=True,
        gridwidth=0.3,
        gridcolor='#E0E0E0',
        showline=False,
        zeroline=False,
        tickformat='%m/%d',
        dtick='D1',
        minor=dict(
            dtick='D1',
            showgrid=True,
            gridwidth=0.2,
            gridcolor='#F0F0F0'
        )
    )

    # Update y-axes with hairline grids
    fig.update_yaxes(
        title_text="Temperature (°C)",
        showgrid=True,
        gridwidth=0.3,
        gridcolor='#E0E0E0',
        showline=False,
        zeroline=False,
        side='left',
        secondary_y=False
    )

    fig.update_yaxes(
        title_text="Humidity (%)",
        showgrid=False,
        showline=False,
        zeroline=False,
        side='right',
        secondary_y=True
    )

    return fig

def create_daily_averages_chart(data_dict, visible_series, time_range, time_of_day_range=None):
    """Create dual-axis chart with daily average temperature and humidity data"""

    # Create subplot with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Calculate daily averages for each sensor
    daily_data = {}
    for sensor_id, df in data_dict.items():
        # Filter by time range if specified
        if time_range:
            mask = (df['datetime'] >= time_range[0]) & (df['datetime'] <= time_range[1])
            filtered_df = df[mask]
        else:
            filtered_df = df

        if not filtered_df.empty:
            # Filter by time of day if specified
            if time_of_day_range:
                start_time = datetime.time(time_of_day_range[0] // 4, (time_of_day_range[0] % 4) * 15)
                end_time = datetime.time(time_of_day_range[1] // 4, (time_of_day_range[1] % 4) * 15)
                
                filtered_df = filtered_df.copy()
                filtered_df['time'] = filtered_df['datetime'].dt.time
                
                if start_time <= end_time:
                    # Normal case: start before end (e.g., 06:00 to 18:00)
                    time_mask = (filtered_df['time'] >= start_time) & (filtered_df['time'] <= end_time)
                else:
                    # Cross-midnight case: start after end (e.g., 18:00 to 06:00)
                    time_mask = (filtered_df['time'] >= start_time) | (filtered_df['time'] <= end_time)
                
                filtered_df = filtered_df[time_mask]

            # Group by date and calculate averages
            daily_avg = filtered_df.groupby(filtered_df['datetime'].dt.date).agg({
                'temperature': 'mean',
                'humidity': 'mean'
            }).reset_index()
            daily_avg['datetime'] = pd.to_datetime(daily_avg['datetime'])
            daily_data[sensor_id] = daily_avg

    # Add temperature traces (left axis)
    for i, (sensor_id, df) in enumerate(daily_data.items()):
        sensor_name = st.session_state.sensor_names.get(sensor_id, f"Sensor {sensor_id}")
        color = PASTEL_COLORS[i % len(PASTEL_COLORS)]

        # Temperature bars
        temp_visible = visible_series.get(f"{sensor_id}_temp_daily", True)
        fig.add_trace(
            go.Bar(
                x=df['datetime'],
                y=df['temperature'],
                name=f"{sensor_name} - Avg Temperature",
                marker_color=color,
                opacity=0.7,
                visible=temp_visible,
                hovertemplate="<b>" + f"{sensor_name} - Avg Temperature" + "</b><br>" +
                             "Date: %{x|%Y/%m/%d}<br>" +
                             "Avg Temperature: %{y:.1f}°C<br>" +
                             "<extra></extra>",
                yaxis='y',
                offsetgroup=f'temp_{i}'
            ),
            secondary_y=False
        )

        # Humidity bars
        humidity_visible = visible_series.get(f"{sensor_id}_humidity_daily", True)
        humidity_color = darken_color(color, 0.2)
        fig.add_trace(
            go.Bar(
                x=df['datetime'],
                y=df['humidity'],
                name=f"{sensor_name} - Avg Humidity",
                marker_color=humidity_color,
                opacity=0.6,
                visible=humidity_visible,
                hovertemplate="<b>" + f"{sensor_name} - Avg Humidity" + "</b><br>" +
                             "Date: %{x|%Y/%m/%d}<br>" +
                             "Avg Humidity: %{y:.1f}%<br>" +
                             "<extra></extra>",
                yaxis='y2',
                offsetgroup=f'humidity_{i}'
            ),
            secondary_y=True
        )

    # Update layout for minimalist design
    fig.update_layout(
        title=None,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=0, r=0, t=40, b=0),
        height=400,
        hovermode='x unified',
        barmode='group',
        bargap=0.1,
        bargroupgap=0.1
    )

    # Update x-axis with day separators
    fig.update_xaxes(
        showgrid=True,
        gridwidth=0.3,
        gridcolor='#E0E0E0',
        showline=False,
        zeroline=False,
        tickformat='%m/%d',
        dtick='D1'
    )

    # Update y-axes with hairline grids
    fig.update_yaxes(
        title_text="Temperature (°C)",
        showgrid=True,
        gridwidth=0.3,
        gridcolor='#E0E0E0',
        showline=False,
        zeroline=False,
        side='left',
        secondary_y=False
    )

    fig.update_yaxes(
        title_text="Humidity (%)",
        showgrid=False,
        showline=False,
        zeroline=False,
        side='right',
        secondary_y=True
    )

    return fig

def main():
    # Initialize session state if not already done
    if 'sensor_data' not in st.session_state:
        # Try to load from disk first
        loaded_data, loaded_names = load_sensor_data()
        st.session_state.sensor_data = loaded_data
        st.session_state.sensor_names = loaded_names
    if 'sensor_names' not in st.session_state:
        st.session_state.sensor_names = {}
    
    st.markdown("<h1 style='color: #888888;'>Sensor Data Visualization</h1>", unsafe_allow_html=True)
    st.markdown("Upload CSV files containing temperature and humidity sensor data for visualization")
    
    # Show currently loaded data status
    if st.session_state.sensor_data:
        loaded_sensors = []
        for sensor_id, data in st.session_state.sensor_data.items():
            sensor_name = st.session_state.sensor_names.get(sensor_id, f"Sensor {sensor_id}")
            loaded_sensors.append(f"{sensor_name} ({len(data)} records)")
        
        st.info(f"📊 **Currently loaded:** {', '.join(loaded_sensors)}")
    else:
        st.info("📤 **No data loaded** - Upload CSV files to begin visualization")

    # Sidebar for file uploads and controls
    with st.sidebar:
        st.markdown("<h2 style='color: #888888;'>Data Upload</h2>", unsafe_allow_html=True)
        
        # Clear all data button
        if st.session_state.sensor_data:
            if st.button("🗑️ Clear All Data", help="Remove all uploaded sensor data"):
                st.session_state.sensor_data = {}
                st.session_state.sensor_names = {}
                save_sensor_data()
                st.rerun()

        uploaded_files = {}
        for i in range(1, 5):
            # Check if this sensor has loaded data
            has_data = i in st.session_state.sensor_data
            data_status = f" ({len(st.session_state.sensor_data[i])} records)" if has_data else ""
            
            # Sensor name input as subheader - use saved name if available
            default_name = st.session_state.sensor_names.get(i, f"Sensor {i}")
            sensor_name = st.text_input(
                f"Name{data_status}",
                value=default_name,
                key=f"name_{i}",
                placeholder=f"Enter name for Sensor {i}"
            )
            
            # Update the name in session state whenever it changes
            if sensor_name != default_name:
                st.session_state.sensor_names[i] = sensor_name
                if has_data:  # Only save if we have data
                    save_sensor_data()

            # File upload
            uploaded_file = st.file_uploader(
                f"Choose CSV file",
                type=['csv'],
                key=f"file_{i}",
                help="Upload a new file to replace existing data" if has_data else None
            )

            if uploaded_file is not None:
                uploaded_files[i] = uploaded_file
                st.session_state.sensor_names[i] = sensor_name

                # Process the file
                with st.spinner(f"Processing Sensor {i} data..."):
                    processed_data, message = process_csv_data(uploaded_file, i)

                    if processed_data is not None:
                        st.session_state.sensor_data[i] = processed_data
                        # Save to disk for persistence
                        save_sensor_data()
                        st.success(f"{len(processed_data)} records loaded")
                    else:
                        st.error(f"{message}")
                        if i in st.session_state.sensor_data:
                            del st.session_state.sensor_data[i]
                            # Save updated state to disk
                            save_sensor_data()
            else:
                # Don't remove data just because no new file is uploaded
                # The data persists until explicitly cleared or replaced
                pass

    # Main content area
    if st.session_state.sensor_data:
        # Get time range for all data
        all_dates = []
        for df in st.session_state.sensor_data.values():
            all_dates.extend(df['datetime'].tolist())

        if all_dates:
            min_date = min(all_dates).date()
            max_date = max(all_dates).date()

            # Time range selection with slider
            st.markdown("<h3 style='color: #888888;'>Time Range Selection</h3>", unsafe_allow_html=True)

            # Convert dates to datetime objects for slider
            min_datetime = datetime.datetime.combine(min_date, datetime.time.min)
            max_datetime = datetime.datetime.combine(max_date, datetime.time.max)

            # Style the slider with custom CSS
            st.markdown("""
            <style>
            /* Style the slider handles as large dots */
            .stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"] {
                width: 20px !important;
                height: 20px !important;
                background-color: #FF9999 !important;
                border-radius: 50% !important;
                border: none !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
            }

            /* Style the base slider track as light grey */
            .stSlider > div[data-baseweb="slider"] > div > div {
                background-color: #E0E0E0 !important;
                height: 4px !important;
            }

            /* Style the active portion (between handles) as accent color */
            .stSlider > div[data-baseweb="slider"] > div > div > div:not([role="slider"]) {
                background-color: #FF9999 !important;
            }
            </style>
            """, unsafe_allow_html=True)

            selected_range = st.slider(
                "Select time range:",
                min_value=min_datetime,
                max_value=max_datetime,
                value=(min_datetime, max_datetime),
                step=datetime.timedelta(hours=1),
                format="HH:mm DD/MM/YY"
            )

            # Use datetime objects directly
            start_datetime = selected_range[0]
            end_datetime = selected_range[1]

            time_range = (start_datetime, end_datetime)

            

            # Data series visibility controls
            st.markdown("<h3 style='color: #888888;'>Raw Data Series Visibility</h3>", unsafe_allow_html=True)
            visible_series = {}

            cols = st.columns(len(st.session_state.sensor_data))
            for i, (sensor_id, df) in enumerate(st.session_state.sensor_data.items()):
                with cols[i]:
                    sensor_name = st.session_state.sensor_names.get(sensor_id, f"Sensor {sensor_id}")
                    st.write(f"**{sensor_name}**")

                    visible_series[f"{sensor_id}_temp"] = st.checkbox(
                        "Temperature",
                        value=True,
                        key=f"temp_{sensor_id}"
                    )

                    visible_series[f"{sensor_id}_humidity"] = st.checkbox(
                        "Humidity",
                        value=False,
                        key=f"humidity_{sensor_id}"
                    )

            # Create and display raw data chart
            st.markdown("<h3 style='color: #888888;'>Raw Sensor Data</h3>", unsafe_allow_html=True)

            try:
                chart = create_dual_axis_chart(
                    st.session_state.sensor_data,
                    visible_series,
                    time_range
                )
                st.plotly_chart(chart, use_container_width=True)

            except Exception as e:
                st.error(f"Error creating raw data chart: {str(e)}")

            # Daily averages visibility controls
            st.markdown("<h3 style='color: #888888;'>Daily Averages Series Visibility</h3>", unsafe_allow_html=True)
            visible_series_daily = {}

            cols_daily = st.columns(len(st.session_state.sensor_data))
            for i, (sensor_id, df) in enumerate(st.session_state.sensor_data.items()):
                with cols_daily[i]:
                    sensor_name = st.session_state.sensor_names.get(sensor_id, f"Sensor {sensor_id}")
                    st.write(f"**{sensor_name}**")

                    visible_series_daily[f"{sensor_id}_temp_daily"] = st.checkbox(
                        "Avg Temperature",
                        value=True,
                        key=f"temp_daily_{sensor_id}"
                    )

                    visible_series_daily[f"{sensor_id}_humidity_daily"] = st.checkbox(
                        "Avg Humidity",
                        value=False,
                        key=f"humidity_daily_{sensor_id}"
                    )

            # Create and display daily averages chart
            st.markdown("<h3 style='color: #888888;'>Daily Averages</h3>", unsafe_allow_html=True)
            
            # Time of day selection for averages calculation
            st.markdown('<span style="color: #888888; font-size: 14px; font-weight: bold;">Time of Day Range for Averages</span>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                start_time = st.time_input(
                    "Start Time",
                    value=datetime.time(0, 0),
                    step=datetime.timedelta(minutes=15),
                    key="start_time"
                )
            with col2:
                end_time = st.time_input(
                    "End Time",
                    value=datetime.time(23, 45),
                    step=datetime.timedelta(minutes=15),
                    key="end_time"
                )
            
            # Convert times to interval format for filtering function
            start_interval = (start_time.hour * 4) + (start_time.minute // 15)
            end_interval = (end_time.hour * 4) + (end_time.minute // 15)
            time_of_day_range = (start_interval, end_interval)

            try:
                daily_chart = create_daily_averages_chart(
                    st.session_state.sensor_data,
                    visible_series_daily,
                    time_range,
                    time_of_day_range
                )
                st.plotly_chart(daily_chart, use_container_width=True)

            except Exception as e:
                st.error(f"Error creating daily averages chart: {str(e)}")

    else:
        # Empty state
        st.info("Please upload at least one CSV file in the sidebar to begin visualization")

        # Show expected CSV format
        with st.expander("Expected CSV Format"):
            st.markdown("""
            Your CSV files should have the following structure (no header row required):

            | Column | Description |
            |--------|-------------|
            | A | Date and Time (e.g., 2025-01-01 12:00:00) |
            | B | Temperature value (numeric) |
            | C | Temperature comfort flag (any value) |
            | D | Humidity value (numeric) |
            | E | Humidity comfort flag (any value) |

            **Example:**
            ```
            DateTime,Temperature,TempComfort,Humidity,HumidityComfort
            2025/07/15 00:15:00,23.5,normal,65.2,normal
            2025/07/15 00:20:00,24.1,normal,66.8,normal
            2025/07/15 00:25:00,24.8,high,67.1,normal
            ```
            """)

if __name__ == "__main__":
    main()
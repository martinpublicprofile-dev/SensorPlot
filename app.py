import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from io import StringIO
import pickle
import os
import json

# Set page configuration
st.set_page_config(
    page_title="Sensor Data",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force app name for mobile installation
st.markdown("""
<head>
    <meta name="application-name" content="Sensor Data">
    <meta name="apple-mobile-web-app-title" content="Sensor Data">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="theme-color" content="#FF9999">
    <link rel="manifest" href="data:application/json;base64,eyJuYW1lIjoiU2Vuc29yIERhdGEiLCJzaG9ydF9uYW1lIjoiU2Vuc29yIERhdGEiLCJkaXNwbGF5Ijoic3RhbmRhbG9uZSIsInRoZW1lX2NvbG9yIjoiI0ZGOTk5OSIsImJhY2tncm91bmRfY29sb3IiOiIjZmZmZmZmIiwiaWNvbnMiOlt7InNyYyI6ImRhdGE6aW1hZ2Uvc3ZnK3htbDtiYXNlNjQsUEhOMlp5QjNhV1IwYUQwaU1qUWlJR2hsYVdkb2REMGlNalFpSUhabGNuTnBiMjQ5SWpFdU1TSWdlRzFzYm5NOUltaDBkSEE2THk5M2QzY3Vkek11YjNKbkx6SXdNREF2YzNabklqNEtJQ0E4Y21WamRDQjNhV1IwYUQwaU1qUWlJR2hsYVdkb2REMGlNalFpSUdacGJHdzlJaU5HUmprelF6a2lMejRLSUNBOGRHVjRkQ0I0UFNJeE1pSWdlVDBpTVRVaUlHWnBiR3c5SWlOeklpQm1iMjUwTFdaaGJXbHNlVDBpYkc5bmFXTnZaU3c4TDNSbGVIUStDaUE4TDNOMlp6NEsiLCJzaXplcyI6IjI0eDI0IiwidHlwZSI6ImltYWdlL3N2Zyt4bWwifV19">
""", unsafe_allow_html=True)

# Add the proper manifest link for PWA installation
manifest_json = json.dumps({
    "name": "Sensor Data",
    "short_name": "Sensor Data",
    "description": "Temperature and humidity sensor data visualization",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#FF9999",
    "scope": "/",
    "icons": [
        {
            "src": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTkyIiBoZWlnaHQ9IjE5MiIgdmlld0JveD0iMCAwIDE5MiAxOTIiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4gIDxyZWN0IHdpZHRoPSIxOTIiIGhlaWdodD0iMTkyIiBmaWxsPSIjRkY5OTk5Ii8+ICA8dGV4dCB4PSI5NiIgeT0iMTIwIiBmaWxsPSIjZmZmIiBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iNDgiIGZvbnQtd2VpZ2h0PSJib2xkIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj7wn5OKPC90ZXh0Pjwvc3ZnPg==",
            "sizes": "192x192",
            "type": "image/svg+xml"
        },
        {
            "src": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEyIiBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDUxMiA1MTIiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4gIDxyZWN0IHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiBmaWxsPSIjRkY5OTk5Ii8+ICA8dGV4dCB4PSIyNTYiIHk9IjMyMCIgZmlsbD0iI2ZmZiIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjEyOCIgZm9udC13ZWlnaHQ9ImJvbGQiIHRleHQtYW5jaG9yPSJtaWRkbGUiPvCfk4o8L3RleHQ+PC9zdmc+",
            "sizes": "512x512",
            "type": "image/svg+xml"
        }
    ]
}).replace('"', '%22').replace(' ', '%20').replace('\n', '')

st.markdown(f'<link rel="manifest" href="data:application/json,{manifest_json}">', unsafe_allow_html=True)

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
    "#B3B3B3"   # 30% grey
]

# File paths for persistent storage
SENSOR_DATA_FILE = "sensor_data.pkl"
SENSOR_NAMES_FILE = "sensor_names.pkl"
UI_STATE_FILE = "ui_state.pkl"

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

def save_ui_state():
    """Save UI state including axis settings, time ranges, and checkbox states"""
    ui_state = {
        'temp_axis_min_raw': getattr(st.session_state, 'temp_axis_min_raw', None),
        'temp_axis_max_raw': getattr(st.session_state, 'temp_axis_max_raw', None),
        'temp_axis_min_daily': getattr(st.session_state, 'temp_axis_min_daily', None),
        'temp_axis_max_daily': getattr(st.session_state, 'temp_axis_max_daily', None),
        'time_range_start': getattr(st.session_state, 'time_range_start', None),
        'time_range_end': getattr(st.session_state, 'time_range_end', None),
        'start_time': getattr(st.session_state, 'start_time', None),
        'end_time': getattr(st.session_state, 'end_time', None),
    }
    
    # Save checkbox states for all sensors
    for sensor_id in st.session_state.get('sensor_data', {}):
        ui_state[f'temp_{sensor_id}'] = getattr(st.session_state, f'temp_{sensor_id}', True)
        ui_state[f'humidity_{sensor_id}'] = getattr(st.session_state, f'humidity_{sensor_id}', False)
        ui_state[f'temp_daily_{sensor_id}'] = getattr(st.session_state, f'temp_daily_{sensor_id}', True)
        ui_state[f'humidity_daily_{sensor_id}'] = getattr(st.session_state, f'humidity_daily_{sensor_id}', False)
    
    try:
        with open(UI_STATE_FILE, 'wb') as f:
            pickle.dump(ui_state, f)
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

def load_ui_state():
    """Load UI state from disk if it exists"""
    try:
        if os.path.exists(UI_STATE_FILE):
            with open(UI_STATE_FILE, 'rb') as f:
                return pickle.load(f)
    except Exception as e:
        # Silent fail - return empty dict if loading fails
        pass
    return {}

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

def create_dual_axis_chart(data_dict, visible_series, time_range, temp_axis_range=None):
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
    temp_axis_config = dict(
        title_text="Temperature (°C)",
        showgrid=True,
        gridwidth=0.3,
        gridcolor='#E0E0E0',
        showline=False,
        zeroline=False,
        side='left'
    )
    
    # Add temperature axis range if specified
    if temp_axis_range and temp_axis_range[0] is not None and temp_axis_range[1] is not None:
        temp_axis_config['range'] = [temp_axis_range[0], temp_axis_range[1]]
    
    fig.update_yaxes(
        **temp_axis_config,
        secondary_y=False
    )

    fig.update_yaxes(
        title_text="Humidity (%)",
        showgrid=False,
        showline=False,
        zeroline=False,
        side='right',
        range=[0, 100],  # Fixed 0-100% range for humidity
        secondary_y=True
    )

    return fig

def create_daily_averages_chart(data_dict, visible_series, time_range, time_of_day_range=None, temp_axis_range=None):
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
    temp_axis_config_daily = dict(
        title_text="Temperature (°C)",
        showgrid=True,
        gridwidth=0.3,
        gridcolor='#E0E0E0',
        showline=False,
        zeroline=False,
        side='left'
    )
    
    # Add temperature axis range if specified
    if temp_axis_range and temp_axis_range[0] is not None and temp_axis_range[1] is not None:
        temp_axis_config_daily['range'] = [temp_axis_range[0], temp_axis_range[1]]
    
    fig.update_yaxes(
        **temp_axis_config_daily,
        secondary_y=False
    )

    fig.update_yaxes(
        title_text="Humidity (%)",
        showgrid=False,
        showline=False,
        zeroline=False,
        side='right',
        range=[0, 100],  # Fixed 0-100% range for humidity
        secondary_y=True
    )

    return fig

def check_password():
    """Check if the user has entered the correct password"""
    # Force title update for mobile app name
    st.markdown('<script>document.title = "Sensor Data";</script>', unsafe_allow_html=True)
    
    if 'password_correct' not in st.session_state:
        st.session_state.password_correct = False
    
    if not st.session_state.password_correct:
        st.title("🔒 Sensor Data Access")
        st.markdown("### Please enter the password to access the sensor data visualization")
        
        password = st.text_input("Password:", type="password", key="password_input")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col2:
            if st.button("Access", type="primary"):
                if password == "sensordata":
                    st.session_state.password_correct = True
                    st.rerun()
                else:
                    st.error("Incorrect password. Please try again.")
        
        st.stop()

def main():
    # Check password first
    check_password()
    
    # Initialize session state if not already done
    if 'sensor_data' not in st.session_state:
        # Try to load from disk first
        loaded_data, loaded_names = load_sensor_data()
        st.session_state.sensor_data = loaded_data
        st.session_state.sensor_names = loaded_names
    if 'sensor_names' not in st.session_state:
        st.session_state.sensor_names = {}
    
    # Load UI state from disk
    if 'ui_state_loaded' not in st.session_state:
        ui_state = load_ui_state()
        for key, value in ui_state.items():
            if key not in st.session_state:
                st.session_state[key] = value
        st.session_state.ui_state_loaded = True
    
    # Initialize UI state defaults if not loaded
    if 'temp_axis_min_raw' not in st.session_state:
        st.session_state.temp_axis_min_raw = None
    if 'temp_axis_max_raw' not in st.session_state:
        st.session_state.temp_axis_max_raw = None
    if 'temp_axis_min_daily' not in st.session_state:
        st.session_state.temp_axis_min_daily = None
    if 'temp_axis_max_daily' not in st.session_state:
        st.session_state.temp_axis_max_daily = None
    
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
        # Add logout option for authenticated users
        st.markdown("---")
        if st.button("🔓 Logout", help="Logout and return to password screen"):
            st.session_state.password_correct = False
            st.rerun()
        
        st.markdown("<h2 style='color: #888888;'>Data Upload</h2>", unsafe_allow_html=True)
        
        # Clear all data button
        if st.session_state.sensor_data:
            if st.button("🗑️ Clear All Data", help="Remove all uploaded sensor data"):
                st.session_state.sensor_data = {}
                st.session_state.sensor_names = {}
                save_sensor_data()
                save_ui_state()
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
                        save_ui_state()
                        st.success(f"{len(processed_data)} records loaded")
                    else:
                        st.error(f"{message}")
                        if i in st.session_state.sensor_data:
                            del st.session_state.sensor_data[i]
                            # Save updated state to disk
                            save_sensor_data()
                            save_ui_state()
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

            # Convert dates to datetime objects for slider - align to daily boundaries at 0:00
            min_datetime = datetime.datetime.combine(min_date, datetime.time.min)  # Start of first day
            max_datetime = datetime.datetime.combine(max_date, datetime.time.min)  # Start of last day
            
            # Use saved time range if available, but align to daily boundaries
            saved_start = st.session_state.get('time_range_start')
            saved_end = st.session_state.get('time_range_end')
            
            # If we have saved values, align them to daily boundaries (0:00)
            if saved_start:
                default_start = datetime.datetime.combine(saved_start.date(), datetime.time.min)
            else:
                default_start = min_datetime
                
            if saved_end:
                default_end = datetime.datetime.combine(saved_end.date(), datetime.time.min)
            else:
                default_end = max_datetime
            
            # Ensure defaults are within valid range
            if default_start < min_datetime:
                default_start = min_datetime
            if default_end > max_datetime:
                default_end = max_datetime

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
                value=(default_start, default_end),
                step=datetime.timedelta(days=1),
                format="DD/MM/YY",
                key="time_range_slider"
            )

            # Use datetime objects directly - ensure they represent full days
            # Start datetime is the beginning of the selected start day (0:00)
            start_datetime = datetime.datetime.combine(selected_range[0].date(), datetime.time.min)
            # End datetime is the end of the selected end day (23:59:59.999999)
            end_datetime = datetime.datetime.combine(selected_range[1].date(), datetime.time.max)
            
            # Save time range to session state
            if (st.session_state.get('time_range_start') != start_datetime or 
                st.session_state.get('time_range_end') != end_datetime):
                st.session_state.time_range_start = start_datetime
                st.session_state.time_range_end = end_datetime
                save_ui_state()

            time_range = (start_datetime, end_datetime)

            

            # Data series visibility controls
            st.markdown("<h3 style='color: #888888;'>Raw Data Series Visibility</h3>", unsafe_allow_html=True)
            visible_series = {}

            cols = st.columns(len(st.session_state.sensor_data))
            for i, (sensor_id, df) in enumerate(st.session_state.sensor_data.items()):
                with cols[i]:
                    sensor_name = st.session_state.sensor_names.get(sensor_id, f"Sensor {sensor_id}")
                    st.write(f"**{sensor_name}**")

                    # Get saved checkbox states, with defaults
                    temp_default = st.session_state.get(f"temp_{sensor_id}", True)
                    humidity_default = st.session_state.get(f"humidity_{sensor_id}", False)
                    
                    visible_series[f"{sensor_id}_temp"] = st.checkbox(
                        "Temperature",
                        value=temp_default,
                        key=f"temp_{sensor_id}",
                        on_change=save_ui_state
                    )

                    visible_series[f"{sensor_id}_humidity"] = st.checkbox(
                        "Humidity",
                        value=humidity_default,
                        key=f"humidity_{sensor_id}",
                        on_change=save_ui_state
                    )

            # Create and display raw data chart
            st.markdown("<h3 style='color: #888888;'>Raw Sensor Data</h3>", unsafe_allow_html=True)
            
            # Temperature axis controls for raw data
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                temp_min_raw = st.number_input(
                    "Min Temperature (°C)",
                    value=st.session_state.temp_axis_min_raw,
                    step=1.0,
                    key="temp_min_raw_input"
                )
            with col2:
                temp_max_raw = st.number_input(
                    "Max Temperature (°C)",
                    value=st.session_state.temp_axis_max_raw,
                    step=1.0,
                    key="temp_max_raw_input"
                )
            with col3:
                if st.button("Auto", key="auto_raw"):
                    st.session_state.temp_axis_min_raw = None
                    st.session_state.temp_axis_max_raw = None
                    save_ui_state()
                    st.rerun()
            
            # Update session state and save
            if st.session_state.temp_axis_min_raw != temp_min_raw or st.session_state.temp_axis_max_raw != temp_max_raw:
                st.session_state.temp_axis_min_raw = temp_min_raw
                st.session_state.temp_axis_max_raw = temp_max_raw
                save_ui_state()
            
            # Prepare temperature axis range
            temp_axis_range_raw = None
            if temp_min_raw is not None and temp_max_raw is not None:
                temp_axis_range_raw = [temp_min_raw, temp_max_raw]

            try:
                chart = create_dual_axis_chart(
                    st.session_state.sensor_data,
                    visible_series,
                    time_range,
                    temp_axis_range_raw
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

                    # Get saved checkbox states, with defaults
                    temp_daily_default = st.session_state.get(f"temp_daily_{sensor_id}", True)
                    humidity_daily_default = st.session_state.get(f"humidity_daily_{sensor_id}", False)
                    
                    visible_series_daily[f"{sensor_id}_temp_daily"] = st.checkbox(
                        "Avg Temperature",
                        value=temp_daily_default,
                        key=f"temp_daily_{sensor_id}",
                        on_change=save_ui_state
                    )

                    visible_series_daily[f"{sensor_id}_humidity_daily"] = st.checkbox(
                        "Avg Humidity",
                        value=humidity_daily_default,
                        key=f"humidity_daily_{sensor_id}",
                        on_change=save_ui_state
                    )

            # Create and display daily averages chart
            st.markdown("<h3 style='color: #888888;'>Daily Averages</h3>", unsafe_allow_html=True)
            
            # Temperature axis controls for daily averages
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                temp_min_daily = st.number_input(
                    "Min Temperature (°C)",
                    value=st.session_state.temp_axis_min_daily,
                    step=1.0,
                    key="temp_min_daily_input"
                )
            with col2:
                temp_max_daily = st.number_input(
                    "Max Temperature (°C)",
                    value=st.session_state.temp_axis_max_daily,
                    step=1.0,
                    key="temp_max_daily_input"
                )
            with col3:
                if st.button("Auto", key="auto_daily"):
                    st.session_state.temp_axis_min_daily = None
                    st.session_state.temp_axis_max_daily = None
                    save_ui_state()
                    st.rerun()
            
            # Update session state and save
            if st.session_state.temp_axis_min_daily != temp_min_daily or st.session_state.temp_axis_max_daily != temp_max_daily:
                st.session_state.temp_axis_min_daily = temp_min_daily
                st.session_state.temp_axis_max_daily = temp_max_daily
                save_ui_state()
            
            # Prepare temperature axis range
            temp_axis_range_daily = None
            if temp_min_daily is not None and temp_max_daily is not None:
                temp_axis_range_daily = [temp_min_daily, temp_max_daily]
            
            # Time of day selection for averages calculation
            st.markdown('<span style="color: #888888; font-size: 14px; font-weight: bold;">Time of Day Range for Averages</span>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                start_time_default = st.session_state.get('start_time', datetime.time(0, 0))
                start_time = st.time_input(
                    "Start Time",
                    value=start_time_default,
                    step=datetime.timedelta(minutes=15),
                    key="start_time",
                    on_change=save_ui_state
                )
            with col2:
                end_time_default = st.session_state.get('end_time', datetime.time(23, 45))
                end_time = st.time_input(
                    "End Time",
                    value=end_time_default,
                    step=datetime.timedelta(minutes=15),
                    key="end_time",
                    on_change=save_ui_state
                )
            
            # Convert times to interval format for filtering function
            # Handle None values with defaults
            if start_time is None:
                start_time = datetime.time(0, 0)
            if end_time is None:
                end_time = datetime.time(23, 45)
                
            start_interval = (start_time.hour * 4) + (start_time.minute // 15)
            end_interval = (end_time.hour * 4) + (end_time.minute // 15)
            time_of_day_range = (start_interval, end_interval)

            try:
                daily_chart = create_daily_averages_chart(
                    st.session_state.sensor_data,
                    visible_series_daily,
                    time_range,
                    time_of_day_range,
                    temp_axis_range_daily
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
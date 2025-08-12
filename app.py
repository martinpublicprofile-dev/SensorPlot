import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from io import StringIO

# Set page configuration
st.set_page_config(
    page_title="Sensor Data Visualization",
    page_icon="📊",
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
                hovertemplate="<b>%{fullData.name}</b><br>" +
                             "Time: %{x}<br>" +
                             "Temperature: %{y:.1f}°C<br>" +
                             "<extra></extra>"
            ),
            secondary_y=False
        )
        
        # Humidity line
        humidity_visible = visible_series.get(f"{sensor_id}_humidity", True)
        fig.add_trace(
            go.Scatter(
                x=df['datetime'],
                y=df['humidity'],
                name=f"{sensor_name} - Humidity",
                line=dict(color=color, width=2, dash='dot'),
                visible=humidity_visible,
                hovertemplate="<b>%{fullData.name}</b><br>" +
                             "Time: %{x}<br>" +
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

def main():
    st.title("📊 Sensor Data Visualization")
    st.markdown("Upload CSV files containing temperature and humidity sensor data for visualization")
    
    # Sidebar for file uploads and controls
    with st.sidebar:
        st.header("📁 Data Upload")
        
        uploaded_files = {}
        for i in range(1, 5):
            st.subheader(f"Sensor {i}")
            
            # File upload
            uploaded_file = st.file_uploader(
                f"Choose CSV file for Sensor {i}",
                type=['csv'],
                key=f"file_{i}"
            )
            
            # Sensor name input
            sensor_name = st.text_input(
                f"Sensor {i} Name",
                value=f"Sensor {i}",
                key=f"name_{i}"
            )
            
            if uploaded_file is not None:
                uploaded_files[i] = uploaded_file
                st.session_state.sensor_names[i] = sensor_name
                
                # Process the file
                with st.spinner(f"Processing Sensor {i} data..."):
                    processed_data, message = process_csv_data(uploaded_file, i)
                    
                    if processed_data is not None:
                        st.session_state.sensor_data[i] = processed_data
                        st.success(f"✅ {len(processed_data)} records loaded")
                    else:
                        st.error(f"❌ {message}")
                        if i in st.session_state.sensor_data:
                            del st.session_state.sensor_data[i]
            else:
                # Remove data if file is removed
                if i in st.session_state.sensor_data:
                    del st.session_state.sensor_data[i]
    
    # Main content area
    if st.session_state.sensor_data:
        # Get time range for all data
        all_dates = []
        for df in st.session_state.sensor_data.values():
            all_dates.extend(df['datetime'].tolist())
        
        if all_dates:
            min_date = min(all_dates).date()
            max_date = max(all_dates).date()
            
            # Time range selection
            st.subheader("📅 Time Range Selection")
            col1, col2 = st.columns(2)
            
            with col1:
                start_date = st.date_input(
                    "Start Date",
                    value=min_date,
                    min_value=min_date,
                    max_value=max_date
                )
            
            with col2:
                end_date = st.date_input(
                    "End Date",
                    value=max_date,
                    min_value=min_date,
                    max_value=max_date
                )
            
            time_range = (
                datetime.datetime.combine(start_date, datetime.time.min),
                datetime.datetime.combine(end_date, datetime.time.max)
            )
            
            # Data series visibility controls
            st.subheader("👁️ Data Series Visibility")
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
                        value=True,
                        key=f"humidity_{sensor_id}"
                    )
            
            # Create and display chart
            st.subheader("📈 Sensor Data Visualization")
            
            try:
                chart = create_dual_axis_chart(
                    st.session_state.sensor_data,
                    visible_series,
                    time_range
                )
                st.plotly_chart(chart, use_container_width=True)
                
                # Display data summary
                st.subheader("📊 Data Summary")
                summary_cols = st.columns(len(st.session_state.sensor_data))
                
                for i, (sensor_id, df) in enumerate(st.session_state.sensor_data.items()):
                    with summary_cols[i]:
                        sensor_name = st.session_state.sensor_names.get(sensor_id, f"Sensor {sensor_id}")
                        
                        # Filter data by time range
                        mask = (df['datetime'] >= time_range[0]) & (df['datetime'] <= time_range[1])
                        filtered_df = df[mask]
                        
                        if not filtered_df.empty:
                            st.metric(
                                label=f"{sensor_name} - Records",
                                value=len(filtered_df)
                            )
                            st.metric(
                                label="Avg Temperature",
                                value=f"{filtered_df['temperature'].mean():.1f}°C"
                            )
                            st.metric(
                                label="Avg Humidity",
                                value=f"{filtered_df['humidity'].mean():.1f}%"
                            )
                        else:
                            st.write("No data in selected range")
                            
            except Exception as e:
                st.error(f"Error creating chart: {str(e)}")
    
    else:
        # Empty state
        st.info("👆 Please upload at least one CSV file in the sidebar to begin visualization")
        
        # Show expected CSV format
        with st.expander("📋 Expected CSV Format"):
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

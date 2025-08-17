# Sensor Data Visualization App

A minimalist Streamlit web application for visualizing temperature and humidity sensor data with advanced time-range selection and clean, responsive charting.

## Features

- **Dual-axis interactive charts** with temperature (left scale) and humidity (right scale)
- **CSV upload support** for up to 4 sensors with custom naming
- **Time range selection** with dual-handle slider and real-time date/time display
- **Daily averages** displayed as bar charts with configurable time-of-day filtering
- **Minimalist design** with pastel colors, hairline grids, and clean interface
- **Session persistence** maintaining sensor data and naming across user sessions

## CSV Data Format

Your CSV files should have the following structure with a header row:

| Column | Description |
|--------|-------------|
| DateTime | Date and Time in YYYY/MM/DD HH:MM:SS format |
| Temperature | Temperature value (numeric) |
| TempComfort | Temperature comfort flag (any value) |
| Humidity | Humidity value (numeric) |
| HumidityComfort | Humidity comfort flag (any value) |

**Example:**
```csv
DateTime,Temperature,TempComfort,Humidity,HumidityComfort
2025/07/15 00:15:00,23.5,normal,65.2,normal
2025/07/15 00:20:00,24.1,normal,66.8,normal
2025/07/15 00:25:00,24.8,high,67.1,normal
```

## Deployment

### Streamlit Cloud

1. **Push to GitHub**: Ensure all files are committed and pushed to your GitHub repository
2. **Connect to Streamlit Cloud**: Go to [Streamlit Cloud](https://streamlit.io/cloud) and connect your GitHub repo
3. **Configure deployment**: 
   - Set main file path: `streamlit_app.py`
   - Python version: 3.11
   - Dependencies will be automatically detected from `pyproject.toml`
4. **Deploy**: Click deploy and your app will be live!

### Manual Requirements File for Streamlit Cloud

If Streamlit Cloud needs a `requirements.txt` file, create one with these contents:
```txt
streamlit>=1.48.0
pandas>=2.3.1
plotly>=6.2.0
```

### Local Development

```bash
# Install dependencies
pip install streamlit pandas plotly

# Run the application (main entry point)
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0

# Alternative: run directly with app.py
streamlit run app.py
```

## Configuration

The app includes optimized settings for both local development and cloud deployment:

- **Port**: 8501 (Streamlit Cloud default)
- **Address**: 0.0.0.0 (accessible from any network interface)
- **CORS**: Disabled for cloud deployment compatibility

## Dependencies

- `streamlit>=1.48.0` - Web application framework
- `pandas>=2.3.1` - Data manipulation and CSV processing
- `plotly>=6.2.0` - Interactive charting and visualization

## Technical Features

- **Time-based filtering** with 15-minute interval precision
- **Cross-midnight time ranges** support (e.g., 20:00 to 06:00)
- **Independent visibility controls** for raw data and daily averages
- **Color-coded visualization** with humidity data 20% darker than temperature
- **Responsive design** optimized for data visualization

## License

This project is open source and available under the MIT License.
# Sensor Data Visualization

## Overview

This is a Streamlit web application designed for visualizing sensor data from CSV files. The application provides an interactive interface for uploading, validating, and displaying sensor readings including temperature and humidity measurements. Users can upload multiple sensor datasets and view them through dynamic, color-coded visualizations using Plotly charts.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit for web interface
- **Visualization**: Plotly for interactive charts and graphs
- **Layout**: Wide layout with expandable sidebar for controls
- **State Management**: Streamlit session state for persisting uploaded data and sensor configurations across user interactions

### Data Processing
- **File Handling**: CSV file upload and validation system
- **Data Validation**: Structured validation ensuring CSV files contain required columns (minimum 5 columns with datetime, temperature, and humidity data)
- **Data Structure**: Pandas DataFrames for data manipulation and processing
- **Time Series Support**: Built-in datetime parsing for time-based sensor readings

### User Interface Design
- **Color Scheme**: Predefined pastel color palette for sensor differentiation
- **Interactive Elements**: File upload widgets, data display components
- **Responsive Design**: Wide layout configuration optimized for data visualization
- **Session Persistence**: Maintains sensor data and naming across user sessions

### Data Requirements
- **CSV Format**: Structured CSV files with header row and specific column requirements
- **Required Columns**: Minimum 5 columns (datetime, temperature, temp_comfort, humidity, humidity_comfort)
- **DateTime Format**: YYYY/MM/DD HH:MM:SS format (e.g., 2025/07/15 00:15:00)
- **Data Types**: First column must be datetime-parseable, columns 2 and 4 must be numeric
- **Validation**: Real-time CSV structure validation with descriptive error messages and format checking

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for the user interface
- **Pandas**: Data manipulation and CSV processing
- **Plotly**: Interactive charting and graph generation with subplot support
- **DateTime**: Built-in Python module for time-based operations

### File Processing
- **StringIO**: Python's built-in module for string-based file operations
- **CSV Processing**: Pandas-based CSV reading and validation

### Visualization Components
- **Plotly Graph Objects**: Advanced chart creation and customization
- **Plotly Subplots**: Multi-panel chart layouts for comparative analysis
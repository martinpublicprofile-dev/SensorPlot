# GitHub Setup Instructions

## Overview
This document provides step-by-step instructions to push your Streamlit sensor data visualization app to GitHub and deploy it on Streamlit Cloud.

## Prerequisites
- GitHub account
- Git installed on your local machine (if pushing from local)
- Streamlit Cloud account (free at share.streamlit.io)

## Method 1: Push from Replit (Recommended)

### Step 1: Create GitHub Repository
1. Go to GitHub.com and log in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Repository name: `sensor-data-visualization` (or your preferred name)
5. Description: `Interactive Streamlit app for environmental sensor data visualization with comprehensive persistence`
6. Set to Public or Private (your choice)
7. Do NOT initialize with README, .gitignore, or license (we already have files)
8. Click "Create repository"

### Step 2: Push from Replit
1. Open the Shell tab in Replit
2. Run these commands one by one:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Streamlit sensor data visualization app

- Interactive dual-axis charts for temperature and humidity data
- Daily averages with time-of-day filtering  
- Manual temperature axis controls with fixed humidity range (0-100%)
- Complete UI state persistence across browser refreshes
- Support for up to 4 sensor CSV uploads
- Minimalist design with pastel color scheme"

# Add your GitHub repository as remote (replace YOUR_USERNAME and YOUR_REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Verify Upload
1. Go to your GitHub repository
2. Verify all files are present:
   - `app.py` (main application)
   - `streamlit_app.py` (entry point)
   - `requirements.txt` (dependencies)
   - `packages.txt` (system packages)
   - `replit.md` (project documentation)
   - Other supporting files

## Method 2: Upload via GitHub Web Interface

If Git commands don't work in Replit:

### Step 1: Create Repository (same as above)

### Step 2: Upload Files
1. On your new GitHub repository page, click "uploading an existing file"
2. Drag and drop or select these key files:
   - `app.py`
   - `streamlit_app.py` 
   - `requirements.txt`
   - `packages.txt`
   - `replit.md`
   - `README.md`
   - `.streamlit/config.toml` (if it exists)
3. Write commit message: "Initial commit: Sensor data visualization app"
4. Click "Commit changes"

## Next Steps: Deploy to Streamlit Cloud

### Step 1: Connect to Streamlit Cloud
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file path: `streamlit_app.py`
6. Click "Deploy!"

### Step 2: Configure Deployment
The app will automatically use:
- `requirements.txt` for Python dependencies
- `packages.txt` for system packages
- `.streamlit/config.toml` for Streamlit configuration

### Expected Deployment Time
- First deployment: 5-10 minutes
- Subsequent deployments: 2-3 minutes

## Deployment URL
Once deployed, you'll get a URL like:
`https://YOUR_USERNAME-sensor-data-visualization-streamlit-app-xyz123.streamlit.app`

## Troubleshooting

### Common Issues
1. **Dependencies not found**: Verify `requirements.txt` is correctly formatted
2. **Import errors**: Ensure `streamlit_app.py` exists and imports properly
3. **Configuration issues**: Check `.streamlit/config.toml` syntax

### Support Files Already Configured
✓ `requirements.txt` - Contains all required Python packages
✓ `packages.txt` - Contains system-level dependencies  
✓ `streamlit_app.py` - Entry point that imports main app
✓ `.streamlit/config.toml` - Streamlit configuration for deployment

## Features of Your App
- **Interactive Charts**: Dual-axis temperature/humidity visualization
- **Data Persistence**: All settings persist across browser refreshes
- **Multiple Sensors**: Support for up to 4 sensor datasets
- **Advanced Controls**: Manual axis ranges, time filtering, series visibility
- **Daily Averages**: Configurable time-of-day filtering for trend analysis
- **Clean Design**: Minimalist interface with pastel color scheme

Your app is production-ready and will work seamlessly on Streamlit Cloud!
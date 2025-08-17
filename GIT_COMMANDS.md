# Quick Git Commands for GitHub Push

## Run these commands in the Replit Shell:

### 1. Initialize and commit your code:
```bash
git init
git add .
git commit -m "Initial commit: Sensor data visualization app with comprehensive persistence"
```

### 2. Connect to your GitHub repository:
**First, create a new repository on GitHub.com, then replace YOUR_USERNAME and YOUR_REPO_NAME below:**

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

## Example with actual repository name:
```bash
git remote add origin https://github.com/johndoe/sensor-data-visualization.git
git branch -M main  
git push -u origin main
```

## If you get authentication errors:
You may need to use a Personal Access Token instead of password. 
Go to GitHub Settings > Developer settings > Personal access tokens to create one.

## Your app includes:
- Complete sensor data visualization with dual-axis charts
- Advanced persistence system for all user settings
- Manual temperature axis controls with fixed humidity range
- Daily averages with time-of-day filtering
- Support for up to 4 sensor CSV uploads
- Production-ready for Streamlit Cloud deployment
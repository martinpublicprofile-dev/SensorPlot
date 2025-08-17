# Git Commands to Push Latest Updates

## Recent Updates Added

✅ **Daily Time Range Slider** - Updated slider to move in daily increments only, days start at 0:00  
✅ **Mobile App Name Fixed** - Implemented multiple PWA approaches to ensure "Sensor Data" appears on mobile home screen  
✅ **Dynamic Manifest Generation** - Proper PWA manifest with embedded icons and correct app metadata  
✅ **Password Protection** - Secure access control requiring "sensordata" password  
✅ **Comprehensive Persistence System** - All UI settings now persist across browser refreshes  
✅ **Manual Axis Controls** - Temperature axis min/max controls with Auto reset buttons  
✅ **Fixed Humidity Range** - Humidity axis always shows 0-100% (no auto-scaling)  
✅ **Time Range Persistence** - Time slider selections automatically saved and restored  
✅ **Checkbox State Memory** - All visibility toggles remembered across sessions  
✅ **Error Fix** - Fixed AttributeError for None time values  

## Commands to Run

**Step 1: Clear Git lock (if needed)**
```bash
rm -f .git/index.lock
```

**Step 2: Add and commit changes**
```bash
# Add all changes  
git add .

# Commit the updates
git commit -m "Update time range slider to daily increments and fix mobile PWA

- Updated time range slider to move in daily increments only (days start at 0:00)
- Changed slider step from hourly to daily for cleaner user experience
- Aligned all datetime calculations to daily boundaries (start: 0:00, end: 23:59:59)
- Updated display format from HH:mm DD/MM/YY to DD/MM/YY for day-based selection
- Enhanced persistent state handling to align saved values to daily boundaries
- Implemented multiple PWA approaches to ensure mobile app installs as 'Sensor Data'
- Added dynamic manifest generation with embedded SVG icons and proper metadata
- Enhanced PWA meta tags including application-name and apple-mobile-web-app-title
- Added JavaScript title override to force correct app name display
- Updated manifest.json with proper PWA configuration for Android installation
- Added secure password protection requiring 'sensordata' for access
- Clean login interface with professional design and logout functionality
- All axis settings (min/max temperature ranges) now persist across refreshes
- All checkbox states (temperature/humidity visibility) remembered
- Time-of-day range settings for averages calculations persist
- Fixed humidity axis to always show 0-100% scale (no auto-scaling)
- Added manual temperature axis controls with Auto reset buttons
- UI state automatically saves on every user interaction
- Fixed AttributeError for None time values with proper defaults"
```

**Step 3: Push to GitHub**
```bash
git push origin main
```

## What's New

1. **Daily Time Range Slider**: Slider now moves in daily increments only - cleaner selection with days starting at 0:00
2. **Mobile App Name Fixed**: Implemented comprehensive PWA solution - app now properly installs as "Sensor Data" on Android devices
3. **PWA Enhancement**: Dynamic manifest generation with custom icons and proper metadata for mobile installation
4. **Password Protection**: Secure access with "sensordata" password - clean login screen with logout functionality
5. **Complete UI Persistence**: Every setting (axis ranges, time selections, checkboxes) now persists indefinitely
6. **Manual Temperature Axis Control**: Set exact min/max values or click "Auto" to reset to automatic scaling
7. **Fixed Humidity Scale**: Always 0-100%, no more auto-scaling that could confuse readings
8. **Enhanced User Experience**: All interactions are automatically saved - no more losing settings on refresh

Your sensor data visualization app now has intuitive daily time selection, proper mobile branding with multiple PWA fixes, secure access control, and maintains all user preferences across browser sessions!
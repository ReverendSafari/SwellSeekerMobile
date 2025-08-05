# SwellSeeker iOS App

A SwiftUI iOS app for surf reporting, connecting to the FastAPI backend.

## 📱 Project Structure

```
SwellSeeker/
├── SwellSeekerApp.swift          # Main app entry point
├── Views/
│   ├── ContentView.swift         # Main view with beach list
│   └── BeachViewModel.swift      # ViewModel for beach data
├── Models/
│   ├── Beach.swift              # Beach data model
│   └── SurfData.swift           # Surf data model
└── Services/
    └── APIService.swift         # API client for backend
```

## 🚀 Setup Instructions

### 1. Install Xcode
- Download Xcode from the Mac App Store
- Or install via command line: `xcode-select --install`

### 2. Create Xcode Project
1. Open Xcode
2. Create New Project → iOS → App
3. Name: "SwellSeeker"
4. Interface: SwiftUI
5. Language: Swift

### 3. Add Swift Files
Copy the Swift files from this directory into your Xcode project:
- `SwellSeekerApp.swift` → Replace the default app file
- `Views/` folder → Add to project
- `Models/` folder → Add to project  
- `Services/` folder → Add to project

### 4. Configure API
1. Update `APIService.swift` with your actual API key
2. Ensure your FastAPI backend is running on `localhost:8001`

### 5. Build and Run
- Select iOS Simulator or device
- Press Cmd+R to build and run

## 🔧 Development Workflow

**Cursor (Code Editing):**
- Write and edit Swift code
- Use AI assistance for development
- Version control with Git

**Xcode (Building/Running):**
- Build the iOS app
- Run on simulator/device
- Debug and test

## 📡 API Endpoints

The app connects to your FastAPI backend:
- `GET /api/v1/beaches/` - List all beaches
- `GET /api/v1/surf-data/{beach_name}` - Get surf data

## 🏄‍♂️ Features

- **Beach List**: Display all available beaches
- **Surf Data**: Fetch and display surf conditions
- **Pull to Refresh**: Refresh beach data
- **Error Handling**: Graceful error display

## 🔄 Next Steps

1. Add surf data detail view
2. Implement caching
3. Add location services
4. Create beautiful UI components
5. Add offline support 
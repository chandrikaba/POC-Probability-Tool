# Diagrams Guide

## 📊 Architecture and Flow Diagrams

This directory contains comprehensive diagrams for the Deal Win Probability Tool in Draw.io format.

## 📁 Available Diagrams

### 1. Architecture_Diagram.drawio
**System Architecture Overview**

This diagram shows the complete system architecture including:
- **User Layer**: Web Browser Users, API Consumers, Postman Users
- **Frontend Layer**: Streamlit application and pages
- **Backend Layer**: FastAPI application and routes
- **Core Business Logic**: Data generator, model trainer, predictor
- **Data & Model Storage**: Input/output data, trained models
- **Machine Learning Layer**: XGBoost, Scikit-learn, Pandas, Joblib

**Key Components:**
- Color-coded layers for easy identification
- Clear separation of concerns
- Data flow connections
- Technology stack visualization

### 2. Workflow_Diagrams.drawio
**Process Flow Diagrams** (3 pages)

#### Page 1: Data Generation Flow
Shows the complete workflow for generating synthetic training data:
1. User initiates data generation
2. API call to backend
3. Schema definition
4. Record generation
5. DataFrame creation
6. Save to Excel
7. Return response

#### Page 2: Model Training Flow
Shows the complete workflow for training the XGBoost model:
1. User initiates training
2. Load synthetic data
3. Preprocessing (Label Encoding, One-Hot)
4. Data splitting (80/20)
5. XGBoost training
6. Validation
7. Model saving
8. Return accuracy

#### Page 3: Prediction Flow
Shows the complete workflow for making predictions:
1. User uploads Excel file
2. File validation
3. Data reading
4. Model loading
5. Preprocessing
6. Prediction
7. Label decoding
8. Result creation
9. Save predictions
10. Return response

## 🚀 How to Open the Diagrams

### Method 1: Online (Recommended)
1. Go to **https://app.diagrams.net** (or **https://draw.io**)
2. Click **"Open Existing Diagram"**
3. Choose **"Open from Device"**
4. Select the `.drawio` file from the `docs/` folder
5. The diagram will open in your browser

### Method 2: Desktop App
1. Download Draw.io desktop app from https://github.com/jgraph/drawio-desktop/releases
2. Install the application
3. Open the `.drawio` file directly

### Method 3: VS Code Extension
1. Install the "Draw.io Integration" extension in VS Code
2. Open the `.drawio` file in VS Code
3. Edit directly in the editor

## 📝 Editing the Diagrams

### Adding New Components
1. Open the diagram in app.diagrams.net
2. Use the left sidebar to drag and drop shapes
3. Use the right sidebar to customize colors and styles
4. Connect elements with arrows

### Customizing Colors
Current color scheme:
- **Green (#d5e8d4)**: Data storage, success states
- **Yellow (#fff2cc)**: Frontend, processing steps
- **Purple (#e1d5e7)**: Backend, API components
- **Blue (#dae8fc)**: User actions, core logic
- **Orange (#ffe6cc)**: Machine learning components
- **Red (#f8cecc)**: Error states, end points

### Exporting Diagrams

#### As PNG/JPG:
1. File → Export as → PNG/JPEG
2. Choose resolution and quality
3. Download

#### As PDF:
1. File → Export as → PDF
2. Choose page size
3. Download

#### As SVG:
1. File → Export as → SVG
2. Download vector format

## 🎨 Diagram Features

### Architecture Diagram Features:
- **Layered Architecture**: Clear separation of concerns
- **Color Coding**: Easy identification of components
- **Connections**: Shows data flow between components
- **Legend**: Explains color meanings
- **Comprehensive**: Shows entire system at a glance

### Workflow Diagram Features:
- **Step-by-Step Flow**: Clear process visualization
- **Decision Points**: Diamond shapes for validation
- **Data Stores**: Cylinder shapes for databases/files
- **Process Steps**: Rectangles for actions
- **Start/End Points**: Rounded rectangles
- **Color Coding**: Consistent with architecture diagram

## 📖 Understanding the Diagrams

### Shapes Meaning:
- **Rounded Rectangle (Green/Red)**: Start/End points
- **Rectangle**: Process steps
- **Diamond**: Decision points
- **Cylinder**: Data storage
- **Note**: File outputs
- **Process Box**: API calls

### Arrow Types:
- **Solid Arrow**: Direct flow
- **Labeled Arrow**: Conditional flow (e.g., "Valid", "Invalid")

### Color Coding:
- **Green**: Success, data storage
- **Yellow**: Processing, frontend
- **Purple**: Backend, API
- **Blue**: User actions, core logic
- **Orange**: ML components
- **Red**: Errors, end states

## 🔄 Updating the Diagrams

When you make changes to the system:

1. **Open the diagram** in app.diagrams.net
2. **Make your changes**:
   - Add new components
   - Update connections
   - Modify labels
3. **Save the file**:
   - File → Save
   - Or Ctrl+S / Cmd+S
4. **Export if needed**:
   - Export as PNG for documentation
   - Keep .drawio for future edits

## 💡 Tips for Using Diagrams

### For Presentations:
1. Export as PNG at high resolution (300 DPI)
2. Use the exported images in PowerPoint/Google Slides
3. Keep the .drawio file for updates

### For Documentation:
1. Export as SVG for scalable quality
2. Embed in Markdown or HTML docs
3. Link to the online diagram for interactive viewing

### For Collaboration:
1. Share the .drawio file with team members
2. Use app.diagrams.net for simultaneous editing
3. Version control the .drawio files in Git

## 📚 Additional Resources

- **Draw.io Documentation**: https://www.diagrams.net/doc/
- **Shape Libraries**: https://www.diagrams.net/blog/shape-libraries
- **Keyboard Shortcuts**: https://www.diagrams.net/shortcuts

## 🎯 Quick Actions

### View Architecture:
```
Open: docs/Architecture_Diagram.drawio
Page: System Architecture
```

### View Data Generation Flow:
```
Open: docs/Workflow_Diagrams.drawio
Page: Data Generation Flow
```

### View Model Training Flow:
```
Open: docs/Workflow_Diagrams.drawio
Page: Model Training Flow
```

### View Prediction Flow:
```
Open: docs/Workflow_Diagrams.drawio
Page: Prediction Flow
```

## 🔗 Integration with Documentation

These diagrams complement:
- **README.md**: Project overview
- **FASTAPI_GUIDE.md**: API documentation
- **STREAMLIT_GUIDE.md**: UI documentation
- **RESTRUCTURING_GUIDE.md**: Architecture details

---

**Created with Draw.io** | **Editable in Browser** | **Version Controlled**

# System Architecture & Design

This document provides a detailed technical overview of the Deal Win Probability Tool, including high-level architecture, class structures, and interaction flows.

## 1. High-Level Architecture

The system follows a modular architecture with a clear separation between the User Interface, API Layer, Core Processing Logic, and Data/Model Storage.

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[Streamlit UI<br>(app.py)]
    end

    subgraph "API Layer"
        API[FastAPI Backend<br>(api.py)]
    end

    subgraph "Core Logic Layer"
        Gen[Data Generator<br>(src/generate_synthetic_data.py)]
        Train[Model Trainer<br>(src/train_xgb_classifier.py)]
        Pred[Predictor<br>(src/predict_xgb_classifier.py)]
    end

    subgraph "Storage Layer"
        subgraph "Data"
            Input[Input Data<br>(data/input/)]
            Output[Output Data<br>(data/output/)]
        end
        subgraph "Models"
            ModelFile[XGBoost Model<br>(models/xgb_classifier.pkl)]
            EncoderFile[Label Encoder<br>(models/label_encoder.pkl)]
        end
    end

    %% Interactions
    UI -->|Calls via Subprocess| Gen
    UI -->|Calls via Subprocess| Train
    UI -->|Calls via Subprocess| Pred
    
    API -->|Calls via Subprocess| Gen
    API -->|Calls via Subprocess| Train
    API -->|Calls via Subprocess| Pred

    Gen -->|Writes| Output
    Train -->|Reads| Output
    Train -->|Saves| ModelFile
    Train -->|Saves| EncoderFile
    
    Pred -->|Reads| Input
    Pred -->|Loads| ModelFile
    Pred -->|Loads| EncoderFile
    Pred -->|Writes| Output
```

## 2. Class Diagram

Although the core logic is implemented as functional scripts, the API layer uses Pydantic models for strict type validation. The diagram below represents the logical structure of the application components.

```mermaid
classDiagram
    class FastAPI_App {
        +generate_synthetic_data()
        +train_model()
        +predict_deal_outcomes(file)
        +health_check()
    }

    class Streamlit_UI {
        +render_sidebar()
        +render_data_generation_page()
        +render_training_page()
        +render_prediction_page()
    }

    class DataGenerator_Script {
        +generate_records(n)
        +save_to_excel()
    }

    class ModelTrainer_Script {
        +load_data()
        +preprocess_data()
        +train_pipeline()
        +save_model()
        +save_encoder()
    }

    class Predictor_Script {
        +load_model()
        +align_columns()
        +impute_missing()
        +predict()
        +save_results()
    }

    %% Pydantic Models
    class HealthResponse {
        +str status
        +str message
        +bool model_loaded
    }

    class SyntheticDataResponse {
        +bool success
        +str message
        +int records_generated
        +str output_path
    }

    class TrainingResponse {
        +bool success
        +str message
        +float validation_accuracy
        +str model_path
    }

    class PredictionResponse {
        +bool success
        +str message
        +str predictions_file
        +int total_records
    }

    %% Relationships
    FastAPI_App ..> SyntheticDataResponse : returns
    FastAPI_App ..> TrainingResponse : returns
    FastAPI_App ..> PredictionResponse : returns
    FastAPI_App ..> HealthResponse : returns

    FastAPI_App --> DataGenerator_Script : executes
    FastAPI_App --> ModelTrainer_Script : executes
    FastAPI_App --> Predictor_Script : executes
```

## 3. Sequence Diagrams

### 3.1 Data Generation Workflow
This flow illustrates how synthetic training data is created.

```mermaid
sequenceDiagram
    participant User
    participant UI_API as Streamlit UI / FastAPI
    participant Script as generate_synthetic_data.py
    participant FS as File System

    User->>UI_API: Request Data Generation
    UI_API->>Script: Execute via Subprocess
    activate Script
    Script->>Script: Generate Random Deal Data
    Script->>FS: Save to data/output/synthetic_deals.xlsx
    Script-->>UI_API: Return Success/Failure
    deactivate Script
    UI_API-->>User: Show Success Message & Record Count
```

### 3.2 Model Training Workflow
This flow shows how the model is trained on the synthetic data.

```mermaid
sequenceDiagram
    participant User
    participant UI_API as Streamlit UI / FastAPI
    participant Script as train_xgb_classifier.py
    participant FS as File System

    User->>UI_API: Request Model Training
    UI_API->>Script: Execute via Subprocess
    activate Script
    Script->>FS: Read synthetic_deals.xlsx
    Script->>Script: Preprocess Data (OneHot/Ordinal Encoding)
    Script->>Script: Train XGBoost Pipeline
    Script->>FS: Save models/xgb_classifier.pkl
    Script->>FS: Save models/label_encoder.pkl
    Script-->>UI_API: Return Accuracy Metrics
    deactivate Script
    UI_API-->>User: Display Accuracy & Model Info
```

### 3.3 Prediction Workflow
This flow demonstrates how the system handles new data for prediction, including the robust schema matching logic.

```mermaid
sequenceDiagram
    participant User
    participant UI_API as Streamlit UI / FastAPI
    participant Script as predict_xgb_classifier.py
    participant FS as File System

    User->>UI_API: Upload Excel File
    UI_API->>FS: Save temp input file
    UI_API->>Script: Execute via Subprocess
    activate Script
    Script->>FS: Load Input File
    Script->>FS: Load Trained Model & Label Encoder
    Script->>FS: Read Synthetic Data (for Schema)
    
    rect rgb(240, 248, 255)
        note right of Script: Robust Preprocessing
        Script->>Script: Detect Missing Columns
        Script->>Script: Fill Defaults (0.0 for Numeric, "UNKNOWN" for Text)
        Script->>Script: Enforce Data Types based on Schema
        Script->>Script: Impute Missing Values (Median/Unknown)
    end
    
    Script->>Script: Generate Predictions & Probabilities
    Script->>FS: Save predictions.xlsx
    Script-->>UI_API: Return Result Path
    deactivate Script
    UI_API-->>User: Show Results & Download Link
```

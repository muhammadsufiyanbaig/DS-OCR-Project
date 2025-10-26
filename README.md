# Data Science OCR Project

A well-structured FastAPI project with SQLModel for database operations, following MVC architecture pattern.

## 📁 Project Structure

```
ds-project/
├── db/
│   ├── __init__.py
│   ├── connection.py       # Database connection and session management
│   └── schemas.py          # Database models/schemas
├── routes/
│   ├── __init__.py
│   └── routes.py           # API routes/endpoints (Views)
├── controller/
│   ├── __init__.py
│   └── controllers.py      # Business logic (Controllers)
├── model/
│   └── __init__.py         # Additional models if needed
├── venv/                   # Virtual environment
├── .env                    # Environment variables
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── test.db                 # SQLite database (auto-generated)
└── README.md              # This file
```

## 🛠️ Tech Stack

- **FastAPI** - Modern web framework for building APIs
- **SQLModel** - SQL databases in Python, designed for simplicity
- **Uvicorn** - ASGI server for running FastAPI
- **PostgreSQL/SQLite** - Database (SQLite for development)
- **Python-dotenv** - Environment variable management
- **Black** - Code formatter
- **isort** - Import sorter

## 📋 Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

## 🚀 Installation & Setup

### 1. Clone or navigate to the project directory

```powershell
cd C:\Users\I-TECH\OneDrive\Desktop\ds-project
```

### 2. Create a virtual environment (if not exists)

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

If you encounter an execution policy error, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Configure environment variables

Edit the `.env` file and update the database URL if needed:

```env
# For SQLite (development)
DATABASE_URL=sqlite:///./test.db

# For PostgreSQL (production)
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

## 🏃 Running the Project

### Method 1: Using Python directly

```powershell
.\venv\Scripts\Activate.ps1; python main.py
```

### Method 2: Using Uvicorn command

```powershell
.\venv\Scripts\Activate.ps1; uvicorn main:app --reload
```

### Method 3: Quick start (one command)

```powershell
.\venv\Scripts\Activate.ps1; python main.py
```

The server will start on: **http://localhost:8000**

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔗 Available Endpoints

### General Endpoints

- `GET /` - Hello World endpoint

## 🏗️ Architecture

This project follows the **MVC (Model-View-Controller)** pattern:

- **Models** (`db/schemas.py`) - Database models and schemas
- **Views** (`routes/routes.py`) - API routes and request/response handling
- **Controllers** (`controller/controllers.py`) - Business logic and data processing

## 🔧 Development

### Format code with Black

```powershell
.\venv\Scripts\Activate.ps1; black .
```

### Sort imports with isort

```powershell
.\venv\Scripts\Activate.ps1; isort .
```

## 📦 Dependencies

See `requirements.txt` for the full list of dependencies:

- fastapi==0.115.0
- uvicorn==0.30.3
- sqlmodel==0.0.22
- psycopg2-binary==2.9.11
- python-dotenv==1.0.1
- black==24.8.0
- isort==5.13.2

## 🗄️ Database

### SQLite (Default - Development)

The project uses SQLite by default for easy setup and testing. The database file `test.db` is automatically created when you run the application.

### PostgreSQL (Production)

To use PostgreSQL:

1. Install PostgreSQL on your system
2. Create a database
3. Update the `.env` file with your PostgreSQL connection string:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

## 🛑 Stopping the Server

Press `Ctrl + C` in the terminal to stop the server.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created with FastAPI and SQLModel

---

**Happy Coding! 🚀**

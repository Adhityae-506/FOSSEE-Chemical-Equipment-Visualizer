# Chemical Equipment parameter visualizer
## Hybrid Web + Desktop Application

This project is part of the FOSSEE Internship Screening Task.  
It is a hybrid solution that functions as both a Web Application and a Desktop Application, powered by a shared Django backend.

🚀 Live Demo Links  
Component | Link  
--- | ---  
🌐 Web App | https://symphonious-truffle-440ed5.netlify.app/  
🔙 Backend API | Render backend link you deployed  
🖥 Desktop App (.exe) | Available inside /desktop_app/dist  

📌 Features  

🌐 Web Application (React + Vite)  
- Upload CSV files  
- Display summary (total count, averages)  
- Show bar & pie charts  
- View last 5 uploaded datasets  
- Download formatted PDF report  

🖥 Desktop Application (PyQt5)  
- Upload CSV directly from your system  
- Fetch real-time summary from backend  
- View interactive Matplotlib charts  
- Display upload history  
- Download and save PDF reports locally  

🗄 Backend (Django REST Framework)  
- CSV parsing & validation  
- Flexible column mapping (supports minor typos)  
- Automatic summary generation  
- Type distribution analytics  
- PDF report generation (ReportLab)  
- Stores last 5 uploaded datasets  
- APIs used by both Web + Desktop


---

# 🛠️ Setup Instructions

This project contains three components:

- Django Backend API  
- React Web Application  
- PyQt5 Desktop Application  

Follow the instructions below to set up and run each part locally.

---

## 1️. Backend Setup (Django API)

### Requirements
- Python 3.10+  
- pip  

### Steps

#### 1. Clone the repository
```bash
git clone https://github.com/Adhityae-506/FOSSEE-Chemical-Equipment-Visualizer.git
cd FOSSEE-Chemical-Equipment-Visualizer
```
#### 2. Create a virtual environment
```bash
python -m venv .venv
```
#### 3. Activate the environment
##### Windows
```bash
.venv\Scripts\activate
```
##### macOS / Linux
```bash
source .venv/bin/activate
```
#### 4. Install backend dependencies
```bash
pip install -r requirement.txt
```
#### 5. Apply migrations
```bash
python manage.py migrate
```
#### 6. Run backend server
```bash
python manage.py runserver
```
##### API will be available at
https:127.0.0.1:8000/api/

## 2️. Web Application Setup (React Frontend)

### Requirements
- Node.js v18+
- npm

### Steps

#### 1. Navigate to frontend folder
```bash
cd frontend
```
#### 2. Install dependencies
```bash
npm install
```
#### 3. Start the development server
```bash
npm run dev
```
##### Web app will run at:
https://localhost:5173

#### Configure API Base URL
Inside frontend/src/api/api.js
```js
const API_BASE = "https://127.0.0.1:8000";
```

## 3️. Desktop Application Setup (PyQt5)
### Requirements
- Python 3.10+
- PyQt5 

### Steps

#### 1. Navigate to desktop app directory
```bash
cd desktop_app
```
#### 2. Run the application
```bash
python main.py
```
##### A GUI window will open
###### IMPORTANT: Make sure the backend server is running before starting the desktop app.

## 4. Using the Application (Web + Desktop)
### Upload CSV File

Upload a .csv file with columns: 
- equipment_name
- type  
- flowrate 
- pressure 
- temperature

## 5. Desktop App EXE
The packaged EXE is available at:
```bash
desktop_app/dist/
```

📊 PDF Report Includes  
- Title & metadata  
- Summary statistics table  
- Equipment type pie chart  
- Page 2 → First 30 rows of CSV  
- Clean and professional styling  

💻 Desktop App (EXE) Usage  
- Download the executable from /desktop_app/dist  
- Double-click to open  
- Upload CSV → View Summary → View Charts → Download Report  

🌐 Web App Usage  
- Open → https://symphonious-truffle-440ed5.netlify.app/  
- Click Upload CSV  
- View summary + charts  
- Download the PDF report  
- Check History to see last 5 datasets  

🛠 Technologies Used  

Frontend  
- React  
- Vite  
- Chart.js  

Backend  
- Django  
- Django REST Framework  
- Pandas  
- Matplotlib  
- ReportLab  
- Whitenoise  

Desktop  
- PyQt5  
- Matplotlib  
- Requests  

📌 Developer Notes  
- Both Desktop and Web applications communicate with a common backend API  
- Desktop version packaged using PyInstaller  
- Fully deployed (Backend: Render, Frontend: Netlify)  

🙌 Contributions  
Made by: **Adhitya E**  
For **FOSSEE IIT-Bombay Internship Screening**





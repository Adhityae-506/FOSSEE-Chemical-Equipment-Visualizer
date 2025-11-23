🧪 Chemical Equipment Parameter Visualizer  
Hybrid Web + Desktop Application

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

📊 PDF Report Includes  
- Title & metadata  
- Summary statistics table  
- Equipment type pie chart  
- Page 2 → First 30 rows of CSV  
- Clean and professional styling  

📁 Project Structure
FOSSEE-Chemical-Equipment-Visualizer/
│
├── backend/ # Django API
│ ├── api/
│ ├── backend/
│ ├── manage.py
│ └── requirements.txt
│
├── react-frontend/ # React + Vite Web UI
│ ├── src/
│ ├── public/
│ └── .env.production
│
└── desktop_app/ # PyQt5 Desktop App
├── main.py
├── api_client.py
└── dist/ # EXE output


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
Made by: **Adhitya Elangovan**  
For **FOSSEE IIT-Bombay Internship Screening**


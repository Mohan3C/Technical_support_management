

# ⭐ TSM – Ticket Support Management System



A Django-based ticketing system for creating, assigning, updating, and resolving support tickets.  
Designed with a responsive UI using Tailwind and optimized database operations.

---

## 🚀 Features

### **User Features**
- Create support tickets  
- View ticket status and progress  
- Track updates in real time  

### **Agent Features**
- Assign tickets  
- Update ticket status (In-Progress, Resolved, etc.)  
- Add comments or notes  
- Manage ticket workflows  

### **System Features**
- Real-time status updates  
- Responsive Tailwind UI  
- Clean and fast database queries  
- Role-based functionality  

---

## 🧩 Tech Stack

- **Backend:** Django, Python  
- **Frontend:** HTML, CSS, Tailwind  
- **Database:** SQLite / PostgreSQL  
- **Tools:** Git, GitHub  

---

## 📂 Project Structure

tsm/
├── media
|    ├── comment_attachments/
|    └── ticket_attachments/
|
├── support
|    |     
|    ├── migrations/
|    ├── static/
|    ├── templates/
|    ├── templatetages/
|    └── # project .py files
|
├── tsm/# project config
└── manage.py



---

## 🛠️ Setup Instructions

```bash
git clone https://github.com/Mohan3C/Technical_support_management.git
cd Technical_support_management

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver



📜 License

This project is for educational and portfolio use.

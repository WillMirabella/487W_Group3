## Web Dashboard Guide
> [!IMPORTANT]  
> This guide is for running the app and dashboard locally. Eventually, when they are migrated to a standalone server, this will need to be updated.

### 1. Setup and start PostgreSQL database
Windows: https://www.w3schools.com/postgresql/postgresql_getstarted.php \
Linux: https://wiki.archlinux.org/title/PostgreSQL

### 2. Run the app backend
```
cd backend
python3 app.py
```

### 3. Run the dashboard
```
cd frontend/dashboard/
python -m http.server 9000
```
> [!TIP]
> Run this in a seperate terminal.

### 4. Access the dashboard
Navigate to http://127.0.0.1:9000/ in a browser of your choice.

### 5. Update the blacklist
Enter an email in the text box and click the - or + button to remove or add to the blacklist.
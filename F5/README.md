# F5 LTM Automation Project

## ***IMPORTANT INFO***
---
***This is an engineering tool, not meant for customers/clients to use***

---

This Django-based project automates F5 LTM (Local Traffic Manager) configuration builds, integrating asynchronous API processing and real-time WebSocket updates. It uses Django Channels for WebSockets and Daphne as the ASGI server.

---

## **Table of Contents**
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Project](#running-the-project)
5. [Features](#features)
6. [API Endpoints](#api-endpoints)
7. [Troubleshooting](#troubleshooting)

---

## **Prerequisites**

Ensure you have the following installed on your system:

- Python 3.8+
- Redis (for Django Channels and background task processing)
- Daphne (ASGI server for WebSockets)
- A virtual environment manager (optional but recommended)

---

## **Installation**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Jeremy-Friese/F5.git
   cd F5
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install and Start Redis:**
   
   - **On macOS:**
     ```bash
     brew install redis
     brew services start redis
     ```
   - **On Ubuntu/Debian:**
     ```bash
     sudo apt update
     sudo apt install redis
     sudo systemctl start redis
     ```
   - **Verify Redis is Running:**
     ```bash
     redis-cli ping
     # Should return "PONG"
     ```

5. **Run Database Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a Superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect Static Files:**
   ```bash
   python manage.py collectstatic
   ```
8. **Modify Device List:**
   - Log in to the Admin panel (Default is to pull from local database).
   - Create a list of device names and their corresponding IP addresses.
   - You can modify how the device list is retrieved by updating the code in the `F5.f5_devices.views` module.
---

## **Configuration**

1. **Set Environment Variables:**

   Create a `.env` file in the project root (if required) to store sensitive configurations like database credentials or secret keys.

   Example:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   CELERY_BROKER_URL=redis://localhost:6379/0
   ```

2. **Update `settings.py`:**
   Ensure the following configurations are correct:
   ```python
   CELERY_BROKER_URL = 'redis://localhost:6379/0'
   DEBUG = True
   ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
   CHANNEL_LAYERS = {
       "default": {
           "BACKEND": "channels.layers.InMemoryChannelLayer",
       },
   }
   ```

---

## **Running the Project**

1. **Start the ASGI Server with Daphne:**
   ```bash
   daphne -b 0.0.0.0 -p 8000 F5.asgi:application
   ```

2. **Start the Celery Worker:**
   ```bash
   celery -A F5 worker --loglevel=info
   ```

3. **Access the Admin Interface:**
   Open your browser and navigate to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) to manage F5 devices.

---

## **Features**

- **Automated LTM Configuration Builds:** Asynchronously configures F5 LTM settings.
- **WebSockets for Real-Time Updates:** Clients receive live status messages about the build process.
- **Django Channels for Async API Processing:** Non-blocking request handling.
- **Celery for Background Tasks:** Ensures non-blocking backend operations.

---

## **API Endpoints**

| Method | Endpoint                | Description                        |
|--------|-------------------------|------------------------------------|
| POST   | `/api/build-ltm/`       | Initiates LTM build process       |
| GET    | `/ws/device-status/`    | WebSocket endpoint for updates    |

---

## **Troubleshooting**

1. **Redis Not Found:**
   Ensure Redis is installed and running:
   ```bash
   redis-cli ping
   ```

2. **WebSockets Not Working:**
   - Ensure Daphne is running:
     ```bash
     daphne -b 0.0.0.0 -p 8000 F5.asgi:application
     ```
   - Check if WebSocket messages are sent from Django:
     ```python
     from channels.layers import get_channel_layer
     from asgiref.sync import async_to_sync
     channel_layer = get_channel_layer()
     async_to_sync(channel_layer.group_send)("device_status", {"type": "send_status_update", "message": "Test Message"})
     ```

3. **Database Errors:**
   Ensure migrations are applied:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

---

This README provides setup and operational instructions for the F5 LTM Automation Project.


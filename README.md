# SecureAccess
 SecureAccess is a Django-based web application that facilitates secure user authentication and access control using RFID technology. The application allows users to log in securely, generates authentication tokens, and communicates with an ESP32 device via WebSocket to verify RFID data. Upon successful RFID verification, users are granted access to authorized areas or functionalities.
 ### Deployment
daphne -b 0.0.0.0 -p 8002 project.asgi:application
### Technology Stack
+ Django: Backend framework for web application development.
+ Channels: Handles WebSocket communication.
+ Django REST Framework: Provides token authentication and API endpoints.
+ Django Templates: Renders HTML pages with dynamic content.
+ HTML, CSS, JavaScript: Frontend technologies for user interface and interaction.
### Structure
+ project/: Django project directory.
+ users/: App directory containing views, models, and templates for user authentication and access control.
+ static/: Static files (CSS, JavaScript) for frontend rendering.
+ templates/: HTML templates for rendering pages.
+ requirements.txt: Python dependencies required for the project.
+ README.md: Project documentation and setup instructions.

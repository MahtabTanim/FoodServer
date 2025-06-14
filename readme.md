# 🍽️ FoodServer — Django-Based Food Marketplace with Real-Time Location & Payments

A comprehensive Django-based food marketplace application that connects customers with local restaurants, featuring real-time location services, secure payments, and intelligent business management.

## 📚 Table of Contents

- [Live Demo](#-live-demo)
- [Application Flowchart](#️-application-flowchart)
- [Tech Stack](#️-tech-stack)
- [Key Features](#-key-features)
- [Getting Started](#-getting-started)
- [Technical Architecture](#️-technical-architecture)
- [Deployment (Heroku)](#-deployment-heroku)
- [Project Structure](#-project-structure)
- [Useful Commands](#️-useful-commands)
- [Configuration & Static Files](#️-configuration--static-files)
- [Acknowledgements](#-acknowledgements)

## 🌐 **Live Demo:** [foodserver.shop](https://foodserver.shop)

## 🗺️ Application Flowchart

Below is a high-level flowchart illustrating the main components and interactions in the FoodServer application:

<img src="foodserver_application_flowchart.svg" alt="FoodServer Application Flowchart" width="600"/>

---

## 🛠️ Tech Stack

- **Backend:** Django, GeoDjango, PostgreSQL, PostGIS, GDAL
- **Frontend:** jQuery, AJAX, Google Maps API, DataTables
- **Authentication:** Django Signals, Token Authentication, Custom User Model
- **DevOps:** Heroku, Gunicorn, WhiteNoise
- **Payment:** Multiple Bangladeshi Payment Gateways (bKash, Nagad, DBBL)

---

## ✨ Key Features

### 🔐 **Advanced User Management**

- **Custom User Model** with email-based authentication
- **Automated User Profiles** created via Django signals
- **Role-based Access Control** (Customer, Vendor, Admin)
- **Smart Redirects** - logged-in users automatically redirected to appropriate dashboards
- **Token-based Email Verification** for secure account activation
- **Password Reset** functionality with secure token validation
- **Vendor Approval System** managed by administrators

### 🏪 **Restaurant & Vendor Management**

- **Restaurant Profiles** with Google Maps integration
- **Read-only Coordinates** display using Maps API
- **Google Autocomplete** for address input fields
- **Category Management** with full CRUD operations
- **Food Items Management** with comprehensive CRUD functionality
- **Dynamic Business Hours** - restaurants automatically hidden during off-hours
- **Revenue Analytics** - monthly revenue tracking per vendor

### 🛒 **Smart Shopping Experience**

- **Interactive Cart** powered by jQuery and AJAX
- **Real-time Cart Updates** with dynamic amount calculations
- **Global Context Processors** for seamless cart management across pages
- **Dynamic Tax Calculation** integrated into checkout process

### 🔍 **Intelligent Search & Discovery**

- **Multi-criteria Search** - find restaurants by name or food items
- **Location-based Discovery** using GeoDjango
- **Automatic Location Detection** for personalized homepage experience
- **Radius-based Filtering** to minimize search results and improve relevance
- **Geospatial Optimization** for efficient location queries

### 💳 **Secure Payment Integration**

- **Multiple Payment Gateways** - bKash, Nagad, DBBL, and other Bangladeshi banks
- **Secure Transaction Processing**
- **Order Confirmation System** with automated email notifications
- **Dynamic Order Status** tracking with real-time updates

### 📧 **Communication & Notifications**

- **Automated Email System** for user and vendor registration
- **Order Confirmation Emails** sent to both customers and restaurants
- **Django Messages Framework** for user feedback and error handling
- **Real-time Status Updates** via AJAX

### 📊 **Data Management & Analytics**

- **PostgreSQL Database** with PostGIS extensions for geospatial data
- **GDAL Integration** for advanced geographic data processing
- **jQuery DataTables** for efficient order pagination and management
- **Revenue Reporting** with monthly breakdowns per vendor

### 🛡️ Security Highlights

- Token-based email verification
- Secure password reset with token validation
- Role-based access control (Customer/Vendor/Admin)
- HTTPS-ready static file serving with WhiteNoise

---

## 🚀 Getting Started

### 1. **Clone the repository**

```bash
git clone https://github.com/yourusername/FoodServer.git
cd FoodServer
```

### 2. **Set up your environment**

- Install [Python 3.12.3](https://www.python.org/downloads/release/python-3123/) (Heroku uses this version, see `.python-version`).
- (Recommended) Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. **Install dependencies**

```bash
pip install -r requirements.txt
```

### 4. **Configure environment variables**

- Copy `.env-sample` to `.env` and fill in your secrets and configuration:

```bash
cp .env-sample .env
# Edit .env with your editor and fill in the values
```

### 5. **Apply migrations**

```bash
python manage.py migrate
```

### 6. **Collect static files**

```bash
python manage.py collectstatic
```

### 7. **Run the development server**

```bash
python manage.py runserver
```

### 8. **Run with Gunicorn (production-like)**

```bash
gunicorn FoodServer.wsgi
```

---

## 🏗️ Technical Architecture

### **Database & Geospatial**

- **PostgreSQL** with PostGIS extensions for production
- **GDAL** integration for geospatial data processing
- **GeoDjango** for location-based features and radius calculations

### **Frontend Technologies**

- **jQuery & AJAX** for dynamic user interactions
- **Google Maps API** for location services and autocomplete
- **Responsive Design** with mobile-first approach
- **DataTables** for advanced table management

### **Backend Framework**

- **Django** with custom user model implementation
- **Django Signals** for automated profile creation
- **Global Context Processors** for cross-app data sharing
- **Token-based Authentication** for secure operations

### **Production Infrastructure**

- **WhiteNoise** for efficient static file serving in production
- **Gunicorn** as WSGI HTTP server for production deployment
- **Heroku** cloud platform with specialized GeoDjango buildpacks

---

## 🚢 Deployment (Heroku)

This application is optimized for Heroku deployment with specialized GeoDjango support.

### **Buildpack Configuration**

The project uses two essential buildpacks:

1. **heroku-geo-buildpack** - For GeoDjango and PostGIS support
2. **heroku/python** - Standard Python runtime

### **Deployment Steps**

1. **Prerequisites:**

   - Heroku account and [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed

2. **Login and create a Heroku app:**

   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Set environment variables on Heroku:**

   ```bash
   heroku config:set $(cat .env | xargs)
   ```

4. **Set up Heroku buildpacks for GeoDjango:**

   ```bash
   heroku buildpacks:add --index 1 https://github.com/heroku/heroku-geo-buildpack.git
   heroku buildpacks:add --index 2 heroku/python
   ```

5. **Push your code:**

   ```bash
   git push heroku main
   ```

6. **Run migrations and collect static files:**

   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py collectstatic --noinput
   ```

7. **Open your app:**
   ```bash
   heroku open
   ```

---

## 📁 Project Structure

```
FoodServer/
├── FoodServer/          # Main Django project settings
├── account/             # User authentication & profiles
├── vendor/              # Restaurant/vendor management
├── menus/               # Food categories & items
├── marketplace/         # Main marketplace views
├── customers/           # Customer-specific features
├── orders/              # Order processing & management
├── static/              # Collected static files
├── media/               # Uploaded media files
└── templates/           # HTML templates
```

---

## 🛠️ Useful Commands

- **Create superuser:**
  ```bash
  python manage.py createsuperuser
  ```
- **Run tests:**
  ```bash
  python manage.py test
  ```
- **Run commands on Heroku:**
  ```bash
  heroku run python manage.py <command>
  ```

---

## ⚙️ Configuration & Static Files

### **Static File Handling**

- **WhiteNoise** used in production to serve static files efficiently without requiring a separate web server
- Configured with `STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"`
- Provides automatic compression and caching for optimal performance
- Eliminates the need for CDN setup in small to medium-scale deployments

### **Procfile Configuration**

```
web: gunicorn FoodServer.wsgi
```

### **Runtime Specification**

- Python version specified in `.python-version` as `3.12`
- Heroku runtime configured in `.python-version` file

---

## 🎨 Acknowledgements

**Template:** [FoodBakery - Food Delivery Template](https://themeforest.net/item/foodbakery-food-delivery-single-multiple-restaurant-template/25426367)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🔗 Links

- **Live Application:** [foodserver.shop](https://foodserver.shop)
- **Repository:** [GitHub](https://github.com/yourusername/FoodServer)
- **Issues:** [GitHub Issues](https://github.com/yourusername/FoodServer/issues)

https://foodserver-media-files.s3.eu-north-1.amazonaws.com/users/profile_profiles/01-Set_Variables.jpg https://foodserver-media-files.s3.eu-north-1.amazonaws.com/04-Set_Value.png

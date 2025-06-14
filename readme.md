# 🍽️ FoodServer — Django-Based Food Marketplace with Real-Time Location & Payments

A comprehensive Django-based food marketplace application that connects customers with local restaurants, featuring real-time location services, secure payments, and intelligent business management.

## 📚 Table of Contents

- [Live Demo](#-live-demo)
- [Screenshots](#-screenshots)
- [Application Flowchart](#️-application-flowchart)
- [Tech Stack](#️-tech-stack)
- [Key Features](#-key-features)
- [Prerequisites](#-prerequisites)
- [Getting Started](#-getting-started)
- [Amazon S3 Configuration](#️-amazon-s3-configuration)
- [Technical Architecture](#️-technical-architecture)
- [Deployment (Heroku)](#-deployment-heroku)
- [Project Structure](#-project-structure)
- [Useful Commands](#️-useful-commands)
- [Configuration & Static Files](#️-configuration--static-files)
- [Acknowledgements](#-acknowledgements)
- [Contributing](#-contributing)
- [Links](#-links)

## 🌐 **Live Demo:** [foodserver.shop](https://foodserver.shop)

## 📸 Screenshots

### Homepage & Restaurant Discovery

<img src="screenshots/Homepage.png" alt="FoodServer Homepage" width="800"/>
*Modern homepage with location-based restaurant discovery and Google Maps integration*

### Dynamic Shopping Cart

<img src="screenshots/dynamic cart.png" alt="Dynamic Cart System" width="800"/>
*Real-time cart updates with AJAX-powered quantity management and instant price calculations*

### Secure Checkout Process

<img src="screenshots/checkout.png" alt="Checkout Process" width="800"/>
*Streamlined checkout with multiple payment gateway integrations*

### Payment Gateway Integration

<div style="display: flex; gap: 10px;">
  <img src="screenshots/payment1.png" alt="Payment Gateway 1" width="400"/>
  <img src="screenshots/payment2.png" alt="Payment Gateway 2" width="400"/>
</div>
*Multiple Bangladeshi payment gateways (bKash, Nagad, DBBL) with secure transaction processing*

### User Profile Management

<img src="screenshots/profile.png" alt="User Profile" width="800"/>
*Comprehensive user profile with order history and account management*

### Restaurant Dashboard

<img src="screenshots/restaurant dashboard.png" alt="Restaurant Dashboard" width="800"/>
*Vendor dashboard with order management, revenue analytics, and business insights*

### Payment History & Analytics

<img src="screenshots/payment history.png" alt="Payment History" width="800"/>
*Detailed payment history with transaction tracking and revenue reporting*

## 🗺️ Application Flowchart

Below is a high-level flowchart illustrating the main components and interactions in the FoodServer application:

<img src="foodserver_application_flowchart.svg" alt="FoodServer Application Flowchart" width="600"/>

---

## 🛠️ Tech Stack

- **Backend:** Django, GeoDjango, PostgreSQL, PostGIS, GDAL
- **Frontend:** jQuery, AJAX, Google Maps API, DataTables
- **Authentication:** Django Signals, Token Authentication, Custom User Model
- **File Storage:** Amazon S3 (Static & Media Files)
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
- HTTPS-ready static file serving with S3 and WhiteNoise

---

## 🚀 Getting Started

### 1. **Clone the repository**

```bash
git clone https://github.com/mahtab-tanim/FoodServer.git
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

Create and configure your environment file:

```bash
cp .env-sample .env
```

**Required Environment Variables:**

```env
# Django Core Settings
SECRET_KEY=your-super-secret-django-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourapp.herokuapp.com,foodserver.shop

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/foodserver_db

# Google Maps API
GOOGLE_API_KEY=your-google-maps-api-key

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=FoodServer <noreply@foodserver.shop>

# AWS S3 Configuration (for Static & Media Files)
USE_S3=True
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_STORAGE_BUCKET_NAME=your-s3-bucket-name
AWS_S3_REGION_NAME=us-east-1
AWS_S3_CUSTOM_DOMAIN=your-bucket.s3.amazonaws.com

```

⚠️ **Important:** Never commit your `.env` file to version control!

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

## ☁️ Amazon S3 Configuration

### **Static & Media Files Storage**

This application uses Amazon S3 for serving static files (CSS, JS, images) and media files (user uploads) in production.

### **S3 Setup Steps**

1. **Create S3 Bucket** with public read access
2. **Configure CORS for Font Files:**
   ```json
   [
     {
       "AllowedHeaders": ["*"],
       "AllowedMethods": ["GET", "HEAD"],
       "AllowedOrigins": ["*"],
       "ExposeHeaders": []
     }
   ]
   ```
3. **Create IAM User** with S3 access permissions
4. **Add environment variables** (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, etc.)

### **Features**

- ✅ Static & media files served from S3
- ✅ CORS configured for font loading
- ✅ Environment toggle (USE_S3=False for local development)
- ✅ Optimized caching headers

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

- **Amazon S3** for static and media file storage
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

### **Amazon S3 Integration**

- **Production Storage** - All static and media files served from Amazon S3
- **CORS Configuration** - Fixed font loading issues with proper CORS headers
- **Environment Toggle** - Easy switching between S3 and local storage (`USE_S3=True/False`)

### **Static File Handling**

**Production (S3):**

- Static files automatically uploaded to S3 during deployment
- Media files uploaded directly to S3 from application
- Optimized cache control headers for performance

**Development (Local):**

- Static files served from local filesystem
- WhiteNoise used for static file serving

### **Procfile Configuration**

```
web: gunicorn FoodServer.wsgi
release: python manage.py collectstatic --noinput
```

### **Runtime Specification**

- Python version specified in `.python-version` as `3.12`
- Heroku runtime configured in `.python-version` file

---

## 🎨 Acknowledgements

**Template:** [FoodBakery - Food Delivery Template](https://themeforest.net/item/foodbakery-food-delivery-single-multiple-restaurant-template/25426367)

---

---

## 🔗 Links

- **Live Application:** [foodserver.shop](https://foodserver.shop)
- **Repository:** [GitHub](https://github.com/MahtabTanim/FoodServer)

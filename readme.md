# FoodServer

A Django-based food marketplace application.

---

## 🚀 Getting Started

### 1. **Clone the repository**

```bash
git clone https://github.com/yourusername/FoodServer.git
cd FoodServer
```

### 2. **Set up your environment**

- Install [Python 3.12.3](https://www.python.org/downloads/release/python-3123/) (Heroku uses this version, see `runtime.txt`).
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

## 🚢 Deployment (Heroku)

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

## 📁 Project Structure

- `FoodServer/` – Main Django project
- `account/`, `vendor/`, `menus/`, `marketplace/`, `customers/`, `orders/` – Django apps
- `static/` – Collected static files
- `media/` – Uploaded media files

---

## 🛠️ Useful Commands

- **Create superuser:**
  `python manage.py createsuperuser`
- **To Run Command on deployed heroku instance**
  `heroku run python manage.py test`

---

## ⚙️ Heroku & Static Files

- Static files are served using [WhiteNoise](https://whitenoise.evans.io/en/stable/).
- Make sure `STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"` is set in `settings.py`.
- The `Procfile` should contain:
  ```
  web: gunicorn FoodServer.wsgi
  ```
- The Python version is specified in `.python-version` as `3.12`.

# Project README

Welcome to the **Django + Gunicorn + Nginx (No SSL)** Dockerized setup. This guide will walk you through cloning the repo, configuring environment variables, building & running containers, applying database migrations, and accessing your app locally.

---

## Table of Contents

- [Project README](#project-readme)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Repository Structure](#repository-structure)
  - [Environment Variables](#environment-variables)
  - [Docker Compose Usage](#docker-compose-usage)
    - [Building and Starting Services](#building-and-starting-services)
    - [Running Migrations](#running-migrations)
    - [Collecting Static Files (Optional)](#collecting-static-files-optional)
    - [Accessing the App](#accessing-the-app)
  - [Nginx Configuration](#nginx-configuration)
  - [Adding SSL Later (Optional)](#adding-ssl-later-optional)
  - [Troubleshooting](#troubleshooting)
  - [License](#license)

---

## Prerequisites

- Docker & Docker Compose installed (v3.8+)
- A UNIX-like shell (Bash, Zsh)
- Git installed

---

## Repository Structure

```
├── Dockerfile
├── docker-compose.yml
├── nginx/
│   └── default.conf
├── config/          # Django project module
├── app/             # Django app(s)
├── requirements.txt
├── .env             # Environment variables (not committed)
└── README.md        # <-- this file
```

---

## Environment Variables

Create a file named `.env` in the project root with these entries:

```ini
# Django settings
DJANGO_SECRET_KEY=your-secret-key
DEBUG=1

# Postgres database
POSTGRES_DB=demo_db
POSTGRES_USER=demo_user
POSTGRES_PASSWORD=strongpassword
DB_HOST=db
DB_PORT=5432

# Domain (if using reverse proxy)
DOMAIN=example.com
```

> **Note:** Do **not** commit `.env` to version control.

---

## Docker Compose Usage

### Building and Starting Services

```bash
# Build images & start containers in detached mode
docker-compose up --build -d
```

This will:  
- Launch a Postgres container (`db`)  
- Build your Python/Gunicorn container (`web`)  
- Launch an Nginx container reverse‑proxying HTTP to your `web` service

### Running Migrations

To apply Django migrations:

```bash
docker-compose exec web python manage.py migrate
```

If you need to create a superuser:

```bash
docker-compose exec web python manage.py createsuperuser
```

### Collecting Static Files (Optional)

If your project uses static files, run:

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Accessing the App

Open your browser at:

```
http://localhost/
```

Your Django app should respond on port 80 via Nginx.

---

## Nginx Configuration

Located at `nginx/default.conf`:

```nginx
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    location / {
        proxy_pass         http://web:8000;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
    }
}
```

This file proxies all incoming HTTP traffic on port 80 to the `web` service on port 8000.

---

## Adding SSL Later (Optional)

To reintroduce HTTPS with Let’s Encrypt:

1. Add a Certbot service back into `docker-compose.yml`.
2. Mount Certbot volumes (`certbot-etc`, `certbot-var`).
3. Include an Nginx server block for 443 with `ssl_certificate` directives.
4. Use `certbot certonly --webroot -w /var/www/certbot -d $DOMAIN` to obtain certificates.

---

## Troubleshooting

- **Database connection errors**: Check `.env` values and that `db` container is healthy (`docker-compose logs db`).
- **Port conflicts**: Ensure ports 80/443 are free or adjust `docker-compose.yml` mappings.
- **Static files not loading**: Verify `collectstatic` ran and your `STATIC_ROOT` settings.

---

## License

This project is licensed under the MIT License.

## RAG (Retrieval-Augmented Generation) feature setup (optional)

The project includes a simple RAG implementation that stores knowledge chunks in the project's SQLite database and can call HuggingFace models for embeddings and LLM generation. This feature is optional; the app will run without these additional packages, but RAG functionality requires installing them.

1. Install optional packages (recommended in a virtualenv):

```powershell
cd mount_everest_summit
pip install -r requirements.txt
pip install langchain langchain-community transformers sentence-transformers scikit-learn PyPDF2
```

2. Create a HuggingFace access token (free tier):
  - Go to https://huggingface.co and create an account.
  - In your profile -> Settings -> Access Tokens create a new token and copy it.
  - You can provide the token to the RAG service by editing `rag_app/services/sqlite_rag_service.py` and passing the token when creating the global `SQLiteRAGService()` instance, or set it as an environment variable and update the code to read it.

3. How to use the UI:
  - Log in to the site (RAG endpoints are protected by login).
  - Visit the RAG dashboard at `/rag_app/` (you can add a link in your nav if needed).
  - Upload PDF or text files, or paste text into the Add Text form. The content will be split into chunks and stored in the database.
  - Use the chat box in the dashboard or the chat widget in the site footer to ask questions. The system will perform semantic search over stored chunks (SQLite) and call the HuggingFace LLM if configured.

4. Notes and troubleshooting:
  - If you don't install the optional packages, the RAG endpoints will return a helpful message that the backends are unavailable.
  - The implementation stores embeddings as JSON strings in the `KnowledgeBase.embedding` field. If you switch to a production vector DB later, you can migrate these.


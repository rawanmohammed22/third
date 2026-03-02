 Student Management API

A RESTful API built with **FastAPI** and **PostgreSQL** for managing students, courses, and books — with **JWT Authentication** and **Cohere AI** chat integration.

---

## 🚀 Features

- **CRUD Operations** — Full create, read, update, delete for Students, Courses & Books
- **JWT Authentication** — Secure Register / Login / Logout
- **Cohere AI Chat** — Integrated AI assistant via `/cohere/chat`
- **Many-to-Many Relationships** — Students ↔ Courses, Students ↔ Books
- **Database Migrations** — Managed with Alembic
- **Docker Support** — PostgreSQL via Docker Compose
- **Layered Architecture** — Routers → Services → Repositories → Models

---

## 🛠️ Tech Stack

| Technology       | Purpose                  |
|------------------|--------------------------|
| FastAPI          | Web Framework            |
| SQLAlchemy       | ORM                      |
| PostgreSQL       | Database                 |
| Alembic          | Database Migrations      |
| Cohere AI        | AI Chat Assistant        |
| Docker           | Database Container       |
| JWT (python-jose)| Authentication           |
| Pydantic         | Data Validation          |

---

## 📁 Project Structure

```
├── app/
│   ├── main.py              # App entry point
│   ├── container.py         # Dependency injection
│   ├── dependencies.py      # Shared dependencies
│   ├── models/              # Database models
│   │   ├── Student.py
│   │   ├── Course.py
│   │   ├── Book.py
│   │   ├── User.py
│   │   ├── student_course.py
│   │   └── student_book.py
│   ├── routers/             # API endpoints
│   │   ├── auth_router.py
│   │   ├── student_router.py
│   │   ├── course_router.py
│   │   └── cohere_router.py
│   ├── services/            # Business logic
│   ├── repositories/        # Database queries
│   ├── schemas/             # Request/Response models
│   ├── controllers/         # Controller layer
│   ├── core/                # Configuration
│   ├── utils/               # Helpers
│   └── Clients/             # External API clients
├── alembic/                 # Migration scripts
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

---

## ⚙️ Setup & Run

### 1. Clone & install
```bash
git clone https://github.com/rawanmohammed22/third.git
cd third
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Start PostgreSQL
```bash
docker-compose up -d
```

### 3. Run migrations
```bash
alembic upgrade head
```

### 4. Run the server
```bash
uvicorn app.main:app --reload
```
Server runs at **http://localhost:8000**

---

## 📖 API Docs

| Docs      | URL                                  |
|-----------|--------------------------------------|
| Swagger   | http://localhost:8000/docs            |
| ReDoc     | http://localhost:8000/redoc           |

---

## 🔑 API Endpoints

### Auth — `/auth`
| Method | Endpoint          | Description       |
|--------|-------------------|--------------------|
| POST   | `/auth/register`  | Register new user  |
| POST   | `/auth/login`     | Login & get token  |
| POST   | `/auth/logout`    | Logout             |

### Students — `/students`
| Method | Endpoint          | Description        |
|--------|-------------------|--------------------|
| GET    | `/students/`      | Get all students   |
| POST   | `/students/`      | Create student     |
| GET    | `/students/{id}`  | Get by ID          |
| PUT    | `/students/{id}`  | Update student     |
| DELETE | `/students/{id}`  | Delete student     |

### Courses — `/courses`
| Method | Endpoint          | Description        |
|--------|-------------------|--------------------|
| GET    | `/courses/`       | Get all courses    |
| POST   | `/courses/`       | Create course      |
| GET    | `/courses/{id}`   | Get by ID          |
| PUT    | `/courses/{id}`   | Update course      |
| DELETE | `/courses/{id}`   | Delete course      |

### Cohere AI — `/cohere`
| Method | Endpoint         | Description         |
|--------|------------------|---------------------|
| POST   | `/cohere/chat`   | Chat with AI        |





 Database Diagram

User ──── has one ───▶ Student
Student ── many-to-many ──▶ Course  (via student_course)
Student ── many-to-many ──▶ Book    (via student_book)


 Author

**Rawan Mohammed** — [GitHub](https://github.com/rawanmohammed22)

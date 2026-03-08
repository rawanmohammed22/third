# FastAPI Student Management System

A robust API for managing student records, built with Python and FastAPI. This project demonstrates backend engineering best practices, including layered architecture and dependency injection.

## Features
* **CRUD Operations:** Complete management of student records.
* * **Authentication & Authorization:** Secure endpoints using JWT.
  * * **Layered Architecture:** Clear separation of concerns (Routers, Services, Repositories).
    * * **Database Migrations:** Managed via Alembic.
      * * **Containerization:** Dockerized for consistent development and deployment environments.
        * * **AI Integration:** Features AI-powered chat functionality utilizing the Cohere AI API.
         
          * ## Tech Stack
          * * **Framework:** FastAPI (Python)
            * * **Database:** PostgreSQL / SQLAlchemy ORM
              * * **Authentication:** JWT (JSON Web Tokens)
                * * **Architecture:** Repository Pattern, `dependency-injector`
                  * * **Infrastructure:** Docker, Alembic
                   
                    * ## Current Status & Known Limitations
                    * *(Honest Assessment)*
                    * * **No Tests:** The project currently lacks automated tests (e.g., `pytest`).
                      * * **Environment Variables:** Missing `.env.example` file to easily configure local setups.
                        * * **Error Handling:** Can be expanded for edge cases in the AI integration.
                         
                          * ## How to Run Locally
                         
                          * 1. Clone the repository
                            2. 2. Ensure Docker and Docker Compose are installed.
                               3. 3. Configure your .env file with your database credentials and Cohere API key.
                                  4. 4. Run the containers:
                                     5.    ```bash
                                              docker-compose up --build
                                              ```
                                           5. Apply migrations:
                                           6.    ```bash
                                                    alembic upgrade head
                                                    ```

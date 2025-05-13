
# 💬 gRPC Microservices Auth & User System with Django API Gateway

This project demonstrates a microservices-based architecture using **gRPC for internal service communication** and **Django** as an external API gateway. The architecture is modular and scalable, designed for production-grade systems like chat apps, eCommerce backends, or SaaS platforms.

---

## 🚀 Features

✅ JWT-based user registration and login (via gRPC Auth Service)  
✅ Token validation with AuthService from API Gateway  
✅ Fetch user data by username using gRPC UserService  
✅ Clean separation between services (Auth, User, API Gateway)  
✅ Modular and production-ready architecture  
✅ Proto-based contract-first communication

---

## ⚙️ Tech Stack

- **Django** – API Gateway
- **gRPC** – Fast, contract-based microservice communication
- **PostgreSQL** – Main production database
- **Python** – Main language for all services
- **Protobuf** – Interface definition
- **HTTP (REST)** – External communication with the API Gateway
- **gRPC** – Internal communication between microservices

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/itx-zeeshan/gRPC-django-demo.git
cd grpc-django-gateway
```

---

### 2. Create Virtual Environment & Install Requirements

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### 3. Configure PostgreSQL

Make sure PostgreSQL is installed and running:

```bash
# Ubuntu
sudo apt update
sudo apt install postgresql postgresql-contrib

# macOS (Homebrew)
brew install postgresql
brew services start postgresql
```

Update your `django_gateway/settings.py` with:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Then run:

```bash
python manage.py migrate
```

---

### 4. Compile Proto Files

```bash
python -m grpc_tools.protoc -I=protos --python_out=generated --grpc_python_out=generated protos/auth.proto
python -m grpc_tools.protoc -I=protos --python_out=generated --grpc_python_out=generated protos/user.proto
```

---

### 5. Run gRPC Services (In Separate Terminals)

**Auth Service**

```bash
python auth_service/server.py
```

**User Service**

```bash
python user_service/server.py
```

---

### 6. Run Django Gateway

```bash
python manage.py runserver
```

---

## 🔑 API Endpoints

| Method | Endpoint        | Description                     |
|--------|------------------|---------------------------------|
| POST   | /register/       | Register new user via AuthService |
| POST   | /login/          | Login and receive JWT token       |
| GET    | /users/?username=xyz | Get user info via UserService    |

Use JWT Bearer Token in headers:
```
Authorization: Bearer <JWT_TOKEN>
```

---

## 📦 gRPC Microservices

### 🔐 AuthService (gRPC)

- `Register(username, password, email)` → returns token + message
- `Login(username, password)` → returns token + message
- `ValidateToken(token)` → returns is_valid: true/false

### 👤 UserService (gRPC)

- `GetUser(username)` → returns id, username, email

---

## 🧪 Example Usage

### 1. Register User

```http
POST /register/
{
  "username": "john",
  "password": "123456",
  "email": "john@example.com"
}
```

### 2. Login

```http
POST /login/
{
  "username": "john",
  "password": "123456"
}
```

Response:
```json
{
  "success": true,
  "data": {
    "access_token": "<JWT>"
  }
}
```

### 3. Get User Info

```http
GET /users/?username=john
Authorization: Bearer <JWT>
```

Response:
```json
{
  "success": true,
  "data": {
    "id": "1",
    "username": "john",
    "email": "john@example.com"
  }
}
```

---

## 📁 Project Structure

```
grpc_demo/
├── auth_service/
│   ├── server.py
│   ├── models.py
├── user_service/
│   ├── server.py
│   ├── models.py
├── django_gateway/
│   ├── views.py
│   ├── urls.py
│   ├── settings.py
├── generated/
│   ├── auth_pb2.py
│   ├── auth_pb2_grpc.py
│   ├── user_pb2.py
│   ├── user_pb2_grpc.py
├── protos/
│   ├── auth.proto
│   ├── user.proto
├── manage.py
├── requirements.txt
```

---

## 📊 Roadmap

- ✅ Token-based Auth using gRPC
- ✅ Django as API Gateway
- 🔄 Add gRPC NotificationService
- 🔄 Add gRPC ChatService
- 🔄 Docker + Docker Compose setup
- 🔄 Add Swagger-like interface for proto contracts

---

## 📄 License

MIT License — free to use, share, and modify.

## 👨‍💼 Author

**Zeeshan Habib**
Software Engineer
📧 [zesbox6@gmail.com](mailto:zesbox6@gmail.com)
🔗 [GitHub](https://github.com/itx-zeeshan) | [LinkedIn](https://www.linkedin.com/in/zeeshan-habib-dev/)

---

**P.S: Reach out for collaboration or freelance work!**
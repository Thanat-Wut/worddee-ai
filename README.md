# Worddee AI

แพลตฟอร์มการเรียนรู้คำศัพท์ภาษาอังกฤษที่ขับเคลื่อนด้วย AI ช่วยให้ผู้เรียนสามารถเพิ่มคำศัพท์ สร้างประโยค และฝึกฝนการใช้คำศัพท์ได้อย่างมีประสิทธิภาพ

## 🎯 คุณสมบัติหลัก

- 📚 จัดการคำศัพท์และความหมาย
- ✍️ สร้างและตรวจสอบประโยคด้วย AI
- 🤖 ระบบ Workflow Automation ด้วย n8n
- 🗄️ จัดเก็บข้อมูลด้วย PostgreSQL
- 🐳 รองรับ Docker Compose สำหรับ deployment ที่ง่าย

## 🏗️ สถาปัตยกรรม

โปรเจกต์ประกอบด้วย 5 services หลัก:

- **Frontend** (Next.js 14 + TypeScript) - UI สำหรับผู้ใช้
- **Backend** (FastAPI) - Business logic และ API endpoints
- **Vocabulary API** (FastAPI) - API สำหรับจัดการคำศัพท์ (repository แยก)
- **PostgreSQL** - ฐานข้อมูลหลัก
- **n8n** - Workflow automation สำหรับตรวจสอบประโยค

## 📋 ความต้องการของระบบ

- Docker และ Docker Compose
- Git
- พื้นที่ว่างอย่างน้อย 2GB

## 🚀 การติดตั้งและรัน

### 1. Clone Repositories

โปรเจกต์นี้ต้องการ 2 repositories:

```bash
# Clone worddee-ai (main project)
git clone https://github.com/Thanat-Wut/worddee-ai.git
cd worddee-ai

# Clone worddee-api (vocabulary API) ไปยัง parent directory
cd ..
git clone https://github.com/Thanat-Wut/worddee-api.git
```

โครงสร้างโฟลเดอร์ที่ถูกต้อง:
```
.
├── worddee-ai/
│   ├── frontend/
│   ├── backend/
│   ├── database/
│   ├── n8n/
│   └── docker-compose.yml
└── worddee-api/
    ├── app/
    ├── Dockerfile
    └── requirements.txt
```

### 2. ตั้งค่า Environment Variables

```bash
cd worddee-ai
cp .env.example .env
```

แก้ไขไฟล์ `.env` ตามความต้องการ:

```env
# Database
POSTGRES_USER=worddee_admin
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=worddee_db
DATABASE_URL=postgresql://worddee_admin:your_secure_password@postgres:5432/worddee_db

# n8n
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your_n8n_password
N8N_WEBHOOK_URL=http://n8n:5678/webhook/validate-sentence
GENERIC_TIMEZONE=Asia/Bangkok

# APIs
VOCAB_API_URL=http://worddee_api:8001
VOCAB_API_KEY=your_256bit_api_key
GEMINI_API_KEY=your_gemini_api_key

# CORS
CORS_ORIGINS=http://localhost:3000,http://frontend:3000

# Frontend
NEXT_PUBLIC_WORDDEE_API_URL=http://localhost:8000
NEXT_PUBLIC_VOCAB_API_URL=http://localhost:8001
```

### 3. รัน Application

```bash
docker-compose up -d
```

รอจนทุก service พร้อมใช้งาน (ประมาณ 2-3 นาที)

### 4. ตรวจสอบสถานะ

```bash
# ดู logs
docker-compose logs -f

# ตรวจสอบสถานะ services
docker-compose ps
```

## 🌐 เข้าถึง Services

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | หน้าเว็บหลัก |
| **Backend API** | http://localhost:8000 | API หลัก |
| **Backend Docs** | http://localhost:8000/docs | API Documentation |
| **Vocabulary API** | http://localhost:8001 | Vocabulary Management |
| **Vocab API Docs** | http://localhost:8001/docs | Vocab API Documentation |
| **n8n** | http://localhost:5678 | Workflow Automation UI |
| **PostgreSQL** | localhost:5432 | Database (ใช้ DBeaver/pgAdmin) |

## 🔧 การพัฒนา

### รัน Services แบบแยก

```bash
# รันเฉพาะ database และ n8n
docker-compose up -d postgres n8n

# รัน backend แบบ local
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# รัน frontend แบบ local
cd frontend
npm install
npm run dev
```

### ดู Logs

```bash
# ดู logs ทั้งหมด
docker-compose logs -f

# ดู logs เฉพาะ service
docker-compose logs -f worddee_backend
docker-compose logs -f worddee_api
docker-compose logs -f frontend
```

### เข้า Container

```bash
# เข้า backend container
docker exec -it worddee_backend bash

# เข้า database
docker exec -it worddee_postgres psql -U worddee_admin -d worddee_db
```

## 🗄️ Database

### Initial Setup

Database จะถูก initialize อัตโนมัติจากไฟล์ `database/init.sql` เมื่อรันครั้งแรก

### Migration

หากต้องการ reset database:

```bash
docker-compose down -v
docker-compose up -d
```

## 🛑 การหยุดและลบ

```bash
# หยุด services
docker-compose down

# หยุดและลบ volumes (ลบข้อมูล database)
docker-compose down -v

# ลบทั้งหมดรวม images
docker-compose down -v --rmi all
```

## 📁 โครงสร้างโปรเจกต์

```
worddee-ai/
├── frontend/              # Next.js application
│   ├── app/
│   ├── components/
│   ├── public/
│   ├── Dockerfile
│   └── package.json
├── backend/              # FastAPI application
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
├── database/            # Database initialization
│   └── init.sql
├── n8n/                # n8n workflows
│   └── workflows/
├── docker-compose.yml  # Docker orchestration
├── .env.example       # Environment variables template
└── README.md
```

## 🔍 Health Checks

ทุก service มี health check endpoints:

```bash
# Backend
curl http://localhost:8000/health

# Vocabulary API
curl http://localhost:8001/health

# Frontend
curl http://localhost:3000

# Database
docker exec worddee_postgres pg_isready -U worddee_admin
```

## 🐛 Troubleshooting

### Service ไม่สามารถเชื่อมต่อกัน

```bash
# ตรวจสอบ network
docker network inspect worddee-ai_worddee_network

# Restart services
docker-compose restart
```

### Port ถูกใช้งานอยู่แล้ว

แก้ไข ports ในไฟล์ `docker-compose.yml`

### Database connection error

- ตรวจสอบ `DATABASE_URL` ในไฟล์ `.env`
- รอให้ PostgreSQL service พร้อมใช้งาน (health check)
- ตรวจสอบ logs: `docker-compose logs postgres`

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License

## 👤 Author

**Thanat Wut**
- GitHub: [@Thanat-Wut](https://github.com/Thanat-Wut)

## 🙏 Acknowledgments

- Next.js Team
- FastAPI Team
- n8n Community
- PostgreSQL Team

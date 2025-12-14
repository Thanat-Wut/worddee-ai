# ✍️ Worddee.ai: AI-Powered English Vocabulary Coach

**Worddee.ai** คือเว็บแอปพลิเคชันฝึกภาษาอังกฤษที่ช่วยให้ผู้เรียนฝึกแต่งประโยคจากคำศัพท์ประจำวัน (Word of the Day) โดยมี AI คอยตรวจไวยากรณ์ ให้คะแนน และแนะนำประโยคที่สละสลวยกว่า พร้อมระบบ Dashboard ติดตามพัฒนาการของผู้เรียนแบบ Real-time

---

## 📂 Project Architecture

โปรเจกต์ Worddee แบ่งออกเป็น **2 repositories** ที่ทำงานสอดประสานกัน:

### 1. **worddee-ai** (Repository นี้) - Main Application
worddee-ai/
├── 📂 backend/ # FastAPI - Orchestrator & AI Integration
│ ├── main.py # Main API Gateway
│ ├── db/ # Database models & connections
│ ├── routes/ # API endpoints
│ ├── schemas/ # Pydantic models
│ ├── services/ # Business logic
│ ├── middleware/ # CORS, logging, auth
│ ├── tests/ # Unit & integration tests
│ └── requirements.txt
│
├── 📂 frontend/ # Next.js 14 - User Interface
│ ├── app/ # App Router pages
│ │ ├── page.tsx # Challenge page (Word of the Day)
│ │ └── dashboard/ # Statistics & progress charts
│ ├── components/ # Reusable UI components
│ ├── lib/ # Utilities (API client, helpers)
│ ├── package.json
│ └── tsconfig.json
│
├── 📂 database/ # PostgreSQL initialization
│ └── init.sql # Database schema
│
├── 📂 n8n/ # AI Workflow Automation
│ └── workflows/ # Pre-configured Gemini workflow
│
├── docker-compose.yml # Multi-container orchestration
├── .env.example # Environment variables template
└── README.md

text

### 2. **[worddee-api](https://github.com/Thanat-Wut/worddee-api)** - Vocabulary Microservice
คลังคำศัพท์แยกออกมาเป็น API Service เฉพาะทาง:
- สุ่มคำศัพท์แบ่งตามระดับ (Beginner/Intermediate/Advanced)
- CRUD operations สำหรับจัดการคำศัพท์
- ให้บริการผ่าน REST API พร้อม OpenAPI documentation

> **📌 หมายเหตุ:** ต้อง clone และรันทั้ง 2 repositories เพื่อใช้งาน Worddee แบบสมบูรณ์

---

## 📸 App Screenshots

| Word of the Day Challenge | Learner Dashboard |
|:---:|:---:|
| ![Challenge](./images/challenge.png) | ![Dashboard](./images/dashboard.png) |
| *หน้าสุ่มคำศัพท์และแต่งประโยค* | *หน้าสรุปผลและกราฟพัฒนาการ* |

---

## 🚀 Getting Started

### Prerequisites (สิ่งที่ต้องมี)
- **Docker & Docker Compose** (v20.10+)
- **Git**
- **Gemini API Key** - ขอฟรีได้ที่ [Google AI Studio](https://aistudio.google.com/app/apikey)

### Installation Steps

#### 1. Clone ทั้ง 2 Repositories
Clone main application
git clone https://github.com/Thanat-Wut/worddee-ai.git
cd worddee-ai

Clone vocabulary API (ในโฟลเดอร์เดียวกัน)
cd ..
git clone https://github.com/Thanat-Wut/worddee-api.git

text

โครงสร้างที่ได้:
📁 your-workspace/
├── worddee-ai/ # Main app
└── worddee-api/ # Vocabulary service

text

#### 2. Setup Environment Variables

**สำหรับ worddee-ai:**
cd worddee-ai
cp .env.example .env

text

แก้ไขไฟล์ `.env`:
Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=worddee_db

AI Service
GEMINI_API_KEY=AIzaSyD_xxxxxxxxxxxxxxxxxxxxx

Vocabulary API (URL ของ worddee-api)
VOCABULARY_API_URL=http://localhost:8001

text

**สำหรับ worddee-api:**
cd ../worddee-api
cp .env.example .env

text

แก้ไขตามต้องการ (โดยปกติค่า default ใช้ได้เลย)

#### 3. Start Services

**เริ่มต้น worddee-api (Vocabulary Service):**
cd worddee-api
docker-compose up -d --build

text

เช็คว่ารันสำเร็จ: เปิด http://localhost:8001/docs (ต้องเห็น Swagger UI)

**เริ่มต้น worddee-ai (Main Application):**
cd ../worddee-ai
docker-compose up -d --build

text

รอประมาณ 2-3 นาที จนกว่า services ทั้งหมดจะพร้อม

#### 4. Setup n8n Workflow (สำคัญมาก!)

1. เปิด n8n: http://localhost:5678
2. Sign up (สร้างบัญชี Admin สำหรับใช้งานในเครื่อง)
3. Import workflow: คลิก **Settings** → **Import from File** → เลือก `n8n/workflows/worddee-gemini.json`
4. Configure Gemini credential:
   - คลิกที่ Node **Google Gemini Chat Model**
   - Credential → **Create New**
   - ใส่ **Gemini API Key** → Save
5. **Activate workflow**: กดปุ่ม **Inactive** (มุมขวาบน) ให้เป็นสีเขียว **Active**

#### 5. Access Application

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | หน้าเว็บหลัก (Challenge & Dashboard) |
| **Backend API** | http://localhost:8000/docs | FastAPI documentation |
| **Vocabulary API** | http://localhost:8001/docs | คลังคำศัพท์ API |
| **n8n Workflow** | http://localhost:5678 | AI automation dashboard |
| **Database** | `localhost:5432` | PostgreSQL (ใช้ DBeaver/pgAdmin) |

---

## ✨ Key Features

### 🎯 Word of the Day Challenge
- สุ่มคำศัพท์จาก `worddee-api` แบ่งตามระดับ (Beginner/Intermediate/Advanced)
- แสดงคำอ่าน (phonetic), ความหมาย, และรูปภาพประกอบ
- ผู้เรียนพิมพ์ประโยคตัวอย่าง → ส่งไปตรวจ

### 🤖 AI-Powered Feedback
- ตรวจประโยคผ่าน **n8n + Google Gemini**
- ให้คะแนน 0-10 (Grammar, Vocabulary, Naturalness)
- แสดงระดับ CEFR (A1-C2)
- แนะนำประโยคที่ดีกว่า (Improved Sentence)

### 📊 Interactive Dashboard
- **Progress Chart**: กราฟแนวโน้มคะแนน (Recharts)
- **Learning Streak**: นับวันติดต่อกันที่ฝึก
- **Total Practice Time**: เวลาเรียนสะสม
- **Recent History**: ประวัติประโยคล่าสุด 10 รายการ

### 💾 Persistent Data
- บันทึก history ทั้งหมดลง PostgreSQL
- รองรับ multi-user (พร้อม authentication - coming soon)

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Next.js 14 (TypeScript) | React App Router, Tailwind CSS |
| **Visualization** | Recharts | Dashboard charts |
| **Backend** | FastAPI (Python 3.11) | API orchestrator, business logic |
| **Vocabulary Service** | FastAPI (Microservice) | Isolated word management |
| **AI Integration** | n8n + Google Gemini | Grammar checking & feedback |
| **Database** | PostgreSQL 16 | Persistent storage |
| **Containerization** | Docker + Docker Compose | Multi-service deployment |

---

## 🧪 Development

### Run in Development Mode

**Backend (with hot reload):**
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000

text

**Frontend (with hot reload):**
cd frontend
npm install
npm run dev

text

### Database Migrations
Enter backend container
docker exec -it worddee-backend bash

Run migrations (if using Alembic)
alembic upgrade head

text

### Run Tests
Backend tests
cd backend
pytest tests/

Frontend tests
cd frontend
npm run test

text

---

## 🐛 Troubleshooting

### n8n workflow ไม่ทำงาน
- เช็คว่า workflow เป็น **Active** (สีเขียว)
- ตรวจสอบ Gemini credential ว่าใส่ API key ถูกต้อง
- ดู logs: `docker logs worddee-n8n`

### Database connection error
- เช็คว่า PostgreSQL container รันอยู่: `docker ps | grep postgres`
- ตรวจสอบ `.env` ว่า username/password ตรงกัน
- Restart: `docker-compose restart db`

### Vocabulary API ไม่ตอบกลับ
- เช็คว่า worddee-api รันอยู่: `curl http://localhost:8001/health`
- ดู logs: `cd worddee-api && docker-compose logs -f`

---

## 📚 API Documentation

### Main Backend Endpoints
GET /api/words/random # ดึงคำสุ่มจาก vocabulary API
POST /api/feedback/submit # ส่งประโยคไปตรวจ AI
GET /api/history # ดึงประวัติทั้งหมด
GET /api/stats # ดึงสถิติ dashboard

text

### Vocabulary API Endpoints
GET /words # ดึงคำศัพท์ทั้งหมด
GET /words/random?level=easy # สุ่มคำตามระดับ
POST /words # เพิ่มคำใหม่
DELETE /words/{id} # ลบคำ

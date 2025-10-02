# Fission Core - Deploy Guide

## 🚀 Cách deploy dự án lên Fission:

### **📋 Quy trình hiện tại:**

#### **1. Clone dự án về local:**
```bash
git clone https://github.com/username/repo.git
cd repo
```

#### **2. Deploy function đơn giản:**
```bash
# Deploy file đơn lẻ (khuyến nghị)
fission function create --name my-service --env nodejs --code /path/to/file.js

# Deploy từ GitHub URL (có thể lỗi với dependencies)
fission function create --name my-service --env nodejs --sourcearchive https://github.com/user/repo/archive/main.zip --entrypoint file.js
```

#### **3. Tạo route:**
```bash
fission route create --name my-route --function my-service --url /my-api --method GET
```

#### **4. Port forwarding:**
```bash
kubectl port-forward svc/router 8090:80 -n fission
```

## ✅ **APIs đang hoạt động:**

### **Simple Functions (✅ Hoạt động):**
- `http://localhost:8090/test-local` - Function đơn giản
- `http://localhost:8090/tables-simple` - Tables service đơn giản

### **Complex Services (❌ Chưa hoạt động):**
- `http://localhost:8090/api` - Main API (có dependencies)
- `http://localhost:8090/tables` - Tables service (Firebase)

## 🔧 **Yêu cầu hệ thống:**

### **Fission Infrastructure:**
```bash
# Kiểm tra Fission pods
kubectl get pods -n fission

# Kiểm tra functions
fission function list

# Kiểm tra routes  
fission route list
```

### **Port Forwarding:**
```bash
# Forward router port
kubectl port-forward svc/router 8090:80 -n fission
```

## 📝 **Ví dụ deploy:**

### **Deploy function đơn giản:**
```bash
# 1. Tạo file function
echo 'module.exports = (context) => { return { status: 200, body: "Hello!" }; };' > hello.js

# 2. Deploy function
fission function create --name hello --env nodejs --code hello.js

# 3. Tạo route
fission route create --name hello-route --function hello --url /hello --method GET

# 4. Test
curl http://localhost:8090/hello
```

### **Deploy service phức tạp:**
```bash
# 1. Clone dự án
git clone https://github.com/ductri09072004/jollicow_be.git

# 2. Tạo wrapper đơn giản
# (Cần chuyển đổi Express → Fission format)

# 3. Deploy wrapper
fission function create --name service --env nodejs --code wrapper.js
```

## ⚠️ **Hạn chế hiện tại:**

### **❌ Không hoạt động:**
- **Express apps** - Cần wrapper
- **Dependencies** - node_modules quá lớn
- **ES6 modules** - Cần chuyển sang CommonJS
- **Firebase** - Cần config credentials
- **Database** - Cần external services

### **✅ Hoạt động tốt:**
- **Simple functions** - Logic đơn giản
- **Mock data** - Không cần database
- **CommonJS** - module.exports/require

## 🎯 **Khuyến nghị:**

### **Cho dự án mới:**
- Viết functions đơn giản
- Sử dụng external APIs
- Tránh dependencies phức tạp

### **Cho dự án hiện tại:**
- Tạo wrapper functions
- Mock data thay vì database
- Chia nhỏ thành microservices

## 📊 **Kiểm tra status:**
```bash
# Functions
fission function list

# Routes
fission route list

# Test API
curl http://localhost:8090/your-endpoint
```

## 🐍 Deploy Python Flask API (Python_test)

### 1) Chạy trực tiếp (Windows)
```bash
cd E:\Study\Python_test
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
# Truy cập: http://localhost:5000/health
```

### 2) Production với Waitress
```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

### 3) Mở firewall cổng 5000 (nếu cần)
```powershell
New-NetFirewallRule -DisplayName "PythonTestAPI_5000" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow
```

### 4) Docker (tùy chọn)
Dockerfile (đặt cạnh `app.py`):
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install waitress
COPY . .
ENV PYTHONUNBUFFERED=1
EXPOSE 5000
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "app:app"]
```
Build và chạy:
```bash
cd E:\Study\Python_test
docker build -t python-test-api .
docker run -d -p 5000:5000 --name python-test-api python-test-api
```

### 5) Kiểm tra nhanh
```bash
curl http://localhost:5000/health
curl http://localhost:5000/api/hello
```
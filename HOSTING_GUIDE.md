# Hướng Dẫn Host Bot Miễn Phí / Free Bot Hosting Guide

## Tiếng Việt

### Giới Thiệu
ReadRSS Lite có thể được host miễn phí trên nhiều nền tảng khác nhau. Dưới đây là hướng dẫn chi tiết cho từng nền tảng.

### 1. GitHub Actions (Khuyến nghị)

**Ưu điểm:**
- Hoàn toàn miễn phí với GitHub
- Tự động deploy khi có thay đổi code
- Không cần server riêng
- Dễ quản lý và theo dõi

**Nhược điểm:**
- Giới hạn 2000 phút/tháng
- Bot sẽ restart mỗi 6 giờ
- Không phù hợp cho bot có traffic cao

**Cách thiết lập:**

1. **Fork repository:**
   - Vào repository gốc trên GitHub
   - Click nút "Fork" ở góc trên bên phải
   - Chọn tài khoản của bạn để fork

2. **Thêm Discord Bot Token:**
   - Vào [Discord Developer Portal](https://discord.com/developers/applications)
   - Tạo application mới hoặc chọn application có sẵn
   - Vào tab "Bot" và copy token

3. **Thiết lập Firebase (nếu cần):**
   - Vào [Firebase Console](https://console.firebase.google.com/)
   - Tạo project mới
   - Vào Settings → Service accounts
   - Generate private key và download file JSON

4. **Cấu hình Secrets trong GitHub:**
   - Vào repository đã fork
   - Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Thêm các secret sau:
     - Name: `DISCORD_TOKEN`, Value: bot token của bạn
     - Name: `FIREBASE_CREDENTIALS`, Value: nội dung file JSON Firebase

5. **Kích hoạt Actions:**
   - Vào tab "Actions" trong repository
   - Click "I understand my workflows, go ahead and enable them"
   - Bot sẽ tự động chạy

6. **Theo dõi bot:**
   - Vào tab "Actions" để xem log
   - Workflow "Run ReadRSS Bot" sẽ chạy bot
   - Workflow "Keep Bot Alive" sẽ ping để giữ bot online

### 2. Railway

**Ưu điểm:**
- 500 giờ miễn phí/tháng
- Automatic deployment
- Custom domain
- Database hỗ trợ

**Cách thiết lập:**

1. **Đăng ký Railway:**
   - Vào [railway.app](https://railway.app)
   - Đăng nhập bằng GitHub

2. **Deploy bot:**
   - Click "New Project"
   - Chọn "Deploy from GitHub repo"
   - Chọn repository ReadRSS-Lite đã fork

3. **Cấu hình environment variables:**
   - Trong project dashboard, vào tab "Variables"
   - Thêm:
     - `DISCORD_TOKEN`: bot token
     - `FIREBASE_CREDENTIALS`: Firebase JSON

4. **Cấu hình build:**
   - Railway sẽ tự động detect Python
   - Build command: `pip install -r requirements.txt`
   - Start command: `cd src && python main.py`

### 3. Render

**Ưu điểm:**
- Hosting miễn phí
- SSL certificate tự động
- Custom domain
- Git integration

**Cách thiết lập:**

1. **Đăng ký Render:**
   - Vào [render.com](https://render.com)
   - Đăng nhập bằng GitHub

2. **Tạo Web Service:**
   - Click "New +"
   - Chọn "Web Service"
   - Connect repository ReadRSS-Lite

3. **Cấu hình service:**
   - Name: readrss-bot
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd src && python main.py`

4. **Thêm environment variables:**
   - Trong dashboard, vào "Environment"
   - Thêm các variables cần thiết

### 4. Replit (Hiện tại)

**Cách thiết lập:**

1. **Import project:**
   - Vào [replit.com](https://replit.com)
   - Click "Create Repl"
   - Chọn "Import from GitHub"
   - Paste URL repository

2. **Cấu hình secrets:**
   - Click biểu tượng khóa (Secrets)
   - Thêm:
     - `DISCORD_TOKEN`
     - `FIREBASE_CREDENTIALS`

3. **Chạy bot:**
   - Click nút "Run"
   - Bot sẽ start và hiển thị log

4. **Giữ bot online:**
   - Repository đã có sẵn GitHub Actions ping
   - Cập nhật URL trong file `.github/workflows/keep-bot-alive.yml`

### Lưu Ý Quan Trọng

1. **Bảo mật:**
   - Không share token Discord
   - Sử dụng environment variables
   - Không commit secrets vào code

2. **Monitoring:**
   - Theo dõi uptime bot
   - Check logs thường xuyên
   - Set up alerts nếu cần

3. **Backup:**
   - Backup cấu hình Firebase
   - Backup Discord bot settings
   - Keep track của các environment variables

---

## English

### Introduction
ReadRSS Lite can be hosted for free on various platforms. Below are detailed guides for each platform.

### 1. GitHub Actions (Recommended)

**Pros:**
- Completely free with GitHub
- Automatic deployment on code changes
- No need for separate server
- Easy management and monitoring

**Cons:**
- 2000 minutes/month limit
- Bot restarts every 6 hours
- Not suitable for high-traffic bots

**Setup Instructions:**

1. **Fork Repository:**
   - Go to the original repository on GitHub
   - Click "Fork" button in top-right corner
   - Select your account to fork to

2. **Get Discord Bot Token:**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create new application or select existing one
   - Go to "Bot" tab and copy token

3. **Setup Firebase (if needed):**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create new project
   - Go to Settings → Service accounts
   - Generate private key and download JSON file

4. **Configure GitHub Secrets:**
   - Go to your forked repository
   - Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Add these secrets:
     - Name: `DISCORD_TOKEN`, Value: your bot token
     - Name: `FIREBASE_CREDENTIALS`, Value: Firebase JSON content

5. **Enable Actions:**
   - Go to "Actions" tab in repository
   - Click "I understand my workflows, go ahead and enable them"
   - Bot will start automatically

6. **Monitor Bot:**
   - Go to "Actions" tab to view logs
   - "Run ReadRSS Bot" workflow runs the bot
   - "Keep Bot Alive" workflow pings to keep bot online

### 2. Railway

**Pros:**
- 500 free hours/month
- Automatic deployment
- Custom domains
- Database support

**Setup Instructions:**

1. **Sign up for Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub

2. **Deploy Bot:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your forked ReadRSS-Lite repository

3. **Configure Environment Variables:**
   - In project dashboard, go to "Variables" tab
   - Add:
     - `DISCORD_TOKEN`: your bot token
     - `FIREBASE_CREDENTIALS`: Firebase JSON

4. **Configure Build:**
   - Railway auto-detects Python
   - Build command: `pip install -r requirements.txt`
   - Start command: `cd src && python main.py`

### 3. Render

**Pros:**
- Free hosting
- Automatic SSL certificates
- Custom domains
- Git integration

**Setup Instructions:**

1. **Sign up for Render:**
   - Go to [render.com](https://render.com)
   - Sign in with GitHub

2. **Create Web Service:**
   - Click "New +"
   - Select "Web Service"
   - Connect ReadRSS-Lite repository

3. **Configure Service:**
   - Name: readrss-bot
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd src && python main.py`

4. **Add Environment Variables:**
   - In dashboard, go to "Environment"
   - Add required variables

### 4. Replit (Current Setup)

**Setup Instructions:**

1. **Import Project:**
   - Go to [replit.com](https://replit.com)
   - Click "Create Repl"
   - Select "Import from GitHub"
   - Paste repository URL

2. **Configure Secrets:**
   - Click lock icon (Secrets)
   - Add:
     - `DISCORD_TOKEN`
     - `FIREBASE_CREDENTIALS`

3. **Run Bot:**
   - Click "Run" button
   - Bot will start and show logs

4. **Keep Bot Online:**
   - Repository has GitHub Actions ping setup
   - Update URL in `.github/workflows/keep-bot-alive.yml`

### Important Notes

1. **Security:**
   - Never share Discord tokens
   - Use environment variables
   - Don't commit secrets to code

2. **Monitoring:**
   - Monitor bot uptime
   - Check logs regularly
   - Set up alerts if needed

3. **Backup:**
   - Backup Firebase configuration
   - Backup Discord bot settings
   - Keep track of environment variables

## Troubleshooting / Khắc Phục Sự Cố

### Common Issues / Lỗi Thường Gặp

1. **Bot không online:**
   - Kiểm tra token Discord
   - Kiểm tra environment variables
   - Xem logs để tìm lỗi

2. **GitHub Actions failed:**
   - Kiểm tra secrets đã cấu hình đúng
   - Xem logs trong Actions tab
   - Đảm bảo requirements.txt đúng

3. **Bot bị disconnect:**
   - Kiểm tra internet connection
   - Kiểm tra Discord API status
   - Restart bot service

### Support / Hỗ Trợ

Nếu gặp vấn đề, có thể:
- Mở issue trên GitHub repository
- Kiểm tra logs chi tiết
- Liên hệ team phát triển

If you encounter issues, you can:
- Open an issue on GitHub repository
- Check detailed logs
- Contact development team
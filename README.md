# ReadRSS lite
ReadRSS Lite is the free version of Aiko (ReadRSS) - a Discord bot built with Python, bringing RSS feed notifications to your Discord server. Stay updated with news sources like Youtube and much more.

ReadRSS Lite là phiên bản miễn phí của Aiko (ReadRSS) - một bot Discord được xây dựng bằng Python, giúp đưa thông báo từ RSS feed đến server Discord của bạn. Nhận thông báo từ các nguồn tin tức như Youtube và nhiều hơn nữa.

```
                        -- ABOUT US --
                                                       Summer 2024
         ██████╗  ██████╗██████╗ ███████╗██╗   ██╗     + HaoWasabi
        ██╔════╝ ██╔════╝██╔══██╗██╔════╝██║   ██║     + nguyluky
        ██║  ███╗██║     ██║  ██║█████╗  ██║   ██║     + NaelTuhline
        ██║   ██║██║     ██║  ██║██╔══╝  ╚██╗ ██╔╝     + tivibin789
        ╚██████╔╝╚██████╗██████╔╝███████╗ ╚████╔╝      + phusomnia
        ╚═════╝  ╚═════╝╚═════╝ ╚══════╝  ╚═══╝        + camdao
``` 
## Installation

1. Clone the repository.  
   Sao chép repository về máy.

2. Create a virtual environment and activate it.  
   Tạo môi trường ảo và kích hoạt nó.

3. Install dependencies:  
   Cài đặt các phụ thuộc:  
    `pip install -r requirements.txt`

4. Create a `.env` file and add the following information:  
    Tạo file `.env` và thêm thông tin sau:
```
DISCORD_TOKEN=your_bot_token_here
FIREBASE_CREDENTIALS=your_firebase_service_account_json
```

5. Run the bot:
    Chạy bot:
    `python main.py`

## **Free Hosting Options / Các Lựa Chọn Host Miễn Phí**

### **1. GitHub Actions (Recommended / Khuyến nghị)**

**English:**
Host your bot directly on GitHub using GitHub Actions. This method runs your bot in the cloud for free with some limitations.

**Steps:**
1. Fork this repository to your GitHub account
2. Go to your repository Settings → Secrets and variables → Actions
3. Add these secrets:
   - `DISCORD_TOKEN`: Your Discord bot token
   - `FIREBASE_CREDENTIALS`: Your Firebase service account JSON
4. Enable GitHub Actions in your repository
5. The bot will automatically start running when you push changes
6. Monitor your bot in the Actions tab

**Limitations:**
- 6-hour maximum runtime per workflow run
- Limited to 2000 minutes/month for free accounts
- Bot will restart every 6 hours automatically

**Vietnamese:**
Host bot trực tiếp trên GitHub bằng GitHub Actions. Phương pháp này chạy bot trên cloud miễn phí với một số giới hạn.

**Các bước:**
1. Fork repository này về tài khoản GitHub của bạn
2. Vào Settings → Secrets and variables → Actions
3. Thêm các secret sau:
   - `DISCORD_TOKEN`: Token bot Discord của bạn
   - `FIREBASE_CREDENTIALS`: JSON tài khoản dịch vụ Firebase
4. Bật GitHub Actions trong repository
5. Bot sẽ tự động chạy khi bạn push code
6. Theo dõi bot ở tab Actions

**Giới hạn:**
- Tối đa 6 giờ chạy liên tục mỗi lần
- Giới hạn 2000 phút/tháng cho tài khoản miễn phí
- Bot sẽ tự động khởi động lại mỗi 6 giờ

### **2. Railway**

**English:**
Railway offers 500 hours of free hosting per month, perfect for Discord bots.

**Steps:**
1. Go to [Railway.app](https://railway.app) and sign up
2. Connect your GitHub account
3. Deploy this repository
4. Add environment variables in Railway dashboard:
   - `DISCORD_TOKEN`
   - `FIREBASE_CREDENTIALS`
5. Your bot will be automatically deployed

**Vietnamese:**
Railway cung cấp 500 giờ hosting miễn phí mỗi tháng, phù hợp cho Discord bot.

**Các bước:**
1. Vào [Railway.app](https://railway.app) và đăng ký
2. Kết nối tài khoản GitHub
3. Deploy repository này
4. Thêm biến môi trường trong dashboard Railway:
   - `DISCORD_TOKEN`
   - `FIREBASE_CREDENTIALS`
5. Bot sẽ được deploy tự động

### **3. Render**

**English:**
Render provides free hosting with automatic deployments from GitHub.

**Steps:**
1. Go to [Render.com](https://render.com) and sign up
2. Connect your GitHub account
3. Create a new Web Service
4. Select this repository
5. Use these settings:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd src && python main.py`
6. Add environment variables in Render dashboard

**Vietnamese:**
Render cung cấp hosting miễn phí với deploy tự động từ GitHub.

**Các bước:**
1. Vào [Render.com](https://render.com) và đăng ký
2. Kết nối tài khoản GitHub
3. Tạo Web Service mới
4. Chọn repository này
5. Sử dụng các cài đặt:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd src && python main.py`
6. Thêm biến môi trường trong dashboard Render

### **4. Replit (Current Setup / Thiết Lập Hiện Tại)**

**English:**
The repository is currently configured for Replit hosting with automatic ping system.

**Steps:**
1. Go to [Replit.com](https://replit.com) and import this repository
2. Add environment variables in Replit secrets
3. Run the bot
4. The GitHub Actions will automatically ping your Replit URL to keep it alive

**Vietnamese:**
Repository hiện đang được cấu hình cho hosting Replit với hệ thống ping tự động.

**Các bước:**
1. Vào [Replit.com](https://replit.com) và import repository này
2. Thêm biến môi trường trong Replit secrets
3. Chạy bot
4. GitHub Actions sẽ tự động ping URL Replit để giữ bot online

### **Important Notes / Lưu Ý Quan Trọng**

**English:**
- Free hosting services have limitations (uptime, resources, etc.)
- For production bots, consider paid hosting solutions
- Always keep your tokens and credentials secure
- Monitor your bot's uptime and performance

**Vietnamese:**
- Các dịch vụ hosting miễn phí có giới hạn (thời gian hoạt động, tài nguyên, v.v.)
- Với bot production, nên xem xét các giải pháp hosting trả phí
- Luôn bảo mật token và thông tin đăng nhập
- Theo dõi uptime và hiệu suất của bot

## **Basic slash commands / Các lệnh cơ bản**

- '/ping': Check bot latency.
Kiểm tra tốc độ phản hồi của bot.

- `/getrss url:<url web>`: Check if the website has an RSS feed.  
Kiểm tra xem trang web có link RSS không.

- `/test`: Send a test post from the fit.sgu website.  
Gửi thử bài đăng đầu tiên từ trang web fit.sgu.

- `/setfeed channel:<select text channel> url:<website url>`: Set up a channel to receive posts from the website.  
Thiết lập kênh để nhận thông báo bài đăng từ trang web bằng URL.

- `/deletefeed channel:<channel> rss:<rss link>`: Remove the RSS feed from the channel.  
Hủy thiết lập nhận thông báo từ link RSS đã đăng ký ở kênh chỉ định.

- `/show`: Show the list of registered RSS feeds in the server.  
Hiển thị danh sách các feed đã được đăng ký trong server.

**Note / Lưu ý**:  
The Lite version of ReadRSS has limited features and cannot be used in DM channels.  
Phiên bản Lite của ReadRSS bị giới hạn tính năng, không thể sử dụng ở các kênh DMChannel.

## **Other Information / Thông Tin Khác**

- **Feed**: Entity containing website information.  
Thực thể chứa thông tin trang web.

- **Emty**: The entity contains the website information of the website.
Thực thể chứa thông tin bài đăng của trang web.

- **Channel**: Server’s communication channels.  
Kênh liên lạc của server.

**Errors / Lỗi có thể gặp**:
- If the bot takes too long to respond, use command-based actions like `_ping` instead of slash commands (`/ping`).  
Nếu bot phản hồi chậm, hãy ưu tiên sử dụng các lệnh như `_ping` thay vì `/ping`.

---

## **Free Hosting Resources / Tài Nguyên Host Miễn Phí**

**For detailed hosting instructions, see [HOSTING_GUIDE.md](HOSTING_GUIDE.md)**  
**Xem hướng dẫn host chi tiết tại [HOSTING_GUIDE.md](HOSTING_GUIDE.md)**

**Quick Links / Liên Kết Nhanh:**
- [GitHub Actions Setup](#1-github-actions-recommended--khuyến-nghị) - Recommended
- [Railway Hosting](https://railway.app) - 500 hours/month
- [Render Hosting](https://render.com) - Free tier available  
- [Replit Hosting](https://replit.com) - Current setup

---

This project is designed with a focus on efficient and responsive Discord integration.  
Dự án này được thiết kế với mục tiêu tích hợp hiệu quả và đáp ứng nhanh trong môi trường Discord.

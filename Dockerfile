# Sử dụng Python image chính thức
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy requirements và cài đặt dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào container
COPY . .

# Expose port 5000 cho Flask app
EXPOSE 5000

# Command để chạy app
CMD ["python", "main.py"]
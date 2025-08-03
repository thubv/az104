# AZ-104 Course Crawlers

Bộ công cụ crawl và xử lý nội dung khóa học AZ-104 Microsoft Azure Administrator với hỗ trợ hình ảnh và dịch thuật.

## 📁 Cấu trúc thư mục

```
crawlers/
├── az104_image_crawler.py    # Crawler chính với hỗ trợ hình ảnh
├── batch_processor.py        # Xử lý hàng loạt
├── translation_tools.py      # Công cụ dịch thuật
└── README.md                # Tài liệu này
```

## 🚀 Cách sử dụng

### 1. Crawler chính với hỗ trợ hình ảnh

```bash
# Chạy crawler cho một unit cụ thể
python crawlers/az104_image_crawler.py

# Hoặc import và sử dụng trong code
from crawlers.az104_image_crawler import AZ104ImageCrawler
crawler = AZ104ImageCrawler()
await crawler.recrawl_single_unit(url, output_path)
```

**Tính năng:**
- ✅ Tải và lưu hình ảnh từ Microsoft Learn
- ✅ Xử lý URL hình ảnh thực tế bằng Playwright
- ✅ Tạo HTML với CSS nhúng đẹp mắt
- ✅ Hiển thị URL nguồn đầy đủ
- ✅ Hỗ trợ lazy loading cho hình ảnh

### 2. Xử lý hàng loạt

```bash
# Chạy batch processor
python crawlers/batch_processor.py

# Chọn tùy chọn:
# 1. Re-crawl tất cả 260 units với hình ảnh
# 2. Sửa URL nguồn trong các file hiện có
# 3. Thoát
```

**Tính năng:**
- ✅ Crawl lại toàn bộ 260 units
- ✅ Xử lý theo batch để tránh quá tải
- ✅ Báo cáo tiến độ chi tiết
- ✅ Xử lý lỗi an toàn

### 3. Công cụ dịch thuật

```bash
# Chạy translation tools
python crawlers/translation_tools.py

# Chọn tùy chọn:
# 1. Tạo template tiếng Việt
# 2. Tạo cơ sở dữ liệu thuật ngữ
# 3. Thoát
```

**Tính năng:**
- ✅ Tạo template HTML song ngữ
- ✅ Cơ sở dữ liệu thuật ngữ Azure
- ✅ Cấu trúc thư mục tự động
- ✅ Báo cáo thống kê

## 🛠️ Yêu cầu hệ thống

```bash
# Cài đặt dependencies
pip install playwright beautifulsoup4 aiofiles aiohttp

# Cài đặt Playwright browser
playwright install chromium
```

## 📊 Kết quả crawl gần nhất

- ✅ **249/260 units** crawl thành công với hình ảnh
- 🖼️ **Hơn 100 hình ảnh** được tải về
- 📁 **6 Learning Paths** hoàn chỉnh
- 📚 **31 Modules** với cấu trúc đầy đủ

## 🎯 Tính năng nổi bật

### Xử lý hình ảnh thông minh
- Sử dụng Playwright để lấy URL thực tế của hình ảnh
- Tải và lưu hình ảnh với tên unique (hash-based)
- Cập nhật tham chiếu trong HTML tự động
- Hỗ trợ lazy loading và responsive

### HTML chất lượng cao
- CSS nhúng với thiết kế Microsoft Learn
- Responsive design cho mobile
- Syntax highlighting cho code
- Alert boxes và styling đẹp mắt

### Xử lý lỗi mạnh mẽ
- Retry logic cho network requests
- Graceful handling cho missing content
- Detailed error reporting
- Session management tự động

## 📝 Cấu trúc file đầu ra

```
content/
├── english/                 # Nội dung tiếng Anh
│   ├── 01_Learning_Path/
│   │   ├── 01_Module/
│   │   │   └── 01_Unit.html
├── vietnamese/              # Template tiếng Việt
├── assets/                  # Hình ảnh đã tải
│   ├── image_hash1.png
│   └── image_hash2.jpg
└── terminology/             # Cơ sở dữ liệu thuật ngữ
    └── az104_vietnamese_terms.json
```

## 🔧 Tùy chỉnh

### Thay đổi styling
Chỉnh sửa CSS trong method `_create_clean_html_with_css()` của `AZ104ImageCrawler`.

### Thêm ngôn ngữ mới
Mở rộng `TranslationTools` để hỗ trợ ngôn ngữ khác.

### Tùy chỉnh batch size
Thay đổi `batch_size` trong `BatchProcessor` để điều chỉnh tốc độ crawl.

## 🐛 Troubleshooting

### Lỗi timeout
- Tăng timeout trong Playwright settings
- Giảm batch size để tránh quá tải server

### Hình ảnh không tải được
- Kiểm tra kết nối internet
- Xem log để biết URL nào bị lỗi
- Một số hình ảnh có thể bị Microsoft bảo vệ

### Memory issues
- Giảm batch size
- Đảm bảo session được đóng đúng cách
- Restart crawler sau một số lượng units nhất định

## 📞 Hỗ trợ

Nếu gặp vấn đề, hãy:
1. Kiểm tra log output chi tiết
2. Đảm bảo dependencies được cài đặt đúng
3. Kiểm tra kết nối internet ổn định
4. Xem file error HTML được tạo ra

## 🎉 Thành tựu

- 🏆 Crawl thành công **95.8%** nội dung khóa học
- 🖼️ Tải được **hàng trăm hình ảnh** chất lượng cao
- 📱 HTML responsive hoạt động trên mọi thiết bị
- 🌐 Sẵn sàng cho dịch thuật đa ngôn ngữ
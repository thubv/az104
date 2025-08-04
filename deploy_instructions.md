# Hướng dẫn Deploy lên GitHub Pages

## Bước 1: Tạo repository trên GitHub
1. Truy cập https://github.com
2. Click "New" để tạo repository mới
3. Tên repository: `az104-azure-administrator-vietnamese`
4. Mô tả: `AZ-104: Microsoft Azure Administrator - Vietnamese Translation`
5. Chọn **Public**
6. **KHÔNG** check "Add a README file"
7. Click "Create repository"

## Bước 2: Push code lên GitHub

Chạy các lệnh sau trong terminal:

```bash
# Thêm remote origin (thay YOUR_USERNAME bằng username GitHub của bạn)
git remote add origin https://github.com/YOUR_USERNAME/az104-azure-administrator-vietnamese.git

# Kiểm tra status
git status

# Add tất cả files
git add .

# Commit
git commit -m "Initial commit: AZ-104 Vietnamese translation project"

# Push lên GitHub
git push -u origin main
```

## Bước 3: Enable GitHub Pages

1. Vào repository trên GitHub
2. Click tab **Settings**
3. Scroll xuống phần **Pages** (bên trái)
4. Trong **Source**, chọn **Deploy from a branch**
5. Chọn branch **main**
6. Folder chọn **/ (root)**
7. Click **Save**

## Bước 4: Truy cập website

Sau vài phút, website sẽ có sẵn tại:
`https://YOUR_USERNAME.github.io/az104-azure-administrator-vietnamese/`

## Lưu ý quan trọng

- GitHub Pages có thể mất 5-10 phút để deploy lần đầu
- Mỗi lần push code mới, GitHub Pages sẽ tự động update
- Website sẽ hoạt động hoàn toàn miễn phí với GitHub Pages

## Kiểm tra deployment

Sau khi enable GitHub Pages, bạn có thể:
1. Vào tab **Actions** để xem quá trình deploy
2. Kiểm tra tab **Settings > Pages** để xem URL website
3. Truy cập URL để test website

## Troubleshooting

Nếu có lỗi:
- Kiểm tra tất cả files đã được push đúng chưa
- Đảm bảo file `index.html` ở root directory
- Kiểm tra GitHub Actions có lỗi không
- Đợi thêm vài phút cho deployment hoàn tất
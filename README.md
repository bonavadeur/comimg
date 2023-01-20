# Công cụ giảm dung lượng file ảnh
## 1. Giới thiệu
ComImg là tool đơn giản, được dùng để giảm dung lượng ảnh mà vẫn giữ nguyên kích thước, phù hợp để lưu trữ ảnh trên các website để tiết kiệm dung lượng lưu trữ
## 2. Hướng dẫn
+ Bước 1: đặt các file ảnh .jpg hoặc .png (có thể nhiều file một lúc) cùng cấp với file run.exe
+ Bước 2: Double-click vào file run.exe để tiến hành nén ảnh, ảnh sau khi được nén sẽ ghi đè lên ảnh cũ.
## 3. Hướng dẫn customize sourcecode
+ Sourcecode nằm ở branch dev, file run.py
+ Để thêm định dạng ảnh muốn nén, thêm dòng như mẫu dòng 12:
```python
jpgImages = Path("./").glob("*.jpg")
```
+ Để chỉnh tỉ lệ nén, sửa tham số quality ở dòng 10:
```python    
img.save(image, quality=50)
```
+ Để biên dịch lại ra file .exe, sử dụng lệnh:
```bash
pyinstaller --onefile -w 'run.py'
```
$\qquad$ file .exe sau khi được biên dịch nằm ở ./dist
+ Nếu chưa có pyinstaller, cài đặt bằng lệnh:
```bash
pip install pyinstaller
```
## 4. Phiên bản:
v1.0: 20/01/2023
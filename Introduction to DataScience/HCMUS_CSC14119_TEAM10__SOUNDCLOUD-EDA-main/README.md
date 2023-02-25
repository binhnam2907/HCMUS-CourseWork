# Tiến trình:
- Hoàn thành xong phần collect data (đã cập nhật lại phần dữ liệu của track.csv và playlist.csv).
- Hoàn thành xong phần EDA
- Hoàn thành xong phần Reference
  
# Lưu ý:
- Đồ án thực hiện trên máy Window
- Phần collect data này chạy khá lâu, nếu máy yếu vui lòng chạy trên Google colab
- Nếu chạy trên google colab (nhân linux) thì không sài được webdriver-manager, vui lòng install selenium, chronium bằng đoạn code sau:
```
!pip install selenium  
!apt-get update # to update ubuntu to correctly run apt install  
!apt install chromium-chromedriver  
!cp /usr/lib/chromium-browser/chromedriver /usr/bin  
import sys  
```
- Sau đó khởi tạo driver trong hàm `initialize_driver` như sau:
```
driver = webdriver.Chrome('chromedriver', options=chrome_options)
```
- Dữ liệu thu thập được chỉ là bản mẫu (nên sài để phân tích), sẽ có thể có chỉnh sửa sau này, nhưng đảm bảo dữ liệu cuối vẫn chạy được trên code phân tích.
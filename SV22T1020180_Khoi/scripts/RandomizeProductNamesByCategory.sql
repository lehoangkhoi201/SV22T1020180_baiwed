/*
  Random tên + giá + mô tả ngắn cho Products theo CategoryName (13 danh mục công nghệ).
  Không xóa/sửa Categories. Sản phẩm thuộc loại không có trong #Templates + #PriceRange sẽ bị bỏ qua.

  DB: LiteCommerceDB — sửa USE nếu khác.

  Backup (khuyến nghị):
    SELECT * INTO dbo.Products_Backup_YYYYMMDD FROM dbo.Products;

  Chạy bằng sqlcmd (Windows) — bắt buộc UTF-8 để giữ dấu tiếng Việt:
    sqlcmd -S . -d LiteCommerceDB -E -f 65001 -i "...\RandomizeProductNamesByCategory.sql"

  Hoặc mở file trong SSMS (UTF-8) rồi Execute.
*/

SET NOCOUNT ON;
GO

USE LiteCommerceDB;
GO

IF OBJECT_ID(N'tempdb..#Templates', N'U') IS NOT NULL DROP TABLE #Templates;
IF OBJECT_ID(N'tempdb..#PriceRange', N'U') IS NOT NULL DROP TABLE #PriceRange;
GO

CREATE TABLE #Templates (
    CategoryName NVARCHAR(255) NOT NULL,
    ProductName  NVARCHAR(255) NOT NULL
);

CREATE TABLE #PriceRange (
    CategoryName NVARCHAR(255) NOT NULL PRIMARY KEY,
    MinPrice     BIGINT NOT NULL,
    MaxPrice     BIGINT NOT NULL
);

/* --- Tên mẫu theo đúng 13 danh mục (khớp chữ với bảng Categories) --- */

INSERT INTO #Templates (CategoryName, ProductName) VALUES
(N'Điện thoại', N'iPhone 15 Pro 256GB'),
(N'Điện thoại', N'iPhone 14 128GB'),
(N'Điện thoại', N'Samsung Galaxy S24 Ultra'),
(N'Điện thoại', N'Samsung Galaxy A55 5G'),
(N'Điện thoại', N'Xiaomi 14T Pro'),
(N'Điện thoại', N'Xiaomi Redmi Note 13 Pro'),
(N'Điện thoại', N'Oppo Reno11 5G'),
(N'Điện thoại', N'Oppo Find X7'),
(N'Điện thoại', N'vivo V30 Pro'),
(N'Điện thoại', N'realme 12 Pro+ 5G'),

(N'Điện tử', N'Smart TV Samsung 55 inch 4K'),
(N'Điện tử', N'Smart TV LG OLED 48 inch'),
(N'Điện tử', N'Smart TV Sony Bravia 65 inch'),
(N'Điện tử', N'Android TV Box Xiaomi'),
(N'Điện tử', N'Loa thông minh Google Nest'),
(N'Điện tử', N'Màn hình di động portable 15.6"'),
(N'Điện tử', N'Máy chiếu mini Full HD'),

(N'Đồ chơi - phụ kiện', N'Bộ lắp ráp LEGO Technic'),
(N'Đồ chơi - phụ kiện', N'Xe điều khiển RC tốc độ cao'),
(N'Đồ chơi - phụ kiện', N'Figure mô hình nhân vật collectible'),
(N'Đồ chơi - phụ kiện', N'Bàn cờ chiến thuật board game'),
(N'Đồ chơi - phụ kiện', N'Đồ chơi STEM robot lập trình'),
(N'Đồ chơi - phụ kiện', N'Búp bê & phụ kiện thời trang'),
(N'Đồ chơi - phụ kiện', N'Súng nước đồ chơi cao cấp'),

(N'Gaming Gear', N'Chuột Logitech G Pro X Superlight'),
(N'Gaming Gear', N'Chuột Razer DeathAdder V3'),
(N'Gaming Gear', N'Bàn phím cơ Keychron K8 Pro'),
(N'Gaming Gear', N'Bàn phím cơ Corsair K70 RGB'),
(N'Gaming Gear', N'Tai nghe SteelSeries Arctis Nova 7'),
(N'Gaming Gear', N'Tai nghe HyperX Cloud III'),
(N'Gaming Gear', N'Tay cầm Xbox Wireless Controller'),
(N'Gaming Gear', N'Tay cầm DualSense PS5'),
(N'Gaming Gear', N'Bàn di chuột RGB XL'),
(N'Gaming Gear', N'Ghế gaming ergonomic'),

(N'Laptop', N'Dell XPS 15 OLED'),
(N'Laptop', N'Dell Inspiron 15 i5'),
(N'Laptop', N'HP Pavilion 14'),
(N'Laptop', N'HP Envy x360'),
(N'Laptop', N'Asus Zenbook 14 OLED'),
(N'Laptop', N'Asus TUF Gaming F15'),
(N'Laptop', N'Lenovo ThinkPad E14'),
(N'Laptop', N'Lenovo Legion 5'),
(N'Laptop', N'MacBook Air M3 13 inch'),
(N'Laptop', N'MacBook Pro 14 M3 Pro'),

(N'Màn hình & thiết bị hiển thị', N'Màn hình Dell UltraSharp 27" 4K'),
(N'Màn hình & thiết bị hiển thị', N'Màn hình LG 27" IPS 144Hz'),
(N'Màn hình & thiết bị hiển thị', N'Màn hình Samsung Odyssey G7 32"'),
(N'Màn hình & thiết bị hiển thị', N'Màn hình Asus ProArt 32" 4K'),
(N'Màn hình & thiết bị hiển thị', N'Màn hình portable USB-C 15.6"'),
(N'Màn hình & thiết bị hiển thị', N'Giá treo màn hình tay kép'),
(N'Màn hình & thiết bị hiển thị', N'Bộ chuyển HDMI sang USB-C'),

(N'Máy tính để bàn (PC)', N'PC văn phòng Intel i5 / 16GB / SSD 512GB'),
(N'Máy tính để bàn (PC)', N'PC gaming RTX 4060 / Ryzen 5'),
(N'Máy tính để bàn (PC)', N'PC đồ họa RTX 4070 / 32GB RAM'),
(N'Máy tính để bàn (PC)', N'Case Corsair 4000D Airflow'),
(N'Máy tính để bàn (PC)', N'Nguồn Corsair RM750e'),
(N'Máy tính để bàn (PC)', N'Mainboard B760 DDR5'),
(N'Máy tính để bàn (PC)', N'RAM DDR5 32GB kit 6000MHz'),
(N'Máy tính để bàn (PC)', N'CPU AMD Ryzen 7 7800X3D'),
(N'Máy tính để bàn (PC)', N'Tản nhiệt khí Noctua NH-D15'),

(N'Phụ kiện điện thoại', N'Ốp lưng silicone chống sốc'),
(N'Phụ kiện điện thoại', N'Kính cường lực full màn hình'),
(N'Phụ kiện điện thoại', N'Cáp sạc USB-C 100W 2m'),
(N'Phụ kiện điện thoại', N'Củ sạc GaN 65W 3 cổng'),
(N'Phụ kiện điện thoại', N'Đế sạc không dây MagSafe'),
(N'Phụ kiện điện thoại', N'Giá đỡ điện thoại xe hơi'),
(N'Phụ kiện điện thoại', N'Gậy selfie Bluetooth'),
(N'Phụ kiện điện thoại', N'Túi chống nước cho điện thoại'),

(N'Phụ kiện livestream & sáng tạo nội dung', N'Tripod nhôm cao 1.7m'),
(N'Phụ kiện livestream & sáng tạo nội dung', N'Đèn ring light 18 inch có chân'),
(N'Phụ kiện livestream & sáng tạo nội dung', N'Micro thu âm USB condenser'),
(N'Phụ kiện livestream & sáng tạo nội dung', N'Webcam Logitech Brio 4K'),
(N'Phụ kiện livestream & sáng tạo nội dung', N'Bộ thu âm wireless collar mic'),
(N'Phụ kiện livestream & sáng tạo nội dung', N'Green screen khung gấp 1.5x2m'),
(N'Phụ kiện livestream & sáng tạo nội dung', N'Capture card HDMI 4K30'),

(N'Thiết bị âm thanh', N'Tai nghe Bluetooth Sony WH-1000XM5'),
(N'Thiết bị âm thanh', N'Tai nghe true wireless AirPods Pro 2'),
(N'Thiết bị âm thanh', N'Loa Bluetooth JBL Charge 5'),
(N'Thiết bị âm thanh', N'Loa máy tính Logitech Z407'),
(N'Thiết bị âm thanh', N'Loa soundbar Samsung'),
(N'Thiết bị âm thanh', N'Micro động Shure SM58'),
(N'Thiết bị âm thanh', N'Interface thu âm Focusrite Scarlett'),

(N'Thiết bị lưu trữ', N'USB 3.2 SanDisk 256GB'),
(N'Thiết bị lưu trữ', N'USB-C Samsung BAR Plus 128GB'),
(N'Thiết bị lưu trữ', N'Ổ cứng ngoài HDD 2TB'),
(N'Thiết bị lưu trữ', N'SSD ngoài Samsung T7 1TB'),
(N'Thiết bị lưu trữ', N'SSD nội bộ NVMe 1TB Gen4'),
(N'Thiết bị lưu trữ', N'Thẻ nhớ microSD 256GB U3'),
(N'Thiết bị lưu trữ', N'NAS Synology 2 bay'),

(N'Thiết bị mạng', N'Router WiFi 6 TP-Link AX3000'),
(N'Thiết bị mạng', N'Router WiFi 6E Asus RT-AXE7800'),
(N'Thiết bị mạng', N'Mesh WiFi 3 pack Deco X55'),
(N'Thiết bị mạng', N'Switch mạng 8 port Gigabit'),
(N'Thiết bị mạng', N'Card mạng USB WiFi 6'),
(N'Thiết bị mạng', N'Bộ kích sóng WiFi repeater'),

(N'Thiết bị thông minh (Smart Home)', N'Camera an ninh 2K trong nhà'),
(N'Thiết bị thông minh (Smart Home)', N'Camera ngoài trời có đèn'),
(N'Thiết bị thông minh (Smart Home)', N'Ổ cắm thông minh WiFi'),
(N'Thiết bị thông minh (Smart Home)', N'Bóng đèn LED thông minh RGB'),
(N'Thiết bị thông minh (Smart Home)', N'Robot hút bụi laser mapping'),
(N'Thiết bị thông minh (Smart Home)', N'Khóa cửa thông minh vân tay'),
(N'Thiết bị thông minh (Smart Home)', N'Cảm biến cửa Zigbee');

/* Khoảng giá (VND) — chỉnh lại nếu DB bạn dùng đơn vị khác */
INSERT INTO #PriceRange (CategoryName, MinPrice, MaxPrice) VALUES
(N'Điện thoại',                         4990000,  35990000),
(N'Điện tử',                            890000,   45990000),
(N'Đồ chơi - phụ kiện',                 150000,   8990000),
(N'Gaming Gear',                        290000,   12990000),
(N'Laptop',                             9990000,  69990000),
(N'Màn hình & thiết bị hiển thị',       1990000,  28990000),
(N'Máy tính để bàn (PC)',               5990000,  89990000),
(N'Phụ kiện điện thoại',                49000,    2490000),
(N'Phụ kiện livestream & sáng tạo nội dung', 290000, 15990000),
(N'Thiết bị âm thanh',                  490000,   24990000),
(N'Thiết bị lưu trữ',                   190000,   18990000),
(N'Thiết bị mạng',                      390000,   12990000),
(N'Thiết bị thông minh (Smart Home)',   290000,   35990000);

/* Cập nhật: chỉ các sản phẩm có Category khớp tên trong #Templates */
UPDATE p
SET
    ProductName = x.ProductName,
    Price = CAST(
        CASE
            WHEN pr.MaxPrice <= pr.MinPrice THEN pr.MinPrice
            ELSE pr.MinPrice + ABS(CHECKSUM(NEWID())) % (pr.MaxPrice - pr.MinPrice + 1)
        END AS MONEY),
    ProductDescription = LEFT(
        N'Sản phẩm ' + c.CategoryName + N': ' + x.ProductName + N'. Bảo hành chính hãng, giao nhanh toàn quốc.',
        2000)
FROM dbo.Products AS p
INNER JOIN dbo.Categories AS c ON c.CategoryID = p.CategoryID
CROSS APPLY (
    SELECT TOP (1) t.ProductName
    FROM #Templates AS t
    WHERE RTRIM(LTRIM(t.CategoryName)) = RTRIM(LTRIM(c.CategoryName))
    ORDER BY NEWID()
) AS x
INNER JOIN #PriceRange AS pr ON RTRIM(LTRIM(pr.CategoryName)) = RTRIM(LTRIM(c.CategoryName));

DECLARE @n INT = @@ROWCOUNT;
PRINT N'Đã cập nhật ' + CAST(@n AS NVARCHAR(20)) + N' sản phẩm (tên + giá + mô tả ngắn).';

/* Kiểm tra nhanh */
SELECT c.CategoryName, COUNT(*) AS SoSanPham, MIN(p.Price) AS GiaMin, MAX(p.Price) AS GiaMax
FROM dbo.Products p
INNER JOIN dbo.Categories c ON c.CategoryID = p.CategoryID
GROUP BY c.CategoryName
ORDER BY c.CategoryName;

DROP TABLE #Templates;
DROP TABLE #PriceRange;
GO

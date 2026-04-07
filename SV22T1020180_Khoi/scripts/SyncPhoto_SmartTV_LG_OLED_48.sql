/*
  Đồng bộ Products.Photo cho mọi dòng: Smart TV LG OLED 48 inch
  → lấy ảnh từ dòng có giá 22666365 (22.666.365).

  sqlcmd -S . -d LiteCommerceDB -E -f 65001 -i "...\SyncPhoto_SmartTV_LG_OLED_48.sql"
*/

SET NOCOUNT ON;
USE LiteCommerceDB;
GO

DECLARE @ProductName NVARCHAR(255) = N'Smart TV LG OLED 48 inch';
DECLARE @RefPrice      MONEY        = 22666365;
DECLARE @Photo         NVARCHAR(255);

SELECT @Photo = NULLIF(RTRIM(LTRIM(Photo)), N'')
FROM dbo.Products
WHERE ProductName = @ProductName
  AND Price = @RefPrice;

IF @Photo IS NULL
BEGIN
    RAISERROR(N'Không tìm thấy sản phẩm tham chiếu hoặc Photo trống.', 16, 1);
    RETURN;
END;

IF @Photo LIKE N'images/products/%'
    SET @Photo = SUBSTRING(@Photo, LEN(N'images/products/') + 1, 255);
IF @Photo LIKE N'/images/products/%'
    SET @Photo = SUBSTRING(@Photo, LEN(N'/images/products/') + 1, 255);

UPDATE dbo.Products
SET Photo = @Photo
WHERE ProductName = @ProductName
  AND ISNULL(RTRIM(LTRIM(Photo)), N'') <> @Photo;

DECLARE @n INT = @@ROWCOUNT;
PRINT N'Đã cập nhật Photo cho ' + CAST(@n AS NVARCHAR(20)) + N' dòng. File: ' + @Photo;
GO

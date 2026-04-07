/*
  Đồng bộ cột Products.Photo cho mọi sản phẩm cùng tên,
  lấy ảnh từ dòng có giá khớp (mặc định: Camera an ninh 2K trong nhà / 33488089).

  App Admin dùng URL: /images/products/ + Photo  → Photo chỉ là tên file, KHÔNG gắn prefix images/products/

  Chạy:
    sqlcmd -S . -d LiteCommerceDB -E -f 65001 -i "...\SyncPhotoFromReferenceProduct.sql"
*/

SET NOCOUNT ON;
USE LiteCommerceDB;
GO

DECLARE @ProductName NVARCHAR(255) = N'Camera an ninh 2K trong nhà';
DECLARE @RefPrice      MONEY        = 33488089;
DECLARE @Photo         NVARCHAR(255);

SELECT @Photo = NULLIF(RTRIM(LTRIM(Photo)), N'')
FROM dbo.Products
WHERE ProductName = @ProductName
  AND Price = @RefPrice;

IF @Photo IS NULL
BEGIN
    RAISERROR(N'Không tìm thấy sản phẩm tham chiếu (tên + giá) hoặc Photo đang trống.', 16, 1);
    RETURN;
END;

/* Bỏ prefix thừa nếu DB cũ lưu full path */
IF @Photo LIKE N'images/products/%'
    SET @Photo = SUBSTRING(@Photo, LEN(N'images/products/') + 1, 255);
IF @Photo LIKE N'/images/products/%'
    SET @Photo = SUBSTRING(@Photo, LEN(N'/images/products/') + 1, 255);

UPDATE dbo.Products
SET Photo = @Photo
WHERE ProductName = @ProductName
  AND ISNULL(RTRIM(LTRIM(Photo)), N'') <> @Photo;

DECLARE @n INT = @@ROWCOUNT;
PRINT N'Đã cập nhật Photo cho ' + CAST(@n AS NVARCHAR(20)) + N' dòng. Giá trị: ' + @Photo;

SELECT ProductID, CAST(Price AS DECIMAL(18, 0)) AS Price, Photo, Unit
FROM dbo.Products
WHERE ProductName = @ProductName
ORDER BY Price;
GO

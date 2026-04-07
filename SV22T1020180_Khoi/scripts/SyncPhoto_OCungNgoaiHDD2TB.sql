/*
  Đồng bộ Photo: Ổ cứng ngoài HDD 2TB — tham chiếu giá 4946209 (4.946.209).

  sqlcmd -S . -d LiteCommerceDB -E -f 65001 -i "...\SyncPhoto_OCungNgoaiHDD2TB.sql"
*/

SET NOCOUNT ON;
USE LiteCommerceDB;
GO

DECLARE @ProductName NVARCHAR(255) = N'Ổ cứng ngoài HDD 2TB';
DECLARE @RefPrice      MONEY        = 4946209;
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

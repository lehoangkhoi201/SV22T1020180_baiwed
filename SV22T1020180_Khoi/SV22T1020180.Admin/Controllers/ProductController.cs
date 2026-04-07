using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SV22T1020180.Admin;
using SV22T1020180.Models.Common;
using SV22T1020180.Models.Catalog;
using SV22T1020180.BusinessLayers;

namespace SV22T1020180.Admin.Controllers
{
    [Authorize]
    public class ProductController : Controller
    {
        private const int PAGE_SIZE = 12;
        private const string PRODUCT_SEARCH_CONDITION = "ProductSearchCondition";

        private readonly IWebHostEnvironment _env;
        private readonly IConfiguration _configuration;

        public ProductController(IWebHostEnvironment env, IConfiguration configuration)
        {
            _env = env;
            _configuration = configuration;
        }

        private async Task<string?> SaveUploadedPhotoAsync(IFormFile? file, string subfolder)
        {
            if (file == null || file.Length == 0)
                return null;

            if (subfolder != "products")
                subfolder = "products";

            string folder = Path.Combine(MediaStoragePaths.ResolveRoot(_env, _configuration), subfolder);
            if (!Directory.Exists(folder))
                Directory.CreateDirectory(folder);

            string fileName = $"{DateTime.Now:yyyyMMddHHmmssfff}_{Guid.NewGuid():N}{Path.GetExtension(file.FileName)}";
            string filePath = Path.Combine(folder, fileName);

            using (var stream = new FileStream(filePath, FileMode.Create))
            {
                await file.CopyToAsync(stream);
            }

            return fileName;
        }

        [Authorize(Roles = AppRoles.AllStaff)]
        public async Task<IActionResult> Index()
        {
            var input = ApplicationContext.GetSessionData<ProductSearchInput>(PRODUCT_SEARCH_CONDITION);
            if (input == null)
            {
                input = new ProductSearchInput()
                {
                    Page = 1,
                    PageSize = PAGE_SIZE,
                    SearchValue = "",
                    CategoryID = 0,
                    SupplierID = 0,
                    MinPrice = 0,
                    MaxPrice = 0
                };
            }
            ViewBag.Categories = await CatalogDataService.ListCategoriesAsync(new PaginationSearchInput { Page = 1, PageSize = 1000 });
            ViewBag.Suppliers = await PartnerDataService.ListSuppliersAsync(new PaginationSearchInput { Page = 1, PageSize = 1000 });
            return View(input);
        }

        [Authorize(Roles = AppRoles.AllStaff)]
        public async Task<IActionResult> Search(ProductSearchInput input)
        {
            input.PageSize = PAGE_SIZE;
            ApplicationContext.SetSessionData(PRODUCT_SEARCH_CONDITION, input);
            var data = await CatalogDataService.ListProductsAsync(input);
            return PartialView(data);
        }

        [Authorize(Roles = AppRoles.AllStaff)]
        [HttpGet]
        public async Task<IActionResult> Detail(int id)
        {
            var product = await CatalogDataService.GetProductAsync(id);
            if (product == null)
                return RedirectToAction("Index");
            ViewBag.Photos = await CatalogDataService.ListPhotosAsync(id);
            ViewBag.Attributes = await CatalogDataService.ListAttributesAsync(id);
            return View(product);
        }

        [Authorize(Roles = AppRoles.AdminManager)]
        [HttpGet]
        public async Task<IActionResult> Create()
        {
            ViewBag.Categories = await CatalogDataService.ListCategoriesAsync(new PaginationSearchInput { Page = 1, PageSize = 1000 });
            ViewBag.Suppliers = await PartnerDataService.ListSuppliersAsync(new PaginationSearchInput { Page = 1, PageSize = 1000 });

            var product = new Product { IsSelling = true };
            return View("Edit", product);
        }

        [Authorize(Roles = AppRoles.AdminManager)]
        [HttpPost]
        public async Task<IActionResult> Create(Product data, IFormFile? uploadPhoto)
        {
            if (uploadPhoto != null)
            {
                string? fileName = await SaveUploadedPhotoAsync(uploadPhoto, "products");
                if (fileName != null)
                    data.Photo = fileName;
            }

            int productId = await CatalogDataService.AddProductAsync(data);
            if (productId > 0)
                return RedirectToAction("Edit", new { id = productId });

            return RedirectToAction("Index");
        }

        [Authorize(Roles = AppRoles.AdminManager)]
        [HttpGet]
        public async Task<IActionResult> Edit(int id)
        {
            var product = await CatalogDataService.GetProductAsync(id);
            if (product == null)
                return RedirectToAction("Index");

            ViewBag.ProductID = id;
            ViewBag.Categories = await CatalogDataService.ListCategoriesAsync(new PaginationSearchInput { Page = 1, PageSize = 1000 });
            ViewBag.Suppliers = await PartnerDataService.ListSuppliersAsync(new PaginationSearchInput { Page = 1, PageSize = 1000 });
            ViewBag.Photos = await CatalogDataService.ListPhotosAsync(id);
            ViewBag.Attributes = await CatalogDataService.ListAttributesAsync(id);

            return View(product);
        }

        [Authorize(Roles = AppRoles.AdminManager)]
        [HttpPost]
        public async Task<IActionResult> Edit(Product data, IFormFile? uploadPhoto)
        {
            if (uploadPhoto != null)
            {
                string? fileName = await SaveUploadedPhotoAsync(uploadPhoto, "products");
                if (fileName != null)
                    data.Photo = fileName;
            }
            else
            {
                var existing = await CatalogDataService.GetProductAsync(data.ProductID);
                if (existing != null)
                    data.Photo = existing.Photo;
            }

            await CatalogDataService.UpdateProductAsync(data);
            return RedirectToAction("Edit", new { id = data.ProductID });
        }

        [Authorize(Roles = AppRoles.AdminManager)]
        [HttpGet]
        public async Task<IActionResult> Delete(int id)
        {
            var product = await CatalogDataService.GetProductAsync(id);
            if (product == null)
                return RedirectToAction("Index");

            ViewBag.IsUsed = await CatalogDataService.IsUsedProductAsync(id);
            return View(product);
        }

        [Authorize(Roles = AppRoles.AdminManager)]
        [HttpPost]
        public async Task<IActionResult> Delete(int id, string confirm)
        {
            if (!string.IsNullOrEmpty(confirm))
                await CatalogDataService.DeleteProductAsync(id);
            return RedirectToAction("Index");
        }

        // Attributes
        [Authorize(Roles = AppRoles.AdminManager)]
        [HttpGet]
        public async Task<IActionResult> ListAttributes(int id)
        {
            var attributes = await CatalogDataService.ListAttributesAsync(id);
            ViewBag.ProductID = id;
            return View(attributes);
        }

        [Authorize(Roles = AppRoles.AdminManager)]
        [HttpGet]
        public IActionResult CreateAttribute(int id)
        {
            if (id <= 0)
                return RedirectToAction("Index");

            var attr = new ProductAttribute { ProductID = id, DisplayOrder = 1 };
            ViewBag.ProductID = id;
            return View("EditAttribute", attr);
        }

        [Authorize(Roles = AppRoles.AdminManager)]
        [HttpPost]
        public async Task<IActionResult> CreateAttribute(ProductAttribute data)
        {
            if (data.ProductID <= 0)
                return RedirectToAction("Index");

            await CatalogDataService.AddAttributeAsync(data);
            return RedirectToAction("Edit", new { id = data.ProductID });
        }

        [Authorize(Roles = AppRoles.AdminManager)]
        [HttpGet]
        public async Task<IActionResult> EditAttribute(int id, long attributeId)
        {
            var attr = await CatalogDataService.GetAttributeAsync(attributeId);
            if (attr == null)
                return RedirectToAction("Edit", new { id });
            ViewBag.ProductID = id;
            return View(attr);
        }

        [Authorize(Roles = AppRoles.AdminManager)]
        [HttpPost]
        public async Task<IActionResult> EditAttribute(ProductAttribute data)
        {
            await CatalogDataService.UpdateAttributeAsync(data);
            return RedirectToAction("Edit", new { id = data.ProductID });
        }

        [Authorize(Roles = AppRoles.AdminManager)]
        [HttpGet]
        public async Task<IActionResult> DeleteAttribute(int id, long attributeId)
        {
            var attr = await CatalogDataService.GetAttributeAsync(attributeId);
            if (attr == null)
                return RedirectToAction("Edit", new { id });
            ViewBag.ProductID = id;
            return View(attr);
        }

        [Authorize(Roles = AppRoles.AdminManager)]
        [HttpPost]
        public async Task<IActionResult> DeleteAttribute(int id, long attributeId, string confirm)
        {
            if (!string.IsNullOrEmpty(confirm))
                await CatalogDataService.DeleteAttributeAsync(attributeId);
            return RedirectToAction("Edit", new { id });
        }

        // Photos
        [Authorize(Roles = AppRoles.AdminManager)]
        [HttpGet]
        public async Task<IActionResult> ListPhotos(int id)
        {
            var photos = await CatalogDataService.ListPhotosAsync(id);
            ViewBag.ProductID = id;
            return View(photos);
        }

        [Authorize(Roles = AppRoles.AdminManager)]
        [HttpGet]
        public IActionResult CreatePhoto(int id)
        {
            if (id <= 0)
                return RedirectToAction("Index");

            var photo = new ProductPhoto { ProductID = id, DisplayOrder = 1 };
            ViewBag.ProductID = id;
            return View("EditPhoto", photo);
        }

        [Authorize(Roles = AppRoles.AdminManager)]
        [HttpPost]
        public async Task<IActionResult> CreatePhoto(int id, IFormFile? Photo, string? Description, int DisplayOrder, bool IsHidden)
        {
            if (id <= 0)
                return RedirectToAction("Index");

            string? fileName = await SaveUploadedPhotoAsync(Photo, "products");

            var data = new ProductPhoto
            {
                ProductID = id,
                Photo = fileName ?? "",
                Description = Description ?? "",
                DisplayOrder = DisplayOrder,
                IsHidden = IsHidden
            };

            await CatalogDataService.AddPhotoAsync(data);
            return RedirectToAction("Edit", new { id });
        }

        [Authorize(Roles = AppRoles.AdminManager)]
        [HttpGet]
        public async Task<IActionResult> EditPhoto(int id, long photoId)
        {
            var photo = await CatalogDataService.GetPhotoAsync(photoId);
            if (photo == null)
                return RedirectToAction("Edit", new { id });
            ViewBag.ProductID = id;
            return View(photo);
        }

        [Authorize(Roles = AppRoles.AdminManager)]
        [HttpPost]
        public async Task<IActionResult> EditPhoto(int id, long photoId, IFormFile? Photo, string? Description, int DisplayOrder, bool IsHidden)
        {
            var existing = await CatalogDataService.GetPhotoAsync(photoId);
            if (existing == null)
                return RedirectToAction("Edit", new { id });

            string? fileName = await SaveUploadedPhotoAsync(Photo, "products");

            existing.Photo = fileName ?? existing.Photo;
            existing.Description = Description ?? "";
            existing.DisplayOrder = DisplayOrder;
            existing.IsHidden = IsHidden;

            await CatalogDataService.UpdatePhotoAsync(existing);
            return RedirectToAction("Edit", new { id });
        }

        [Authorize(Roles = AppRoles.AdminManager)]
        [HttpGet]
        public async Task<IActionResult> DeletePhoto(int id, long photoId)
        {
            var photo = await CatalogDataService.GetPhotoAsync(photoId);
            if (photo == null)
                return RedirectToAction("Edit", new { id });
            ViewBag.ProductID = id;
            return View(photo);
        }

        [Authorize(Roles = AppRoles.AdminManager)]
        [HttpPost]
        public async Task<IActionResult> DeletePhoto(int id, long photoId, string confirm)
        {
            if (!string.IsNullOrEmpty(confirm))
                await CatalogDataService.DeletePhotoAsync(photoId);
            return RedirectToAction("Edit", new { id });
        }

    }
}

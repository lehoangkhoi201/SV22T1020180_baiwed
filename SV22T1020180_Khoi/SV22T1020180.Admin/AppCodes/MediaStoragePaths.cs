namespace SV22T1020180.Admin
{
    /// <summary>
    /// Thư mục lưu ảnh chung (sản phẩm, nhân viên) — cùng cấp solution, đường dẫn tương đối trong appsettings.
    /// </summary>
    public static class MediaStoragePaths
    {
        public static string ResolveRoot(IWebHostEnvironment env, IConfiguration config)
        {
            var configured = config["MediaStorage:Root"];
            if (string.IsNullOrWhiteSpace(configured))
                configured = Path.Combine("..", "MediaStorage");
            var full = Path.GetFullPath(Path.Combine(env.ContentRootPath, configured));
            Directory.CreateDirectory(Path.Combine(full, "products"));
            Directory.CreateDirectory(Path.Combine(full, "employees"));
            return full;
        }

        public static string ProductsPath(IWebHostEnvironment env, IConfiguration config) =>
            Path.Combine(ResolveRoot(env, config), "products");

        public static string EmployeesPath(IWebHostEnvironment env, IConfiguration config) =>
            Path.Combine(ResolveRoot(env, config), "employees");
    }
}

namespace SV22T1020180.BusinessLayers
{
    /// <summary>
    /// Giữ API cũ; logic thực tế ở PasswordHasher.
    /// </summary>
    public static class CryptHelper
    {
        public static string HashMD5(string input) => PasswordHasher.HashMd5(input);
    }
}

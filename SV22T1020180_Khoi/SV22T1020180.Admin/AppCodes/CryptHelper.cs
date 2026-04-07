namespace SV22T1020180.Admin;

public static class CryptHelper
{
    public static string HashMD5(string input) => BusinessLayers.PasswordHasher.HashMd5(input);
}

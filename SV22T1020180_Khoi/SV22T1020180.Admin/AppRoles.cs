namespace SV22T1020180.Admin;

public static class AppRoles
{
    public const string Admin = "admin";
    public const string Manager = "manager";
    public const string Sale = "sale";

    public const string AdminManager = Admin + "," + Manager;

    public const string AllStaff = Admin + "," + Manager + "," + Sale;
}

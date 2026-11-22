// LAB.exe - mở IKEMEN GO ở chế độ phòng luyện tập của dự án (cờ -lab).
// Logic LAB nằm ở external/mods/lab.lua. File này chỉ là trình khởi chạy.
// Biên dịch lại: chạy tools/lab/build.ps1
using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

static class Lab
{
    [STAThread]
    static void Main(string[] args)
    {
        string dir = AppDomain.CurrentDomain.BaseDirectory;
        string exe = Path.Combine(dir, "Ikemen_GO.exe");
        string mod = Path.Combine(dir, "external", "mods", "lab.lua");
        if (!File.Exists(exe))
        {
            MessageBox.Show("Không tìm thấy Ikemen_GO.exe.\nĐặt LAB.exe trong thư mục gốc của game.",
                "LAB", MessageBoxButtons.OK, MessageBoxIcon.Error);
            return;
        }
        if (!File.Exists(mod))
        {
            MessageBox.Show("Thiếu file external/mods/lab.lua.", "LAB",
                MessageBoxButtons.OK, MessageBoxIcon.Error);
            return;
        }
        // Tham số thêm (nếu có) được chuyển tiếp, ví dụ: LAB.exe -windowed
        string extra = "";
        foreach (string a in args)
        {
            extra += " \"" + a.Replace("\"", "") + "\"";
        }
        var psi = new ProcessStartInfo(exe, "-lab" + extra);
        psi.WorkingDirectory = dir;
        psi.UseShellExecute = false;
        Process.Start(psi);
    }
}

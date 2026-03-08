Add-Type @"
  using System;
  using System.Runtime.InteropServices;
  public class User32 {
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")]
    public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder text, int count);
  }
"@
$hwnd = [User32]::GetForegroundWindow()
$sb = [System.Text.StringBuilder]::new(256)
[User32]::GetWindowText($hwnd, $sb, 256) | Out-Null
$sb.ToString()

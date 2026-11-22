# Biên dịch LAB.exe ra thư mục gốc dự án bằng trình biên dịch C# có sẵn trong Windows (.NET Framework 4).
$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$csc = Join-Path $env:WINDIR "Microsoft.NET\Framework64\v4.0.30319\csc.exe"
& $csc /nologo /target:winexe /codepage:65001 /out:"$root\LAB.exe" /r:System.Windows.Forms.dll "$PSScriptRoot\LAB.cs"

# Daily maintenance gate for the SecondBrain LLM Wiki.
# Runs the read-only + build checks and appends a timestamped report to maintenance.log.
# Registered as the "SecondBrain Maintenance" Windows scheduled task.

$ErrorActionPreference = "Continue"
Set-Location -Path $PSScriptRoot\..

$logFile = "maintenance.log"
$ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

"===== $ts =====" | Out-File -FilePath $logFile -Append -Encoding utf8

python scripts/wiki_tool.py doctor        *>&1 | Out-File -FilePath $logFile -Append -Encoding utf8
python scripts/wiki_tool.py build         *>&1 | Out-File -FilePath $logFile -Append -Encoding utf8
python scripts/wiki_tool.py lint          *>&1 | Out-File -FilePath $logFile -Append -Encoding utf8
python scripts/wiki_tool.py source-lint   *>&1 | Out-File -FilePath $logFile -Append -Encoding utf8
python scripts/audit_public.py            *>&1 | Out-File -FilePath $logFile -Append -Encoding utf8

"" | Out-File -FilePath $logFile -Append -Encoding utf8

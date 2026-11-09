param(
    [int]$Port = 8501
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$activateScript = Join-Path $projectRoot ".venv\Scripts\Activate.ps1"

if (-not (Test-Path -LiteralPath $activateScript)) {
    throw "Nie znaleziono .venv. Utwórz środowisko zgodnie z instrukcją projektu."
}

Push-Location $projectRoot
try {
    . $activateScript
    python -m streamlit run main.py --server.address 127.0.0.1 --server.port $Port
}
finally {
    Pop-Location
}

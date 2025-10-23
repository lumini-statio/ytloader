# Script para instalar Python 3.11 y instalar dependencias
Write-Host "=== Instalador de Python 3.11 y dependencias ===" -ForegroundColor Green

# Verificar si ya está instalado Python 3.11
$pythonInstalled = $false
$pythonPath = ""

# Buscar Python 3.11 en las rutas comunes
$possiblePaths = @(
    "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
    "$env:APPDATA\Python\Python311\python.exe",
    "C:\Python311\python.exe",
    "$env:ProgramFiles\Python311\python.exe"
)

foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $pythonInstalled = $true
        $pythonPath = $path
        Write-Host "Python 3.11 encontrado en: $path" -ForegroundColor Yellow
        break
    }
}

# Si no está instalado, descargar e instalar
if (-not $pythonInstalled) {
    Write-Host "Python 3.11 no encontrado. Descargando e instalando..." -ForegroundColor Yellow
    
    # URL de descarga de Python 3.11
    $pythonUrl = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
    $installerPath = "$env:TEMP\python-3.11-installer.exe"
    
    try {
        # Descargar el instalador
        Write-Host "Descargando Python 3.11..." -ForegroundColor Cyan
        Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath
        
        # Instalar Python silenciosamente
        Write-Host "Instalando Python 3.11..." -ForegroundColor Cyan
        $process = Start-Process -FilePath $installerPath -ArgumentList @(
            "/quiet",
            "InstallAllUsers=1",
            "PrependPath=1",
            "Include_test=0",
            "Include_launcher=1",
            "Include_pip=1",
            "Include_tcltk=1"
        ) -Wait -PassThru
        
        if ($process.ExitCode -eq 0) {
            Write-Host "Python 3.11 instalado exitosamente" -ForegroundColor Green
            
            # Actualizar la ruta de Python
            $pythonPath = "$env:ProgramFiles\Python311\python.exe"
            
            # Actualizar la variable de entorno PATH para la sesión actual
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
        } else {
            Write-Host "Error en la instalación de Python. Código de salida: $($process.ExitCode)" -ForegroundColor Red
            exit 1
        }
    }
    catch {
        Write-Host "Error al descargar o instalar Python: $($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
    finally {
        # Limpiar archivo temporal
        if (Test-Path $installerPath) {
            Remove-Item $installerPath -Force -ErrorAction SilentlyContinue
        }
    }
}

# Verificar que requirements.txt existe
if (-not (Test-Path "requirements.txt")) {
    Write-Host "ERROR: No se encontró el archivo requirements.txt" -ForegroundColor Red
    Write-Host "Asegúrate de que el archivo requirements.txt esté en el mismo directorio que este script." -ForegroundColor Yellow
    exit 1
}

Write-Host "Instalando dependencias desde requirements.txt..." -ForegroundColor Cyan
try {
    # Crear entorno virtual
    & $pythonPath -m venv venv
    
    # Ruta al pip del entorno virtual
    $venvPython = ".\venv\Scripts\python.exe"
    $venvPip = ".\venv\Scripts\pip.exe"
    
    # Verificar que se creó el entorno virtual
    if (-not (Test-Path $venvPython)) {
        Write-Host "Error: No se pudo crear el entorno virtual" -ForegroundColor Red
        exit 1
    }
    
    # Actualizar pip e instalar dependencias usando el entorno virtual
    & $venvPython -m pip install --upgrade pip
    & $venvPython -m pip install -r requirements.txt
    
    Write-Host "Dependencias instaladas exitosamente en el entorno virtual" -ForegroundColor Green
    Write-Host "Para activar el entorno virtual ejecuta: .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
}
catch {
    Write-Host "Error al instalar dependencias: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "=== Proceso completado ===" -ForegroundColor Green
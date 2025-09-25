# process_manager.ps1
# Script PowerShell para gerenciamento de processos do Windows

function Get-RunningProcesses {
    param (
        [string]$Name = "*"
    )
    try {
        Get-Process -Name $Name | Select-Object Name, Id, CPU, WorkingSet, StartTime
    }
    catch {
        Write-Host "Erro ao listar processos: $($_.Exception.Message)"
        return $null
    }
}

function Find-ProcessByName {
    param (
        [Parameter(Mandatory=$true)][string]$ProcessName
    )
    try {
        Get-Process -Name "*$ProcessName*" | Select-Object Name, Id, CPU, WorkingSet, StartTime
    }
    catch {
        Write-Host "Erro ao encontrar processo '$ProcessName': $($_.Exception.Message)"
        return $null
    }
}

function Start-NewProcess {
    param (
        [Parameter(Mandatory=$true)][string]$ExecutablePath,
        [string]$Arguments = ""
    )
    try {
        $process = Start-Process -FilePath $ExecutablePath -ArgumentList $Arguments -PassThru
        Write-Host "Processo '$ExecutablePath' iniciado com PID: $($process.Id)"
        return $process.Id
    }
    catch {
        Write-Host "Erro ao iniciar processo '$ExecutablePath': $($_.Exception.Message)"
        return $null
    }
}

function Stop-SystemProcess {
    param (
        [Parameter(Mandatory=$true)][int]$ProcessId
    )
    try {
        Stop-Process -Id $ProcessId -Force -Confirm:$false
        Write-Host "Processo com PID $ProcessId terminado."
        return $true
    }
    catch {
        Write-Host "Erro ao terminar processo com PID $ProcessId: $($_.Exception.Message)"
        return $false
    }
}

# --- Exemplos de Uso ---
if ($MyInvocation.MyCommand.Name -eq (Get-Item $MyInvocation.MyCommand.Path).Name) {
    Write-Host "`n--- Listando alguns processos ---"
    Get-RunningProcesses -Name "explorer"

    Write-Host "`n--- Encontrando processos por nome (ex: 'chrome') ---"
    Find-ProcessByName -ProcessName "chrome"

    # Exemplo de iniciar e parar um processo (descomente para testar em Windows)
    # Write-Host "`n--- Iniciando e parando um processo (ex: notepad.exe) ---"
    # $notepadPid = Start-NewProcess -ExecutablePath "notepad.exe"
    # if ($notepadPid) {
    #     Start-Sleep -Seconds 2
    #     Stop-SystemProcess -ProcessId $notepadPid
    # }
}

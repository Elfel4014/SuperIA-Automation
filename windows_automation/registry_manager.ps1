# registry_manager.ps1
# Script PowerShell para manipulação do Registro do Windows

function New-RegistryKey {
    param (
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)][string]$Name
    )
    try {
        New-Item -Path $Path -Name $Name -Force | Out-Null
        Write-Host "Chave '$Name' criada com sucesso em '$Path'."
        return $true
    }
    catch {
        Write-Host "Erro ao criar chave '$Name' em '$Path': $($_.Exception.Message)"
        return $false
    }
}

function Set-RegistryValue {
    param (
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)][string]$Name,
        [Parameter(Mandatory=$true)]$Value,
        [string]$PropertyType = "String" # Pode ser String, DWord, QWord, Binary, MultiString, ExpandString
    )
    try {
        Set-ItemProperty -Path $Path -Name $Name -Value $Value -PropertyType $PropertyType -Force | Out-Null
        Write-Host "Valor '$Name' definido com sucesso em '$Path'."
        return $true
    }
    catch {
        Write-Host "Erro ao definir valor '$Name' em '$Path': $($_.Exception.Message)"
        return $false
    }
}

function Get-RegistryValue {
    param (
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)][string]$Name
    )
    try {
        $value = Get-ItemProperty -Path $Path -Name $Name | Select-Object -ExpandProperty $Name
        Write-Host "Valor '$Name' lido de '$Path': $value"
        return $value
    }
    catch {
        Write-Host "Erro ao ler valor '$Name' de '$Path': $($_.Exception.Message)"
        return $null
    }
}

function Remove-RegistryValue {
    param (
        [Parameter(Mandatory=$true)][string]$Path,
        [Parameter(Mandatory=$true)][string]$Name
    )
    try {
        Remove-ItemProperty -Path $Path -Name $Name -Force | Out-Null
        Write-Host "Valor '$Name' excluído com sucesso de '$Path'."
        return $true
    }
    catch {
        Write-Host "Erro ao excluir valor '$Name' de '$Path': $($_.Exception.Message)"
        return $false
    }
}

function Remove-RegistryKey {
    param (
        [Parameter(Mandatory=$true)][string]$Path
    )
    try {
        Remove-Item -Path $Path -Recurse -Force | Out-Null
        Write-Host "Chave '$Path' excluída com sucesso."
        return $true
    }
    catch {
        Write-Host "Erro ao excluir chave '$Path': $($_.Exception.Message)"
        return $false
    }
}

# --- Exemplos de Uso ---
if ($MyInvocation.MyCommand.Name -eq (Get-Item $MyInvocation.MyCommand.Path).Name) {
    $testPath = "HKCU:\Software\SuperIA_Test_PS"

    Write-Host "`n--- Testando criação de chave e valores ---"
    New-RegistryKey -Path "HKCU:\Software" -Name "SuperIA_Test_PS"
    Set-RegistryValue -Path $testPath -Name "TestStringPS" -Value "Hello SuperIA PowerShell"
    Set-RegistryValue -Path $testPath -Name "TestDwordPS" -Value 54321 -PropertyType "DWord"

    Write-Host "`n--- Testando leitura de valores ---"
    $string_value_ps = Get-RegistryValue -Path $testPath -Name "TestStringPS"
    $dword_value_ps = Get-RegistryValue -Path $testPath -Name "TestDwordPS"
    $non_existent_value_ps = Get-RegistryValue -Path $testPath -Name "NonExistentPS"

    Write-Host "`n--- Testando exclusão de valores ---"
    Remove-RegistryValue -Path $testPath -Name "TestStringPS"
    Remove-RegistryValue -Path $testPath -Name "TestDwordPS"

    Write-Host "`n--- Testando exclusão de chave ---"
    Remove-RegistryKey -Path $testPath
    Remove-RegistryKey -Path "HKCU:\Software\NonExistentKeyPS"
}

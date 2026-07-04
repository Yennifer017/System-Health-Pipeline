param (
    [string]$InputFile = "./output/raw_metrics.csv",
    [string]$OutputFile = "./output/analysis.json"
)

if (!(Test-Path $InputFile)) {
    Write-Error "Input file not found: $InputFile"
    exit 1
}

$data = Import-Csv $InputFile
$data = $data | Where-Object { $_.CPU -ne $null -and $_.CPU -ne "" }

function Get-Status {
    param (
        [int]$Value,
        [int]$WarningThreshold,
        [int]$CriticalThreshold,
        [switch]$LowerIsCritical
    )

    if ($LowerIsCritical) {
        if ($Value -le $CriticalThreshold) {
            return "CRITICAL"
        }

        if ($Value -le $WarningThreshold) {
            return "WARNING"
        }
    }
    else {
        if ($Value -ge $CriticalThreshold) {
            return "CRITICAL"
        }

        if ($Value -ge $WarningThreshold) {
            return "WARNING"
        }
    }

    return "INFO"
}

function Convert-Metric {
    param (
        $row
    )
    $cpu  = [int]$Row.CPU
    $disk = [int]$Row.Disk
    $ram  = [int]$Row.RAM

    $cpuStatus = Get-Status -Value $cpu -WarningThreshold 70 -CriticalThreshold 90
    $diskStatus = Get-Status -Value $disk -WarningThreshold 70 -CriticalThreshold 90
    $ramStatus = Get-Status -Value $ram -WarningThreshold 1500 -CriticalThreshold 500 -LowerIsCritical

    return [PSCustomObject]@{
        timestamp   = $Row.Timestamp
        cpu         = $cpu
        disk        = $disk
        ram         = $ram
        cpu_status  = $cpuStatus
        disk_status = $diskStatus
        ram_status  = $ramStatus
    }
}


$result = foreach ($row in $data) {
    Convert-Metric -Row $row
}
$result | ConvertTo-Json -Depth 10 | Out-File -Encoding UTF8 $OutputFile

Write-Host "Analysis completed!"
Write-Host "Output written to: $OutputFile"
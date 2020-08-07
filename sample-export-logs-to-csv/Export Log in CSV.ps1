$pathToOutputFile = "logs.csv"
$postParams = @{Authorization='Your_token'}
#GET Logs
$logs = (Invoke-WebRequest -Uri https://sds.stormshieldcs.eu/api/v1/logs -Method GET -Headers $postParams | ConvertFrom-Json )

ForEach($log in $logs) {
    $manage_right = ""
    $access_right = ""
    
    $log | Select-Object -ExpandProperty  "manage_right"
    
    # Support manage_right entity
    ForEach($email in $log.manage_right) { 
        $manage_right += $email.email + ','
    }
    # Support access_right entity
    ForEach($email in $log.access_right) { 
        $access_right += $email.email + ','
    }
    # Overwrite value in log
    $log.manage_right = $manage_right
    $log.access_right = $access_right
    
}

$logs | Export-Csv $pathToOutputFile -Delimiter (59) -NoTypeInformation

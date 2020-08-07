$pathToOutputFile = "users.csv"
$postParams = @{Authorization='Your_token'}
#GET Users
$Users = (Invoke-WebRequest -Uri https://sds.stormshieldcs.eu/api/v1/users -Method GET -Headers $postParams | ConvertFrom-Json )

ForEach($User in $Users) {
    $roles = ""
       
    $User | Select-Object -ExpandProperty  "roles"
    
    # Support roles entity
    ForEach($role in $User.roles) { 
        $roles += $role + ','
    }
    
    # Overwrite value in User
    $User.roles = $roles
    
}

$Users | Export-Csv $pathToOutputFile -Delimiter (59) -NoTypeInformation

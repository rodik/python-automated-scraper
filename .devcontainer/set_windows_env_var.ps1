
# Set ENV var on developer machine - don't run this in the container!

############################################
# Windows - Run as ADMINISTRATOR!
############################################

# prepare secrets json:
Set-Variable -Name "CREDENTIALS_JSON" -Value '
# paste credentials.json content here
'

# set Environment variable on local machine
[System.Environment]::SetEnvironmentVariable('GDRIVE_API_CREDENTIALS', $CREDENTIALS_JSON, [System.EnvironmentVariableTarget]::User)

# check
$env:GDRIVE_API_CREDENTIALS

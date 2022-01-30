##########################
# Set Github repo secret
##########################

# prepare secrets json
CREDENTIALS_JSON=$(cat << EOF 
# paste credentials.json content here
EOF
)

# check string
echo $CREDENTIALS_JSON

# set secret on Github 
gh auth login
gh secret set GDRIVE_API_CREDENTIALS --body "$CREDENTIALS_JSON"




##########################
# Set ENV var on developer machine
##########################

### Windows - run PowerShell ISE as admin:

# # paste json here and run commands:
# Set-Variable -Name "CREDENTIALS_JSON" -Value '
# # paste credentials.json content here
# '

# # set
# [System.Environment]::SetEnvironmentVariable('GDRIVE_API_CREDENTIALS', $CREDENTIALS_JSON)

# # check
# $env:GDRIVE_API_CREDENTIALS

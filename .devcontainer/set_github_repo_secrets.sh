
# Set ENV var on developer machine - don't run this in the container!

############################################
# Windows - run PowerShell ISE as admin:
############################################

# prepare secrets json:
Set-Variable -Name "CREDENTIALS_JSON" -Value '
# paste credentials.json content here
'

# set Environment variable on local machine
[System.Environment]::SetEnvironmentVariable('GDRIVE_API_CREDENTIALS', $CREDENTIALS_JSON, [System.EnvironmentVariableTarget]::User)

# check
$env:GDRIVE_API_CREDENTIALS


############################
# Ubuntu - open (local machine) terminal:
############################

# 1. prepare secrets json
CREDENTIALS_JSON=$(cat << EOF 
# paste credentials.json content here
EOF
)

# 2. set Environment variable on local machine
export GDRIVE_API_CREDENTIALS=$CREDENTIALS_JSON

# 3. check
echo $GDRIVE_API_CREDENTIALS



# (optional) Set Github repo secret using gh cli
# this replaces step 7 from Readme instructions

# 1. prepare secrets json
CREDENTIALS_JSON=$(cat << EOF 
# paste credentials.json content here
EOF
)

# 2. check string
echo $CREDENTIALS_JSON

# 3. (optional) set secret on Github repo - requires 'gh cli'
gh auth login
gh secret set GDRIVE_API_CREDENTIALS --body "$CREDENTIALS_JSON"



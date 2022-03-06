
# (optional) Set Github repo secret using gh cli
# this replaces step 8 from Readme instructions

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




# Set ENV var on developer machine - don't run this in the container!

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


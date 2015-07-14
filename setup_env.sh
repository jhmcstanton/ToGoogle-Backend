ENV_NAME="togoogleenv"
python3 -m venv $ENV_NAME
source "$ENV_NAME/bin/activate"
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
echo "Your ToGoogle python3 environment is now configured."
echo "To activate this environment, from the root of the project, use the command 'source $ENV_NAME/bin/activate'"
echo "To deactivate this environment simply type 'deactivate' in your favorite terminal."

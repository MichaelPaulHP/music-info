

# DEV
## build
- poetry build

## Firebase functions
### generate requirements 
- poetry export -f requirements.txt --output requirements.txt --without-hashes --without-dev
- copy requirements.txt to functions folder
### Install packages from requirements.txt 
- cd functions/venv/Scripts/
- activate
- pip install -r requirements.txt
### deploy 
- firebase deploy --only functions
echo [$(date)]: "START"
echo [$(date)]:"Creating env with python 3.8"
conda create --prefix ./e nv python=3.8 -y 
echo [$(date)]:"Activatig env"
source  activate ./env
echo [$(date)]:"Installing dev requirements"
pip install -r requirements.txt
echo [$(date)]:"END"./
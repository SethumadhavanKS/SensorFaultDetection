import os
from pathlib import Path
packageName = 'sensor'

lstOFFiles = [
    "github/workflows/.gitkeep",
    f"src/{packageName}/__init__.py",
    f"src/{packageName}/components/__init__.py",
    f"src/{packageName}/components/data_ingestion.py",
    f"src/{packageName}/components/data_transformation.py",
    f"src/{packageName}/components/data_validation.py",
    f"src/{packageName}/components/model_evaluation.py",
    f"src/{packageName}/components/model_pusher.py",
    f"src/{packageName}/components/model_trainer.py",
    f"src/{packageName}/entity/__init__.py",
    f"src/{packageName}/entity/artifact_entity.py",
    f"src/{packageName}/entity/config_entity.py",
    f"src/{packageName}/pipeline/__init__.py",
    f"src/{packageName}/pipeline/training_pipeline.py",
    f"src/{packageName}/pipeline/prediction_pipeline.py",
    f"src/{packageName}/logger.py",
    f"src/{packageName}/exception.py",
    f"src/{packageName}/config.py",
    f"src/{packageName}/utils/__init__.py",
    f"src/{packageName}/utils/utils.py",
    f"src/{packageName}/model_resolver.py",
    "notebooks/research.ipynb",
    "notebooks/data/.gitkeep",
    "requirements.txt",
    "setup.py",
    "init_setup.sh",
    "test.py",
    "data_dump.py",
    "main.py",
    ".env"
]

#Creating directory
for filePath in lstOFFiles:
    filePath = Path(filePath)
    fileDir,fileName = os.path.split(filePath)

    if fileDir != "":
        os.makedirs(fileDir, exist_ok=True)
        
    #Creating file
    if(not os.path.exists(filePath)) or (os.path.getsize(filePath)==0):
        with open(filePath, "w") as f:
            pass
    else:
        print("File already exists")


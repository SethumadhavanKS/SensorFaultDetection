from setuptools import find_packages, setup
from typing import List

REQUIREMENT_FILE_NAME = "requirements.txt"
HYPHEN_E_DOT = "-e ."

def getRequirements() -> List[str]:

    with open(REQUIREMENT_FILE_NAME) as reqFile:
        reqList = reqFile.readlines()
        reqList = [reqNm.replace("\n","") for reqNm in reqList]

    if (HYPHEN_E_DOT in reqList):
        reqList.remove(HYPHEN_E_DOT)
    return reqList

setup(
    name = "sensor",
    version = "1.0.0",
    author= "Sethumadhavan",
    author_email= "zethumadhavansethu@gmail.com",
    packages= find_packages(),
    install_requires= getRequirements()
)
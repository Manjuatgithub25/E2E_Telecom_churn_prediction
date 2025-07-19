from setuptools import find_packages, setup


HYPEN_E_DOT='-e .'
def get_requirements(file_path:str):                # returns list of requirements by reading requirements.txt
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements



setup(
    name='TELECOM_CHURN_PREDICTION',
    version='0.0.1',
    author='Manjunath',
    author_email='manjunathyashram5@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')

)  
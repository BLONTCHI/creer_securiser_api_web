import yaml
import os


class ApiConfiguration:
    def __init__(self, filename:str) -> None:
        self.filename = filename
        with open(filename) as f:
            # expandvars() permet de remplacer automatiquement les variables d'environnement 
            # par leurs valeurs dans le fichier de configuration
            self.config = yaml.safe_load(os.path.expandvars(f.read()))
            
    
    @property
    def token_secret_key(self) -> str:
        return self.config["tokenSecretKey"]
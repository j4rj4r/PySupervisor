![Test Image 1](https://github.com/j4rj4r/PySupervisor/blob/master/github_assets/pysupervision.png)

# PySupervisor

PySupervisor permet de savoir depuis votre poste quelles sont les postes actuellement utilisés, par qui et sous quel systeme.

### Fonctionnalités :

- Multi-plateformes
- Simple d'utilisation
- Simple d'installation
- Détection automatique du réseau et de sa taille


### Installation :
Pour pouvoir utiliser PySupervisor vous aurez obligatoirement besoin de la librairie [Psutil](https://psutil.readthedocs.io/en/latest/#)
 et de [Python3](https://www.python.org/download/releases/3.0/). (Pour pouvoir utiliser le client ou le serveur).
Si vous avez python3 et pip d'installé sur votre machine vous pouvez installer psutil avec :
```
python3 -m pip install psutil
```

### Utilisation :
Vous devez dans un premier temps lancer le serveur sur toutes les machines que vous voulez monitorer. Pour cela, vous devez utiliser la commande :
```
python3 pysupervisor.py -l Serveur
```
Puis si vous voulez accéder aux postes disponibles sur votre reseau :
```
python3 pysupervisor.py -l Client
```

#### Utilisation avancée :
Vous pouvez demander au serveur d'écouter sur le port que vous voulez :
```
python3 pysupervisor.py -l Serveur -Pe 1234
```
Et vous pouvez indiquer au client sur quel  port ecoute le serveur :
```
python3 pysupervisor.py -l Serveur -Ps 1234
```

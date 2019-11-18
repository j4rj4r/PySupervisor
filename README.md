# PySupervisor

PySupervisor permet de savoir depuis votre poste quelles sont les postes actuellement utilises, par qui et sous quel systeme.


### Fonctionnalites :

- Multi-plateformes
- 
- Markdown Extras : Support ToC (Table of Contents), Emoji, Task lists, @Links...;
- Compatible with all major browsers (IE8+), compatible Zepto.js and iPad;
- Support identification, interpretation, fliter of the HTML tags;
- Support TeX (LaTeX expressions, Based on KaTeX), Flowchart and Sequence Diagram of Markdown extended syntax;
- Support AMD/CMD (Require.js & Sea.js) Module Loader, and Custom/define editor plugins;

###Installation :
Pour pouvoir utiliser PySupervisor vous aurez obligatoirement besoin de la librairie [Psutil](https://psutil.readthedocs.io/en/latest/#)
 et de [Python3](https://www.python.org/download/releases/3.0/). (Pour pouvoir utiliser le client ou le serveur).
Si vous avez python3 et pip d'installe sur votre machine vous pouvez installer psutil avec :
```
python3 -m pip install psutil
```

###Utilisation :
Vous devez dans un premer temps lancer le serveur sur toutes les machines que vous voulez monitore pour cela vous devez utiliser la commande :
```
python3 pysupervisor.py -l Server
```
Puis si vous voulez acceder aux postes disponibles sur votre reseau :
```
python3 pysupervisor.py -l Client
```

####Utilisation de la partie client :

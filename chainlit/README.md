# OrangeBot
**OrangeBot** est un poc pour la création de chatbot spécialisé basé sur ChatGPT.
Ce projet permet de créer un chatbot qui répond aux questions des utilisateurs grâce aux documents de référence qui sont fournis au démarrage de l'application.

## Installation avec docker
### Prérequis
- [x] Assurez-vous que `Docker` est l'os de votre machine. Sinon, [Clickez](https://github.com/DMonsia/hadoop-cluster/blob/main/docker-installation.md) ici pour l'installer.
- [x] Assurez-vous que `make` est installé sur votre machine. [Clickez](https://www.makeuseof.com/how-to-fix-make-command-not-found-error-ubuntu/) ici pour l'installer.

### Installation
Pour installer OrangeBot, suivez les étapes suivantes:

1. Clonez le référentiel sur votre machine locale
Ouvrez ensuite le dossier du projet.
- Créez un répertoire data. Le dossier `./data` est utilisé pour stocker toutes les données générées par l'application.
- Créez un fichier `.env` et ajouter votre clé API de ChatGPT
```
OPENAI_API_KEY = "sk-..."
``` 

2. Créer une image Docker de l'application
Exécutez la commande suivante pour créer l'image de l'application.
```bash
make build
```

3. Démarrer le conteneur de l'application
Utilisez ensuite la commande suivante pour démarrer le conteneur docker de l'application:
```bash
make run DATA_FILE=${PWD}/data
```

## Installation avec un environnement virtuel
### Prérequis
- [x] Assurez-vous que `tesseract-ocr` est installé sur votre machine. Sinon, taper la commande suivante pour l'installer.
```bash
sudo apt install -y tesseract-ocr
```

### Installation
Pour installer OrangeBot, suivez les étapes suivantes:

1. Clonez le référentiel sur votre machine locale
Ouvrez ensuite le dossier du projet.
- Créez un répertoire data. Le dossier `./data` est utilisé pour stocker toutes les données générées par l'application.
- Créez un fichier `.env` et ajouter votre clé API de ChatGPT
```
OPENAI_API_KEY = "sk-..."
```

2. Créer un environnement virtuel dédié au projet avec python >= 10

3. Installer les dépendances de l'application
Toutes les dépendances Python nécessaires pour l'exécution de l'apa se trouve dans le fichier `requirements.txt`. Il est fortement conseillé de créer un environnement.

4. Démarrer l'app
Entrer la commande:
```bash
chainlit run main.py
```

## Utiliser l'application
Une fois le serveur opérationnel, vous pouvez accéder à l'interface de **OrangeBot** à l'adresse `localhost:8000` dans votre navigateur Web.

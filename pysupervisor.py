import socket, psutil, os, ipaddress,itertools,argparse
from _thread import *
import threading


class Serveur : #Class permettant de gérer le serveur

	def __init__(self,PortEcoute = 1998) : #Contructeur On initialise les variables | PortEcoute falcultatif
		self.PortEcoute = PortEcoute

	def LaunchServeur (self) : #Methode permettant de lancer le serveur
		s = socket.socket()
		s.bind(('', self.PortEcoute))
		s.listen(5) #On permet 5 connexions en attente
		while True :
			c, addr = s.accept()
			start_new_thread(self.sendDataComputer, (c,)) #On lance un thread pour chaque connexion au serveur
		s.close()

	def sendDataComputer (self,c) :
		a = psutil.users()
		while True :
			sendData = "Nom d'utilisateur : " + a[0].name + "\nSysteme d'exploitation : " + os.uname().sysname + "\nVersion du systeme : " + os.uname().version
			c.send(sendData.encode())
			if c.recv(1024).decode() == "end" : #Accusé de reception pour fermer la connexion
				break
		c.close() #On ferme la connexion


class Client : #Class permettant de gérer le client

	def __init__(self, PortServeur = 1998) : #Contructeur on initialise les variables | PortServeur falcultatif
		self.PortServeur = PortServeur

	def LaunchClient(self, IpServeur) : #Méthode permettant de lancer le client
		try:
			s = socket.socket()
			s.connect(('',self.PortServeur))
			print (s.recv(1024).decode())
			s.send("end".encode()) #On envoit un accusé de deconnexion
			s.close() #On ferme la connexion
			input('')
			print ("\033[2J")
		except ConnectionRefusedError :
			print("Le serveur n'existe plus.")

	def IsServerUp(self, ListIp): #Liste des ip avec un serveur up. Permet de voir si le port est ouvert
		ListIpUp = []
		for ip in ListIp :
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(0.1)
			result = sock.connect_ex((ip, self.PortServeur))
			if result == 0:
				ListIpUp.append(ip)
			sock.close()
		return ListIpUp

	def GetNetworkAddrIpList(self) :#Permet de faire une liste de toutes les addresses ip du réseau. On utilise le masque pour faire la liste.
		CompteurZero = 0
		ListIp = []
		IPAddr = socket.gethostbyname(socket.gethostname()) #On récupère notre adresse ip
		for snic, addrs in psutil.net_if_addrs().items(): #On récupère la liste des interfaces avec leurs infos
			for addr in addrs :
				if IPAddr == addr.address : #Si l'adresse ip qu'on a récupéré est égal à l'adresse ip dans la liste des interfaces
					NetworkMask = addr.netmask #On a trouvé le masque du réseau
		maskbi = bin(int(ipaddress.IPv4Address(NetworkMask)))
		maskbi = maskbi.replace('0b','') #Permet d'enlever le 0b au debut du binaire pour pas avoir de probleme quand on compte le nombre de 0
		IPAddrbi = bin(int(ipaddress.IPv4Address(IPAddr)))
		for bi in maskbi : #On compte le nombre de 0
			if int(bi) == 0 :
				CompteurZero += 1
		for x in map(''.join, itertools.product('01', repeat=CompteurZero)): #Permet d'incrementer la partie variable de l'adresse ip et de faire la list de toutes les ip du réseau
			IPNetwork = IPAddrbi.replace(IPAddrbi[-CompteurZero:], x)
			IPNetwork = IPNetwork.replace('0b','')
			ListIp.append("".join ( [str(int( i , 2)) +'.' for i in [ IPNetwork[0:8] , IPNetwork[8:16] , IPNetwork[16:24] , IPNetwork[24:32] ] ] )[:-1])
		return ListIp



if __name__ == '__main__': #Partie pricipal du script
	print("""\
 _____        _____                             _
|  __ \      / ____|                           (_)
| |__) |   _| (___  _   _ _ __   ___ _ ____   ___ ___  ___  _ __
|  ___/ | | |\___ \| | | | '_ \ / _ \ '__\ \ / / / __|/ _ \| '__|
| |   | |_| |____) | |_| | |_) |  __/ |   \ V /| \__ \ (_) | |
|_|    \__, |_____/ \__,_| .__/ \___|_|    \_/ |_|___/\___/|_|
	 _/ |            | |
        |___/            |_|                                      """)

	print("PySupervisor | Outil de supervision réseau")
	print("Une aide est disponible avec la commande : python3 pysupervisor.py -h\n")
	parser = argparse.ArgumentParser()
	parser.add_argument('-l','--launch', help='Permet de lancer le serveur ou le client (Param: Serveur ou Client)', type=str, required=True)
	parser.add_argument('-Pe','--PortEcoute',help='Permet de definir sur quel port le serveur va ecouter (1998 par default)', type=int, required=False)
	parser.add_argument('-Ps','--PortServeur',help='Pernet de definir au client sur quel port le serveur ecoute (1998 par default)', type=int, required=False)
	args = parser.parse_args() #On recupère les arguments
	if args.launch.upper() == "SERVEUR" : #Si l'argument lance le serveur
		print("Lancement du serveur...")
		if args.PortEcoute : #Si l'argument PortEcoute existe
			a = Serveur(PortEcoute=args.PortEcoute)
		else :
			a = Serveur()
		a.LaunchServeur()
	if args.launch.upper() == "CLIENT" : #Si l'argument lance le Client
		print("Lancement du client...")
		if args.PortServeur : #SI l'argument PortServeur existe
			a = Client(PortServeur=args.PortServeur)
		else :
			a = Client()
		ListIp = a.GetNetworkAddrIpList()
		print("Nombre d'adresse ip sur le réseau : " + str(len(ListIp)-1))
		print("Plage d'adresse : " + str(ListIp[0]) + " - " + str(ListIp[len(ListIp)-1]))
		ServerUp = a.IsServerUp(ListIp)
		GetInfo = "default"
		try :
			while GetInfo.upper() != "EXIT": #Tant que l'utilisateur ne veut pas quitter le programme
				print("Liste des ordinateurs disponibles sur le réseau : ")
				print('\n'.join(map(str,ServerUp))) #On affiche les ip disponibles
				GetInfo = input("Obtenir les informations de quelle ip ? ")
				if  GetInfo not in ServerUp :
					print("Cette adress ip n'est pas disponible ! Merci de réessayer.")
					input()
					print ("\033[2J")
				else :
					a.LaunchClient(GetInfo)
		except KeyboardInterrupt :
			print("\nFermeture du programme")

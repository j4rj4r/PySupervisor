import socket, psutil, os, ipaddress,itertools,argparse

class Serveur : #Class permettant de gérer le serveur

	def __init__(self,PortEcoute = 1999) : #Contructeur On initialise les variables | PortEcoute falcultatif
		self.PortEcoute = PortEcoute

	def LaunchServeur (self) : #Methode permettant de lancer le serveur
		a = psutil.users() #Permet de récupérer
		s = socket.socket()
		s.bind(('', self.PortEcoute))
		while True :
			s.listen(5) #On permet 5 connexions en attente
			c, addr = s.accept()
			sendData = a[0].name + ";" + os.name
			c.send(sendData.encode())
			if c.recv(1024).decode() == "end" : #Accusé de reception pour fermé la connexion
				c.close() #On fermme la connexion


class Client : #Class permettant de gérer le client

	def __init__(self, PortServeur = 1999) : #Contructeur on initialise les variables | PortServeur falcultatif
		self.PortServeur = PortServeur

	def LaunchClient(self) : #Méthode permettant de lancer le client
		s = socket.socket()
		s.connect(('',self.PortServeur))
		print (s.recv(1024).decode())
		s.send("end".encode()) #On envoit un accusé de deconnexion
		s.close() #On ferme la connexion

	def IsServerUp(self, ListIp): #Liste des ip avec un serveur up. Permet de voir si le port est ouvert
		ListIpUp = []
		for ip in ListIp :
			try :
				s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				s.settimeout(0.1)
				s.sendto("Are you open bitch ?".encode(), (ip, self.PortServeur))
				recv, svr = s.recvfrom(255)
				s.close()
			except socket.timeout :
				pass
			except ConnectionResetError:
				ListIpUp.append(ip)
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
		maskbifinal = maskbi.replace('0b','') #Permet d'enlever le 0b au debut du binaire pour pas avoir de probleme quand on compte le nombre de 0
		IPAddrbi = bin(int(ipaddress.IPv4Address(IPAddr)))
		for bi in maskbifinal : #On compte le nombre de 0
			if int(bi) == 0 :
				CompteurZero += 1
		for x in map(''.join, itertools.product('01', repeat=CompteurZero)): #Permet d'incrementer la partie variable de l'adresse ip et de faire la list de toutes les ip du réseau
			IPNetwork = IPAddrbi.replace(IPAddrbi[-CompteurZero:], x)
			IPNetwork = IPNetwork.replace('0b','')
			ListIp.append("".join ( [str(int( i , 2)) +'.' for i in [ IPNetwork[0:8] , IPNetwork[8:16] , IPNetwork[16:24] , IPNetwork[24:32] ] ] )[:-1])
		return ListIp



if __name__ == '__main__':
	print("""\
 _____        _____                             _
|  __ \      / ____|                           (_)
| |__) |   _| (___  _   _ _ __   ___ _ ____   ___ ___  ___  _ __
|  ___/ | | |\___ \| | | | '_ \ / _ \ '__\ \ / / / __|/ _ \| '__|
| |   | |_| |____) | |_| | |_) |  __/ |   \ V /| \__ \ (_) | |
|_|    \__, |_____/ \__,_| .__/ \___|_|    \_/ |_|___/\___/|_|
	 _/ |            | |
        |___/            |_|                                      """)

	print("Outil de supervision de réseau")
	print("Si vous voulez une aide vous pouvez faire : python3 pysupervisor.py -h\n")
	parser = argparse.ArgumentParser() #On recupère les arguments
	parser.add_argument('-l','--launch', help='Launch Server or Client', type=str, required=True)
	parser.add_argument('-d','--debug',help='Debug', required=False)
	args = parser.parse_args()
	if args.launch == "Server" : #Si l'argument lance le serveur
		print("Lancement du serveur...")
		a = Serveur()
		a.LaunchServeur()
	if args.launch == "Client" : #Si l'argument lance le Client
		print("Lancement du client...")
		a = Client()
		ListIp = a.GetNetworkAddrIpList()
		print("Nombre d'adresse ip sur le réseau : " + str(len(ListIp)))
		print("Plage d'adresse : " + str(ListIp[0]) + " - " + str(ListIp[len(ListIp)-1]))
		ServerUp = ["169.254.239.204"]#a.IsServerUp(ListIp)
		GetInfo = "default"
		while GetInfo not in ServerUp : #Tant que l'utilisateur ne veut pas une adresse valide
			print("Liste des ordinateurs disponibles sur le réseau : ")
			print('\n'.join(map(str,ServerUp))) #On affiche les ip disponibles
			GetInfo = input("Obtenir les informations de quelle ip ? ")
			if  GetInfo not in ServerUp :
				print("Cette adress ip n'est pas disponible ! Merci de réessayer.")

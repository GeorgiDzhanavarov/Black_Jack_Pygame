import socket
import threading
from time import sleep
import Player
import Dealer

HOST = '127.0.0.1'
PORT = 12345

dealer = Dealer.Dealer()
players = []
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print("Server is listening for incoming connections...")

# Function to handle client connections
def handle_client(client_socket, client_address):
    print(f"Connection from {client_address} has been established.")
    curr_player = None
    for player in players:
        if player.socket == client_socket:
            curr_player = player
            client_data = str(curr_player.money)
            client_socket.sendall(client_data.encode())
            break   

    while True:
        # Receive data from the client
        try:
            data = client_socket.recv(1024).decode()
        except:
             break
        if not data:
            break
        
        if data == "bet50 button clicked":
            if curr_player.bet(50) is False:
                client_data = "incorrect bet"
                client_socket.sendall(client_data.encode())
            else:
                client_data = str(curr_player.money)
                client_socket.sendall(client_data.encode())
                while not all(player.bet_value is not None for player in players):
                    client_socket.sendall("waiting".encode())
                    sleep(1)
                start_game(curr_player)
        if data == "bet100 button clicked":
            if curr_player.bet(100) is False:
                client_data = "incorrect bet"
                client_socket.sendall(client_data.encode())
            else:
                client_data = str(curr_player.money)
                client_socket.sendall(client_data.encode())
                while not all(player.bet_value is not None for player in players):
                    client_socket.sendall("waiting".encode())
                    sleep(1)
                start_game(curr_player)
        if data == "betall button clicked":
            if curr_player.bet(curr_player.money) is False:
                client_data = "incorrect bet"
                client_socket.sendall(client_data.encode())
            else:
                client_data = str(curr_player.money)
                client_socket.sendall(client_data.encode())
                while not all(player.bet_value is not None for player in players):
                    client_socket.sendall("waiting".encode())
                    sleep(1)
                start_game(curr_player)
        if data == "hit button clicked":
                dealer.deal_one_card(curr_player)
                card_data = make_card_data()
                client_socket.sendall(card_data.encode())
                if curr_player.hit_option() is False:
                    curr_player.stay_option()
                    client_socket.sendall("no".encode())
                    while not all(player.is_ready is not False for player in players):
                        client_socket.sendall("waiting".encode())
                        sleep(1)
                    end_game(curr_player)
                else:
                    client_socket.sendall("yes".encode())
        if data == "stay button clicked":
                curr_player.stay_option()
                card_data = make_card_data()
                client_socket.sendall(card_data.encode())
                while not all(player.is_ready is not False for player in players):
                        client_socket.sendall("waiting".encode())
                        sleep(1)
                end_game(curr_player)
        if data == "double button clicked":
                if curr_player.double_option() is True:
                    dealer.deal_one_card(curr_player)
                    curr_player.stay_option()
                    card_data = make_card_data()
                    client_socket.sendall(card_data.encode())
                    while not all(player.is_ready is not False for player in players):
                        client_socket.sendall("waiting".encode())
                        sleep(1)
                    end_game(curr_player)
                else:
                    client_socket.sendall("you are brokie".encode())      
        print(f"Received from client {client_address}: {data}")
    # Close the connection   
    players.remove(curr_player)
    client_socket.close()
    print(f"Connection from {client_address} has been closed.")

def start_game(curr_player):
    if players[0] == curr_player:
        dealer.new_deck()
        dealer.players = players
        dealer.deal_cards()
        data = make_card_data()
        for player in dealer.players:
            player.socket.sendall(data.encode())   

def end_game(curr_player):
    if players[0] == curr_player:
        dealer.hit()
        dealer.pay_player()
        card_data = make_card_data()
        for player in players:
            data = card_data + "|" + str(player.money)
            player.socket.sendall(data.encode())
        dealer.clear_dealer()
        for player in players:
            player.clear_player()
    

def make_card_data():
    data = ""
    for card in dealer.cards:
        data += " " + card.name
    for player in dealer.players:
        data += ","
        for card in player.cards:
            data += " " + card.name  
    return data 

# Function to accept incoming connections and create threads for each client
def accept_connections():
    while True:
        # Accept incoming connection
            client_socket, client_address = server_socket.accept()
            if len(players) >= 3:
                print("Maximum connections reached. Rejecting new connection.")
                client_socket.sendall("server is full".encode())
                client_socket.close()
                continue   
            players.append(Player.Player(1000, client_socket))
            client_socket.sendall(str(len(players)).encode())
            # Create a new thread to handle the client connection
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
 #Main           
if __name__ == "__main__":
    accept_connections()
import pygame
import sys
import Button
import RoundButton
import TextField
import socket

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600

GREEN = (0, 100, 0)

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Black Jack")

# Dealer Image
dealer_image = pygame.image.load("images/dealer.png")  
dealer_image = pygame.transform.scale(dealer_image, (50, 50))

#Reversed card image
reversed_card_image = pygame.image.load("cards/back.png")
reversed_card_image = pygame.transform.scale(reversed_card_image, (80, 100))

# Card information
dealer_cards = []
player1_cards = []
player2_cards = []
player3_cards = []

# Player image
player_image = pygame.image.load("images/player.png")  
player_image = pygame.transform.scale(player_image, (50, 50))

# All buttons and fields
start_button = Button.Button(400, 300, 200, 100, "START")
play_again_button = Button.Button(20, 20, 100, 50, "play again")
hit_button = Button.Button(20, 20, 100, 50, "HIT")
stay_button = Button.Button(20, 80, 100, 50, "STAY")
double_button = Button.Button(20, 140, 100, 50, "DOUBLE")
bet_50_button = RoundButton.RoundButton(40,230,25,(204,204,0),"50$")
bet_100_button = RoundButton.RoundButton(40,290,25,(0,0,204),"100$")
bet_all_in_button = RoundButton.RoundButton(40,350,25,(204,0,0),"All")
balance_field = TextField.TextField(20,500,150,70,"Balance")
server_is_full_message = TextField.TextField(400,200,200,70,"Server is full :(")
dealer_chat = TextField.TextField(600,50,300,50,"Waiting for players")
player_name = TextField.TextField(250,560,50,40,"You")

#All phases of the client
def menu():
    while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if start_button.handle_event(event):
                    connecting_phase()

            window.fill(GREEN)
            start_button.draw(window)
            pygame.display.flip()

def connecting_phase():
    HOST = '127.0.0.1'
    PORT = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    client_socket.connect((HOST, PORT)) 
    data = client_socket.recv(1024).decode()
    print(data)
    if data == "server is full":
        server_is_full_window()
    elif data == "2":
        player_name.rect.x = 500
    elif data == "3":
        player_name.rect.x = 750
    client_data = client_socket.recv(1024).decode()
    balance_field.change_text("Balance:\n" + client_data)
    bet_phase(client_socket)

def server_is_full_window():
     while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if start_button.handle_event(event):
                    connecting_phase()

            window.fill(GREEN)
            server_is_full_message.draw(window)
            start_button.draw(window)
            pygame.display.flip()

def bet_phase(client_socket):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client_socket.close()
                pygame.quit()
                sys.exit()
            if bet_50_button.handle_event(event):
                client_socket.sendall("bet50 button clicked".encode())
                data = client_socket.recv(1024).decode()
                if data == "incorrect bet":
                    dealer_chat.change_text("You can't place that bet")
                else:
                    dealer_chat.change_text("Bet placed")
                    balance_field.change_text("Balance:\n" + data)
                    waiting_for_all_bets_phase(client_socket)
            if bet_100_button.handle_event(event):
                client_socket.sendall("bet100 button clicked".encode())
                data = client_socket.recv(1024).decode()
                if data == "incorrect bet":
                    dealer_chat.change_text("You can't place that bet")
                else:
                    dealer_chat.change_text("Bet placed")
                    balance_field.change_text("Balance:\n" + data)
                    waiting_for_all_bets_phase(client_socket)
            if bet_all_in_button.handle_event(event):
                client_socket.sendall("betall button clicked".encode())
                data = client_socket.recv(1024).decode()
                if data == "incorrect bet":
                    dealer_chat.change_text("You can't place that bet")
                else:
                    dealer_chat.change_text("Bet placed")
                    balance_field.change_text("Balance:\n" + data)
                    waiting_for_all_bets_phase(client_socket)

        window.fill(GREEN)
        window.blit(dealer_image, (500,80))
        for number in range (1,4):
            window.blit(player_image, (200*number*1.25,500))    
        bet_50_button.draw(window)
        bet_100_button.draw(window)
        bet_all_in_button.draw(window)
        balance_field.draw(window)
        dealer_chat.change_text("Place your bet")
        dealer_chat.draw(window)
        player_name.draw(window)
        pygame.display.flip()

def waiting_for_all_bets_phase(client_socket):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client_socket.close()
                pygame.quit()
                sys.exit()

        window.fill(GREEN)
        window.blit(dealer_image, (500,80))
        for number in range (1,4):
            window.blit(player_image, (200*number*1.25,500))
        balance_field.draw(window)
        dealer_chat.change_text("Please wait for all bets")
        dealer_chat.draw(window)
        player_name.draw(window)
        pygame.display.flip()
        data = "waiting"
        data = client_socket.recv(1024).decode()
        print(data)
        if data != "waiting":
            game_phase(client_socket, data)    

def game_phase(client_socket, data):
    read_data(data)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client_socket.close()
                pygame.quit()
                sys.exit()
            if hit_button.handle_event(event):
                client_socket.sendall("hit button clicked".encode())
                card_data = client_socket.recv(1024).decode()
                continue_data = client_socket.recv(1024).decode()
                read_data(card_data)
                if continue_data == "no":
                    waiting_for_results_phase(client_socket)
            if stay_button.handle_event(event):
                client_socket.sendall("stay button clicked".encode())
                card_data = client_socket.recv(1024).decode()
                read_data(card_data)
                waiting_for_results_phase(client_socket)
            if double_button.handle_event(event):
                client_socket.sendall("double button clicked".encode())
                card_data = client_socket.recv(1024).decode()
                if card_data != "you are brokie":
                    read_data(card_data)
                    waiting_for_results_phase(client_socket)

        window.fill(GREEN)
        window.blit(dealer_image, (500,80))
        for number in range (1,4):
            window.blit(player_image, (200*number*1.25,500))   
        place_cards()
        window.blit(reversed_card_image,(400,70))
        balance_field.draw(window)
        dealer_chat.change_text("You can play now")
        dealer_chat.draw(window)
        player_name.draw(window)
        hit_button.draw(window)
        stay_button.draw(window)
        double_button.draw(window)
        pygame.display.flip()

def waiting_for_results_phase(client_socket):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client_socket.close()
                pygame.quit()
                sys.exit()

        window.fill(GREEN)
        window.blit(dealer_image, (500,80))
        place_cards()
        window.blit(reversed_card_image,(400,70))
        for number in range (1,4):
            window.blit(player_image, (200*number*1.25,500))
        balance_field.draw(window)
        dealer_chat.change_text("Please wait for all players")
        dealer_chat.draw(window)
        player_name.draw(window)
        pygame.display.flip()
        data = "waiting"
        data = client_socket.recv(1024).decode()
        if data != "waiting":
            result_phase(client_socket, data)

def result_phase(client_socket, data):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client_socket.close()
                pygame.quit()
                sys.exit()
            if play_again_button.handle_event(event):
                bet_phase(client_socket)

        window.fill(GREEN)
        window.blit(dealer_image, (500,80))
        read_data(data.split("|")[0])
        place_cards()
        for number in range (1,4):
            window.blit(player_image, (200*number*1.25,500))
        balance_field.change_text("Balance:\n" + data.split("|")[1])
        balance_field.draw(window)
        dealer_chat.change_text("Better luck next time XD")
        dealer_chat.draw(window)
        player_name.draw(window)
        if data.split("|")[1] != "0":
            play_again_button.draw(window)
        pygame.display.flip()


#Additional functions       
def place_cards():
    cords = [400,70]  
    for card in dealer_cards:
        window.blit(card, cords)
        cords[0] -= 50
        cords[1] += 50
    cords = [300,400]  
    for card in player1_cards:
        window.blit(card, cords)
        cords[0] += 50
        cords[1] -= 50
    cords = [500,400]  
    for card in player2_cards:
        window.blit(card, cords)
        cords[0] += 50
        cords[1] -= 50
    cords = [700,400]  
    for card in player3_cards:
        window.blit(card, cords)
        cords[0] += 50
        cords[1] -= 50

def read_data(data):
    card_size = (80,100)
    dealer_cards.clear()
    player1_cards.clear()
    player2_cards.clear()
    player3_cards.clear()
    splitted_data = data.split(",")

    for card in splitted_data[0].split(" "):
        if card == "":
            continue
        card_image = pygame.image.load("cards/" + card + ".png")
        card_image = pygame.transform.scale(card_image, card_size)
        dealer_cards.append(card_image)
    for card in splitted_data[1].split(" "):
        if card == "":
            continue
        card_image = pygame.image.load("cards/" + card + ".png")
        card_image = pygame.transform.scale(card_image, card_size)
        player1_cards.append(card_image)
    if len(splitted_data) > 2:
        for card in splitted_data[2].split(" "):
            if card == "":
                continue
            card_image = pygame.image.load("cards/" + card + ".png")
            card_image = pygame.transform.scale(card_image, card_size)
            player2_cards.append(card_image)
    if len(splitted_data) > 3:
        for card in splitted_data[3].split(" "):
            if card == "":
                continue
            card_image = pygame.image.load("cards/" + card + ".png")
            card_image = pygame.transform.scale(card_image, card_size)
            player3_cards.append(card_image)

def make_cards_images(data):
    new_data = data.split(",")
    cards = new_data[0].split(" ")
    for card in cards:
        if card == "":
            continue
        card_image = pygame.image.load("cards/" + card + ".png")
        card_image = pygame.transform.scale(card_image, (25, 50))
        dealer_cards.append(card_image)
    cards = new_data[1].split(" ")
    for card in cards:
        if card == "":
            continue
        card_image = pygame.image.load("cards/" + card + ".png")
        card_image = pygame.transform.scale(card_image, (25, 50))
        player1_cards.append(card_image)
    if len(new_data) > 2:
        cards = new_data[2].split(" ")
        for card in cards:
            if card == "":
                continue
            card_image = pygame.image.load("cards/" + card + ".png")
            card_image = pygame.transform.scale(card_image, (25, 50))
            player2_cards.append(card_image)
    if len(new_data) > 3:
        cards = new_data[3].split(" ")
        for card in cards:
            if card == "":
                continue
            card_image = pygame.image.load("cards/" + card + ".png")
            card_image = pygame.transform.scale(card_image, (25, 50))
            player3_cards.append(card_image)

#Main
if __name__ == "__main__":
    menu()
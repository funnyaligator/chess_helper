import threading
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import chess
from stockfish import Stockfish
import board_handling as bd
from subprocess import Popen, PIPE
import selenium.webdriver.support.expected_conditions as EC

chrome_options = Options()
chrome_options.binary_location = "/usr/bin/chromium"

driver = webdriver.Chrome(options=chrome_options)


# initialize selenium driver and stockfish engine
# profile_path = '/home/user/Downloads/firefox_profile_vscode'
# firefox_options = webdriver.FirefoxOptions()
# firefox_options.profile = profile_path
# driver = webdriver.Firefox(options=firefox_options)
#print(driver.capabilities)
#driver.set_window_size(700, 900)  # Set window size for better visibility

stockfish_process = Popen(['/home/user/Desktop/code/li_play/stockfish_15.1_linux_x64/stockfish-ubuntu-20.04-x86-64'], stdin=PIPE, stdout=PIPE)



# function to extract current moves in UCI notation
def raw_to_uci(driver):
    try:
        moves = driver.find_element(By.TAG_NAME, 'l4x').text
        uci_moves = [move for move in moves.split('\n') if not move.isdigit() and move]
        return uci_moves
    except:
        pass

# function to determine player's color based on the chessboard
def get_color(chessboard):
    return 'white' if 'white' in chessboard else 'black'

# function to generate FEN notation given a list of moves in UCI notation
def get_fen(moves):
    board = chess.Board()
    for move in moves:
        board.push_san(move)
    return board.fen()

# function to get the best move using stockfish engine
def get_best_move(fen):
    stockfish_process.stdin.write(('position fen ' + fen + '\n').encode())
    stockfish_process.stdin.write('go depth 7\n'.encode())
    stockfish_process.stdin.flush()
    
    while True:
        line = stockfish_process.stdout.readline().decode().strip()
        if line.startswith('bestmove'):
            return line.split()[1]

# function to get the size of the chessboard element
def get_board_size():
    return driver.find_element(By.CSS_SELECTOR, '.cg-wrap > cg-container:nth-child(1) > cg-board:nth-child(1)')

def draw_canvas():
    driver.execute_script('''
                        var canvas = document.getElementById('chessboard-canvas');
                        
                        if (!canvas) {
                            canvas = document.createElement('canvas');
                            canvas.setAttribute('width', window.innerWidth);
                            canvas.setAttribute('height', window.innerHeight);
                            canvas.setAttribute('style', 'position:absolute; top:0; left:0; pointer-events:none;');
                            canvas.setAttribute('id', 'chessboard-canvas');
                            var body = document.getElementsByTagName('body')[0];
                            body.appendChild(canvas);
                        }
                        ''')

# main loop for playing the game
lichess_url = 'https://www.lichess.org'
driver.get(lichess_url)

# signin = driver.find_element(By.CLASS_NAME, "signin") # find sign in button
# signin.click()

# element_present = EC.presence_of_element_located((By.NAME, "username"))
# wait(driver, 10).until(element_present)
# login_element = driver.find_element(By.NAME, 'username')
# # login_element.click()
# login_element.send_keys('coffees-morningus')

# password_element = driver.find_element(By.NAME, 'password')
# # login_element.click()
# password_element.send_keys('fucklichess1')

# sign_element = driver.find_element(By.CSS_SELECTOR, "#main-wrap > main > form > div.one-factor > button");
# sign_element.click()





wait_for_gamePage = wait(driver, 10)
wait_for_gamePage.until(lambda driver: driver.current_url != lichess_url)

last_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
player_color = 'white'



def play_game():
    global last_fen, player_color
    
    wait_for_moves = wait(driver, 10)
    
    while True:
        try:
            # Wait for the next move
            moves_result = wait_for_moves.until(lambda driver: raw_to_uci(driver))
            moves = moves_result
            recent_fen = get_fen(moves)
            
            if recent_fen != last_fen:
                if recent_fen[18] == '8' or recent_fen[20] == '8':
                    player_color = get_color(driver.find_element(By.CSS_SELECTOR, ".cg-wrap").get_attribute('class'))
                    threading.Thread(target=draw_canvas).start()
                
                board_size = get_board_size()
                best_m = get_best_move(recent_fen)
                threading.Thread(target=bd.move_to_line, args=(driver, board_size.size["width"], board_size.location, best_m, player_color)).start()
                last_fen = recent_fen
        
        except Exception as e:
            # Print the exception for debugging purposes
            # print(e)
            pass


game_thread = threading.Thread(target=play_game)
game_thread.start()
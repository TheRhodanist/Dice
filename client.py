import tkinter as tk
import random as ran
import threading as threading
import socket


class App(tk.Frame):
    def __init__(self):
        super().__init__()
        self.rDice = tk.IntVar()
        self.sNumDice = tk.IntVar()
        self.playerName = tk.StringVar()
        self.concResult = tk.StringVar()
        self.resultSum = tk.IntVar()
        self.history = False
        self.msg = None
        self.server = None
        self.coinResult = False
        self.initUI()


    def initUI(self):
        self.frame = tk.Frame(self.master, width=700, height=370)
        self.frame.pack(fill=tk.BOTH, expand=1)
        self.master.title("Dice")

        self.rD6 = tk.Radiobutton(self.master, text="D6", variable=self.rDice, value=6)
        self.rD6.select()
        self.rD6.place(x=50, y=30)
        self.rD20 = tk.Radiobutton(self.master, text="D20", variable=self.rDice, value=20)
        self.rD20.place(x=140, y=30)

        self.slider = tk.Scale(self.master, showvalue=0, from_=1, to=5, orient=tk.HORIZONTAL, length=180, tickinterval=1, variable=self.sNumDice)
        self.slider.set(3)
        self.slider.place(x=30, y=75)

        self.btnCoin = tk.Button(self.master, text="Coinflip", width=6, command=self.woot)
        self.btnCoin.place(x=265, y=30)

        self.btnRoll = tk.Button(self.master, text="Roll", width=6)
        self.btnRoll.place(x=265, y=75)

        self.lblResultPlayer = tk.Label(self.master, textvariable=self.playerName, font=('Helvetica', 30))
        self.lblResultPlayer.place(x=85, y=160)

        self.lblResult = tk.Label(self.master, textvariable=self.concResult, font=('Helvetica', 25))
        self.lblResult.place(x=100, y=220)

        self.lblResultSum = tk.Label(self.master, textvariable=self.resultSum, font=('Helvetica', 45))
        self.lblResultSum.place(x=120, y=270)

        self.lbPlayer = tk.Listbox(self.master, width=40, height=8)
        self.lbPlayer.place(x=400, y=40)

        self.lbHistory = tk.Listbox(self.master, width=40, height=7)
        self.lbHistory.place(x=400, y=230)

        self.lblPlayer = tk.Label(self.master, text="Player", font=('Helvetica', 12))
        self.lblPlayer.place(x=405, y=5)

        self.lblHistory = tk.Label(self.master, text="History", font=('Helvetica', 12))
        self.lblHistory.place(x=405, y=195)

    def coinFlip(self):
        if(ran.random() > 0.5):
            self.coinResult = True
        else:
            self.coinResult = False



    def woot(self):
        self.playerName.set("Marci rollt:")
        self.concResult.set("3 + 5 + 6")
        self.resultSum.set(30)
        self.sendMessage(b"Marci:3D6-3/5/6-14")
        self.lbHistory.insert(tk.END, "foo")

    def update(self, message):
        #self.history.append(message)
        #self.lbHistory.redraw()

        self.lbHistory.insert(tk.END, message)

    def setServer(self, serv):
        self.server = serv

    def sendMessage(self, message):
        self.server.send(message)


class ServerApp(threading.Thread):

    socket = None
    host = ""
    port = 0
    callback = False
    running = True

    def __init__(self, ip, port, function):
        super().__init__()
        self.host = ip
        self.port = port
        self.callback = function

    def run(self):
        #initialize the Socket
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        print(self.sock)

        #MessageLoop
        while self.running:
            self.listen()

    def send(self,message):
        self.sock.sendall(message)

    def listen(self):
        message = self.sock.recv(4096)
        if message=="EXIT":
            self.running = False
            self.close()
        else:

            self.callback(message)

    def close(self):
        self.sock.close()
        print("Socket Closed")



def main():
    def close():
        root.destroy()
        server.close()
    root = tk.Tk()
    app = App()
    root.protocol("WM_DELETE_WINDOW", close)
    server = ServerApp("noobfilter.eu", 11100, app.update)
    app.setServer(server)
    server.start()

    root.mainloop()

if __name__ == "__main__":
    main()








# if name is clicked in 'player' list, only display results of said player in history

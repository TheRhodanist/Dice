import tkinter as tk
import random as rnd
import threading
import socket
import json
import signal

class App(tk.Frame):
    def __init__(self):
        super().__init__(None,width=800, height=370)
        self.rDice = 6
        self.sNumDice = tk.IntVar()
        self.playerName = tk.StringVar()
        self.me = tk.StringVar()
        self.concResult = tk.StringVar()
        self.resultSum = tk.IntVar()
        self.coin = tk.StringVar()
        self.server = None
        self.initUI()
        #self.initDSA()
        #self.initDegenesis()

        
    def initUI(self):
        initFrame = tk.Frame(self.master, width=700, height=420)
        initFrame.pack(fill=tk.BOTH, expand=1)

        b_dsa = tk.Button(initFrame, text="DSA",height=2, width=8,command= lambda: des(self,self.initDSA))
        b_dsa.pack()

        b_degen = tk.Button(initFrame, text="DEGENESIS",height=2, width=8,command= lambda: des(self,self.initDegenesis))
        b_degen.pack()

        def des(self,func):
            func()
            initFrame.destroy()





    def initDSA(self):
        #self.frame = tk.Frame(self.master, width=700, height=370)
        self.pack(fill=tk.BOTH, expand=1)
        self.master.title("DSA")
        self.rD6 = tk.Radiobutton(self.master, text="D6", variable=self.rDice, value=6)
        self.rD6.select()
        self.rD6.place(x=50, y=30)
        rD20 = tk.Radiobutton(self.master, text="D20", variable=self.rDice, value=20)
        rD20.place(x=140, y=30)

        self.slider = tk.Scale(self.master, showvalue=0, from_=1, to=5, orient=tk.HORIZONTAL, length=180, tickinterval=1, variable=self.sNumDice)
        self.slider.set(3)
        self.slider.place(x=30, y=75)

        self.btnCoin = tk.Button(self.master, text="Coinflip", state=tk.DISABLED, width=6, command=self.coinFlip)
        self.btnCoin.place(x=265, y=30)

        self.lblCoinResul = tk.Label(self.master, textvariable=self.coin)
        self.lblCoinResul.place(x=265, y=10)

        self.btnRoll = tk.Button(self.master, text="Roll", width=6, state=tk.DISABLED, command=self.roll)
        self.btnRoll.place(x=265, y=75)

        self.lblResultPlayer = tk.Label(self.master, textvariable=self.playerName, font=('Helvetica', 30))
        self.lblResultPlayer.place(x=60, y=160)

        self.lblResult = tk.Label(self.master, textvariable=self.concResult, font=('Helvetica', 25))
        self.lblResult.place(x=50, y=230)

        self.lblResultSum = tk.Label(self.master, textvariable=self.resultSum, font=('Helvetica', 45))
        self.lblResultSum.place(x=60, y=280)

        # self.lbPlayer = tk.Listbox(self.master, width=40, height=8)
        # self.lbPlayer.place(x=400, y=40)

        self.eMe = tk.Entry(self.master, textvariable=self.me)
        self.eMe.place(x=480, y=10)

        self.btnSubmitName = tk.Button(self.master, text="Ok", command=self.submitName)
        self.btnSubmitName.place(x=680, y=10)

        self.lbHistory = tk.Listbox(self.master, width=40, height=16)
        self.lbHistory.place(x=420, y=40)

        # self.lblPlayer = tk.Label(self.master, text="Player", font=('Helvetica', 12))
        # self.lblPlayer.place(x=405, y=5)

        self.lblHistory = tk.Label(self.master, text="History", font=('Helvetica', 12))
        self.lblHistory.place(x=425, y=5)

    def initDegenesis(self):
        #self.frame = tk.Frame(self.master, width=700, height=370)
        self.master.title("DEGENESIS")
        self.master.config(width=800,height=400)
        self.config(width=800,height=400)
        self.pack(fill=tk.BOTH, expand=1)
        


        self.slider = tk.Scale(self.master, showvalue=0, from_=3, to=12, orient=tk.HORIZONTAL, length=220, tickinterval=1, variable=self.sNumDice)
        self.slider.set(3)
        self.slider.place(x=20, y=55)

        self.btnCoin = tk.Button(self.master, text="Coinflip", state=tk.DISABLED, width=6, command=self.coinFlip)
        self.btnCoin.place(x=265, y=30)

        self.lblCoinResul = tk.Label(self.master, textvariable=self.coin)
        self.lblCoinResul.place(x=265, y=10)

        self.btnRoll = tk.Button(self.master, text="Roll", width=6, state=tk.DISABLED, command=self.roll)
        self.btnRoll.place(x=265, y=75)

        self.lblResultPlayer = tk.Label(self.master, textvariable=self.playerName, font=('Helvetica', 30))
        self.lblResultPlayer.place(x=20, y=160)

        self.lblResult = tk.Label(self.master, textvariable=self.concResult, font=('Helvetica', 25))
        self.lblResult.place(x=20, y=230)

        self.lblResultSum = tk.Label(self.master, textvariable=self.resultSum, font=('Helvetica', 45))
        self.lblResultSum.place(x=20, y=310)

        # self.lbPlayer = tk.Listbox(self.master, width=40, height=8)
        # self.lbPlayer.place(x=400, y=40)

        self.eMe = tk.Entry(self.master, textvariable=self.me)
        self.eMe.place(x=500, y=10)

        self.btnSubmitName = tk.Button(self.master, text="Ok", command=self.submitName)
        self.btnSubmitName.place(x=660, y=10)

        self.lbHistory = tk.Listbox(self.master, width=60, height=16)
        self.lbHistory.place(x=420, y=40)

        # self.lblPlayer = tk.Label(self.master, text="Player", font=('Helvetica', 12))
        # self.lblPlayer.place(x=405, y=5)

        self.lblHistory = tk.Label(self.master, text="History", font=('Helvetica', 12))
        self.lblHistory.place(x=425, y=5)


    def coinFlip(self):
        self.coin.set(rnd.choice(['Heads', 'Tail']))

    def submitName(self):
        if self.me.get() == '':
            return
        data = {'action': 'submitName'}
        data.update({'name': self.me.get()})
        self.eMe.lower()
        self.btnSubmitName.lower()
        self.btnRoll.configure(state=tk.NORMAL)
        self.btnCoin.configure(state=tk.NORMAL)
        self.sendMessage(data)

    def roll(self):
        data = {'action': 'roll', 'dice': self.rDice, 'name': self.me.get()}
        data['rolls'] = []
        for n in range(0, self.sNumDice.get()):
            data['rolls'].append(rnd.randint(1, self.rDice))
        self.sendMessage(data)
        self.concResult.set('')
        self.resultSum.set('')
        self.playerName.set('')

    def update(self, _data):
        data = json.loads(_data.decode())
        if data['action'] == 'roll':
            resStr = ''
            self.concResult.set('')
            self.resultSum.set('')
            self.playerName.set(data['name'] + ' rollt:')
            for n in data['rolls'][:-1]:
                resStr += str(n) + ' + '
            else:
                resStr += str(data['rolls'][-1])

            if len(resStr) > 20:
                resStr = resStr[:20] + "\n" + resStr[20:]
            self.concResult.set(resStr)
            hist = data['name'] + ' {}D{}: '.format(len(data['rolls']), data['dice']) + self.concResult.get() + '     '
            if data['dice'] == 6:
                self.resultSum.set(sum(data['rolls']))
                hist += ' [{}]'.format(sum(data['rolls']))
            else:
                self.resultSum.set('')
            self.lbHistory.insert(0, hist)
        elif data['action'] == 'submitName':
            self.lbHistory.insert(0, '{} joined'.format(data['name']))
            # self.lbPlayer.insert(tk.END, data['name'])
        elif data['action'] == 'drop':
            self.lbHistory.insert(0, '{} left'.format(data['name']))
            # try:
                # self.lbPlayer.delete(self.lbPlayer.get(0, tk.END).index(data['name']))
            # except ValueError:
            #     pass
        # elif data['action'] == 'elo':
            # self.lbPlayer.delete(0, tk.END)
            # self.lbPlayer.insert(0, data['name'])
            # self.sendMessage({'action': 'elo', 'name': self.me.get()})

    def setServer(self, serv):
        self.server = serv

    def sendMessage(self, data):
        self.server.send(json.dumps(data).encode())

class ServerApp(threading.Thread):

    socket = None
    host = ""
    port = 0
    callback = False

    def __init__(self, ip, port, function):
        threading.Thread.__init__(self)
        self.host = ip
        self.port = port
        self.terminate = threading.Event()
        self.callback = function

    def run(self):
        #initialize the Socket
        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        print(self.sock)

        #MessageLoop
        while not self.terminate.is_set():
            self.listen()
        print('socket closed\nexit cleanly')

    def send(self,message):
        self.sock.sendall(message)

    def listen(self):
        try:
            message = self.sock.recv(4096)
        except OSError:
            return
        self.callback(message)

class ServiceExit(Exception):
    pass

def serviceExit(signum=signal.SIGINT, frame=None):
    print('\ninterrupt detected, running cleanup')
    raise ServiceExit

def main():
    signal.signal(signal.SIGTERM, serviceExit)
    signal.signal(signal.SIGINT, serviceExit)
    def destroy():
        if app.me.get() != '':
            app.sendMessage({'action': 'drop', 'name': app.me.get()})
        root.destroy()
    root = tk.Tk()
    root.protocol('WM_DELETE_WINDOW', destroy)
    app = App()
    server = ServerApp("noobfilter.eu", 11100, app.update)
    app.setServer(server)
    try:
        server.start()
        root.mainloop()
    except (ServiceExit, KeyboardInterrupt):
        pass
    server.terminate.set()
    server.sock.close()
    server.join()

if __name__ == "__main__":
    main()

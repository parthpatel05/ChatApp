# second app to run, also pre sep 2022 version
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
import socket
import threading

# chat bot made using tutorial by Python Engineer
from chat import getResponse

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

client = None
address = None

class Manager(ScreenManager):
    WelcomeScreen = ObjectProperty(None)
    ChatScreen = ObjectProperty(None)
    AIChatScreen = ObjectProperty(None)


class WelcomeScreen(Screen):
    def on_enter(self):
        global s, r, client, address
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # send connection, will recieve messages
        r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # recieve connection, will make client/address from
        client, address = None, None
        Clock.schedule_once(self.showIP)

    def showIP(self, dt):
        self.ids.ipLabel.text = local_ip


    def aiBtn(self):
        #show_AIPop()
        self.manager.current = "aichatscreen"

    def sendBtn(self):
        show_SendPop()

    def waitBtn(self):
        show_RecievePop()

    def testBtn(self):
        print("test")
        self.manager.current = "chatscreen"





class ChatScreen(Screen):
    def on_enter(self, *args):
        recThread = threading.Thread(target=self.reciever)
        recThread.start()

    def send(self):# sends messages
        message = self.ids.inputBox.text
        self.ids.inputBox.text = ""
        self.ids.chat.text = self.ids.chat.text + local_ip +": " + message + "\n"
        print(message)
        client.send(message.encode())

    def reciever(self):# recieves messages
        end_connection = False
        while not end_connection:
            message = s.recv(1024).decode()
            if len(message) > 0:
                self.ids.chat.text = self.ids.chat.text + address[0] +": " + message + "\n"
                print(message)
            else:  # if conection closed
                end_connection = True
                print("-!-!-!-connection ended-!-!-!-")


    def clearChat(self):
        self.ids.chat.text = ""


class InfoScreen(Screen):
    pass

class AIChatScreen(Screen):
    def on_enter(self, *args):
        self.ids.inputBox.text = ""
        print(self.ids.inputBox.text)
        self.ids.chat.text = self.ids.chat.text +"AI : " +"Let's Chat \n"

    def send(self):
        message = self.ids.inputBox.text
        self.ids.inputBox.text = ""
        self.ids.chat.text = self.ids.chat.text + local_ip + ": " + message + "\n"
        print(message)
        res = getResponse(message)
        self.ids.chat.text = self.ids.chat.text + "AI" + ": " + res + "\n"



# this is when we put ai on server and need to connect with sockets
class AIPop(FloatLayout):
    pass

def show_AIPop():
    show = AIPop()

    popupWindow = Popup(title="Connecting", content=show, size_hint=(None,None),size=(400,400))


    popupWindow.open()
# end future ai

class SendPop(FloatLayout):
    otherIP = None
    ref = None

    def tBtn(self):
        self.ids.enterBtn.disabled = True
        self.ids.contBtn.disabled = False


    def Btn(self):
        self.otherIp = self.ids.Ip.text
        t2 = threading.Thread(target=self.connect)

        t2.start()

        print(self.otherIp)
        self.ids.Connecting.text = "Connecting..."
        self.ids.enterBtn.disabled = True


    def connect(self):
        global client, address
        s.connect((self.otherIp, 55555))

        # recieve the connection, making sender socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        r.bind((local_ip, 55556))
        r.listen()

        # conecting to a specific client
        client_acquired = False
        while not client_acquired:
            client, address = r.accept()
            if len(address) > 0:
                if address[0] == self.otherIp:
                    client_acquired = True

        self.tBtn()


    def dis(self):
        print(self.ref)
        self.ref.dismiss()


def show_SendPop():
    show = SendPop()

    popupWindow = Popup(title="Connecting", content=show, size_hint=(None,None),size=(400,400))

    show.ref = popupWindow
    popupWindow.open()


class RecievePop(FloatLayout):
    ref = None

    def oneTime(self):
        self.ids.scanBtn.disabled = True
        self.press()

    def press(self):
        global local_ip
        self.ids.acceptBtn.disabled = True
        self.ids.declineBtn.disabled = True
        print(local_ip)
        r.bind((local_ip, 55555))


        print("listening: ...")
        # run waiter in thread
        waiterThread = threading.Thread(target=self.waiter)
        waiterThread.start()
        waiterThread.join()

        # when waiter returns, enable accept/ decline
        self.ids.acceptBtn.disabled = False
        self.ids.declineBtn.disabled = False
        """"""

        # if accept(new function) make the objects, enable cont
        # if decline(new function) disable acc/dec and call press

    def waiter(self):# waits for connection, when it comes updates client/address and returns to press
        global client, address
        r.listen()
        client_acquired = False
        while not client_acquired :
            client, address = r.accept()
            if len(address) > 0:
                # update ipLabel
                self.ids.ipLabel.text = address[0]
                print("This person is trying to connect to you")
                print(address)
                client_acquired = True

    def accepted(self):
        s.connect((address[0], 55556))
        self.ids.acceptBtn.disabled = True
        self.ids.declineBtn.disabled = True

        self.ids.contBtn.disabled = False


    def declined(self):
        self.press()
        print("declined")

    def dis(self):
        print(self.ref)
        self.ref.dismiss()

def show_RecievePop():
    show = RecievePop()

    popupWindow = Popup(title="Connecting", content=show, size_hint=(None,None),size=(400,400))

    show.ref = popupWindow
    popupWindow.open()


class MyApp(App):
    def build(self):
        self.m = Manager(transition=NoTransition())


if __name__ == "__main__":
    MyApp().run()
    #client.close()
    #s.close()
    #r.close()


# todo timeout when connecting
# todo when endchat should retrun to main window
# todo make ai
# todo change info btn to point to info screen

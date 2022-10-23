import tkinter
import threading
import datetime
import time
app = tkinter.Tk()
app . overrideredirect (True )
app. attributes('-alpha', 0.9)
app. attributes('-topmost',1)
app. geometry( '130x25+100+100 ')
labelDateTime = tkinter . Label(app, width=130)
labelDateTime .pack(fill=tkinter .BOTH，expand=tkinter.YES)
labelDateTime .configure(bg = 'gray')
X = tkinter.IntVar(value=0)
Y = tkinter.IntVar(value=0)
canMove = tkinter .IntVar(value=0)
still = tkinter .IntVar(value=1)
def onLeftButtonDown( event):
app.attributes('-alpha',0.4)
X.set(event.x)
Y.set(event.y)
canMove.set(1)
labelDateTime.bind('<Button-1>',onLeftButtonDown)
def onLeftButtonUp(event) :
    app.attributes('-alpha',0.9)
    canMove.set(0)
labelDateTime.bind('<ButtonRelease-1>',onLeftButtonUp)
def onLeftButtonMove (event):
    if canMove.get()==0:
        return
    newX = app.winfo_x()+(event.x-X.get())
    newY = app.winfo_y()+(event.y-Y.get())
    labelDateTime .bind('<ButtonRelease-1>',onLeftButtonUp)
def onLeftButtonMove (event):
if canMove.get()==0:
return
newX = app.winfo_ x()+(event.x-X.get())
newY = app.winfo_ y()+(event.y-Y.get())
g = '130x25+'+str(newX)+'+'+str(newY)
app.geometry(g)
labelDateTime .bind('<B1 -Motion>',onLeftButtonMove)
def onRightButtonDown(event):
    still. set(0)   
    t.join(0.2)
    app .destroy( )
labelDateTime .bind('<Button-3>'onRight ButtonDown)
def nowDateTime( ):
    while still.get( )==1:
        s = str( datetime .datetime .now())[:19]
        labelDateTime[ 'text'] = S
        time.sleep(0.2)
t = threading.Thread(target=nowDateTime)
t.daemon = True
t.start( )
app.main1oop( )
import tkinter as tk
from random import choice
import cv2
import os
import pygame
import re
import sqlite3
import subprocess
import threading
import time
from PIL import Image

total = []



class mainw(object):
    def win1(self):
        self.i=1
        self.root = tk.Tk()
        self.root.title('carrito')
        #root.iconbitmap('logo_aposento_nuevo_01_rKM_icon.ico')
        self.root.geometry('1000x528+0+0')
        self.root.configure(background='#266fb7')
        self.titulo = tk.Frame(self.root, width=1000, height=40, bd=0, relief='flat',background='grey')
        self.titulo.pack(side="top")
        self.arriba = tk.Frame(self.root, width=1000, height=521.5, bd=0, relief='flat', background='#ffffff')
        self.arriba.pack(side="top")
        
        self.cam = tk.Frame(self.arriba, width=800, height=481.5, bd=3, relief='sunken',background='#ffffff')
        self.cam.pack(side="left")
        self.items = tk.Frame(self.arriba, width=380, height=481.5, bd=0, relief='flat',background='#ffffff')
        self.items.pack(side="right")
        
        self.petra = tk.Label(self.titulo,font=('arial', 20, 'bold'), text='Petra market ', bd=10, background='#266fb7', fg='#ffffff' )
        self.petra.pack()
        self.objetos= tk.Text(self.items,height=17,bd=0,relief="flat",foreground="#898a8c",highlightbackground="#ffffff")
        self.objetos.pack()
        self.objetos.config(state='disable')
        self.total= tk.Text(self.items,height=4,bd=0,relief="flat",foreground="#898a8c",highlightbackground="#ffffff")
        self.total.pack()
        self.total.config(state='disable')

        self.listo = tk.Button(self.items, text='Listo', padx=15, pady=10, bd=0, fg='#ffffff', background='#266fb7',command = self.listo).pack(pady=10)

        width, height = 800, 600
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.root.bind('<Escape>', lambda e: self.root.quit())
        self.lmain = tk.Label(self.cam)
        self.lmain.pack()
        _, uframe = self.cap.read()
        self.frame = cv2.flip(uframe, 1)
        
        cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = Image.PhotoImage(image=img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        self.lmain.after(10, self.show_frame)
        self.root.mainloop()

    def codigo(self):
        longitud = 5.
        valores = "12345"
        p = ""
        p = p.join([choice(valores) for i in range(longitud)])

        return p

    def show_frame(self):
        
        _, uframe = self.cap.read()
        self.frame = cv2.flip(uframe, 1)
        
        cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = Image.PhotoImage(image=img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        self.lmain.after(10, self.show_frame)
      
    def clasificar(self):     
        arch = open("output.txt","w")
        while True:
            time.sleep(2)
            img_counter = 0
            img_name = "imagenopencv"+".png".format(img_counter)
            cv2.imwrite(img_name,self.frame)
            os.rename(img_name,"\Users\juanm\Documents\tensorflow-prog5\carrito.py"+img_name)
            imgsub = '--image=\Users\juanm\Documents\tensorflow-prog5\carrito.py'+img_name
            scr= subprocess.Popen(['python','-m','scripts.label_image','--graph=tf_files/retrained_graph.pb',imgsub], stdout=subprocess.PIPE,stderr=subprocess
            .PIPE)
            output = str(scr.stdout.read())
            des = scr.stderr.read()
            out= output.split("\\n")
            for item in out:
                if re.search('b',item):
                    nomI = item.index('b')
                    self.nom = item[nomI+2:(item.index("("))-1]
                    self.valor = item[(item.index("="))+1:(item.index(")"))]
                    
                    if float(self.valor) > 0.95:
                        tot = 0
                        precio = self.precio()[0][0]
                        total.append(precio)
                        for a in total:
                            tot = tot+a
    
                        tex = str(self.i)+". "+str(self.nom)+"\t\t"+str(precio)+"\n"
                        self.objetos.config(state='normal')
                    
                        self.objetos.insert(tk.END,tex)
                        self.objetos.config(state='disable')
                        self.total.config(state='normal')
                        self.total.delete(1.0,tk.END)

                        self.total.insert(tk.END,str(tot))
                        pygame.init()  
                        bar = pygame.mixer.Sound("barcode.wav")
                        bar.play()                   
                        self.i += 1
                
            os.remove('\Users\juanm\Documents\tensorflow-prog5\carrito.py'+img_name)
    def listo(self):

        for a in total:
            total.remove(a)
        
        self.i = 1
        self.objetos.config(state='normal')
                    
        self.objetos.delete(1.0,tk.END)
        self.objetos.config(state='disable')
        self.total.config(state='normal')
        self.total.delete(1.0,tk.END)
        pygame.init()  
        bar = pygame.mixer.Sound("Caja.wav")
        bar.play()  
        
    def precio (self):
        db = sqlite3.connect('productos.db')
        cursor = db.cursor()
        cursor.execute('''SELECT precio FROM productos where producto = ?''',(self.nom,))
        prod = cursor.fetchall()
        return prod

    def entrenar (self):
        

        scr= subprocess.Popen(['python','-m','scripts.label_image','--graph=tf_files/retrained_graph.pb',imgsub], stdout=subprocess.PIPE,stderr=subprocess
            .PIPE)


if __name__ == '__main__':
    window = mainw() 
    hilo = threading.Thread(target=window.clasificar)
    hilo.start()
    window.win1()
   

from os import system
from tkinter import *
from tkinter import ttk
from typing import Sized
from xml.etree.ElementTree import ProcessingInstruction
import xml.etree.cElementTree as ET
from xml.dom import minidom
from PIL import ImageTk, Image
from tkinter import filedialog as FileDialog
from Analizar_Maquina import AMaquina
from Analizar_Simulacion import ASimulacion
from ListaSeleccionados import ColaS, nodoS
from ListaEstado import ColaE, nodoE
import time
import subprocess
import threading

class app():
    def __init__(self):
        self.root = Tk()
        self.rut1=''
        
        self.rep=False
        self.camb=False
        self.cont=0
        
        #Configurando ventana
        self.root.title("DIGITAL INTELLIGENCE S.A.")
        self.root.iconbitmap("icono.ico")
        self.root.resizable(False,False)
        self.root.geometry("675x650")
        self.root.configure(bg="#1D1E1B")

        #Agregando menú
        self.menu()

        #Titulo
        Label(self.root,text="DIGITAL INTELLIGENCE S.A.",fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 30, "bold"),borderwidth = 2,width = 30,relief="ridge").place(x=20,y=20)

        self.tabControl = ttk.Notebook(self.root)

        img=PhotoImage(file='min.png')
        self.Proceso(img)
        self.Reportes(img)
        
        self.tabControl.place(x=20,y=75)
        self.root.mainloop()

    def menu(self):
        menubar = Menu(self.root)

        #Menú Cargar
        Cmenu = Menu(menubar)
        Cmenu.add_command(label="Archivo de configuración", command=self.BusArchvivoConfig)
        Cmenu.add_command(label="Archivo de simulación", command=self.BusArchvivoSimul)
        Cmenu.add_command(label="Salir",command=exit)
        menubar.add_cascade(label="Cargar", menu=Cmenu)

        #Menú Ayuda
        Amenu = Menu(menubar)
        Amenu.add_command(label="Información del estudiante", command=self.InfoE)
        Amenu.add_command(label="Información de la aplicación", command=self.InfoA)

        menubar.add_cascade(label="Ayuda", menu=Amenu)

        self.root.config(menu=menubar)

    def Reportes(self,img):
        self.root.option_add('*TCombobox*Listbox*Background', '#1D1E1B')
        self.root.option_add('*TCombobox*Foreground', '#D90808')
        self.root.option_add('*TCombobox*Font', ("Fixedsys", 14, "bold"))
        

        tab1 = Frame(self.tabControl)
        tab1.config(bg="#1D1E1B", width=635, height=525)
        
        Label(tab1, text="Reporte XML: ", wraplength=890,fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 14, "bold")).place(x=10,y=10)
        #componentes
        componentes = Frame(tab1)
        scrollbarY = ttk.Scrollbar(componentes,orient=VERTICAL)
        scrollbarX = ttk.Scrollbar(componentes,orient=HORIZONTAL)
        self.LRXML = Listbox(componentes, width=32, height=4, xscrollcommand=scrollbarX.set, yscrollcommand=scrollbarY.set, bg="#1D1E1B", fg="#D90808",font=("Fixedsys", 14, "bold"))
        #for i in range(20):
            #self.LRXML.insert(END, "Elementoooooooooooooooooooooooooooooooo {}".format(i))
        scrollbarY.config(command=self.LRXML.yview)
        scrollbarY.pack(side=RIGHT, fill=Y)
        scrollbarX.config(command=self.LRXML.xview)
        scrollbarX.pack(side=BOTTOM, fill=X)
        self.LRXML.pack()
        componentes.place(x=10,y=40)

        Label(tab1, text="Reporte HTML: ", wraplength=890,fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 14, "bold")).place(x=10,y=180)
        #componentes
        componentes = Frame(tab1)
        scrollbarY = ttk.Scrollbar(componentes,orient=VERTICAL)
        scrollbarX = ttk.Scrollbar(componentes,orient=HORIZONTAL)
        self.LRHTML = Listbox(componentes, width=32, height=4, xscrollcommand=scrollbarX.set, yscrollcommand=scrollbarY.set, bg="#1D1E1B", fg="#D90808",font=("Fixedsys", 14, "bold"))
        #for i in range(20):
            #self.LRHTML.insert(END, "Elementoooooooooooooooooooooooooooooooo {}".format(i))
        scrollbarY.config(command=self.LRHTML.yview)
        scrollbarY.pack(side=RIGHT, fill=Y)
        scrollbarX.config(command=self.LRHTML.xview)
        scrollbarX.pack(side=BOTTOM, fill=X)
        self.LRHTML.pack()
        componentes.place(x=10,y=210)
        
        Label(tab1, text="Reporte Graphviz: ", wraplength=890,fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 14, "bold")).place(x=10,y=350)
        #componentes
        componentes = Frame(tab1)
        scrollbarY = ttk.Scrollbar(componentes,orient=VERTICAL)
        scrollbarX = ttk.Scrollbar(componentes,orient=HORIZONTAL)
        self.LRGraph = Listbox(componentes, width=32, height=4, xscrollcommand=scrollbarX.set, yscrollcommand=scrollbarY.set, bg="#1D1E1B", fg="#D90808",font=("Fixedsys", 14, "bold"))
        #for i in range(20):
            #self.LRGraph.insert(END, "Elementoooooooooooooooooooooooooooooooo {}".format(i))
        scrollbarY.config(command=self.LRGraph.yview)
        scrollbarY.pack(side=RIGHT, fill=Y)
        scrollbarX.config(command=self.LRGraph.xview)
        scrollbarX.pack(side=BOTTOM, fill=X)
        self.LRGraph.pack()
        componentes.place(x=10,y=380)
        
        Button(tab1,text='Generar',fg="#FFFFFF", bg="#D90808", font=("Fixedsys", 14, "bold"), command=lambda: self.genXML()).place(x=460,y=80)
        Button(tab1,text='Generar',fg="#FFFFFF", bg="#D90808", font=("Fixedsys", 14, "bold"), command=lambda: self.genHTML()).place(x=460,y=245)
        Button(tab1,text='Generar',fg="#FFFFFF", bg="#D90808", font=("Fixedsys", 14, "bold"), command=lambda: self.genGraph()).place(x=460,y=410)
        self.tabControl.add(tab1, text = 'Reportes')

    def Proceso(self,img):
        self.root.option_add('*TCombobox*Listbox*Background', '#1D1E1B')
        self.root.option_add('*TCombobox*Foreground', '#D90808')
        self.root.option_add('*TCombobox*Font', ("Fixedsys", 14, "bold"))
        

        tab1 = Frame(self.tabControl)
        tab1.config(bg="#1D1E1B", width=635, height=525)
        
        Label(tab1, text="Archivo de configuración: ", wraplength=890,fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 14, "bold")).place(x=10,y=10)
        self.Rutaa1=Label(tab1, text="...", wraplength=620,fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 11, "bold"))
        self.Rutaa1.place(x=10,y=30)

        Label(tab1, text="Archivo de simulación: ", wraplength=890,fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 14, "bold")).place(x=10,y=60)
        self.Rutaa2=Label(tab1, text="...", wraplength=620,fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 11, "bold"))
        self.Rutaa2.place(x=10,y=80)

        Label(tab1, text="Producto que se está trabajando: ", wraplength=890,fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 14, "bold")).place(x=10,y=110)
        self.Producto=Label(tab1, text="...", wraplength=620,fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 14, "bold"))
        self.Producto.place(x=10,y=140)

        Label(tab1, text="Componentes necesarios: ", wraplength=890,fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 14, "bold")).place(x=10,y=180)
        #componentes
        componentes = Frame(tab1)
        scrollbar = ttk.Scrollbar(componentes,orient=VERTICAL)
        self.listComponentes = Listbox(componentes, width=19, height=5, yscrollcommand=scrollbar.set, bg="#1D1E1B", fg="#D90808",font=("Fixedsys", 14, "bold"))
        #for i in range(2):
            #self.listComponentes.insert(END, "Elemento {}".format(i))
        scrollbar.config(command=self.listComponentes.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.listComponentes.pack()
        componentes.place(x=10,y=210)


        #componentes
        componentes = Frame(tab1)
        scrollbarY = ttk.Scrollbar(componentes,orient=VERTICAL)
        scrollbarX = ttk.Scrollbar(componentes,orient=HORIZONTAL)
        self.listEnsam = Listbox(componentes, width=32, height=13, xscrollcommand=scrollbarX.set, yscrollcommand=scrollbarY.set, bg="#1D1E1B", fg="#D90808",font=("Fixedsys", 14, "bold"))
        #for i in range(2):
            #self.listEnsam.insert(END, "Elemento {}".format(i))
        scrollbarY.config(command=self.listEnsam.yview)
        scrollbarY.pack(side=RIGHT, fill=Y)
        scrollbarX.config(command=self.listEnsam.xview)
        scrollbarX.pack(side=BOTTOM, fill=X)
        self.listEnsam.pack()
        componentes.place(x=250,y=210)

        self.pb = ttk.Progressbar(tab1,orient='horizontal',mode='determinate',length=230, maximum=100)
        self.pb.place(x=10,y=350)

        tabimg = Canvas(tab1,width=100,height=100, bg="black")
        tabimg.create_image(0,0,image=img,anchor="nw")
        tabimg.place(x=10,y=400)

        self.tiempo=Label(tab1, text="tiempo ", wraplength=890,fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 14, "bold"))
        self.tiempo.place(x=120,y=440)

        self.hilo1 = threading.Thread(target=self.Simulacion)

        Button(tab1,text='Iniciar',fg="#FFFFFF", bg="#D90808", font=("Fixedsys", 14, "bold"), command=self.hilo1.start).place(x=530,y=160)

        self.tabControl.add(tab1, text = 'Proceso')

    def InfoE(self):
        win = Toplevel()
        win.wm_title("Window")
        win.resizable(False,False)
        win.config(height=200,width=530,bg="#1D1E1B")
        win.title("Información del estudiante")
        win.iconbitmap("icono.ico")

        Label(win, text="Javier Alejandro Gutierrez de León",fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 15, "bold")).place(x=10,y=10)
        Label(win, text="202004765",fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 15, "bold")).place(x=10,y=40)
        Label(win, text="Introducción a la Programación y Computación 2 sección A",fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 15, "bold")).place(x=10,y=70)
        Label(win, text="Ingeniería en Ciencias y Sistemas",fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 15, "bold")).place(x=10,y=100)
        Label(win, text="4to Semestre",fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 15, "bold")).place(x=10,y=130)

        Button(win,text='Aceptar',fg="#FFFFFF", bg="#D90808", font=("Fixedsys", 14, "bold"),command=win.destroy).place(x=210,y=155)

    def InfoA(self):
        win = Toplevel()
        win.wm_title("Window")
        win.resizable(False,False)
        win.config(height=230,width=530,bg="#1D1E1B")
        win.title("Información de la aplicación")
        win.iconbitmap("icono.ico")

        Label(win, text="En esta aplicación se pueden crear simulaciones del tiempo que toma ensamblar un producto que se solicite, según la configuración establecida por el usuario. \n\n Programado en Python 3.9.6 \n Reportes generados con Graphviz y HTML5",fg="#D90808", wraplength=510,bg="#1D1E1B", font=("Fixedsys", 15, "bold")).place(x=10,y=10)
        
        Button(win,text='Aceptar',fg="#FFFFFF", bg="#D90808", font=("Fixedsys", 14, "bold"),command=win.destroy).place(x=210,y=180)

    def BusArchvivoConfig(self):
        win = Toplevel()
        win.wm_title("Window")
        win.resizable(False,False)
        win.config(height=150,width=530,bg="#1D1E1B")
        win.title("Cargar Archivo de Configuración")
        win.iconbitmap("icono.ico")

        Label(win, text="Buscar Archivo",fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 15, "bold")).place(x=10,y=10)
        self.rut1=Entry(win,width=37, text="",fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 15, "bold"))
        self.rut1.place(x=10,y=40)
        Button(win,text='Buscar',fg="#FFFFFF", bg="#D90808", font=("Fixedsys", 14, "bold"),command=lambda: self.Ruta1()).place(x=430,y=40)
        
        Button(win,text='Aceptar',fg="#FFFFFF", bg="#D90808", font=("Fixedsys", 14, "bold"),command=win.destroy).place(x=210,y=100)

    def Ruta1(self):
        #Utilizando fliedialog de tkinter para abrir un archivo
        ruta=FileDialog.askopenfilename(title="Abrir un fichero")
        self.rut1.delete(0,END)
        self.rut1.insert(0, ruta)
        self.Rutaa1.config(text=ruta)

    def Finalizado(self,Nombre):
        win = Toplevel()
        win.wm_title("Window")
        win.resizable(False,False)
        win.config(height=150,width=330,bg="#1D1E1B")
        win.title("Cargar Archivo de Configuración")
        win.iconbitmap("icono.ico")

        Label(win, text="Simulación de {}, finalizada con exito".format(Nombre), wraplength=300,fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 15, "bold")).place(x=10,y=10)
        
        Button(win,text='Aceptar',fg="#FFFFFF", bg="#D90808", font=("Fixedsys", 14, "bold"),command=win.destroy).place(x=210,y=100)

    def BusArchvivoSimul(self):
        win = Toplevel()
        win.wm_title("Window")
        win.resizable(False,False)
        win.config(height=150,width=530,bg="#1D1E1B")
        win.title("Cargar Archivo de Simulación")
        win.iconbitmap("icono.ico")

        Label(win, text="Buscar Archivo",fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 15, "bold")).place(x=10,y=10)
        self.rut2=Entry(win,width=37, text="",fg="#D90808", bg="#1D1E1B", font=("Fixedsys", 15, "bold"))
        self.rut2.place(x=10,y=40)
        Button(win,text='Buscar',fg="#FFFFFF", bg="#D90808", font=("Fixedsys", 14, "bold"),command=lambda: self.Ruta2()).place(x=430,y=40)
        
        Button(win,text='Aceptar',fg="#FFFFFF", bg="#D90808", font=("Fixedsys", 14, "bold"),command=win.destroy).place(x=210,y=100)

    def Ruta2(self):
        #Utilizando fliedialog de tkinter para abrir un archivo
        ruta=FileDialog.askopenfilename(title="Abrir un fichero")
        self.rut2.delete(0,END)
        self.rut2.insert(0, ruta)
        self.Rutaa2.config(text=ruta)

    def Simulacion(self):
        
        while self.Rutaa1.cget("text")!="..." and self.Rutaa2.cget("text")!="...":
            self.HTML=''
            print(self.Rutaa1.cget("text"))
            print(self.Rutaa2.cget("text"))
            self.ObjMaquina=AMaquina.AnalizarArchivoM(self.Rutaa1.cget("text"))
            simulacion=ASimulacion.AnalizarArchivoS(self.Rutaa2.cget("text"))
            #print('L1')
            #print(ObjMaquina.retornar_seleccionado(1).getListLineas().retornar_seleccionado(1).getTEnsamblaje())
            #print('L2')
            #print(ObjMaquina.retornar_seleccionado(1).getListLineas().retornar_seleccionado(2).getTEnsamblaje())

            #************************** Configuracion Maquina **************************
            
            print('Nombre: '+simulacion.getNombreS())
            self.listEnsam.insert(END, "Nombre: {}".format(simulacion.getNombreS()))
            #Insertando XML
            
            self.SalidaXML = ET.Element("SalidaSimulacion")
            self.NomXML = ET.SubElement(self.SalidaXML, "Nombre").text=str(simulacion.getNombreS())
            self.ListProductos = ET.SubElement(self.SalidaXML, "ListadoProductos")
            #Insertando componentes a la lista de HTML
            self.LRHTML.insert(END, simulacion.getNombreS())
            #Insertando componentes a la lista de XML
            self.LRXML.insert(END, simulacion.getNombreS())
                       
            self.NombreSimulacion=simulacion.getNombreS()
            self.HTML+='''<html lang="en">
            <head>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
                <meta name="description" content="" />
                <meta name="author" content="" />
                <title>{}</title>
                <link rel="icon" type="image/x-icon" href="assets/favicon.ico" />
                <script src="https://use.fontawesome.com/releases/v5.15.3/js/all.js" crossorigin="anonymous"></script>
                <link href="https://cdnjs.cloudflare.com/ajax/libs/simple-line-icons/2.5.5/css/simple-line-icons.min.css" rel="stylesheet" />
                <link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,700,300italic,400italic,700italic" rel="stylesheet" type="text/css" />
                <link href="css/styles.css" rel="stylesheet" />
            </head>

            <body id="page-top">
                <header class="masthead d-flex align-items-center">
                    <div class="container px-4 px-lg-5 text-center">
                        <h1 class="mb-1">{}</h1>
                    </div>
                </header>
                <section class="content-section bg-light" id="about">
                    <div class="container px-4 px-lg-5 text-center">'''.format(simulacion.getNombreS(),simulacion.getNombreS())

            #************************** Configuracion Maquina **************************
            self.ConfMaq=self.ObjMaquina.retornar_seleccionado(1)
            print('Lineas de ensamblaje'+self.ConfMaq.getNoLineas())
            liss=self.ConfMaq.getListLineas()
            liss.mostrar()

            i=1
            Simular=False
            while simulacion.getListP().retornar_seleccionado(i) != None:
                #print(simulacion.getListP().retornar_seleccionado(i).getNombre())
                j=1
                while self.ConfMaq.getListProductos().retornar_seleccionado(j) != None:
                    if simulacion.getListP().retornar_seleccionado(i).getNombre() == self.ConfMaq.getListProductos().retornar_seleccionado(j).getNombre():
                        Simular=True
                        #Insertando componentes a la lista de ensamblaje
                        self.listEnsam.insert(END, self.ConfMaq.getListProductos().retornar_seleccionado(j).getNombre())
                        self.HTML+='<br><h1>{}</h1><br>\n<table class="table table-striped table-dark">'.format(self.ConfMaq.getListProductos().retornar_seleccionado(j).getNombre())
                        self.ProductoXML=ET.SubElement(self.ListProductos, "Producto")
                        ET.SubElement(self.ProductoXML, "Nombre").text=str(self.ConfMaq.getListProductos().retornar_seleccionado(j).getNombre())
                        self.ElabOptima=ET.SubElement(self.ProductoXML, "ElaboracionOptima")
                        #Cambiando label por producto que se está trabajando
                        self.Producto.config(text=self.ConfMaq.getListProductos().retornar_seleccionado(j).getNombre())
                        #Insertando componentes a la lista de Productos
                        self.listComponentes.insert(END, self.ConfMaq.getListProductos().retornar_seleccionado(j).getNombre())
                        
                        #Insertando componentes a la lista de Graficas
                        self.LRGraph.insert(END, self.ConfMaq.getListProductos().retornar_seleccionado(j).getNombre())
                        
                        print(self.ConfMaq.getListProductos().retornar_seleccionado(j).getNombre())
                        c2=self.ConfMaq.getListProductos().retornar_seleccionado(j).getCola()
                        
                        k=1
                        while c2.retornar_seleccionado(k) != None:
                            self.listComponentes.insert(END, "Linea {} Columna {}".format(c2.retornar_seleccionado(k).getLinea(),c2.retornar_seleccionado(k).getComponente()))
                            k+=1
                        self.armar(self.ConfMaq.getNoLineas(),c2)
                    j+=1
                
                if Simular:
                    self.Finalizado(simulacion.getListP().retornar_seleccionado(i).getNombre())
                    time.sleep(2)
                i+=1
            self.HTML+="</div></section>"
            self.HTML+='''<a class="scroll-to-top rounded" href="#page-top"><i class="fas fa-angle-up"></i></a>
                            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/js/bootstrap.bundle.min.js"></script>
                            <script src="js/scripts.js"></script>
                        </body>
                    </html>'''
            f = open(self.NombreSimulacion+'.html','w')
            f.write(self.HTML)
            f.close()
            break
        
    def armar(self,n,cola):
        
        print("Numero de Lineas "+n)
        self.NLineas=n
        self.HTML+='<thead><tr>'
        for x in range(1,int(n)+1):
            self.HTML+='<th scope="col">{}</th>'.format('Linea '+str((int(x))))
        self.HTML+='</tr>\n</thead>\n<tbody>\n'
        colaaa=cola 
        ListaSelec=ColaS()
        Estado=ColaE()
        x=1
        L=0
        C=0
        for x in range(int(n)+1):
            k=1  
            while colaaa.retornar_seleccionado(k) != None:
                if x == int(colaaa.retornar_seleccionado(k).getLinea()):
                    L=colaaa.retornar_seleccionado(k).getLinea()
                    C=colaaa.retornar_seleccionado(k).getComponente()
                    print("Linea {} Componente {}".format(colaaa.retornar_seleccionado(k).getLinea(),colaaa.retornar_seleccionado(k).getComponente()))
                    break
                k+=1 
            if L!=0:
                if int(L)==int(x):
                    t=self.ConfMaq.getListLineas().retornar_seleccionado(x).getTEnsamblaje()
                    print(t)
                    ListaSelec.insertar(nodoS(L,C,0,False,t))
                    Estado.insertar(nodoE(L,'Iniciando'))
                else:
                    t=self.ConfMaq.getListLineas().retornar_seleccionado(x).getTEnsamblaje()
                    print(t)
                    ListaSelec.insertar(nodoS(x,C,0,False,t))
                    Estado.insertar(nodoE(x,'No se usa'))
                


        self.recorrer(ListaSelec,colaaa,n,Estado)
             
    def genHTML(self):
        for i in self.LRHTML.curselection():
            print(self.LRHTML.get(i))
            system('{}.html'.format(str(self.LRHTML.get(i))))
            
    def genXML(self):
        for i in self.LRXML.curselection():
            print(self.LRXML.get(i))
            system('{}.xml'.format(str(self.LRHTML.get(i))))

    def genGraph(self):
        ObjMaquina=AMaquina.AnalizarArchivoM(self.Rutaa1.cget("text"))
        ConfMaq=ObjMaquina.retornar_seleccionado(1)
        for i in self.LRGraph.curselection():
            print(self.LRGraph.get(i))
            j=1
            while ConfMaq.getListProductos().retornar_seleccionado(j) != None:
                if self.LRGraph.get(i) == ConfMaq.getListProductos().retornar_seleccionado(j).getNombre():
                    c2=ConfMaq.getListProductos().retornar_seleccionado(j).getCola()
                    k=1
                    contenido='digraph G {rankdir=LR '
                    while c2.retornar_seleccionado(k) != None:
                        if c2.retornar_seleccionado(k+1) != None:
                            contenido+='L{}C{} ->'.format(c2.retornar_seleccionado(k).getLinea(),c2.retornar_seleccionado(k).getComponente())
                        else:
                            contenido+='L{}C{}'.format(c2.retornar_seleccionado(k).getLinea(),c2.retornar_seleccionado(k).getComponente())
                        k+=1   
                    contenido+='}'
                    f = open ('img.txt','w')
                
                    f.write(contenido)
                    f.close()
                    subprocess.run('bin\dot.exe -Tpng img.txt -o {}.png'.format(self.LRGraph.get(i)))
                    print("Imagen generada")
                j+=1
        system('{}.png'.format(str(self.LRGraph.get(i)))) 

    def recorrer(self, Ls, colaE,n,Estado):
        self.tiempo.config(text="0s")
        tiempo=0
        self.cont=0
        cambio=False
        
        self.lim=colaE.long()

        prog = threading.Thread(target=self.progreso)
        prog.start()

        self.HTML+=''

        while colaE.retornar_seleccionado(1)!=None:
            cambio=False
            for c in range(1,int(n)+1,1):
                L=Ls.retornar_seleccionado(c).getLinea()
                C=Ls.retornar_seleccionado(c).getComponente()
                P=Ls.retornar_seleccionado(c).getPosicion()
                es=Ls.retornar_seleccionado(c).getEstado()
                T=int(Ls.retornar_seleccionado(c).getTE())
                TT=0
                if L!=0:
                    TT=int(self.ObjMaquina.retornar_seleccionado(1).getListLineas().retornar_seleccionado(1).getTEnsamblaje())
                print(TT)
                #self.ConfMaq.getListLineas().retornar_seleccionado(x).getTEnsamblaje()
                if int(C) == int(P):
                    try:
                        if str(colaE.retornar_seleccionado(1).getLinea())==str(L) and str(colaE.retornar_seleccionado(1).getComponente())==str(C):
                            k=1
                            if es==True:
                                
                                if T==1:
                                    colaE.EliminarP()
                                    
                                    while colaE.retornar_seleccionado(k) != None:
                                        if int(L) == int(colaE.retornar_seleccionado(k).getLinea()):
                                            C=colaE.retornar_seleccionado(k).getComponente()
                                            
                                        k+=1
                                    
                                    if L!=0 :
                                        cambio=True
                                        Estado.Modificar(L,"Ensamblando componente "+str(C))
                                        self.cont+=1
                                        #print('asas'+self.ObjMaquina.retornar_seleccionado(1).getListLineas().retornar_seleccionado(L).getTEnsamblaje())
                                        Ls.Modificar(L, C, P,False,TT)
                                        print("aqui")
                                else:
                                    Ls.Modificar(L, C, P,True,(int(T)-1))
                                    Estado.Modificar(L,"Ensamblando componente "+str(C))
                                    
                            else:
                                Ls.Modificar(L, C, P,True,T)
                        else:
                            self.rep=True
                            Estado.Modificar(L,"No hacer nada")
                    except:
                        pass
                else:
                    if str(P).isdigit():
                        if int(C)<int(P):
                            Ls.Modificar(L, C, P-1,es,T)
                            Estado.Modificar(L,"Mover brazo - componente "+str(P-1))
                            if int(C) == int(P-1) and str(colaE.retornar_seleccionado(1).getLinea())==str(L) and str(colaE.retornar_seleccionado(1).getComponente())==str(C):
                                Ls.Modificar(L, C, P-1,True,T) 
                        else:
                            Ls.Modificar(L, C, P+1,es,T)
                            Estado.Modificar(L,"Mover brazo - componente "+str(P+1))
                            if int(C) == int(P+1) and str(colaE.retornar_seleccionado(1).getLinea())==str(L) and str(colaE.retornar_seleccionado(1).getComponente())==str(C):
                                Ls.Modificar(L, C, P+1,True,T)
            
                if cambio==True:
                    cambio=False
                    Ls.Modificar(L, C, P,self.rep,TT)
                    self.rep=False 
           
            
            if self.cont<=self.lim:
                
                tiempo+=1
                print("Tiempo "+str(tiempo)+"s")   
                self.listEnsam.insert(END, "* Tiempo "+str(tiempo)+"s")
                self.TiempoXML=ET.SubElement(self.ElabOptima, "Tiempo", NoSegundo=str(tiempo))
                #ET.SubElement(self.TiempoXML, "LineaEnsamblaje", NoLinea=str(tiempo)).text=str()
                Ls.mostrar()
                self.HTML+='''<tr class="bg-primary">
                <td colspan="{}">{}</td>
                </tr>'''.format(str(self.NLineas),"Tiempo "+str(tiempo)+"s")
                #self.NLineas
                
                Estado.mostrar(self.listEnsam)
               
                self.HTML+=Estado.mostrarHTML()
                self.HTML+='</tr>'
                Estado.mostrarXML(self.TiempoXML)
                #colaE.mostrar()
                #Ls.imp(anterior,n)

                self.tiempo.config(text=str(tiempo)+"s")
                time.sleep(1)
        self.HTML+='</tbody></table>'
        self.listEnsam.insert(END, "")
        self.listEnsam.insert(END, "*********************************")
        self.listEnsam.insert(END, "")
        ET.SubElement(self.ProductoXML, "TiempoTotal").text=str(tiempo)
        xmlstr = minidom.parseString(ET.tostring(self.SalidaXML)).toprettyxml(indent="   ")
        #self.
        with open(str(self.NombreSimulacion)+".xml", "w") as f:
            f.write(xmlstr)
        prog.join()
        
    def progreso(self):
        while True:
            self.pb.step((self.cont/self.lim)*100)
            time.sleep(1)
            if (self.cont/self.lim)*100==100:
                self.pb.step(99.99)
                time.sleep(1)
                break
            
            

    #***************************************************************************
  

app()
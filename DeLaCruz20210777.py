# Práctica 2: Sistema Cariovascular

# Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
# Tecnológico Nacional de México [TecNM - Tijuana]
# Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

# Nombre del alumno: Kevin Dario De La Cruz Bojorquez
# Número de control: 20210777
# Correo institucional: kevin.delacruz201@tectijuana.edu.mx

# Asignatura: Modelado de Sistemas Fisiológicos
# Docente: Dr. Paul Antonio Valle Trujillo; Vsul.valle@tectijuana.edu.mx

# Instalar librerias en consola
# pip install numpy control matplotlib

# Liberias 
import control as ctrl
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

#Datos Generales de la Simulacion
u = np.array(pd.read_excel('signal.xlsx',header=None))
x0,t0,tend,dt,w,h = 0,0,15,1E-3,10,5
N = round((tend-t0)/dt) + 1
t = np.linspace(t0,tend,N)                  
u = np.reshape(signal.resample(u,N),-1)    
signals = ['Respuestas: Hipotenso, Normotenso e Hipertenso','Respuestas Normotenso, Hipotenso y Controlador','Respuestas: Normotenso, Hipertenso y Controlador']

def cardio(Z,L,R,C):
    num = [L*R,R*Z]
    den = [C*L*R*Z, L*R+L*Z, R*Z]
    sys = ctrl.tf(num,den)
    L = np.roots(den)
    return sys,L

#Funcion de transferencia: Normotenso
Z,L,R,C = 0.010,0.001,1.00,1.500
sysnormo,L = cardio(Z,L,R,C)
print(f'funcion de transferencia del normotenso (control): {sysnormo}')
print(f"Polos del sistema: L1 = {L[0]:.3e}, L2 = {L[1]:.3e}\n")

#Funcion de transferencia: Hipotenso
Z,L,R,C = 0.010,0.001,1.00,3.500
syshipo,L = cardio(Z,L,R,C)
print(f'funcion de transferencia del hipotenso (caso1): {syshipo}')
print(f"Polos del sistema: L1 = {L[0]:.3e}, L2 = {L[1]:.3e}\n")

#Funcion de transferencia: Hipertenso
Z,L,R,C = 0.010,0.001,1.00,1.000
syshiper,L = cardio(Z,L,R,C)
print(f'funcion de transferencia del hipertenso (caso2): {syshiper}')
print(f"Polos del sistema: L1 = {L[0]:.3e}, L2 = {L[1]:.3e}\n")

#Componentes de controlador
def controlador(kP,kI,kD,sys):
    Cr = 1E-6
    Re = 1/(Cr*kI)
    Rr = kP*Re
    Ce = kD/Rr
    numPID = [Re*Rr*Ce*Cr,Re*Ce+Rr*Cr,1]
    denPID = [Re*Cr,0]
    PID = ctrl.tf(numPID,denPID)
    sysPID = ctrl.feedback(ctrl.series(PID,sys),1,sign=-1)
    return sysPID

#Controlador Hipotenso
hipoPID = controlador(458.483,1112094.736,0.00627,syshipo)
print(f'Funcion de transferencia del hipotenso en lazo cerrado: {hipoPID}')

#Controlador Hipertenso
hiperPID = controlador(126.595,293327.703,0.00140,syshiper)
print(f'Funcion de transferencia del hipertenso en lazo cerrado: {hiperPID}')

#Respuesta de lazo abierto
_,PpN = ctrl.forced_response(sysnormo,t,u,x0)
_,PpL = ctrl.forced_response(syshipo,t,u,x0)
_,PpH = ctrl.forced_response(syshiper,t,u,x0)

#Controlador para lazo cerrado
_,PIDL = ctrl.forced_response(hipoPID,t,PpN,x0)
_,PIDH = ctrl.forced_response(hiperPID,t,PpN,x0)

# Colores
clr1 = np.array([0,114,189])/255
clr2 = np.array([237,177,32])/255
clr3 = np.array([34,139,34])/255
clr4 = np.array([0.5,0.5,0.5])

# Gráfica 
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman','DejaVu Serif']

# Figura 1: Hipotenso, Normotenso e Hipertenso
fg1 = plt.figure(1,figsize=(w,h))
plt.plot(t,PpL,'-',linewidth=0.5,color=clr1,label=r'$P_p(t)$: Hipotenso')
plt.plot(t,PpN,'-',linewidth=0.5,color=clr2,label=r'$P_p(t)$: Normotenso')
plt.plot(t,PpH,'-',linewidth=0.5,color=clr3,label=r'$P_p(t)$: Hipertenso')
plt.grid(False)
plt.xlim(0,15)
plt.xticks(np.arange(0,16,1))
plt.ylim(-0.6,1.6)
plt.yticks(np.round(np.arange(-0.6,1.8,0.2),1))
plt.xlabel('t [s]')
plt.ylabel('Vi(t) [V]')
plt.legend(bbox_to_anchor=(0.5,1.08),loc='center',ncol=3,frameon=False)
fg1.savefig('individuos_python.pdf',bbox_inches='tight')  
plt.show()

# Figura 2: Normotenso, Hipotenso y Controlador
fg2 = plt.figure(2,figsize=(w,h))
plt.plot(t,PpN,'-',linewidth=0.5,color=clr2,label=r'$P_p(t)$: Normotenso')
plt.plot(t,PpL,'-',linewidth=0.5,color=clr1,label=r'$P_p(t)$: Hipotenso')
plt.plot(t,PIDL,':',linewidth=2,color=clr4,label=r'$PID(t)$: Hipotenso')
plt.grid(False)
plt.xlim(0,15)
plt.xticks(np.arange(0,16,1))
plt.ylim(-0.6,1.6)
plt.yticks(np.round(np.arange(-0.6,1.8,0.2),1))
plt.xlabel('t [s]')
plt.ylabel('Vi(t) [V]')
plt.legend(bbox_to_anchor=(0.5,1.08),loc='center',ncol=3,frameon=False)
fg2.savefig('hipotenso_python.pdf',bbox_inches='tight')
plt.show()

# Figura 3: Normotenso, Hipertenso y Controlador
fg3 = plt.figure(3,figsize=(w,h))
plt.plot(t,PpN,'-',linewidth=0.5,color=clr2,label=r'$P_p(t)$: Normotenso')
plt.plot(t,PpH,'-',linewidth=0.5,color=clr1,label=r'$P_p(t)$: Hipertenso')
plt.plot(t,PIDH,':',linewidth=2,color=clr4,label=r'$PID(t)$: Hipertenso')
plt.grid(False)
plt.xlim(0,15)
plt.xticks(np.arange(0,16,1))
plt.ylim(-0.6,1.6)
plt.yticks(np.round(np.arange(-0.6,1.8,0.2),1))
plt.xlabel('t [s]')
plt.ylabel('Vi(t) [V]')
plt.legend(bbox_to_anchor=(0.5,1.08),loc='center',ncol=3,frameon=False)
fg3.savefig('hipertenso_python.pdf',bbox_inches='tight')
plt.show()
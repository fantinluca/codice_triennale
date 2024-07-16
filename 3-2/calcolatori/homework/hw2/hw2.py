import os, re, sys
import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt

# funzione che esegue un comando shell e ritorna il suo output
def get_command_output(command):
    stream = os.popen(command)
    return stream.readlines()

# stampare output su file reindirizzando lo standard output
redirect = input("Digita y se vuoi stampare gli output del programma su file: ")
if (redirect=='y'):
    print("Programma iniziato")
    orig_stdout = sys.stdout
    f = open('out.txt', 'w')
    sys.stdout = f

# parametri
L = np.arange(50,1470,50)
K = 20
SERVER = 'paris.testdebit.info'
# definire strutture dati per risultati
# dizionario per tutti gli RTT, array di array per gli RTT minimi, massimi, medi e deviazione standard
rtt = {l:np.array([0]*K) for l in L}
min,max,avg,std = 0,1,2,3
rtt_data = [[],[],[],[]]
labels = ['min','max','avg','std']
colors = ['g', 'r', 'm', 'y']

# stima numero di link attraversati
# prima stima: ripetere ping di sistema indicando TTL decrescente; prosegue finchè la richiesta scade
ttl_ping = 256
print("Stima numero di link attraversati:")
while (True):
    command = f'ping {SERVER} -n 1 -l 10 -i {ttl_ping-1}'
    print(f'TTL in uso: {ttl_ping}')
    output = get_command_output(command)
    row = output[2]
    if ('TTL scaduto durante il passaggio.' not in row): ttl_ping -= 1
    elif ('Richiesta scaduta.' in row): continue
    else: break
print(f'Con ping: {ttl_ping}')

# seconda stima: usare tracert, restituisce numero di link attraversati
command = f'tracert {SERVER}'
print("tracert in uso")
output = get_command_output(command)
ttl_tracert = len(output)-7+1
print(f'Con tracert: {ttl_tracert}')

# ricavare valori di RTT
# viene ripetuto psping modificando dimensione pacchetto, numero ping e server costanti
for l in L:
    command = f'psping -n {K} -w 0 -l {l} -f {SERVER}'
    print(f'L in uso: {l}')
    # se richiesta va in timeout, list comprehension ritorna errore; se succede, errore catturato e richiesta ripetuta
    # dalle vari righe, RTT vengono ricavati tramite regex e convertiti in float
    # viene costruita lista di RTT che viene salvato in dizionario associato a dimensione usato
    while True:
        try:
            output = get_command_output(command)
            signals = output[7:7+K]
            rtts = [re.findall('[\d\.]+',s) for s in signals]
            rtts = [float(a[1]) for a in rtts]
            break
        except Exception:
            pass
    rtt[l] = np.array(rtts)

    # viene calcolato minimo, massimo, media, deviazione standard; vengono salvati nella lista corrispondente
    rtt_data[min].append(np.min(rtts))
    rtt_data[max].append(np.max(rtts))
    rtt_data[avg].append(np.average(rtts))
    rtt_data[std].append(np.std(rtts))

# si prendono le dimensioni, i valori minimi e si esegue l'interpolazione lineare
result = poly.Polynomial.fit(np.array(L), np.array(rtt_data[min]), 1)
T,a = result.convert().coef

print(f'EQUAZIONE DELLA FUNZIONE L-RTT = {result}')
print(f'A = {a}')

# vengono calcolati i throughput
S = (2*ttl_ping)/a
S_bottleneck = 2/a

print(f'S = {S} bit/s')
print(f'S_BOTTLENECK = {S_bottleneck} bit/s')

# vengono creati i grafici dimensione pacchetti-RTT minimi/massimi/medi/deviazione standard
for i in range(4):
    plt.plot(np.array(L), np.array(rtt_data[i]), f'{colors[i]}o')
    if (i==0):
        func = np.empty(0)
        for l in L:
            func = np.append(func, (a*l+T))
        plt.plot(np.array(L), func)
    figure = plt.gcf()
    figure.set_size_inches(11.0,6.0)
    plt.title(labels[i])
    plt.savefig(f'{labels[i]}.png', dpi=600)
    plt.show()

# se output è stato reindirizzato, si avvisa utente di fine programma
if (redirect=='y'):
    sys.stdout = orig_stdout
    f.close()
    print("Programma terminato")
from PIL import Image
import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
import os

np.seterr(all='raise')
# 1. Caricare un'immagine a colori RGB in formato BMP e/o JPG e/o PGM (uno dei tre formati è sufficiente)
# l'utente può scegliere tra le imamgini presenti nella stessa cartella dello script
folder = os.path.dirname(__file__)
images = []
for file in os.listdir(folder): 
    if (file.endswith('.bmp') or file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.pmg')):
        images.append(file)
if (len(images) == 0):
    print("Non sono presenti immmagini nella cartella; aggiungerne almeno una e riavviare il codice.")
    exit()
for i in range(len(images)):
    print("- "+str(i+1)+": "+images[i])
while True:
    try:
        img = input("Inserisci il numero corrispondente all'immagine che vuoi usare tra quelle mostrate sopra: ")
        img = int(img)
        break
    except ValueError:
        print("Inserisci uno dei numeri mostrati prima")

limit_round = False
save_compressed = False

tmp = input("Inserisci 1 se vuoi arrotondare e limitare all'intervallo [0,255] i risultati delle DCT inverse, altrimenti inserisci qualsiasi altro valore: ")
if (tmp=='1'): limit_round = True
    
image_name = images[img-1]
image = Image.open(image_name)

# 2. Effettuare il cambio di spazio dei colori da RGB a YCbCr
image_ycbcr = image.convert('YCbCr')
# associamo indici a componenti YCbCr
C = {"Y":0, "Cb":1, "Cr":2}
# oggetto PIL.Image diventa array np con componenti YCbCr espressi per righe e colonne (range 0-255)
np_ycbcr = list(image_ycbcr.getdata())
np_ycbcr = np.reshape(np_ycbcr, (image.size[1], image.size[0], 3))
np_ycbcr = np.uint8(np_ycbcr)
# separiamo componenti e le salviamo separatamente in scala di grigi
C_data = []
for (f,c) in C.items():
    C_data.append(np_ycbcr[:,:,c])
    print("Salvando componente", f, "come immagine", end="")
    Image.fromarray(C_data[c], "L").save(image_name[:-4]+"_"+str(f)+image_name[-4:])
    print(": OK")

# 3 Per ognuna delle componenti Y, Cb e Cr, dato un numero R tra 1 e 100:
# definiamo valori di N da usare
n = [8, 16, 64]
# definiamo colori dei vari plot di PSNR
n_c = ['r', 'b', 'g']
# definiamo i valori di R da usare (da 30 a 100)
r = np.arange(30, 105, 5)
# etichette per legenda grafico dei plot di PSNR
values = [("N="+str(N)) for N in n]

for I in range(3):
    N = n[I]
    PSNR = []
    C_dct = []
    r_plot = r

    # 3.1 Effettua la DCT bidimensionale con blocchi di dimensione parametrizzabile N della componente
    for (f,c) in C.items():
        print("Effettuando DCT su componente", f, "(N="+str(N)+")", end="")
        c_d = C_data[c]
        # definiamo np array con stessa forma di dati immagine
        c_shape = c_d.shape
        dct = np.zeros(c_shape)
        # costruiamo array con varie posizioni iniziali dei blocchi
        # (da 0 alla dimensione dell'immagine c_shape[i], per multipli di N)
        # facciamo cicli su di essi
        for i in np.r_[:c_shape[0]:N]:
            for j in np.r_[:c_shape[1]:N]:
                # effettuiamo DCT a 2 dimensioni su blocco
                dct[i:(i+N), j:(j+N)] = fftpack.dctn(c_d[i:(i+N), j:(j+N)], axes=[0,1], norm="ortho")
        # salviamo risultato
        C_dct.append(dct)
        print(": OK")

    # 3.2 Mette a zero una frazione pari a R% dei coefficienti DCT dell'intera componente,
    # e più precisamente quelli con valore assoluto più piccolo di un'opportuna soglia
    for R in r:
        e = '\r'
        if (R==max(r)): e = '\n'
        print("Effettuando sogliaggio, DCT inversa, calcolo PSNR; R="+str(R), end=e)
        C_dct_threshed = []
        for (f,c) in C.items():
            # troviamo il valore maggiore dell'R% dei valori presenti nella dct (considerati ordinati)
            # poi, mettiamo a 0 i valori minori
            dct = C_dct[c]
            p = np.percentile(dct, R, method='lower')
            C_dct_threshed.append(dct * (abs(dct) > p))

        # 3.3 Effettua la DCT inversa sui blocchi dopo sogliaggio,
        # ottenendo la versione "compressa" della componente
        C_idct = []
        for (f,c) in C.items():
            c_d_t = C_dct_threshed[c]
            shape = c_d_t.shape
            idct = np.zeros(shape)
            # effettuiamo la DCT inversa a blocchi in modo analogo a prima
            for i in np.r_[:shape[0]:N]:
                for j in np.r_[:shape[1]:N]:
                    idct[i:(i+N), j:(j+N)] = fftpack.idctn(c_d_t[i:(i+N), j:(j+N)], axes=[0,1], norm="ortho")
            # se utente ha scelto di farlo, valori vengono arrotondati e limitati
            if (limit_round): idct = np.clip(np.round(idct), 0, 255)
            C_idct.append(idct)

        # 3.4 Calcola l'MSE tra la componente originale e la componente "compressa"
        C_mse = []
        for c in C.values():
            C_mse.append((np.square(C_data[c] - C_idct[c])).mean())
        # 4 Calcola l'MSE pesato: MSE_P = 3/4 MSE_Y + 1/8 MSE_Cb + 1/8 MSE_Cr
        coeff = [3/4, 1/8, 1/8]
        mse_p = sum((C_mse[c] * coeff[c]) for c in C.values())
        # 5 Calcola il PSNR pesato come 10log_10 (255^2/MSE_P)
        try:
            PSNR.append(10 * np.log10(np.square(255) / mse_p))
        except Exception:
            i = np.where(r_plot==R)[0][0]
            r_plot = np.delete(r_plot,i)

    # tracciamo curva per funzione R->PSNR
    plt.plot(r_plot, PSNR, n_c[I])

plt.legend(labels=values)
figure = plt.gcf()
figure.set_size_inches(11.0,6.0)
plt.savefig(image_name[:-4]+"_plot.png", dpi=600)
plt.show()
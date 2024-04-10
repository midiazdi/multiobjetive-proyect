import re
import numpy as np

# Cadena de entrada representando la lista de listas, cada lista en una nueva línea
cadena_entrada = """
[5.05420208e-01 9.58545188e-01 5.02271501e-02 7.69788805e-01 9.99997761e-01 6.41399858e-03]
 [4.55325046e-03 6.75965484e-03 2.47881257e-01 4.28531357e-02 9.99999332e-01 6.70085976e-01]
 [3.54507390e-01 9.48300395e-01 1.14022003e-01 8.05196639e-01 9.99874077e-01 3.57338230e-03]
 [7.97788230e-03 9.85902224e-01 7.99304193e-02 8.70376852e-01 9.99999753e-01 1.49405441e-02]
 [4.32818893e-01 9.61431778e-01 1.58996576e-01 7.69788805e-01 9.99952355e-01 3.61017858e-03]
 [4.16025953e-01 9.48661360e-01 1.17519869e-01 8.03943840e-01 9.99999851e-01 3.63754454e-03]
 [3.61861069e-01 9.48300395e-01 1.14022003e-01 8.05196639e-01 9.99994790e-01 7.94111953e-04]
 [4.32818893e-01 9.58545188e-01 9.08783417e-02 7.69788805e-01 9.99997771e-01 6.41399858e-03]
 [5.23287443e-04 8.78498876e-01 7.83882573e-02 8.01418474e-01 9.99993894e-01 4.25112202e-03]
 [3.78164559e-03 9.05014191e-01 1.03518033e-01 7.04903156e-01 9.99994726e-01 4.34178882e-03]
 [7.10901272e-03 1.72237776e-03 1.60696867e-01 2.56166701e-01 9.99994914e-01 6.32794678e-01]
 [5.08234524e-03 1.72237776e-03 1.60696867e-01 2.56166701e-01 9.99994807e-01 5.92685035e-01]
 [6.76594204e-03 1.14424376e-02 8.04074353e-02 1.59617290e-01 9.99940204e-01 5.40120211e-01]
 [5.79917456e-02 9.34336656e-01 6.90210864e-02 7.78840299e-01 9.99897857e-01 6.23937896e-03]
 [5.01024922e-03 7.10212143e-01 1.14022003e-01 7.57243429e-01 9.99874561e-01 3.63754454e-03]
 [6.52943797e-04 1.72773452e-03 7.82267831e-02 1.44951354e-02 9.99998261e-01 2.35140629e-02]
 [4.43169049e-03 2.89572817e-04 1.70544486e-01 4.36747785e-02 9.99940415e-01 1.93226983e-01]
 [3.45897445e-03 9.87214427e-03 2.53366207e-01 4.18862918e-03 9.99995951e-01 5.85802071e-01]
 [5.38422599e-04 1.35875304e-03 1.04603198e-01 2.71588094e-01 9.99807626e-01 3.73383972e-01]
 [5.53689855e-02 6.04651122e-01 2.32242699e-01 5.80936119e-01 9.99908996e-01 2.61114881e-03]
 [5.51924288e-03 6.00716472e-01 9.61276206e-02 7.12959843e-01 9.99848751e-01 3.18409130e-02]
 [5.62683712e-02 9.48661360e-01 1.17519869e-01 7.98737327e-01 9.99999985e-01 3.63754454e-03]
 [2.61945501e-02 9.79269777e-01 8.56040230e-02 8.04224143e-01 9.99991640e-01 1.53177796e-02]
 [1.67796483e-03 1.66614668e-03 1.60696867e-01 1.24962547e-01 9.99994870e-01 6.30917892e-01]
 [9.15770208e-03 1.72237776e-03 1.60696867e-01 1.93468621e-01 9.99995489e-01 6.64485831e-01]
 [3.85139802e-03 2.81261191e-03 1.60696867e-01 1.24962547e-01 9.99994914e-01 6.32794678e-01]
 [2.14808482e-04 8.51767213e-01 9.03619258e-02 6.13311846e-01 9.99899519e-01 1.76448351e-02]
 [2.56204796e-02 9.61258059e-01 1.69622129e-01 8.53171503e-01 9.99957864e-01 2.22917420e-02]
 [2.65543281e-02 9.34336656e-01 8.56064227e-02 8.14114319e-01 9.99902782e-01 6.23937896e-03]
 [7.13402189e-03 9.61431778e-01 1.59734425e-01 8.45679562e-01 9.99993414e-01 1.17554384e-02]
 [5.85696788e-02 8.40237858e-03 1.42865130e-01 1.93308801e-01 9.99988679e-01 2.09370416e-01]
 [5.23287443e-04 2.22697016e-03 7.83882573e-02 8.01418474e-01 9.99993414e-01 4.15189486e-03]
 [1.64066880e-04 3.04285733e-03 2.54850073e-01 2.45997033e-01 9.99999514e-01 5.64600242e-01]
 [6.42661739e-04 1.78927069e-03 7.82267831e-02 2.69443808e-01 9.99817041e-01 1.91124780e-02]
 [3.85356279e-03 4.19385240e-03 1.60110487e-01 3.38146316e-03 9.99999881e-01 3.66995612e-01]
 [7.16239622e-03 1.35875304e-03 8.11377250e-02 1.60190673e-01 9.99894082e-01 3.73383972e-01]
 [7.10901272e-03 3.04285733e-03 2.50552358e-01 1.39485139e-01 9.99996342e-01 6.74712953e-01]
 [2.68713020e-04 3.44492018e-04 7.81007896e-02 1.16739070e-01 9.99989804e-01 4.87773341e-01]
 [5.53689855e-02 4.76033059e-01 2.32242699e-01 5.80936119e-01 9.99848802e-01 3.09170589e-02]
 [3.88998528e-03 4.19385240e-03 1.80908184e-01 5.47056907e-01 9.99998991e-01 1.59102343e-02]
 [2.15633508e-02 6.54304735e-04 6.15625299e-02 1.18696355e-01 9.99825989e-01 3.58636964e-01]
 [2.60531669e-02 9.86024195e-01 8.40291588e-02 8.59764247e-01 9.99991213e-01 1.47363077e-02]
 [2.15633508e-02 3.28826759e-04 6.15625299e-02 8.09352863e-03 9.99954873e-01 5.58950712e-01]
 [7.21982566e-03 6.62520674e-03 1.68500826e-01 5.71506571e-01 9.99859474e-01 1.63181335e-02]
 [3.98235675e-04 4.36146013e-04 7.81007896e-02 2.50778490e-02 9.99996147e-01 4.23045709e-01]
 [7.10901272e-03 3.04285733e-03 2.50552358e-01 7.65349598e-02 9.99999514e-01 4.72025763e-01]
 [3.98235675e-04 4.77616797e-03 7.81007896e-02 6.34567549e-02 9.99996147e-01 4.23045709e-01]
 [3.98235675e-04 4.36146013e-04 7.81007896e-02 1.16739070e-01 9.99811476e-01 4.87773341e-01]
 [7.63104800e-03 8.60241992e-02 9.20693962e-02 6.27621580e-01 9.99997825e-01 5.92256855e-03]
 [5.53689855e-02 4.39166582e-01 2.32242699e-01 5.57528907e-01 9.99848802e-01 3.09170589e-02]
"""

# Dividir la cadena de entrada en líneas (cada línea representa una lista)
listas = cadena_entrada.strip().split('\n')

# Convertir cada línea a una lista de números en formato decimal
listas_decimales = []
for lista in listas:
    numeros_notacion_cientifica = re.findall(r"[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?", lista)
    numeros_decimales = [format(np.float64(numero), '.8f') for numero in numeros_notacion_cientifica]
    listas_decimales.append(numeros_decimales)

print(listas_decimales)

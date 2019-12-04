
# Src : https://stackoverflow.com/a/37861832/503842
import numpy as np
d = [0.000, 0.166, 0.333]   #ideal target distances, these can be all zeros.
p = [0.000, 0.254, 0.998]   #your performance goes here

print("d is: " + str(["%.8f" % elem for elem in d]))
print("p is: " + str(["%.8f" % elem for elem in p]))

def rmse(predictions, targets):
    """
    Retourne la racine de l'erreur quadratique moyenne
    entre deux vecteurs de même dimension
    """
    differences = predictions - targets                       #the DIFFERENCEs.
    differences_squared = differences ** 2                    #the SQUAREs of ^
    mean_of_differences_squared = differences_squared.mean()  #the MEAN of ^
    rmse_val = np.sqrt(mean_of_differences_squared)           #ROOT of ^
    return rmse_val                                           #get the ^

    #One liner
    #return np.sqrt(((predictions - targets) ** 2).mean())

rmse_val = rmse(np.array(d), np.array(p))
print("rms error is: " + str(rmse_val))
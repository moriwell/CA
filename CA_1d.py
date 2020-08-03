import numpy as np
import matplotlib.pyplot as plt 
import cv2
import config as p

def debug(array):
    plt.imshow(array)
    plt.show() 

def CA_1d(U,w,A,B):
    CA = np.zeros((w))
    for i in range(1,w-1):
        Ujk_n = np.max((U[i-1],U[i+1]))
        CA[i] = calc_value(Ujk_n,A,B)

    return CA

def calc_value(Ujk_n,A,B):
    if Ujk_n < B/2:
        return 0
    if ((Ujk_n >= B/2) and (Ujk_n < (A + B)/2)):
        return 2 * Ujk_n - B
    if Ujk_n >= (A + B)/2:
        return A
        
def main():

    w =  13
    A = 5
    B = 2
    data = []
    U = np.zeros((w))

    if p.mode == "erosion":
        for i in range(w):
            x_ = abs(i-int(w/2))
            U[i]= x_
    else:
        for i in range(w):
            x_ = abs(i-int(w/2))
            U[i] = x_
        in_value = np.max(U)
        U = abs(in_value - U)-1
    
    print(U[1:w-1])
    data.append(U[1:w-1])
    CA = CA_1d(U,w,A,B)
    print(CA[1:w-1])
    data.append(CA[1:w-1])
    for i in range(12):
        CA = CA_1d(CA,w,A,B)
        print(CA[1:w-1])
        data.append(CA[1:w-1])

    plt.imshow(np.array(data))
    plt.xlabel("空間 j ")
    plt.xticks(range(w-2))
    plt.ylabel("時間経過 n ")
    plt.yticks(range(12))
    plt.colorbar()
    # plt.grid(c='white', zorder=50)
    plt.show() 

if __name__ == "__main__":
    main()


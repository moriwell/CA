import numpy as np
import matplotlib.pyplot as plt 
import cv2
import config as p

def debug(array):
    plt.imshow(array)
    plt.show() 

def CA(U,h,w,A,B):
    CA = np.zeros((h,w))
    for i in range(1,h-1):
        for j in range(1,w-1):
            Ujk_n = np.max((U[i-1][j],U[i+1][j],U[i][j-1],U[i][j+1]))
            
            CA[i][j] = calc_value(Ujk_n,A,B)

    return CA
def calc_value(Ujk_n,A,B):
    if Ujk_n < B/2:
        return 0
    if ((Ujk_n >= B/2) and (Ujk_n < (A + B)/2)):
        return 2 * Ujk_n - B
    if Ujk_n >= (A + B)/2:
        return A
        
def FFT(array):
    img_f = np.fft.fft2(array)
    fshift = np.fft.fftshift(img_f)
    magnitude_spectrum = 20*np.log(np.abs(fshift))

    return fshift

def IFFT(array):
    f_ishift = np.fft.ifftshift(array)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    return img_back

def normalize(array):
    if np.max(array) > 0: 
        max_v = np.max(array)
        min_v = np.min(array)
        array = (array - min_v)/(max_v-min_v)
        return array
    else:
        return array * 0

def main():
    # path = input("input img path")
    img = cv2.imread(p.path)

    print(img.shape)
    img_ = img[:,:,1]
    h = len(img_)
    w = len(img_[0])
    # h = 100
    # w = 100 
    img_f = FFT(img_) 
    img_if = IFFT(img_f)
    # debug(img_if)


    U = np.zeros((h,w))
    if p.mode == "erosion":
        for i in range(h):
            for j in range(w):
                x_ = abs(j-int(w/2))
                y_ = abs(i-int(h/2))
                U[i][j] = x_ + y_
    else:
        for i in range(h):
            for j in range(w):
                x_ = abs(j-int(w/2))
                y_ = abs(i-int(h/2))
                U[i][j] = x_ + y_
        in_value = np.max(U)
        U = abs(in_value - U)
    debug(U)
    
    CA_2D = CA(U,h,w,p.A,p.B)
    fact = normalize(CA_2D)
    img_masked_f = img_f * fact
    img_if = IFFT(img_masked_f)


    for i in range(100):
        CA_2D = CA(CA_2D,h,w,p.A,p.B)
        fact = normalize(CA_2D)
        img_masked_f = img_f * fact
        img_if = IFFT(img_masked_f)
        debug(img_if)


if __name__ == "__main__":
    main()


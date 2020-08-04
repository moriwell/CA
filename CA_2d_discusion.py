import numpy as np
import matplotlib.pyplot as plt 
import cv2
import config as p

def debug_img(array):
    plt.imshow(array, cmap = "gray")
    plt.colorbar()
    plt.show() 

def debug_CA(array):
    plt.imshow(array)
    plt.colorbar()
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

def filtering(CA,img_f,h,w):
    fact = normalize(CA)
    img_masked_f = img_f * fact[1:h-1,1:w-1]
    img_if = IFFT(img_masked_f)
    return img_if

def main(B):
    if p.input_data == "test":
        h = 102
        w = 102 

    else:
        img = cv2.imread(p.path)
        img_ = img[:,:,1]
        h = len(img_) + 2
        w = len(img_[0]) + 2
        img_f = FFT(img_) 
        img_if = IFFT(img_f)


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
    # debug_CA(U[1:h-1,1:w-1])
    
    if p.input_data == "image":
        img_masked_f = filtering(U,img_f,h,w)
        debug_img(img_masked_f[1:h-1,1:w-1])



    CA_2D = CA(U,h,w,p.A,B)
    if p.input_data == "image":
        img_masked_f = filtering(CA_2D,img_f,h,w)
        debug_img(img_masked_f[1:h-1,1:w-1])
        debug_CA(CA_2D[1:h-1,1:w-1])


    for i in range(200):
        CA_2D = CA(CA_2D,h,w,p.A,B)
        if p.input_data == "image":
            img_masked_f = filtering(CA_2D,img_f,h,w)
            debug_img(img_masked_f[1:h-1,1:w-1])
            debug_CA(CA_2D[1:h-1,1:w-1])
        else:
            # debug_CA(CA_2D[1:h-1,1:w-1]) 
            sub = CA_2D[1:h-1,1:w-1] == p.A
            if sub.all():
                flag = True
                break
    print(i+2)
    return flag

if __name__ == "__main__":
    for i in range(150):
        B = i - 10
        flag = main(B)
        if flag == False:
            break


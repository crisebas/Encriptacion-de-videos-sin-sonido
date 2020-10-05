import numpy as np 

def generate_iterations(x_0, y_0, z_0, higher):
    s, r, b = 10, 28, 8/3
    
    x_list = [x_0]
    y_list = [y_0]
    z_list = [z_0]

    h = 0
    i = 0

    while h < 0.01:
        x = x_list[i]
        y = y_list[i]
        z = z_list[i]

        position = RK4(x, y, z, s, r, b, h)

        x_list.append(position[0])
        y_list.append(position[1])
        z_list.append(position[2])

        h+=0.0000005
        i+=1

    x_list, y_list, z_list = transform_list(x_list, y_list, z_list, higher)

    return x_list, y_list, z_list

def RK4(x, y, z, s, r, b, h):
    k_1 = X(x, y, s)
    l_1 = Y(x, y, z, r)
    m_1 = Z(x, y, z, b)

    k_2 = X((x + k_1*h*0.5), (y + l_1*h*0.5), s)
    l_2 = Y((x + k_1*h*0.5), (y + l_1*h*0.5), (z + m_1*h*0.5), r)
    m_2 = Z((x + k_1*h*0.5), (y + l_1*h*0.5), (z + m_1*h*0.5), b)

    k_3 = X((x + k_2*h*0.5), (y + l_2*h*0.5), s)
    l_3 = Y((x + k_2*h*0.5), (y + l_2*h*0.5), (z + m_2*h*0.5), r)
    m_3 = Z((x + k_2*h*0.5), (y + l_2*h*0.5), (z + m_2*h*0.5), b)

    k_4 = X((x + k_3*h), (y + l_3*h), s)
    l_4 = Y((x + k_3*h), (y + l_3*h), (z + m_3*h), r)
    m_4 = Z((x + k_3*h), (y + l_3*h), (z + m_3*h), b)

    x += (k_1 + 2*k_2 + 2*k_3 + k_4)*h*(1/6)
    y += (l_1 + 2*l_2 + 2*l_3 + l_4)*h*(1/6)
    z += (m_1 + 2*m_2 + 2*m_3 + m_4)*h*(1/6)

    return(x, y, z)

def X(x, y, s):
    return s*(y - x)

def Y(x, y, z, r):
    return (-x)*z + r*x - y

def Z(x, y, z, b):
    return x*y - b*z

def transform_list(x_list, y_list, z_list, higher):
    for i in range(2, higher+2):
        x_list[i] = int(x_list[i]*10000000000) % 1000
        y_list[i] = int(y_list[i]*10000000000) % 1000
        z_list[i] = int(z_list[i]*10000000000) % 1000
    
    return x_list, y_list, z_list
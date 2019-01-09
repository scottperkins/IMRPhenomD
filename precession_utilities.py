import autograd.numpy as np
import utilities as util


"""A variety of utilities for the construction of the precessing model IMRPhenomPv3:"""

###############################################################################################
#Foundational quantities PHYSICAL REVIEW D 95, 104004

#S1, S2, and L are 3D vectors - m1, m2 are scalars and in seconds
def xi(m1,m2,S1, S2,L): 
    S1 = np.asarray(S1)
    S2 = np.asarray(S2)
    L = np.asarray(L)
    sumL = 0
    L_hat = np.divide(L,np.sqrt( np.asarray( [x^2 for x in L]) ))
    q = m2/m1
    return ((1 + q) * np.sum(np.asarray( [S1[i] * L_hat[i] for i in np.arange( len(L_hat) )] ) )+
             ( 1 + 1/q) *np.sum(np.asarray( [S2[i] * L_hat[i] for i in np.arange( len(L_hat) )] ) ))

#J2, L2, and S2 are  magnitudes
def theta_L(J2, L2, S2):
    return np.arccos((J2 + L2 - S2)/(2 * np.sqrt(J2*L2)))

#calculates the magnitude of the orbital angular momentum
def L(eta, f,M):
    return (2*np.pi*M*f)**(-1/3)*eta*M**2

#PN expansion coefficient defined in PhysRevD.95.104004 - dimensionless
def v(f,M):
    return (2 * np.pi*M * f)**(1/3)

#s1 and s2 are vectors
def S2(s1,s2):
    stotal= np.asarray([s1[x]+s2[x] for x in np.arange(len(s1))])
    return np.sum(np.asarray([x**2 for x in stotal]))

#L is a magnitude
def L_vec(L, theta_L):
    return np.asarray([L*np.sin(theta_L), 0, L*np.cos(theta_L)])     

###############################################################################################
#Finding S+ and S- PHYSICAL REVIEW D 95, 104004
def S1_2(A,B,C,D):
    return (-B/3. - (2**0.3333333333333333*(-B**2 + 3*C))/
            (3.*(-2*B**3 + 9*B*C - 27*D + 3*np.sqrt(3)*
                  np.sqrt(-(B**2*C**2) + 4*C**3 + 4*B**3*D - 18*B*C*D + 27*D**2))**0.3333333333333333) + 
           (-2*B**3 + 9*B*C - 27*D + 3*np.sqrt(3)*
                np.sqrt(-(B**2*C**2) + 4*C**3 + 4*B**3*D - 18*B*C*D + 27*D**2))**0.3333333333333333/
            (3.*2**0.3333333333333333))
def S2_2(A,B,C,D):
    return (-B/3. + ((1 + (0,1)*np.sqrt(3))*(-B**2 + 3*C))/
        (3.*2**0.6666666666666666*(-2*B**3 + 9*B*C - 27*D + 
             3*np.sqrt(3)*np.sqrt(-(B**2*C**2) + 4*C**3 + 4*B**3*D - 18*B*C*D + 27*D**2))**
           0.3333333333333333) - ((1 - (0,1)*np.sqrt(3))*
          (-2*B**3 + 9*B*C - 27*D + 3*np.sqrt(3)*
              np.sqrt(-(B**2*C**2) + 4*C**3 + 4*B**3*D - 18*B*C*D + 27*D**2))**0.3333333333333333)/
        (6.*2**0.3333333333333333))
def S3_2(A,B,C,D):
    return (-B/3. + ((1 - (0,1)*np.sqrt(3))*(-B**2 + 3*C))/
        (3.*2**0.6666666666666666*(-2*B**3 + 9*B*C - 27*D + 
             3*np.sqrt(3)*np.sqrt(-(B**2*C**2) + 4*C**3 + 4*B**3*D - 18*B*C*D + 27*D**2))**
           0.3333333333333333) - ((1 + (0,1)*np.sqrt(3))*
          (-2*B**3 + 9*B*C - 27*D + 3*np.sqrt(3)*
              np.sqrt(-(B**2*C**2) + 4*C**3 + 4*B**3*D - 18*B*C*D + 27*D**2))**0.3333333333333333)/
        (6.*2**0.3333333333333333))
def S_plus_2(A,B,C,D):
    s1 = S1_2(A,B,C,D)
    s2 = S2_2(A,B,C,D)
    s3 = S3_2(A,B,C,D)
    return np.amax([s1,s2,s3])
def S_minus_2(A,B,C,D):
    s1 = S1_2(A,B,C,D)
    s2 = S2_2(A,B,C,D)
    s3 = S3_2(A,B,C,D)
    return np.amin([s1,s2,s3])

###############################################################################################
#a coefficients PHYSICAL REVIEW D 88, 063011
def a0(eta): return (96/5)*eta

def a1(eta): return 1/2 + 3/4 * eta

def a2 (eta, xi): return -3/(4*eta)*xi

def a3(beta3): return 4*np.pi - beta3

def a4(eta, sigma4): return 34103/18144 + 13661/2016 * eta + 56/18 * eta**2 - sigma4

def a5(eta, beta5): return -4159/672 * np.pi - 189/8 * np.pi *eta - beta5

def a6(eta, beta6): 
    return ( 16447322263/139708800 + 16/3 * np.pi**2 - 856/105 * np.log(16) - 
            1712/105 * utilities.gammaE - beta6 + eta*(451/48 * np.pi**2 - 56198689/217728) +
            eta**2 * 541/896 - eta**3 * 5605/2592)

def a7(eta, beta7): return (-4415/4032 * np.pi + 358675/6048 * np.pi * eta + 91495/1512 * np.pi *eta**2
                            - beta7)

###############################################################################################
#Betas PHYSICAL REVIEW D 88, 063011
def beta3(m1, m2,c1,q,eta,xi): 
    M = m1 + m2
    spin_dot1 = S1_dot_L_avg(c1,q,eta,xi)
    spin_dot2 = S2_dot_L_avg(c1,q,eta,xi)
    term1 = (113/12 + 25/4 * m1/m2)*spin_dot1
    term2 = (113/12 + 25/4 * m2/m1)*spin_dot2
    return (1/M**2) * ( term1 + term2)

def beta5(m1, m2,c1,q,eta,xi): 
    M = m1 + m2
    spin_dot1 = S1_dot_L_avg(c1,q,eta,xi)
    spin_dot2 = S2_dot_L_avg(c1,q,eta,xi)
    term1 = (31319/1008 - 1159/24 * eta + m2/m1 * (809/84 - 281/8 * eta)) * spin_dot1
    term2 = (31319/1008 - 1159/24 * eta + m1/m2 * (809/84 - 281/8 * eta)) * spin_dot2
    return (1/M**2) * ( term1 + term2)

def beta6(m1, m2,c1,q,eta,xi): 
    M = m1 + m2
    spin_dot1 = S1_dot_L_avg(c1,q,eta,xi)
    spin_dot2 = S2_dot_L_avg(c1,q,eta,xi)
    term1 = (75/2 + 151/6 * m2/m1 ) * spin_dot1
    term2 = (75/2 + 151/6 * m1/m2 ) * spin_dot2
    return (np.pi/M**2) * (term1 + term2)

def beta7(m1, m2,c1,q,eta,xi): 
    M = m1 + m2
    spin_dot1 = S1_dot_L_avg(c1,q,eta,xi)
    spin_dot2 = S2_dot_L_avg(c1,q,eta,xi)
    term1 = ( 130325/756 - 796069/2016 * eta + 100019/864 * eta**2 + 
            m2/m1 * (1195759/18144 - 257023/1008 * eta +2903/32*eta**2) ) *spin_dot1
    term2 = ( 130325/756 - 796069/2016 * eta + 100019/864 * eta**2 + 
            m1/m2 * (1195759/18144 - 257023/1008 * eta +2903/32*eta**2) ) *spin_dot2
    return (1/M**2) * (term1 + term2)

#S1,S2 are magnitudes
def sigma4(m1, m2, mu, Sav, S1,S2, c1,q,eta,xi,S_plus,S_minus,v0 ):
    M = m1 +m2
    s1s2 = S1_dot_S2_avg(Sav,S1,S2)
    s1Ls2L = S1_dot_L_S2_dot_L_avg(c1,q,eta,xi,S_plus,S_minus,v0)
    S1L_squared = S1_dot_L_squared_avg(c1,q,eta,xi,S_plus,S_minus,v0)
    S2L_squared = S2_dot_L_squared_avg(c1,q,eta,xi,S_plus,S_minus,v0)
    term1 = (1/(mu*M**3)) * (247/48*s1s2 - 721/48 * s1Ls2L)
    term2 = 1/(M**2 * m1**2) * ( 233/96 * S1**2 - 719/96 * S1L_squared) 
    term3 = 1/(M**2 * m2**2) * ( 233/96 * S2**2 - 719/96 * S2L_squared) 
    return term1 + term2 + term3

###############################################################################################
#Orbit averaged angular momentum products - PHYSICAL REVIEW D 95, 104004
def S1_dot_L_avg(c1,q,eta,xi):
    num = c1*(1+q) - q*eta*xi
    denom = eta*(1-q**2)
    return num/denom

def S2_dot_L_avg(c1,q,eta,xi):
    num = c1*(1+q) - eta*xi
    denom = eta*(1-q**2)
    return -q*num/denom

#S1 and S2 are magnitudes
def S1_dot_S2_avg(Sav, S1,S2):
    return Sav**2/2 - (S1**2 + S2**2)/2

def S1_dot_L_squared_avg(c1,q,eta,xi,S_plus,S_minus,v0):
    term1 = S1_dot_L_avg(c1,q,eta,xi)
    term2 = (S_plus**2 - S_minus**2)**2 * v0**2 / (32*eta**2 * (1-q)**2 )
    return term1 + term2

def S2_dot_L_squared_avg(c1,q,eta,xi,S_plus,S_minus,v0):
    term1 = S1_dot_L_avg(c1,q,eta,xi)
    term2 = q**2*(S_plus**2 - S_minus**2)**2 * v0**2 / (32*eta**2 * (1-q)**2 )
    return term1 + term2

def S1_dot_L_S2_dot_L_avg(c1,q,eta,xi,S_plus,S_minus,v0):
    return (S1_dot_L_squared_avg(c1,q,eta,xi,S_plus,S_minus,v0)*
             S2_dot_L_squared_avg(c1,q,eta,xi,S_plus,S_minus,v0)
            - q*(S_plus**2 - S_minus**2)**2 * v0**2 / (32*eta**2 * (1-q)**2 ))

###############################################################################################
#Formula from PHYSICAL REVIEW D 95, 104004
def R_m (S_plus, S_minus): return S_plus**2 + S_minus**2

def cp (S_plus,c1,eta): return (S_plus**2 * eta**2 - c1**2)

def cm ( S_minus, c1, eta): return (S_minus**2 * eta**2 - c1**2)

def ad (S1, S2, eta, delta_m, c1, xi, cp, cm) :
    t1 = -3*(S1**2 - S2**2 )* eta * delta_m
    t2 = 3 * (c1/eta)*(c1 - 2*eta**2 * xi)
    return (t1 + t2)/( 4 * np.sqrt(cp * cm))

def cd (c1, eta, cp, cm, Rm): return (3 / 128) * (Rm**2 / ( eta * np.sqrt(cp * cm)))

def hd(c1, eta, cp, cm): return (c1/eta**2) * (1 - (cp + cm)/(2 * np.sqrt(cp*cm))) 

def fd (cp, cm, eta): return (cp + cm)/(8*eta**4) * (1 - (cp+cm)/(2 * np.sqrt(cp*cm)))

###############################################################################################
#PHYSICAL REVIEW D 95, 104004
def Omega_z_0 (a1, ad): return a1+ad

def Omega_z_1 (a2, ad, xi, hd): return a2 - ad*xi - ad*hd

def Omega_z_2 (ad, hd, xi, cd, fd): return ad*hd*xi + cd - ad*fd + ad*hd**2

def Omega_z_4 (cd, ad, hd, fd, xi): return (cd+ad*hd**2 - 2 *ad*fd)*(hd*xi + hd**2 -fd) - ad*fd**2

def Omega_z_5 (cd, ad, fd, hd, xi): 
    t1 = cd - ad*fd + ad*hd**2
    t2 = xi + 2 * hd
    t3 = cd + ad*hd**2 - 2*ad*fd
    t4 = xi + hd
    return t1*fd*t2 - t3*hd**2 * t4 - ad*fd**2 * hd

###############################################################################################
#PHYSICAL REVIEW D 95, 104004
def Omega_z_0_avg (g0, O_z_0): return 3 * g0 * O_z_0

def Omega_z_1_avg (g0, O_z_1): return 3 * g0 * O_z_1

def Omega_z_2_avg (g0,g2, O_z_2, O_z_0): return 3*(g0*O_z_2 + g2 * O_z_0)

def Omega_z_3_avg (g0, g2, g3,O_z_3, O_z_1, O_z_0): return 3*(g0*O_z_3 + g2*O_z_1 + g3*O_z_0)

def Omega_z_4_avg (g0,g2,g3,g4, O_z_4, O_z_2,  O_z_1, O_z_0): return 3*(g0*O_z_4 + g2*O_z_2 +g3 * O_z_1
                                                                        + g4*O_z_0)
def Omega_z_5_avg(g0, g2, g3,g4,g5, O_z_5, O_z_3, O_z2, O_z_1, O_z_0):
    return 3*(g0*O_z_5 + g2*O_z_3 + g3*O_z_2 + g4*O_z_1 + g5 * O_z_0)

###############################################################################################

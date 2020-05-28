#给出计算函数
#利用BSM模型计算期权价格的函数
def BSMOption(S,K,t,r,sigma,type):

    d1 = (np.log(S/K)+(r+(sigma**2/2))*t)/(sigma*np.sqrt(t))
    d2=d1-sigma*np.sqrt(t)

    if (type=='CO'):
        C = S*n.cdf(d1)-(K*np.exp(-r*t)*n.cdf(d2))
        return C
    else:
        P = K*np.exp(-r*t)*n.cdf(-d2)-S*n.cdf(-d1)
        return P

#利用Bisection 方法计算隐含波动率
def bisect(S,K,r,t,types,MP):

    a = 0.0001       #最小值
    b = 0.9999        #最大值
    N = 1       #迭代数
    #N=3
    tol = 10**-4

    # #利用Bisection方法计算隐含波动率的匿名函数
    f = lambda s:BSMOption(S,K,t,r,s,types)-MP

    while (N<=200):
        sig = (a+b)/2
        if (f(sig)==0 or (b-a)/2<tol):
            return sig
        N = N+1
        if (np.sign(f(sig))==np.sign(f(a))):
            a = sig
        else:
            b = sig

#利用secant方法计算隐含波动率
def secant(S,K,r,t,types,MP):

    x0 = 0.09
    xx = 1
    tolerance = 10**(-7)
    epsilon = 10**(-14)

    maxIterations = 200
    SolutionFound = False

    #利用Secant方法计算隐含波动率的匿名函数
    f = lambda s:BSMOption(S,K,t,r,s,types)-MP

    for i in range(1,maxIterations+1):
        y = f(x0)
        yprime = (f(x0)-f(xx))/(x0-xx)

        if (abs(yprime)<epsilon):
            break

        x1 = x0 - y/yprime

        if (abs(x1-x0)<=tolerance*abs(x1)):
            SolutionFound = True
            break
        x0 = x1

    if (SolutionFound):
        return x1
    else:
        print ("Did not converge")

    #利用newton方法计算隐含波动率
def newton(S,K,r,t,types,MP):

    x0 = 1
    xx = 0.001
    tolerance = 10**(-7)
    epsilon = 10**(-14)

    maxIterations = 200
    SolutionFound = False

    #
    # #利用Newton方法计算隐含波动率的匿名函数
    f = lambda s:BSMOption(S,K,t,r,s,types)-MP

    for i in range(1,maxIterations+1):
        y = f(x0)
        yprime = (f(x0+xx)-f(x0-xx))/(2*x0*xx)

        if (abs(yprime)<epsilon):
            break

        x1 = x0 - y/yprime

        if (abs(x1-x0)<=tolerance*abs(x1)):
            SolutionFound = True
            break

        x0 = x1

    if (SolutionFound):
        return x1
    else:
        print ("Did not converge")
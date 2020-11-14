import src.general_classes.general as General

class Signal:
    def __init__(self, parent, *args, **kwargs) -> None:

        self.parent = parent

        self.v = 193.4 * 10 ** 12
        self.h = 6.62606957  * 10 ** (-34) #Planck constant
        self.Fn = 5.0 #Amplifier Noise Figure
        self.fn = General.dBtoLinear(self.Fn)
        self.Bo = 12.5 * 10 ** 9 #Reference Bandwidth
        self.Alpha = 0.2 * 10 ** (-3) #Amplifier Gain distribution dB/m
        self.pIn = 0.001
        self.Pin = General.linearWTodBm(self.pIn)
        self.pRef = 0.001
        self.Pref = General.linearWTodBm(self.pRef)
        self.OSNRin = 30
        self.osnrIn = General.dBtoLinear(self.OSNRin)


    def initialise(self) -> None:
        self.signalPower = self.pIn
        self.asePower = self.pIn / self.osnrIn
        self.nlPower = 0.0


    def setSignalPower(self, powerWatts: float) -> None:
        self.signalPower = powerWatts


    def getSignalPower(self) -> float:
        return self.signalPower


    def setASEPower(self, powerWatts: float):
        self.asePower = powerWatts


    def getAsePower(self):
        return self.asePower


    def setNonLinearPower(self, powerWatts: float) -> float:
        self.nlPower = powerWatts


    def getNonLinearPower(self) -> float:
        return self.nlPower


    def getosnr(self) -> float:
        return self.signalPower/(self.asePower+self.nlPower);


    def getOSNR(self) -> float:
        return 10 * General.linearTodB(self.getosnr())


    def pASE(self, fn: float, gain: float) -> float:
        return 2 * self.nASE(fn, gain) * self.Bo


    def nASE(self, fn: float, gain: float) -> float: #Densidade Espectral de Ruído por polarização
        assert(gain >= 1.0) 
        return (self.h * self.v * (gain-1.0) * fn)/2.0

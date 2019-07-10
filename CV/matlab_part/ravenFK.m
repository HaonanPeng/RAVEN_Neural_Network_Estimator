function T=ravenFK(th1,th2,d3,th4,th5,th6)
% Input should be rad and micro meter.
%This function will return the 4x4 transform matix
toRad=pi/180;
mtoMicrometer=10^6;

th1 = -th1 * toRad;
th2 = th2 * toRad;
d3 = d3;
th4 = th4 * toRad;
th5 = th5 * toRad;
th6 = th6 * toRad;

La12=75*toRad;
La23=52*toRad;
La3=0;
d4=-0.470*mtoMicrometer;
Lw=0.01612*mtoMicrometer;

T=DHcalculator(0,0,0,th1)*DHcalculator(La12,0,0,th2)*DHcalculator(pi-La23,0,d3,pi/2)*DHcalculator(0,La3,d4,th4)*DHcalculator(pi/2,0,0,th5);%*DHcalculator(pi/2,Lw,0,th6);

T(1,4) = T(1,4);
T(3,4) = -T(3,4);
T(2,4) = -T(2,4);

end
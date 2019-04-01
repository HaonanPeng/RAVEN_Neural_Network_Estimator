function T=ravenFK(th1,th2,d3,th4,th5,th6)
% Input should be rad.
%This function will return the 4x4 transform matix

toRad=pi/180;
mtoMicrometer=10^6;

La12=75*toRad;
La23=52*toRad;
La3=0;
d4=-0.47*mtoMicrometer;
Lw=0.013*mtoMicrometer;

T=DHcalculator(0,0,0,th1)*DHcalculator(La12,0,0,th2)*DHcalculator(pi-La23,0,d3,pi/2)*DHcalculator(0,La3,d4,th4)*DHcalculator(pi/2,0,0,th5)*DHcalculator(pi/2,Lw,0,th6);

end
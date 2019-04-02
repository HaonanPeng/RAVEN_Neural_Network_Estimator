function T=DHcalculator(al,a,d,th)
T=Transxrad(al,0,0,0)*Transxrad(0,a,0,0)*Transzrad(th,0,0,0)*Transzrad(0,0,0,d);
end
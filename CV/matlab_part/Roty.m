function MRoty=Roty(th)
thd=th*pi/180;
MRoty=[cos(thd),0,sin(thd);0,1,0;-sin(thd),0,cos(thd)];

end
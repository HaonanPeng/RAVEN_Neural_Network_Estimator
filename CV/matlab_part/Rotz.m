function MRotz=Rotz(th)
thd=th*pi/180;
MRotz=[cos(thd),-sin(thd),0;sin(thd),cos(thd),0;0,0,1];

end
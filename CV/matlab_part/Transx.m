function MTransx=Transx(th,x,y,z)
thd=th*pi/180;
MTransx=[1,0,0,x;0,cos(thd),-sin(thd),y;0,sin(thd),cos(thd),z;0,0,0,1];

end
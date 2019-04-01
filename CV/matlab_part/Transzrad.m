function MTransz=Transzrad(th,x,y,z)
thd=th;
MTransz=[cos(thd),-sin(thd),0,x;sin(thd),cos(thd),0,y;0,0,1,z;0,0,0,1];

end
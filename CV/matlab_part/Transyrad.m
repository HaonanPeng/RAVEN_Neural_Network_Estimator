function MTransy=Transyrad(th,x,y,z)
thd=th;
MTransy=[cos(thd),0,sin(thd),x;0,1,0,y;-sin(thd),0,cos(thd),z;0,0,0,1];

end
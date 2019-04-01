function MRotk=Rotk(kx,ky,kz,th)
%this is function about rotate about a non-xyz axis
n=norm([kx;ky;kz],2);
kx=kx/n;
ky=ky/n;
kz=kz/n;
thd=th*pi/180;
c=cos(thd);
v=1-cos(thd);
s=sin(thd);
MRotk=[kx^2*v+c,kx*ky*v-kz*s,kx*kz*v+ky*s;
    kx*ky*v+kz*s,ky^2*v+c,ky*kz*v-kx*s;
    kx*kz*v-ky*s,ky*kz*v+kx*s,kz^2*v+c];

end
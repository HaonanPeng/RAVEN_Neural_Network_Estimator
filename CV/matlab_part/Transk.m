function MRotk=Transk(kx,ky,kz,th)
%this is function about rotate about a non-xyz axis in T form, do not
%contain translation
n=norm([kx;ky;kz],2);
kx=kx/n;
ky=ky/n;
kz=kz/n;
thd=th*pi/180;
c=cos(thd);
v=1-cos(thd);
s=sin(thd);
MRotk=[kx^2*v+c,kx*ky*v-kz*s,kx*kz*v+ky*s,0;
    kx*ky*v+kz*s,ky^2*v+c,ky*kz*v-kx*s,0;
    kx*kz*v-ky*s,ky*kz*v+kx*s,kz^2*v+c,0;
    0,0,0,1];

end
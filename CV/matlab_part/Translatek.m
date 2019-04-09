function MRotk=Translatek(kx,ky,kz,length)
%this is function about translate about a non-xyz axis in T form, do not
%contain rotation
n=norm([kx;ky;kz],2);
kx=kx/n;
ky=ky/n;
kz=kz/n;
kx=kx*length;
ky=ky*length;
kz=kz*length;
MRotk=[1,0,0,kx;
    0,1,0,ky;
    0,0,1,kz;
    0,0,0,1];
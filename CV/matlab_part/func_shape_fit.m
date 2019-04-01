close all, clear all, clc

syms x


for sigma = 0.1:0.1:1
    y1 = normpdf(x,0,sigma);
    
    a = 1/double(subs(y1,x,0));
    y2 = 1/(x^1.5+a);
    
    figure()
    fplot((y1+y2)/2,[0,5*sigma])
    hold on;
    fplot(y1,[0,5*sigma])
    fplot(y2,[0,5*sigma])
    legend('y1+y2','y1','y2')
    title(sprintf('sigma = %d', sigma))
end






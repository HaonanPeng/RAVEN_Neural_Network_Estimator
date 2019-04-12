close all, clear all, clc

decay = 0.5;
inter = 0.1;
for i = 1:30
    decay = decay + 0.5^i*inter;
end

ans = decay
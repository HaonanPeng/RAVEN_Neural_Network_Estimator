close all, clear all, clc
raven_state = importdata('raven_state_traj2.txt');
raven_center = raven_state(:,1:4);
dlmwrite('raven_state_center.txt',raven_center)

for i = 108:115
    figure(i)
    plot(raven_state(:,i))
    
end
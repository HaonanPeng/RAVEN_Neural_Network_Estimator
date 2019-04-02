close all, clear all, clc

result_traj1 = importdata('img_process_result_traj1_new.txt');
time = result_traj1(:,2) - result_traj1(1,2);
% filter setting
windowSize = 5; 

figure()
plot( result_traj1(:,3))
hold on
plot( result_traj1(:,4))
plot( result_traj1(:,5))
title('green')
xlabel('time')
ylabel('position')
legend('x','y','z')

figure()
plot(time , result_traj1(:,6))
hold on
plot(time , result_traj1(:,7))
plot(time , result_traj1(:,8))
title('yellow')
xlabel('time')
ylabel('position')
legend('x','y','z')

figure()
plot(time , result_traj1(:,9))
hold on
plot(time , result_traj1(:,10))
plot(time , result_traj1(:,11))
title('red')
xlabel('time')
ylabel('position')
legend('x','y','z')

figure()
plot(time , result_traj1(:,5),'g')
hold on
plot(time , result_traj1(:,8),'y')
plot(time , result_traj1(:,11),'r')
title('Z Axis')
xlabel('time')
ylabel('position')
legend('green','yellow','red')
close all, clear all, clc

result_traj1 = importdata('img_process_result_traj2.txt');

% filter setting
windowSize = 5; 

figure()
plot3(moving_average_filter(result_traj1(:,3),windowSize),moving_average_filter(result_traj1(:,4),windowSize),moving_average_filter(result_traj1(:,5),windowSize),'g')
hold on
plot3(moving_average_filter(result_traj1(:,6),windowSize),moving_average_filter(result_traj1(:,7),windowSize),moving_average_filter(result_traj1(:,8),windowSize),'y')
plot3(moving_average_filter(result_traj1(:,9),windowSize),moving_average_filter(result_traj1(:,10),windowSize),moving_average_filter(result_traj1(:,11),windowSize),'r')

xlabel('x')
ylabel('y')
zlabel('z')

legend('green','yellow','red')


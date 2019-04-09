close all, clear all, clc

ball_traj_frameWorld = importdata('img_process_result_traj1.txt');
raven_center_traj_frameWorld = importdata('img_process_result_traj1_raven_center.txt');
raven_state = importdata('raven_state_traj1_toggled.txt');

um2mm = 0.001;

%% raven frames defination, for left arm
R_b_w = Rotz(90);
T_b_w = zeros(4,4);
T_b_w(1:3,1:3) = R_b_w;
T_b_w(:,4) = [-2.2 ; -70 ; 435.65 ; 1];

T_0_b = [0, 0, 1,300.71;
         0,-1, 0,61;
         1, 0, 0,-7;
         0, 0, 0,1];

T_b_0 = inverse_trans_matrix(T_0_b);
T_w_b = inverse_trans_matrix(T_b_w);

%% 3D ball centers and end effector center

% filter setting
windowSize = 10; 

% frame transform
% raven_center_traj_frame0_T = raven_center_traj_frame0' ;
% raven_center_traj_frame0_T(4,:) = 1;
% raven_center_traj_frameBase_T = T_0_b * raven_center_traj_frame0_T;
% raven_center_traj_frameWorld_T = T_w_b * raven_center_traj_frameBase_T;
% raven_center_traj_frameWorld = raven_center_traj_frameWorld_T';
% raven_center_traj_frameWorld = raven_center_traj_frame0;

% draw single ball
figure()
plot3(ball_traj_frameWorld(:,3),ball_traj_frameWorld(:,4),ball_traj_frameWorld(:,5),'g')
hold on
plot3(ball_traj_frameWorld(:,6),ball_traj_frameWorld(:,7),ball_traj_frameWorld(:,8),'y')
plot3(ball_traj_frameWorld(:,9),ball_traj_frameWorld(:,10),ball_traj_frameWorld(:,11),'r')

plot3(raven_center_traj_frameWorld(:,1),raven_center_traj_frameWorld(:,2),raven_center_traj_frameWorld(:,3),'linewidth',2)

xlabel('x(mm)')
ylabel('y(mm)')
zlabel('z(mm)')

legend('greenBall','yellowBall','redBall','end effector')
title('Position of Balls and end effector in World Frame')



%% 3D draw raven end effector traj with CV and RAVEN state
ravenstate_center_traj_frame0 = raven_state(:,230:232)*um2mm;
ravenstate_center_traj_frame0_T = ravenstate_center_traj_frame0' ;
ravenstate_center_traj_frame0_T(4,:) = 1;
ravenstate_center_traj_frameBase_T = T_0_b * ravenstate_center_traj_frame0_T;
ravenstate_center_traj_frameWorld_T = T_b_w * ravenstate_center_traj_frameBase_T;
ravenstate_center_traj_frameWorld = ravenstate_center_traj_frameWorld_T';



figure()
plot3(raven_center_traj_frameWorld(:,1),raven_center_traj_frameWorld(:,2),raven_center_traj_frameWorld(:,3))
hold on 
plot3(ravenstate_center_traj_frameWorld(:,1),ravenstate_center_traj_frameWorld(:,2),ravenstate_center_traj_frameWorld(:,3))
xlabel('x(mm)')
ylabel('y(mm)')
zlabel('z(mm)')
title('raven center')
legend('CV','ravenstate pos')
title('Position of the end effector')

%% 2D draw raven end effector traj with CV and RAVEN state
raven_pos_x_frameWorld = raven_center_traj_frameWorld(:,1);
raven_pos_x_frameWorld_filtered = moving_average_filter(raven_pos_x_frameWorld,windowSize);
figure()
plot(ball_traj_frameWorld(:,2)-ball_traj_frameWorld(1,2),)
hold on
plot(raven_state(:,1)-ball_traj_frameWorld(1,2),ravenstate_center_traj_frameWorld(:,1))
xlabel('time(s)')
ylabel('position(mm)')
title('End Effecor Position in X axis')
legend('CV','ravenstate pos')

figure()
plot(ball_traj_frameWorld(:,2)-ball_traj_frameWorld(1,2),moving_average_filter(raven_center_traj_frameWorld(:,2),windowSize))
hold on
plot(raven_state(:,1)-ball_traj_frameWorld(1,2),ravenstate_center_traj_frameWorld(:,2))
xlabel('time(s)')
ylabel('position(mm)')
title('End Effecor Position in Y axis')
legend('CV','ravenstate pos')

figure()
plot(ball_traj_frameWorld(:,2)-ball_traj_frameWorld(1,2),moving_average_filter(raven_center_traj_frameWorld(:,3),windowSize))
hold on
plot(raven_state(:,1)-ball_traj_frameWorld(1,2),ravenstate_center_traj_frameWorld(:,3))
xlabel('time(s)')
ylabel('position(mm)')
title('End Effecor Position in Z axis')
legend('CV','ravenstate pos')

%% 2D draw raven end effector traj with CV and RAVEN state FK
result_traj_size = size(ball_traj_frameWorld);
for iter = 1:result_traj_size(1)
    [M , idx] = min(abs(raven_state(:,1)-ball_traj_frameWorld(iter,2)));
    T = ravenFK(raven_state(idx,108),raven_state(idx,109),1000000*pi/180*raven_state(idx,110),raven_state(idx,112),raven_state(idx,113),raven_state(idx,114));
    raven_center_FK(iter,:) = T(1:3,4)';

end
ravenstate_center_FK_traj_frame0 = raven_center_FK*um2mm;
ravenstate_center_FK_traj_frame0_T = ravenstate_center_FK_traj_frame0' ;
ravenstate_center_FK_traj_frame0_T(4,:) = 1;
ravenstate_center_FK_traj_frameBase_T = T_0_b * ravenstate_center_FK_traj_frame0_T;
ravenstate_center_FK_traj_frameWorld_T = T_b_w * ravenstate_center_FK_traj_frameBase_T;
ravenstate_center_FK_traj_frameWorld = ravenstate_center_FK_traj_frameWorld_T';

figure()
plot(ball_traj_frameWorld(:,2)-ball_traj_frameWorld(1,2),raven_center_traj_frameWorld(:,1))
hold on
plot(ball_traj_frameWorld(:,2)-ball_traj_frameWorld(1,2),ravenstate_center_FK_traj_frameWorld(:,1))
xlabel('time')
ylabel('position')
title('x_FK')
legend('CV','RavenState_FK')

figure()
plot(ball_traj_frameWorld(:,2)-ball_traj_frameWorld(1,2),raven_center_traj_frameWorld(:,2))
hold on
plot(ball_traj_frameWorld(:,2)-ball_traj_frameWorld(1,2),ravenstate_center_FK_traj_frameWorld(:,2))
xlabel('time')
ylabel('position')
title('y_FK')
legend('CV','RavenState_FK')

figure()
plot(ball_traj_frameWorld(:,2)-ball_traj_frameWorld(1,2),raven_center_traj_frameWorld(:,3))
hold on
plot(ball_traj_frameWorld(:,2)-ball_traj_frameWorld(1,2),ravenstate_center_FK_traj_frameWorld(:,3))
xlabel('time')
ylabel('position')
title('z_FK')
legend('CV','RavenState_FK')

close all, clear all, clc

ball_traj_frameWorld_CV = importdata('img_process_result_traj1.txt');
raven_center_traj_frameWorld_CV = importdata('img_process_result_traj1_raven_center.txt');
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
windowSize = 11; 

% frame transform
% raven_center_traj_frame0_T = raven_center_traj_frame0' ;
% raven_center_traj_frame0_T(4,:) = 1;
% raven_center_traj_frameBase_T = T_0_b * raven_center_traj_frame0_T;
% raven_center_traj_frameWorld_T = T_w_b * raven_center_traj_frameBase_T;
% raven_center_traj_frameWorld = raven_center_traj_frameWorld_T';
% raven_center_traj_frameWorld = raven_center_traj_frame0;

% draw single ball
figure()
plot3(ball_traj_frameWorld_CV(:,3),ball_traj_frameWorld_CV(:,4),ball_traj_frameWorld_CV(:,5),'g')
hold on
plot3(ball_traj_frameWorld_CV(:,6),ball_traj_frameWorld_CV(:,7),ball_traj_frameWorld_CV(:,8),'y')
plot3(ball_traj_frameWorld_CV(:,9),ball_traj_frameWorld_CV(:,10),ball_traj_frameWorld_CV(:,11),'r')

plot3(raven_center_traj_frameWorld_CV(:,1),raven_center_traj_frameWorld_CV(:,2),raven_center_traj_frameWorld_CV(:,3),'linewidth',2)

xlabel('x(mm)')
ylabel('y(mm)')
zlabel('z(mm)')

legend('greenBall','yellowBall','redBall','end effector')
title('Position of Balls and end effector in World Frame')



%% 3D draw raven end effector traj with CV and RAVEN state
raven_center_traj_frame0_ravenstate = raven_state(:,230:232)*um2mm;
raven_center_traj_frame0_T_ravenstate = raven_center_traj_frame0_ravenstate' ;
raven_center_traj_frame0_T_ravenstate(4,:) = 1;
raven_center_traj_frameBase_T_ravenstate = T_0_b * raven_center_traj_frame0_T_ravenstate;
raven_center_traj_frameWorld_T_ravenstate = T_b_w * raven_center_traj_frameBase_T_ravenstate;
raven_center_traj_frameWorld_ravenstate = raven_center_traj_frameWorld_T_ravenstate';



figure()
plot3(raven_center_traj_frameWorld_CV(:,1),raven_center_traj_frameWorld_CV(:,2),raven_center_traj_frameWorld_CV(:,3))
hold on 
plot3(raven_center_traj_frameWorld_ravenstate(:,1),raven_center_traj_frameWorld_ravenstate(:,2),raven_center_traj_frameWorld_ravenstate(:,3))
xlabel('x(mm)')
ylabel('y(mm)')
zlabel('z(mm)')
title('raven center')
legend('CV','ravenstate pos')
title('Position of the end effector')

%% 2D draw raven end effector traj with CV and RAVEN state
time_difference = 0.8*1.18;
time_decay = 0.6;
time_ravenstate = raven_state(:,1)-ball_traj_frameWorld_CV(1,2) + time_difference;
time_CV = ball_traj_frameWorld_CV(:,2)-ball_traj_frameWorld_CV(1,2)-time_decay;

raven_pos_x_frameWorld_CV = raven_center_traj_frameWorld_CV(:,1);
raven_pos_x_frameWorld_filtered = moving_average_filter(raven_pos_x_frameWorld_CV,windowSize);
figure()
plot(time_CV,raven_pos_x_frameWorld_CV,'y--')
hold on
plot(time_ravenstate,raven_center_traj_frameWorld_ravenstate(:,1),'r')
plot(time_CV(windowSize:(end-windowSize)),raven_pos_x_frameWorld_filtered(windowSize:(end-windowSize)),'b');

xlabel('time(s)')
ylabel('position(mm)')
title('End Effecor Position in X axis')
legend('CV raw','ravenstate pos','CV filtered')

raven_pos_y_frameWorld_CV = raven_center_traj_frameWorld_CV(:,2);
raven_pos_y_frameWorld_CV_filtered = moving_average_filter(raven_pos_y_frameWorld_CV,windowSize);
figure()
plot(time_CV,raven_pos_y_frameWorld_CV,'y--')
hold on
plot(time_ravenstate,raven_center_traj_frameWorld_ravenstate(:,2),'r')
plot(time_CV(windowSize:(end-windowSize)),raven_pos_y_frameWorld_CV_filtered(windowSize:(end-windowSize)),'b');
xlabel('time(s)')
ylabel('position(mm)')
title('End Effecor Position in Y axis')
legend('CV raw','ravenstate pos', 'CV filtered')


raven_pos_z_frameWorld_CV = raven_center_traj_frameWorld_CV(:,3);
raven_pos_z_frameWorld_CV_filtered = moving_average_filter(raven_pos_z_frameWorld_CV,windowSize);
figure()
plot(time_CV,raven_pos_z_frameWorld_CV,'y--')
hold on
plot(time_ravenstate,raven_center_traj_frameWorld_ravenstate(:,3),'r')
plot(time_CV(windowSize:(end-windowSize)),raven_pos_z_frameWorld_CV_filtered(windowSize:(end-windowSize)),'b');
xlabel('time(s)')
ylabel('position(mm)')
title('End Effecor Position in Z axis')
legend('CV raw','ravenstate pos', 'CV filtered')

%% 2D orientation of the endeffector
T_0_w = T_b_w * T_0_b;
size_ravenstate = size(raven_state);
size_CV = size(raven_center_traj_frameWorld_CV);

for idx = 1 : size_ravenstate(1) % rotation of end effector from raven state
    T_frame0_ravenstate = zeros(4,4);
    T_frame0_ravenstate(1:3,1:3) = reshape(raven_state(idx,8:16),[3,3]);
    T_frame0_ravenstate(1:3,4) = raven_state(idx,230:232);
    T_frame0_ravenstate(4,4) = 1;
    T_frameWorld_ravenstate = T_0_w * inverse_trans_matrix(T_frame0_ravenstate);
    eulZYX_frameWorld_ravenstate(idx,:) = rotm2eul(T_frameWorld_ravenstate(1:3,1:3));
end

for idx = 1 : size_CV(1) % rotation of end effector from CV
    T_frameWorld_CV = reshape(raven_center_traj_frameWorld_CV(idx,4:19),[4,4]);
    eulZYX_frameWorld_CV(idx,:) = rotm2eul(T_frameWorld_CV(1:3,1:3));
end

figure()
plot(time_CV,eulZYX_frameWorld_CV(:,1))
hold on
plot(time_ravenstate,eulZYX_frameWorld_ravenstate(:,1))
xlabel('time(s)')
ylabel('angel(rad)')
title('end effector rotation in world frame, Z axis')
legend('CV','ravenstate')

figure()
plot(time_CV,eulZYX_frameWorld_CV(:,2))
hold on
plot(time_ravenstate,eulZYX_frameWorld_ravenstate(:,2))
xlabel('time(s)')
ylabel('angel(rad)')
title('end effector rotation in world frame, Y axis')
legend('CV','ravenstate')

figure()
plot(time_CV,eulZYX_frameWorld_CV(:,3))
hold on
plot(time_ravenstate,eulZYX_frameWorld_ravenstate(:,3))
xlabel('time(s)')
ylabel('angel(rad)')
title('end effector rotation in world frame, X axis')
legend('CV','ravenstate')

%% 2D draw raven end effector traj with CV and RAVEN state FK
% result_traj_size = size(ball_traj_frameWorld_CV);
% for iter = 1:result_traj_size(1)
%     [M , idx] = min(abs(raven_state(:,1)-ball_traj_frameWorld_CV(iter,2)));
%     T = ravenFK(raven_state(idx,108),raven_state(idx,109),1000000*pi/180*raven_state(idx,110),raven_state(idx,112),raven_state(idx,113),raven_state(idx,114));
%     raven_center_FK(iter,:) = T(1:3,4)';
% 
% end
% ravenstate_center_FK_traj_frame0 = raven_center_FK*um2mm;
% ravenstate_center_FK_traj_frame0_T = ravenstate_center_FK_traj_frame0' ;
% ravenstate_center_FK_traj_frame0_T(4,:) = 1;
% ravenstate_center_FK_traj_frameBase_T = T_0_b * ravenstate_center_FK_traj_frame0_T;
% ravenstate_center_FK_traj_frameWorld_T = T_b_w * ravenstate_center_FK_traj_frameBase_T;
% ravenstate_center_FK_traj_frameWorld = ravenstate_center_FK_traj_frameWorld_T';
% 
% figure()
% plot(ball_traj_frameWorld_CV(:,2)-ball_traj_frameWorld_CV(1,2),raven_center_traj_frameWorld_CV(:,1))
% hold on
% plot(ball_traj_frameWorld_CV(:,2)-ball_traj_frameWorld_CV(1,2),ravenstate_center_FK_traj_frameWorld(:,1))
% plot(time_ravenstate, raven_center_traj_frameWorld_ravenstate(:,1))
% xlabel('time')
% ylabel('position')
% title('x FK')
% legend('CV','ravenstate FK','ravenstate pos')
% 
% figure()
% plot(ball_traj_frameWorld_CV(:,2)-ball_traj_frameWorld_CV(1,2),raven_center_traj_frameWorld_CV(:,2))
% hold on
% plot(ball_traj_frameWorld_CV(:,2)-ball_traj_frameWorld_CV(1,2),ravenstate_center_FK_traj_frameWorld(:,2))
% plot(time_ravenstate, raven_center_traj_frameWorld_ravenstate(:,2))
% xlabel('time')
% ylabel('position')
% title('y FK')
% legend('CV','ravenstate FK','ravenstate pos')
% 
% figure()
% plot(ball_traj_frameWorld_CV(:,2)-ball_traj_frameWorld_CV(1,2),raven_center_traj_frameWorld_CV(:,3))
% hold on
% plot(ball_traj_frameWorld_CV(:,2)-ball_traj_frameWorld_CV(1,2),ravenstate_center_FK_traj_frameWorld(:,3))
% plot(time_ravenstate, raven_center_traj_frameWorld_ravenstate(:,3))
% xlabel('time')
% ylabel('position')
% title('z FK')
% legend('CV','ravenstate FK','ravenstate pos')

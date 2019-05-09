close all, clear all, clc

ball_traj_frameWorld_CV = importdata('data_files/img_process_result_traj11_filtered.txt');
raven_center_traj_frameWorld_CV = importdata('data_files/img_process_result_traj11_raven_center_filtered.txt');
raven_state = importdata('data_files/raven_state_traj11_toggled.txt');

ball_traj_frameWorld_CV_unfiltered = importdata('data_files/img_process_result_traj11.txt');
raven_center_traj_frameWorld_CV_unfiltered = importdata('data_files/img_process_result_traj11_raven_center.txt');

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
fig1 = figure();
plot3(ball_traj_frameWorld_CV(:,3),ball_traj_frameWorld_CV(:,4),ball_traj_frameWorld_CV(:,5),'g')
hold on
plot3(ball_traj_frameWorld_CV(:,6),ball_traj_frameWorld_CV(:,7),ball_traj_frameWorld_CV(:,8),'y')
plot3(ball_traj_frameWorld_CV(:,9),ball_traj_frameWorld_CV(:,10),ball_traj_frameWorld_CV(:,11),'r')

plot3(raven_center_traj_frameWorld_CV(:,2),raven_center_traj_frameWorld_CV(:,3),raven_center_traj_frameWorld_CV(:,4),'linewidth',2)

xlabel('x(mm)')
ylabel('y(mm)')
zlabel('z(mm)')

legend('green ball','yellow ball','red ball','end effector')
title('Position of Balls and end effector in World Frame')
saveas(fig1,'result_figures/Position of Balls and end effector in World Frame.png')
saveas(fig1,'result_figures/Position of Balls and end effector in World Frame.fig')



%% 3D draw raven end effector traj with CV and RAVEN state
raven_center_traj_frame0_ravenstate = raven_state(:,2:4)*um2mm;
raven_center_traj_frame0_T_ravenstate = raven_center_traj_frame0_ravenstate' ;
raven_center_traj_frame0_T_ravenstate(4,:) = 1;
raven_center_traj_frameBase_T_ravenstate = T_0_b * raven_center_traj_frame0_T_ravenstate;
raven_center_traj_frameWorld_T_ravenstate = T_b_w * raven_center_traj_frameBase_T_ravenstate;
raven_center_traj_frameWorld_ravenstate = raven_center_traj_frameWorld_T_ravenstate';



fig2 = figure();
plot3(raven_center_traj_frameWorld_CV(:,2),raven_center_traj_frameWorld_CV(:,3),raven_center_traj_frameWorld_CV(:,4))
hold on 
plot3(raven_center_traj_frameWorld_ravenstate(:,1),raven_center_traj_frameWorld_ravenstate(:,2),raven_center_traj_frameWorld_ravenstate(:,3))
xlabel('x(mm)')
ylabel('y(mm)')
zlabel('z(mm)')
legend('CV','ravenstate pos')
title('Position of the end effector in World Frame')
saveas(fig2,'result_figures/Position of the end effector.png')
saveas(fig2,'result_figures/Position of the end effector.fig')

%% 2D draw raven end effector traj with CV and RAVEN state
time_difference = 0;
time_decay = 0.6;
time_ravenstate = raven_state(:,1)-ball_traj_frameWorld_CV(1,2) + time_difference;
time_CV = ball_traj_frameWorld_CV(:,2)-ball_traj_frameWorld_CV(1,2)-time_decay;
time_CV_unfiltered = ball_traj_frameWorld_CV_unfiltered(:,2)-ball_traj_frameWorld_CV(1,2)-time_decay;

raven_pos_x_frameWorld_CV = raven_center_traj_frameWorld_CV(:,2);

fig3 = figure();
plot(time_CV_unfiltered,raven_center_traj_frameWorld_CV_unfiltered(:,2),'g--')
hold on
plot(time_CV,raven_pos_x_frameWorld_CV,'b')

plot(time_ravenstate,raven_center_traj_frameWorld_ravenstate(:,1),'r')

xlabel('time(s)')
ylabel('position(mm)')
title('End Effecor Position in X axis in World Frame')
legend('CV unfiltered','CV filtered','ravenstate pos')
saveas(fig3,'result_figures/End Effecor Position in X axis.png')
saveas(fig3,'result_figures/End Effecor Position in X axis.fig')

raven_pos_y_frameWorld_CV = raven_center_traj_frameWorld_CV(:,3);
fig4 = figure();
plot(time_CV_unfiltered,raven_center_traj_frameWorld_CV_unfiltered(:,3),'g--')
hold on
plot(time_CV,raven_pos_y_frameWorld_CV,'b')
plot(time_ravenstate,raven_center_traj_frameWorld_ravenstate(:,2),'r')
xlabel('time(s)')
ylabel('position(mm)')
title('End Effecor Position in Y axis in World Frame')
legend('CV unfiltered','CV filtered','ravenstate pos')
saveas(fig4,'result_figures/End Effecor Position in Y axis.png')
saveas(fig4,'result_figures/End Effecor Position in Y axis.fig')


raven_pos_z_frameWorld_CV = raven_center_traj_frameWorld_CV(:,4);
fig5 = figure();
plot(time_CV_unfiltered,raven_center_traj_frameWorld_CV_unfiltered(:,4),'g--')
hold on
plot(time_CV,raven_pos_z_frameWorld_CV,'b')
plot(time_ravenstate,raven_center_traj_frameWorld_ravenstate(:,3),'r')
xlabel('time(s)')
ylabel('position(mm)')
title('End Effecor Position in Z axis in World Frame')
legend('CV unfiltered','CV filtered','ravenstate pos')
saveas(fig5,'result_figures/End Effecor Position in Z axis.png')
saveas(fig5,'result_figures/End Effecor Position in Z axis.fig')

%% 2D draw difference between CV and ravenstate position
size_CV = size(raven_center_traj_frameWorld_CV);
for idx_CV = 1 :size_CV(1)
    [M, idx_ravenstate] = min(abs(time_ravenstate - time_CV(idx_CV)));
    difference_x_frameWorld(idx_CV) = raven_center_traj_frameWorld_CV(idx_CV,2) - raven_center_traj_frameWorld_ravenstate(idx_ravenstate,1);
    difference_y_frameWorld(idx_CV) = raven_center_traj_frameWorld_CV(idx_CV,3) - raven_center_traj_frameWorld_ravenstate(idx_ravenstate,2);
    difference_z_frameWorld(idx_CV) = raven_center_traj_frameWorld_CV(idx_CV,4) - raven_center_traj_frameWorld_ravenstate(idx_ravenstate,3);
end
fig9 = figure();
plot(time_CV, difference_x_frameWorld)
hold on 
plot(time_CV, difference_y_frameWorld)
plot(time_CV, difference_z_frameWorld)
xlabel('time(s)')
ylabel('difference(mm)')
legend('x axis','y axis','z axis')
title('Difference between CV and ravenstate Position in World Frame')
saveas(fig5,'result_figures/difference between CV and ravenstate position.png')
saveas(fig5,'result_figures/difference between CV and ravenstate position.fig')

%% 2D orientation of the endeffector
rad2deg = 180/pi;

T_0_w = T_b_w * T_0_b;
size_ravenstate = size(raven_state);
size_CV = size(raven_center_traj_frameWorld_CV);

for idx = 1 : size_ravenstate(1) % rotation of end effector from raven state
    T_frame0_ravenstate = zeros(4,4);
    T_frame0_ravenstate(1:3,1:3) = reshape(raven_state(idx,14:22),[3,3]);
    T_frame0_ravenstate(1:3,4) = raven_state(idx,2:4);
    T_frame0_ravenstate(4,4) = 1;
    T_frameWorld_ravenstate = T_0_w * inverse_trans_matrix(T_frame0_ravenstate);
    eulZYX_frameWorld_ravenstate(idx,:) = rotm2eul(T_frameWorld_ravenstate(1:3,1:3));
end

for idx = 1 : size_CV(1) % rotation of end effector from CV
    T_frameWorld_CV = reshape(raven_center_traj_frameWorld_CV(idx,5:20),[4,4]);
    eulZYX_frameWorld_CV(idx,:) = rotm2eul(T_frameWorld_CV(1:3,1:3));
end

fig6 = figure();
scatter(time_CV,eulZYX_frameWorld_CV(:,1)*rad2deg,1)
hold on
scatter(time_ravenstate,eulZYX_frameWorld_ravenstate(:,1)*rad2deg,1)
xlabel('time(s)')
ylabel('angel(deg)')
title('End Effector Rotation on Z axis in World Frame')
legend('CV','ravenstate')
saveas(fig6,'result_figures/end effector rotation in world frame, Z axis.png')
saveas(fig6,'result_figures/end effector rotation in world frame, Z axis.fig')

fig7 = figure();
scatter(time_CV,eulZYX_frameWorld_CV(:,2)*rad2deg,1)
hold on
scatter(time_ravenstate,eulZYX_frameWorld_ravenstate(:,2)*rad2deg,1)
xlabel('time(s)')
ylabel('angel(deg)')
title('End Effector Rotation on Y axis in World Frame')
legend('CV','ravenstate')
saveas(fig7,'result_figures/end effector rotation in world frame, Y axis.png')
saveas(fig7,'result_figures/end effector rotation in world frame, Y axis.fig')

fig8 = figure();
scatter(time_CV,eulZYX_frameWorld_CV(:,3)*rad2deg,1)
hold on
scatter(time_ravenstate,eulZYX_frameWorld_ravenstate(:,3)*rad2deg,1)
xlabel('time(s)')
ylabel('angel(deg)')
title('End Effector Rotation on X axis in World Frame')
legend('CV','ravenstate')
saveas(fig8,'result_figures/end effector rotation in world frame, X axis.png')
saveas(fig8,'result_figures/end effector rotation in world frame, X axis.fig')

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

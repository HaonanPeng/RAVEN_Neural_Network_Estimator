close all, clear all, clc

result_traj_frameWorld = importdata('img_process_result_traj2.txt');
raven_center_traj_frame0 = importdata('img_process_result_traj2_raven_center.txt');
raven_state = importdata('raven_state.txt');

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
%%

% filter setting
windowSize = 5; 

% frame transform
% raven_center_traj_frame0_T = raven_center_traj_frame0' ;
% raven_center_traj_frame0_T(4,:) = 1;
% raven_center_traj_frameBase_T = T_0_b * raven_center_traj_frame0_T;
% raven_center_traj_frameWorld_T = T_w_b * raven_center_traj_frameBase_T;
% raven_center_traj_frameWorld = raven_center_traj_frameWorld_T';
raven_center_traj_frameWorld = raven_center_traj_frame0;

% draw single ball
figure()
plot3(result_traj_frameWorld(:,3),result_traj_frameWorld(:,4),result_traj_frameWorld(:,5),'g')
hold on
plot3(result_traj_frameWorld(:,6),result_traj_frameWorld(:,7),result_traj_frameWorld(:,8),'y')
plot3(result_traj_frameWorld(:,9),result_traj_frameWorld(:,10),result_traj_frameWorld(:,11),'r')

plot3(raven_center_traj_frameWorld(:,1),raven_center_traj_frameWorld(:,2),raven_center_traj_frameWorld(:,3),'linewidth',2)

xlabel('x')
ylabel('y')
zlabel('z')

legend('greenBall','yellowBall','redBall','raven_center')
title('Position of Balls in World Frame')



%% 3D draw raven end effector traj with CV and RAVEN state
ravenstate_center_traj_frame0 = raven_state(:,2:4)*um2mm;
ravenstate_center_traj_frame0_T = ravenstate_center_traj_frame0' ;
ravenstate_center_traj_frame0_T(4,:) = 1;
ravenstate_center_traj_frameBase_T = T_0_b * ravenstate_center_traj_frame0_T;
ravenstate_center_traj_frameWorld_T = T_b_w * ravenstate_center_traj_frameBase_T;
ravenstate_center_traj_frameWorld = ravenstate_center_traj_frameWorld_T';



figure()
plot3(raven_center_traj_frameWorld(:,1),raven_center_traj_frameWorld(:,2),raven_center_traj_frameWorld(:,3))
hold on 
plot3(ravenstate_center_traj_frameWorld(:,1),ravenstate_center_traj_frameWorld(:,2),ravenstate_center_traj_frameWorld(:,3))
xlabel('x')
ylabel('y')
zlabel('z')
title('raven center')
legend('CV','raven state pos d')

%% 2D draw raven end effector traj with CV and RAVEN state
figure()
plot(result_traj_frameWorld(:,2),result_traj_frameWorld(:,3))
hold on
plot(raven_state(:,1),ravenstate_center_traj_frameWorld(:,1))
xlabel('time')
ylabel('position')
title('x')
legend('CV','RavenState')

figure()
plot(result_traj_frameWorld(:,2),result_traj_frameWorld(:,4))
hold on
plot(raven_state(:,1),ravenstate_center_traj_frameWorld(:,2))
xlabel('time')
ylabel('position')
title('y')
legend('CV','RavenState')

figure()
plot(result_traj_frameWorld(:,2),result_traj_frameWorld(:,5))
hold on
plot(raven_state(:,1),ravenstate_center_traj_frameWorld(:,3))
xlabel('time')
ylabel('position')
title('z')
legend('CV','RavenState')

%% 2D draw raven end effector traj with CV and RAVEN state FK
result_traj_size = size(result_traj_frameWorld);
for iter = 1:result_traj_size(1)
    [M , idx] = min(abs(raven_state(:,1)-result_traj_frameWorld(iter,2)));
    T = ravenFK(raven_state(idx,108),raven_state(idx,109),10000*raven_state(idx,110),raven_state(idx,112),raven_state(idx,113),raven_state(idx,114));
    raven_center_FK(iter,:) = T(1:3,4)';

end
ravenstate_center_FK_traj_frame0 = raven_center_FK*um2mm;
ravenstate_center_FK_traj_frame0_T = ravenstate_center_FK_traj_frame0' ;
ravenstate_center_FK_traj_frame0_T(4,:) = 1;
ravenstate_center_FK_traj_frameBase_T = T_0_b * ravenstate_center_FK_traj_frame0_T;
ravenstate_center_FK_traj_frameWorld_T = T_b_w * ravenstate_center_FK_traj_frameBase_T;
ravenstate_center_FK_traj_frameWorld = ravenstate_center_FK_traj_frameWorld_T';

figure()
plot(result_traj_frameWorld(:,2),result_traj_frameWorld(:,3))
hold on
plot(result_traj_frameWorld(:,2),ravenstate_center_FK_traj_frameWorld(:,1))
xlabel('time')
ylabel('position')
title('x_FK')
legend('CV','RavenState_FK')

figure()
plot(result_traj_frameWorld(:,2),result_traj_frameWorld(:,4))
hold on
plot(result_traj_frameWorld(:,2),ravenstate_center_FK_traj_frameWorld(:,2))
xlabel('time')
ylabel('position')
title('y_FK')
legend('CV','RavenState_FK')

figure()
plot(result_traj_frameWorld(:,2),result_traj_frameWorld(:,5))
hold on
plot(result_traj_frameWorld(:,2),ravenstate_center_FK_traj_frameWorld(:,3))
xlabel('time')
ylabel('position')
title('z_FK')
legend('CV','RavenState_FK')

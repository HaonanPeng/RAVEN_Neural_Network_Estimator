close all, clear all, clc

%% load data
raven_state_traj1 = importdata('raven_state_traj3.txt');

raven_center_traj1_frameWorld_CV = importdata('img_process_result_traj3_raven_center_filtered.txt');

result_label_file_name = 'test_raven_state.txt';

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

%% data processing

time_decay = 0.6;


% traj1 difference
time_ravenstate_traj1 = raven_state_traj1(:,1)-raven_center_traj1_frameWorld_CV(1,1);
time_CV_traj1 = raven_center_traj1_frameWorld_CV(:,1)-raven_center_traj1_frameWorld_CV(1,1)-time_decay;

raven_center_traj1_frame0_ravenstate = raven_state_traj1(:,2:4)*um2mm;
raven_center_traj1_frame0_T_ravenstate = raven_center_traj1_frame0_ravenstate' ;
raven_center_traj1_frame0_T_ravenstate(4,:) = 1;
raven_center_traj1_frameBase_T_ravenstate = T_0_b * raven_center_traj1_frame0_T_ravenstate;
raven_center_traj1_frameWorld_T_ravenstate = T_b_w * raven_center_traj1_frameBase_T_ravenstate;
raven_center_traj1_frameWorld_ravenstate = raven_center_traj1_frameWorld_T_ravenstate';

size_CV = size(raven_center_traj1_frameWorld_CV);
for idx_CV = 1 :size_CV(1)
    [M, idx_ravenstate] = min(abs(time_ravenstate_traj1 - time_CV_traj1(idx_CV)));
    difference_x_frameWorld_traj1(idx_CV) = raven_center_traj1_frameWorld_CV(idx_CV,2) - raven_center_traj1_frameWorld_ravenstate(idx_ravenstate,1);
    difference_y_frameWorld_traj1(idx_CV) = raven_center_traj1_frameWorld_CV(idx_CV,3) - raven_center_traj1_frameWorld_ravenstate(idx_ravenstate,2);
    difference_z_frameWorld_traj1(idx_CV) = raven_center_traj1_frameWorld_CV(idx_CV,4) - raven_center_traj1_frameWorld_ravenstate(idx_ravenstate,3);
    raven_state_total(idx_CV,:) = raven_state_traj1(idx_ravenstate,:);
end

img_process_result_traj1 = [raven_center_traj1_frameWorld_CV,difference_x_frameWorld_traj1',difference_y_frameWorld_traj1',difference_z_frameWorld_traj1'];

figure()
plot(difference_x_frameWorld_traj1)
hold on
plot(difference_y_frameWorld_traj1)
plot(difference_z_frameWorld_traj1)
title('difference of traj3')
legend('x','y','z')


%% save files
dlmwrite('test_ravenstate.txt',raven_state_total,'precision',16,'delimiter',' ')
dlmwrite('test_img_process_result.txt',img_process_result_traj1,'precision',16,'delimiter',' ')


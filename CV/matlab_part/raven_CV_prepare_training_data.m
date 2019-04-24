close all, clear all, clc

%% load data
raven_state_traj1 = importdata('raven_state_traj1.txt');
raven_state_traj2 = importdata('raven_state_traj2.txt');

raven_center_traj1_frameWorld_CV = importdata('img_process_result_traj1_raven_center_filtered.txt');
raven_center_traj2_frameWorld_CV = importdata('img_process_result_traj2_raven_center_filtered.txt');

result_label_file_name = 'training_raven_state.txt';

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
end

% traj2 difference
time_ravenstate_traj2 = raven_state_traj2(:,1)-raven_center_traj2_frameWorld_CV(1,1);
time_CV_traj2 = raven_center_traj2_frameWorld_CV(:,1)-raven_center_traj2_frameWorld_CV(1,1)-time_decay;

raven_center_traj2_frame0_ravenstate = raven_state_traj2(:,2:4)*um2mm;
raven_center_traj2_frame0_T_ravenstate = raven_center_traj2_frame0_ravenstate' ;
raven_center_traj2_frame0_T_ravenstate(4,:) = 1;
raven_center_traj2_frameBase_T_ravenstate = T_0_b * raven_center_traj2_frame0_T_ravenstate;
raven_center_traj2_frameWorld_T_ravenstate = T_b_w * raven_center_traj2_frameBase_T_ravenstate;
raven_center_traj2_frameWorld_ravenstate = raven_center_traj2_frameWorld_T_ravenstate';

size_CV = size(raven_center_traj2_frameWorld_CV);
for idx_CV = 1 :size_CV(1)
    [M, idx_ravenstate] = min(abs(time_ravenstate_traj2 - time_CV_traj2(idx_CV)));
    difference_x_frameWorld_traj2(idx_CV) = raven_center_traj2_frameWorld_CV(idx_CV,2) - raven_center_traj2_frameWorld_ravenstate(idx_ravenstate,1);
    difference_y_frameWorld_traj2(idx_CV) = raven_center_traj2_frameWorld_CV(idx_CV,3) - raven_center_traj2_frameWorld_ravenstate(idx_ravenstate,2);
    difference_z_frameWorld_traj2(idx_CV) = raven_center_traj2_frameWorld_CV(idx_CV,4) - raven_center_traj2_frameWorld_ravenstate(idx_ravenstate,3);
end

figure()
plot(difference_x_frameWorld_traj1)
hold on
plot(difference_y_frameWorld_traj1)
plot(difference_z_frameWorld_traj1)
title('difference of traj1')

figure()
plot(difference_x_frameWorld_traj2)
hold on
plot(difference_y_frameWorld_traj2)
plot(difference_z_frameWorld_traj2)
title('difference of traj2')

%% Merge trajectories
ravenstate_total = [raven_state_traj1;raven_state_traj2];

img_process_result_traj1 = [raven_center_traj1_frameWorld_CV,difference_x_frameWorld_traj1',difference_y_frameWorld_traj1',difference_z_frameWorld_traj1'];
img_process_result_traj2 = [raven_center_traj2_frameWorld_CV,difference_x_frameWorld_traj2',difference_y_frameWorld_traj2',difference_z_frameWorld_traj2'];
img_process_result_total = [img_process_result_traj1;img_process_result_traj2];

%% seperate an untouched test data set
% if do not want to seperate, mute this part
seperate_start = 0.5; % this is where the seperation started, such as 0.6 means start from 60% of the data
seperate_rate = 0.05; % this is the percentage of the seperated data
seperate_end = seperate_start + seperate_rate;

size_raven_state_total = size(ravenstate_total);
size_img_process_result_total = size(img_process_result_total);

% seperated_ravenstate_total = ravenstate_total(round(seperate_start*size_raven_state_total(1)):round(seperate_end*size_raven_state_total(1)),:);
seperated_img_process_result_total = img_process_result_total(round(seperate_start*size_img_process_result_total(1)):round(seperate_end*size_img_process_result_total(1)),:);
% size_seperated_ravenstate = size(seperated_ravenstate_total);
size_seperated_img_process_result_total = size(seperated_img_process_result_total);



img_process_result_total(round(seperate_start*size_img_process_result_total(1)):round(seperate_end*size_img_process_result_total(1)),:) = [];

% figure()

[M, seperate_ravenstate_idx_start] = min(abs(ravenstate_total(:,1) - seperated_img_process_result_total(1,1) + time_decay));
for idx_CV = 1 :size_seperated_img_process_result_total(1)
    [M, idx_ravenstate] = min(abs(ravenstate_total(:,1) - seperated_img_process_result_total(idx_CV,1) + time_decay));
    seperated_feature(idx_CV,:) = ravenstate_total(idx_ravenstate,:);
end
[M, seperate_ravenstate_idx_end] = min(abs(ravenstate_total(:,1) - seperated_img_process_result_total(idx_CV,1) + time_decay));
ravenstate_total(seperate_ravenstate_idx_start:seperate_ravenstate_idx_end,:) = [];

seperated_label = seperated_img_process_result_total;

dlmwrite('test_ravenstate.txt',seperated_feature,'precision',16,'delimiter',' ')
dlmwrite('test_img_process_result.txt',seperated_label,'precision',16,'delimiter',' ')


%% save files
dlmwrite('training_ravenstate.txt',ravenstate_total,'precision',16,'delimiter',' ')
dlmwrite('training_img_process_result.txt',img_process_result_total,'precision',16,'delimiter',' ')


close all, clear all, clc

%% load data
total_traj_number = 6;

raven_state_traj_set{1} = importdata('data_files/raven_state_traj1_toggled.txt');
raven_state_traj_set{2} = importdata('data_files/raven_state_traj2_toggled.txt');
raven_state_traj_set{3} = importdata('data_files/raven_state_traj8_toggled.txt');
raven_state_traj_set{4} = importdata('data_files/raven_state_traj9_toggled.txt');
raven_state_traj_set{5} = importdata('data_files/raven_state_traj10_toggled.txt');
raven_state_traj_set{6} = importdata('data_files/raven_state_traj11_toggled.txt');

raven_center_traj_frameWorld_CV_set{1} = importdata('data_files/img_process_result_traj1_raven_center_filtered.txt');
raven_center_traj_frameWorld_CV_set{2} = importdata('data_files/img_process_result_traj2_raven_center_filtered.txt');
raven_center_traj_frameWorld_CV_set{3} = importdata('data_files/img_process_result_traj8_raven_center_filtered.txt');
raven_center_traj_frameWorld_CV_set{4} = importdata('data_files/img_process_result_traj9_raven_center_filtered.txt');
raven_center_traj_frameWorld_CV_set{5} = importdata('data_files/img_process_result_traj10_raven_center_filtered.txt');
raven_center_traj_frameWorld_CV_set{6} = importdata('data_files/img_process_result_traj11_raven_center_filtered.txt');

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

img_process_result_total = [];
ravenstate_total = [];
for iter = 1 : total_traj_number
    % initialize
    difference_x_frameWorld_traj = [];
    difference_y_frameWorld_traj = [];
    difference_z_frameWorld_traj = [];
    
    raven_state_traj = raven_state_traj_set{iter};
    raven_center_traj_frameWorld_CV = raven_center_traj_frameWorld_CV_set{iter};
    
    % traj1 difference
    time_ravenstate_traj = raven_state_traj(:,1)-raven_center_traj_frameWorld_CV(1,1);
    time_CV_traj = raven_center_traj_frameWorld_CV(:,1)-raven_center_traj_frameWorld_CV(1,1)-time_decay;

    raven_center_traj_frame0_ravenstate = raven_state_traj(:,2:4)*um2mm;
    raven_center_traj_frame0_T_ravenstate = raven_center_traj_frame0_ravenstate' ;
    raven_center_traj_frame0_T_ravenstate(4,:) = 1;
    raven_center_traj_frameBase_T_ravenstate = T_0_b * raven_center_traj_frame0_T_ravenstate;
    raven_center_traj_frameWorld_T_ravenstate = T_b_w * raven_center_traj_frameBase_T_ravenstate;
    raven_center_traj_frameWorld_ravenstate = raven_center_traj_frameWorld_T_ravenstate';

    size_CV = size(raven_center_traj_frameWorld_CV);
    for idx_CV = 1 :size_CV(1)
        [M, idx_ravenstate] = min(abs(time_ravenstate_traj - time_CV_traj(idx_CV)));
        difference_x_frameWorld_traj(idx_CV) = raven_center_traj_frameWorld_CV(idx_CV,2) - raven_center_traj_frameWorld_ravenstate(idx_ravenstate,1);
        difference_y_frameWorld_traj(idx_CV) = raven_center_traj_frameWorld_CV(idx_CV,3) - raven_center_traj_frameWorld_ravenstate(idx_ravenstate,2);
        difference_z_frameWorld_traj(idx_CV) = raven_center_traj_frameWorld_CV(idx_CV,4) - raven_center_traj_frameWorld_ravenstate(idx_ravenstate,3);
    end

    figure()
    plot(difference_x_frameWorld_traj)
    hold on
    plot(difference_y_frameWorld_traj)
    plot(difference_z_frameWorld_traj)
    title('difference of traj')
    legend('x','y','z')

    img_process_result{iter} = [raven_center_traj_frameWorld_CV,difference_x_frameWorld_traj',difference_y_frameWorld_traj',difference_z_frameWorld_traj'];

    img_process_result_total = [img_process_result_total;img_process_result{iter}];   
    ravenstate_total = [ravenstate_total;raven_state_traj];
end

%% seperate an untouched test data set
% if do not want to seperate, mute this part
seperate_start = 0.4; % this is where the seperation started, such as 0.6 means start from 60% of the data
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

dlmwrite('data_files/test_ravenstate.txt',seperated_feature,'precision',16,'delimiter',' ')
dlmwrite('data_files/test_img_process_result.txt',seperated_label,'precision',16,'delimiter',' ')


%% save files
dlmwrite('data_files/training_ravenstate.txt',ravenstate_total,'precision',16,'delimiter',' ')
dlmwrite('data_files/training_img_process_result.txt',img_process_result_total,'precision',16,'delimiter',' ')
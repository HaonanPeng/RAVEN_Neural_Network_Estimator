close all, clear all, clc

%% solve filtered
txtfile_name = 'data_files/img_process_result_traj13_filtered.txt';
resultfile_name = 'data_files/img_process_result_traj13_raven_center_filtered.txt';
result_traj = importdata(txtfile_name);

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

%% draw raven end effector
data_lenth = size(result_traj);
raven_center = zeros(data_lenth(1),29);
for iter = 1:data_lenth(1)
    ball_centers = [result_traj(iter,3:5);result_traj(iter,6:8);result_traj(iter,9:11)];
    raven_center(iter,1) = result_traj(iter,2);
    [raven_center(iter,2:4), T_matrix] = end_effector_PR(ball_centers);  
    raven_center(iter,5:20) = reshape(T_matrix,[1,16]);
    raven_center(iter,21:29) = result_traj(iter,3:11);
end

dlmwrite(resultfile_name,raven_center,'precision',16,'delimiter',' ')


%% solve unfiltered

txtfile_name = 'data_files/img_process_result_traj13.txt';
resultfile_name = 'data_files/img_process_result_traj13_raven_center.txt';
result_traj = importdata(txtfile_name);

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

%% draw raven end effector
data_lenth = size(result_traj);
raven_center = zeros(data_lenth(1),29);
for iter = 1:data_lenth(1)
    ball_centers = [result_traj(iter,3:5);result_traj(iter,6:8);result_traj(iter,9:11)];
    raven_center(iter,1) = result_traj(iter,2);
    [raven_center(iter,2:4), T_matrix] = end_effector_PR(ball_centers);  
    raven_center(iter,5:20) = reshape(T_matrix,[1,16]);
    raven_center(iter,21:29) = result_traj(iter,3:11);
end

dlmwrite(resultfile_name,raven_center,'precision',16,'delimiter',' ')


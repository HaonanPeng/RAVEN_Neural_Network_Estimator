close all ,clear all, clc

raven_center_traj_frameWorld_CV_set{1} = importdata('data_files/img_process_result_traj1_raven_center_filtered.txt');
raven_center_traj_frameWorld_CV_set{2} = importdata('data_files/img_process_result_traj2_raven_center_filtered.txt');
raven_center_traj_frameWorld_CV_set{3} = importdata('data_files/img_process_result_traj8_raven_center_filtered.txt');
raven_center_traj_frameWorld_CV_set{4} = importdata('data_files/img_process_result_traj9_raven_center_filtered.txt');
raven_center_traj_frameWorld_CV_set{5} = importdata('data_files/img_process_result_traj10_raven_center_filtered.txt');
raven_center_traj_frameWorld_CV_set{6} = importdata('data_files/img_process_result_traj11_raven_center_filtered.txt');

traj_numbers = 6;
figure()
for iter = 1: traj_numbers
    raven_center_traj_frameWorld_CV = [];
    raven_center_traj_frameWorld_CV = raven_center_traj_frameWorld_CV_set{iter};
    
    plot3(raven_center_traj_frameWorld_CV(:,2),raven_center_traj_frameWorld_CV(:,3),raven_center_traj_frameWorld_CV(:,4))
    hold on
    
end

xlabel('x(mm)')
ylabel('y(mm)')
zlabel('z(mm)')
legend('traj1','traj2','traj8','traj9','traj10','traj11')
title('Position of the end effector in World Frame')
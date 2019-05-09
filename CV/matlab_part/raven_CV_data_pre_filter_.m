close all, clear all ,clc

ball_traj_frameWorld_CV = importdata('data_files/img_process_result_traj11.txt');
result_file_name = 'data_files/img_process_result_traj11_filtered.txt';

windowSize = 21;

size_data = size(ball_traj_frameWorld_CV);

ball_traj_frameWorld_CV_filtered(:,1:2) = ball_traj_frameWorld_CV(:,1:2);

for idx = 3:11
    filtered_array = moving_average_filter(ball_traj_frameWorld_CV(:,idx),windowSize);
    ball_traj_frameWorld_CV_filtered(:,idx) = filtered_array;
end

dlmwrite(result_file_name,ball_traj_frameWorld_CV_filtered,'precision',16,'delimiter',' ')
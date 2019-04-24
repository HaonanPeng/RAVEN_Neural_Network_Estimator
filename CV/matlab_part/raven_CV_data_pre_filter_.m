close all, clear all ,clc

ball_traj_frameWorld_CV = importdata('img_process_result_traj3.txt');
result_file_name = 'img_process_result_traj3_filtered.txt';

windowSize = 21;

size_data = size(ball_traj_frameWorld_CV);

ball_traj_frameWorld_CV_filtered(:,1:2) = ball_traj_frameWorld_CV(((windowSize+1)/2) : (size_data(1) - (windowSize-1)/2),1:2);

for idx = 3:11
    filtered_array = moving_average_filter(ball_traj_frameWorld_CV(:,idx),windowSize);
    ball_traj_frameWorld_CV_filtered(:,idx) = filtered_array(((windowSize+1)/2) : (size_data(1) - (windowSize-1)/2));
end

dlmwrite(result_file_name,ball_traj_frameWorld_CV_filtered,'precision',16,'delimiter',' ')
close all, clear all, clc

raven_state = importdata('raven_state_traj1.txt');

size_ravenstate = size(raven_state);
line_idx = 1;
for col_index = 1: 50 : size_ravenstate(1)
    raven_state_toggled(line_idx, :) =  raven_state(col_index,:);
    line_idx = line_idx +1;
end

dlmwrite('raven_state_traj1_toggled.txt',raven_state_toggled,'precision',16)
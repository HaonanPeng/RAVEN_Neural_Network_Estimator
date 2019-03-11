close all, clear all, clc

load('CameraParams.dat','-mat')

tic
%% undistort section

% image_folder_open = 'D:\iCloudDrive\Research Credit\Codes\Full Test - Jan 11\Camera Calibration\Ground Truth - Markers';
% image_folder_save = 'D:\iCloudDrive\Research Credit\Codes\Full Test - Jan 11\Camera Calibration\Ground Truth - Markers';

image_folder_open = 'C:\Users\Xingjian Yang\iCloudDrive\Research Credit\Test - Full - March 6\img_test_sample';
image_folder_save = 'C:\Users\Xingjian Yang\iCloudDrive\Research Credit\Test - Full - March 6\img_test_sample\undistort';
filenames = dir(fullfile(image_folder_open, '*.jpg'));  % read all images with specified extention, its jpg in our case
total_images = numel(filenames);    % count total number of photos present in that folder

for n = 1:total_images
    old_name = filenames(n).name;
    old_name_no_extention = erase(old_name,'.jpg');
    formatSpec = '%s - undistort.jpg';
    %new_name = sprintf(formatSpec,n);
    new_name = sprintf(formatSpec,old_name_no_extention);
    path_new_name= fullfile(image_folder_save,new_name);         % it will specify images names with full path and extension
    path_old_file = strcat(filenames(n).folder,'\',filenames(n).name);
    I = imread(path_old_file);
    [s1,s2,s3]=size(I);
    I_r = zeros(s1,s2,s3);
    I_g = zeros(s1,s2,s3);
    I_b = zeros(s1,s2,s3);
    J = undistortImage(I,cameraParams);
    
%     size_des = [720,1280]; % 720P 
%     size_origin = size(J);
%     J_resize = imresize(J, size_des(2)/size_origin(2));
    
    imwrite(J,path_new_name)
end

toc
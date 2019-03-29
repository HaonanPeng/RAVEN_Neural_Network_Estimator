close all, clear all, clc

time_gap = 0.000001;

image_folder_open = 'C:\Users\Xingjian Yang\iCloudDrive\Research Credit\Codes\Test - Full - Jan 29\img_test_sample\origin';
image_folder_save = 'C:\Users\Xingjian Yang\iCloudDrive\Research Credit\Codes\Test - Full - Jan 29\img_test_sample\new';
filenames = dir(fullfile(image_folder_open, '*.jpg'));  % read all images with specified extention, its jpg in our case
total_images = numel(filenames);    % count total number of photos present in that folder



for n = 1:total_images
    old_name = filenames(n).name;
    old_name_no_extention = erase(old_name,'.jpg');
    new_name_no_extention = num2str(str2num(old_name_no_extention)+time_gap,'%10.6f');
    formatSpec = '%s.jpg';
    new_name = sprintf(formatSpec,new_name_no_extention);
    path_new_name= fullfile(image_folder_save,new_name);         % it will specify images names with full path and extension
    path_old_file = strcat(filenames(n).folder,'\',filenames(n).name);
    I = imread(path_old_file);
    imwrite(I,path_new_name)
end

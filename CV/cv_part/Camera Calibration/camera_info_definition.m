close all, clear all, clc

working_path = 'C:\Users\Xingjian Yang\iCloudDrive\Research Credit\Test - Full - March 6';

%% Initializations
%camera settings (same with Camera_Info_Definition.py)---------------------
load('CameraParams.dat','-mat') %camera parameters
num_cam = 4; %number of cameras
f = 4; % camera focal length (mm)
ps = f/1420; % pixel size (mm)
resolution = [1280,720]; % photo resolution

% chessboard settings------------------------------------------------------
squareSize = 9.1; %chessboard square size(mm)
syms tx ty tz
Rx = [1 0 0; 0 cos(tx) -sin(tx); 0 sin(tx) cos(tx)];
Ry = [cos(ty) 0 sin(ty); 0 1 0; -sin(ty) 0 cos(ty)];
Rz = [cos(tz) -sin(tz) 0; sin(tz) cos(tz) 0; 0 0 1];        

P_chess = [-123.78-cos(12.7/180*pi)*9, 563.92-sin(12.7/180*pi)*9, 164-9/2*sqrt(3);   %cam 0
           130.79-cos(33.5/180*pi)*9, 547.11+sin(33.5/180*pi)*9, 164-9/2*sqrt(3);  %cam 1
           -97-cos(10.8/180*pi)*100, 6.16+sin(10.8/180*pi)*100, 164-9/2*sqrt(3); %cam 2
           42.8-cos(34.7/180*pi)*11, 0-sin(34.7/180*pi)*11, 164-9/2*sqrt(3)]; %cam 3
           
R_chess = zeros(3,3,num_cam);
R_chess(:,:,1)= subs(Rz,tz,192.7/180*pi)*subs(Rx,tx,-60.5/180*pi);
R_chess(:,:,2)= subs(Rz,tz,146.5/180*pi)*subs(Rx,tx,-60.5/180*pi);
R_chess(:,:,3)= subs(Rz,tz,-16.5/180*pi)*subs(Rx,tx,-60.5/180*pi);
R_chess(:,:,4)= subs(Rz,tz,34.7/180*pi)*subs(Rx,tx,-60.5/180*pi);


%object settings-----------------------------------------------------------
num_ref = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]; %number of reference objects
P_obj = [-166.99,310.63,328.9;              % obj1 (reference) mark1_high
         -166.99,310.63,220.2;              % obj2 (reference) mark1_low
         -14.47,310.63,328.9;               % obj3 (reference) mark2_high
         -14.47,310.63,220.2;               % obj4 (reference) mark2_low
         -13.84,202.32,328.9;              % obj5 (reference) mark3_high
         -13.84,202.32,220.2;              % obj6 (reference) mark3_low
         -164.44,202.32,328.9;             % obj7 (reference) mark4_high
         -164.44,202.32,220.2;             % obj8 (reference) mark4_low
         -127.84,267.56,328.9;              % obj9 (reference) mark5_high
         -127.84,267.56,220.2;              % obj10 (reference) mark5_low
         -100.55,290.11,328.9;             % obj11 (reference) mark6_high
         -100.55,290.11,220.2;             % obj12 (reference) mark6_low
         -69.86,267.56,328.9;             % obj13 (reference) mark7_high
         -69.86,267.56,220.2;             % obj14 (reference) mark7_low
         -100.87,243.36,328.9;             % obj15 (reference) mark8_high
         -100.87,243.36,220.2];             % obj16 (reference) mark8_low
     
[num_obj,n] = size(P_obj);

%% Camera's Location/Rotation in Chessboard coordinate
%Img_chess = imageDatastore('C:\Users\Xingjian Yang\iCloudDrive\Research Credit\Test - Full - March 6\Camera Calibration\Chessboard');
Img_chess_path = strcat(working_path,'\','Camera Calibration\Chessboard');
Img_chess = imageDatastore(Img_chess_path);
P_cam2chess = zeros(num_cam,3);
R_cam2chess = zeros(3,3,num_cam);
for i = 1:num_cam
    img = readimage(Img_chess,i);
    [P_cam2chess(i,:), R_cam2chess(:,:,i)]= func_Chessboard_Localization(img,cameraParams,squareSize);
end
 
%% Camera's Location/Rotation in Chessboard coordinate
P_cam = [];
R_cam = zeros(3,3,num_cam);
for i = 1:num_cam
    P_cam = [P_cam;(R_chess(:,:,i)*P_cam2chess(i,:)'+P_chess(i,:)')'];
    R_cam(:,:,i) = R_chess(:,:,i)*R_cam2chess(:,:,i);
end

%% RotationMatrix Correction
Image_object_center = zeros(num_obj,2,num_cam);
% cam0: objects' image coordinate 
Image_object_center(:,:,1) = [755 27; 770 344;  % obj1,2 (reference) mark1_high/low
                              301 85; 270 389;  % obj3,4 (reference) mark2_high/low
                              414 234; 398 493;  % obj5,6 (reference) mark3_high/low
                              787 193; 801 463;  % obj7,8 (reference) mark4_high/low
                              660 114; 664 408;  % obj9,10 (reference) mark5_high/low
                              566 87; 562 389;  % obj11,12 (reference) mark6_high/low
                              498 134; 487 422;  % obj13,14 (reference) mark7_high/low
                              598 159; 596 440];  % obj15,16 (reference) mark8_high/low

% cam1: objects' image coordinate 
Image_object_center(:,:,2) = [869 215; 877 484;  % obj1,2 (reference) mark1_high/low
                              506 97; 479 399;  % obj3,4 (reference) mark2_high/low
                              398 227; 367 488;  % obj5,6 (reference) mark3_high/low
                              722 313; 717 550;  % obj7,8 (reference) mark4_high/low
                              727 234; 723 496;  % obj9,10 (reference) mark5_high/low
                              696 191; 690 466;  % obj11,12 (reference) mark6_high/low
                              595 195; 580 468;  % obj13,14 (reference) mark7_high/low
                              635 240; 624 500];  % obj15,16 (reference) mark8_high/low
                          
% cam2: objects' image coordinate   
Image_object_center(:,:,3) = [312 261; 279 578;  % obj1,2 (reference) mark1_high/low
                              759 324; 783 620;  % obj3,4 (reference) mark2_high/low
                              893 125; 946 465;  % obj5,6 (reference) mark3_high/low
                              359 26; 324 396;  % obj7,8 (reference) mark4_high/low
                              455 199; 440 532;  % obj9,10 (reference) mark5_high/low
                              529 255; 525 573;  % obj11,12 (reference) mark6_high/low
                              642 229; 653 552;  % obj13,14 (reference) mark7_high/low
                              565 164; 566 503];  % obj15,16 (reference) mark8_high/low
                          
% cam3: objects' image coordinate 
Image_object_center(:,:,4) = [547 302; 521 569;  % obj1,2 (reference) mark1_high/low
                              906 199; 916 503;  % obj3,4 (reference) mark2_high/low
                              745 15; 736 364;  % obj5,6 (reference) mark3_high/low
                              356 163; 303 465;  % obj7,8 (reference) mark4_high/low
                              560 226; 533 516;  % obj9,10 (reference) mark5_high/low
                              660 236; 643 525;  % obj11,12 (reference) mark6_high/low
                              700 181; 686 486;  % obj13,14 (reference) mark7_high/low
                              583 170; 556 476];  % obj15,16 (reference) mark8_high/low
                         
                          

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for i = 1:num_cam
    fprintf('cam %d rotation correction=====================================',i-1);
    [RotationMatrix_new,P_cam_new,ERROR_pre,ERROR_now] = func_RotationMatrix_Correction_withPosition(R_cam2chess(:,:,i),R_chess(:,:,i),P_cam(i,:),Image_object_center(:,:,i),P_obj,resolution,ps,f,num_ref);
    P_cam(i,:) = P_cam_new;
    %[RotationMatrix_new,ERROR_pre,ERROR_now] = func_RotationMatrix_Correction(R_cam2chess(:,:,i),R_chess(:,:,i),P_cam(i,:),Image_object_center(:,:,i),P_obj,resolution,ps,f,num_ref);
    
    %ERROR_pre
    euler_pre = rotm2eul(R_cam2chess(:,:,i))/pi*180;
    ERROR_now
    euler_now = rotm2eul(RotationMatrix_new)/pi*180;
    R_cam2chess(:,:,i) = RotationMatrix_new;
    R_cam(:,:,i) = R_chess(:,:,i)*R_cam2chess(:,:,i); %update new R_cam
end


%% Write in .txt file for Camera_Info_Definition.py 
% fprintf print in column from left to right, so print rotationMatrix's transposition 
for i = 1:num_cam
    info_P_chess = strcat(working_path,'\','Camera_Info_txt\info_P_chess.txt');
    fileID = fopen(info_P_chess,'a+');
    fprintf(fileID,'%.6f %.6f %.6f\n ',P_chess(i,:));
    fclose(fileID);
    
    info_R_chess = strcat(working_path,'\','Camera_Info_txt\info_R_chess.txt');
    fileID = fopen(info_R_chess,'a+');
    fprintf(fileID,'%.6f %.6f %.6f\n %.6f %.6f %.6f\n %.6f %.6f %.6f\n',R_chess(:,:,i)');
    fclose(fileID);
    
    info_P_cam2chess = strcat(working_path,'\','Camera_Info_txt\info_P_cam2chess.txt');
    fileID = fopen(info_P_cam2chess,'a+');
    fprintf(fileID,'%.4f %.4f %.4f\n ',P_cam2chess(i,:));
    fclose(fileID);
    
    info_R_cam2chess = strcat(working_path,'\','Camera_Info_txt\info_R_cam2chess.txt');
    fileID = fopen(info_R_cam2chess,'a+');
    fprintf(fileID,'%.4f %.4f %.4f\n %.4f %.4f %.4f\n %.4f %.4f %.4f\n',R_cam2chess(:,:,i)');
    fclose(fileID);
    
    info_P_cam = strcat(working_path,'\','Camera_Info_txt\info_P_cam.txt');
    fileID = fopen(info_P_cam,'a+');
    fprintf(fileID,'%.6f %.6f %.6f\n ',P_cam(i,:));
    fclose(fileID);
    
    info_R_cam = strcat(working_path,'\','Camera_Info_txt\info_R_cam.txt');
    fileID = fopen(info_R_cam,'a+');
    fprintf(fileID,'%.6f %.6f %.6f\n %.6f %.6f %.6f\n %.6f %.6f %.6f\n',R_cam(:,:,i)');
    fclose(fileID);
end

dlmwrite(strcat(working_path,'\camera_info_txt\info_cam0_marker.txt'),Image_object_center(:,:,1),'delimiter','\t','precision',3)
dlmwrite(strcat(working_path,'\camera_info_txt\info_cam1_marker.txt'),Image_object_center(:,:,2),'delimiter','\t','precision',3)
dlmwrite(strcat(working_path,'\camera_info_txt\info_cam2_marker.txt'),Image_object_center(:,:,3),'delimiter','\t','precision',3)
dlmwrite(strcat(working_path,'\camera_info_txt\info_cam3_marker.txt'),Image_object_center(:,:,4),'delimiter','\t','precision',3)

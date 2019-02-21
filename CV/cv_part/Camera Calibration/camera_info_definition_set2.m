close all, clear all, clc


%% Initializations
%camera settings (same with Camera_Info_Definition.py)---------------------
load('CameraParams.dat','-mat') %camera parameters
num_cam = 4; %number of cameras
f = 4; % camera focal length (mm)
ps = f/1420; % pixel size (mm)
resolution = [1280,720]; % photo resolution

% chessboard settings------------------------------------------------------
squareSize = 9; %chessboard square size(mm)
syms tx ty tz
Rx = [1 0 0; 0 cos(tx) -sin(tx); 0 sin(tx) cos(tx)];
Ry = [cos(ty) 0 sin(ty); 0 1 0; -sin(ty) 0 cos(ty)];
Rz = [cos(tz) -sin(tz) 0; sin(tz) cos(tz) 0; 0 0 1];        

P_chess = [304.8+6*sqrt(2), -304.8-38*sqrt(2), 116.6-9*sqrt(3);   %cam 0
           304.8+38*sqrt(2), 304.8+6*sqrt(2), 116.6-9*sqrt(3);  %cam 1
           -304.8-6*sqrt(2), 304.8+38*sqrt(2), 116.6-9*sqrt(3); %cam 2
           -304.8-38*sqrt(2), -304.8-6*sqrt(2), 116.6-9*sqrt(3)]; %cam 3
R_chess = zeros(3,3,num_cam);
R_chess(:,:,1)= subs(Rz,tz,45/180*pi)*subs(Rx,tx,-60/180*pi);
R_chess(:,:,2)= subs(Rz,tz,135/180*pi)*subs(Rx,tx,-60/180*pi);
R_chess(:,:,3)= subs(Rz,tz,-135/180*pi)*subs(Rx,tx,-60/180*pi);
R_chess(:,:,4)= subs(Rz,tz,-45/180*pi)*subs(Rx,tx,-60/180*pi);


%object settings-----------------------------------------------------------
num_ref = [1,2,3,4,5,6,7,8]; %number of reference objects
P_obj = [127,-127,279.4;              % obj1 (reference) mark0_high
         127,-127,215.9;              % obj2 (reference) mark0_low
         127,127,279.4;               % obj3 (reference) mark1_high
         127,127,215.9;               % obj4 (reference) mark1_low
         -127,127,279.4;              % obj5 (reference) mark2_high
         -127,127,215.9;              % obj6 (reference) mark2_low
         -127,-127,279.4;             % obj7 (reference) mark3_high
         -127,-127,215.9;             % obj8 (reference) mark3_low
         10 29.3 244.475;             % obj9 ball0
         50 29.3 284.475;             % obj10 ball1
         90	29.3 244.475];            % obj11 ball2
[num_obj,n] = size(P_obj);

%% Camera's Location/Rotation in Chessboard coordinate
Img_chess = imageDatastore('D:\iCloudDrive\Research Credit\Codes\Test - Full - Jan 11\Camera Calibration\Chessboard');
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
Image_object_center(:,:,1) = [635 211;              % obj1 (reference) mark0_high
                          635 378;              % obj2 (reference) mark0_low
                          1023 406;              % obj3 (reference) mark1_high
                          1042 539;               % obj4 (reference) mark1_low
                          631 531;              % obj5 (reference) mark2_high
                          632 641;              % obj6 (reference) mark2_low
                          239 402;             % obj7 (reference) mark3_high
                          221 535;             % obj8 (reference) mark3_low
                          693.5 490.5;
758.5 383.5;
832.5 443.5];

% cam1: objects' image coordinate 
Image_object_center(:,:,2) = [244 408;              % obj1 (reference) mark0_high
                          225  539;              % obj2 (reference) mark0_low
                          631 200;              % obj3 (reference) mark1_high
                          628 368;               % obj4 (reference) mark1_low
                          1033 418;              % obj5 (reference) mark2_high
                          1048 552;              % obj6 (reference) mark2_low
                          635 538;             % obj7 (reference) mark3_high
                          635 648;             % obj8 (reference) mark3_low
                          673.5 460.5;
608.5 345.5;
530.5 405.5];
                          
% cam2: objects' image coordinate 
Image_object_center(:,:,3) = [630 543;              % obj1 (reference) mark0_high
                          629 650;              % obj2 (reference) mark0_low
                          231 391;              % obj3 (reference) mark1_high
                          212 526;               % obj4 (reference) mark1_low
                          623 183;              % obj5 (reference) mark2_high
                          622 352;              % obj6 (reference) mark2_low
                          1035 415;             % obj7 (reference) mark3_high
                          1051 549;             % obj8 (reference) mark3_low
                          558.5 455.5;
504.5 396.5;
444.5 497.5];
                          
% cam3: objects' image coordinate 
Image_object_center(:,:,4) = [1069 410;              % obj1 (reference) mark0_high
                          1088 544;              % obj2 (reference) mark0_low
                          670 534;              % obj3 (reference) mark1_high
                          672 646;               % obj4 (reference) mark1_low
                          277 404;              % obj5 (reference) mark2_high
                          259 538;              % obj6 (reference) mark2_low
                          680 190;             % obj7 (reference) mark3_high
                          679 361;             % obj8 (reference) mark3_low
                          640.5 500.5;
701.5 444.5;
757.5 541.5];
                         
                          

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for i = 1:num_cam
    fprintf('cam %d rotation correction=====================================',i);
    [RotationMatrix_new,ERROR_pre,ERROR_now] = func_RotationMatrix_Correction(R_cam2chess(:,:,i),R_chess(:,:,i),P_cam(i,:),Image_object_center(:,:,i),P_obj,resolution,ps,f,num_ref);
    ERROR_pre;
    euler_pre = rotm2eul(R_cam2chess(:,:,i))/pi*180;
    ERROR_now
    euler_now = rotm2eul(RotationMatrix_new)/pi*180;
    R_cam2chess(:,:,i) = RotationMatrix_new;
    R_cam(:,:,i) = R_chess(:,:,i)*R_cam2chess(:,:,i); %update new R_cam
end


%% Write in .txt file for Camera_Info_Definition.py 
% fprintf print in column from left to right, so print rotationMatrix's transposition 
for i = 1:num_cam
    fileID = fopen('D:\iCloudDrive\Research Credit\Codes\Test - Full - Jan 11\Camera_Info_txt\info_P_chess.txt','a+');
    fprintf(fileID,'%.6f %.6f %.6f\n ',P_chess(i,:));
    fclose(fileID);
    
    fileID = fopen('D:\iCloudDrive\Research Credit\Codes\Test - Full - Jan 11\Camera_Info_txt\info_R_chess.txt','a+');
    fprintf(fileID,'%.6f %.6f %.6f\n %.6f %.6f %.6f\n %.6f %.6f %.6f\n',R_chess(:,:,i)');
    fclose(fileID);
    
    fileID = fopen('D:\iCloudDrive\Research Credit\Codes\Test - Full - Jan 11\Camera_Info_txt\info_P_cam2chess.txt','a+');
    fprintf(fileID,'%.4f %.4f %.4f\n ',P_cam2chess(i,:));
    fclose(fileID);
    
    fileID = fopen('D:\iCloudDrive\Research Credit\Codes\Test - Full - Jan 11\Camera_Info_txt\info_R_cam2chess.txt','a+');
    fprintf(fileID,'%.4f %.4f %.4f\n %.4f %.4f %.4f\n %.4f %.4f %.4f\n',R_cam2chess(:,:,i)');
    fclose(fileID);
    
    fileID = fopen('D:\iCloudDrive\Research Credit\Codes\Test - Full - Jan 11\Camera_Info_txt\info_P_cam.txt','a+');
    fprintf(fileID,'%.6f %.6f %.6f\n ',P_cam(i,:));
    fclose(fileID);
    
    fileID = fopen('D:\iCloudDrive\Research Credit\Codes\Test - Full - Jan 11\Camera_Info_txt\info_R_cam.txt','a+');
    fprintf(fileID,'%.6f %.6f %.6f\n %.6f %.6f %.6f\n %.6f %.6f %.6f\n',R_cam(:,:,i)');
    fclose(fileID);
end

    

  

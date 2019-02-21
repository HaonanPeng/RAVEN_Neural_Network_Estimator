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

P_chess = [54, -81, 20+116.6-9*sqrt(3);   %cam 0
           53.25-9, 34, 20+116.6-9*sqrt(3);  %cam 1
           31, 81, 20+116.6-9*sqrt(3); %cam 2
           -71, 80, 20+116.6-9*sqrt(3)]; %cam 3
R_chess = zeros(3,3,num_cam);
R_chess(:,:,1)= subs(Rz,tz,0/180*pi)*subs(Rx,tx,-60/180*pi); % cam 0 
R_chess(:,:,2)= subs(Rz,tz,90/180*pi)*subs(Rx,tx,-60/180*pi); % cam 1
R_chess(:,:,3)= subs(Rz,tz,180/180*pi)*subs(Rx,tx,-60/180*pi); % cam 2
R_chess(:,:,4)= subs(Rz,tz,-90/180*pi)*subs(Rx,tx,-60/180*pi); % cam 3


%object settings-----------------------------------------------------------


%% Camera's Location/Rotation in Chessboard coordinate
Img_chess = imageDatastore('D:\iCloudDrive\Research Credit\Codes\Test - Full - Jan 23\Camera Calibration\Chessboard');
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
num_obj = 5;
num_ref = [1,2,3,4,5]; %number of reference objects

%---------------------CAM 0 ---------------------------
P_obj_0 = [10,10,150;                   % 1A
         -100,80,120;              % 2C
         -80,-80,105;               % 3A
         30,-100,120;               % 4D
         -45,-59,150];  %5C 
    
% cam0: objects' image coordinate 
Image_object_center_0 = [642 352;         %1A
                          473 597;              % 2C 
                          37 500;              % 3A 
                          367 273;               % 4D\
                       260,300];  %5C
                          
%---------------------CAM 1 ---------------------------
P_obj_1 = [10,10,150;                   % 1A
         -80,100,120;              % 2A
         -80,-100,105;               % 3D
         30,-100,120;               % 4D
         -31,-45,150];  %5A 
% cam1: objects' image coordinate 
Image_object_center_1 = [605,177;         %1A
                          952,424;              % 2A
                          209,481;              % 3D
                          45,276;               % 4D
                        382, 254];

%---------------------CAM 2 ---------------------------
P_obj_2 = [10,10,150;                   % 1A
         -100,100,120;              % 2B
         -100,-80,105;               % 3B
         30,-80,120;               % 4A
          -45,-31,150];
% cam2: objects' image coordinate 
Image_object_center_2 = [553,321;         %1A
                          1201,295;              % 2B
                          922,602;              % 3B
                          468,543;               % 4A
                           758,391];  %5B
%---------------------CAM 3 ---------------------------
P_obj_3 = [-10,10,150;                   % 1B
         -100,100,120;              % 2B
         -80,-80,105;               % 3A
         10,-100,120;               % 4C
         -59,-45,150]; %5C
% cam3: objects' image coordinate 
Image_object_center_3 = [594,295;         %1B
                          133,121;              % 2B
                          1166,450;              % 3A
                          993,515;               % 4C  
                           926,244]; 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% error_ball_sum = 0;
% warning('off','all')
% for i = 1:num_cam
%     fprintf('cam %d rotation correction=====================================',i);
%     if i == 1
%         [RotationMatrix_new,ERROR_pre,ERROR_now] = func_RotationMatrix_Correction(R_cam2chess(:,:,i), R_chess(:,:,i),P_cam(i,:),Image_object_center_0,P_obj_0,resolution,ps,f,num_ref);
%     elseif i ==2
%         [RotationMatrix_new,ERROR_pre,ERROR_now] = func_RotationMatrix_Correction(R_cam2chess(:,:,i), R_chess(:,:,i),P_cam(i,:),Image_object_center_1,P_obj_1,resolution,ps,f,num_ref);
%     elseif i ==3
%         [RotationMatrix_new,ERROR_pre,ERROR_now] = func_RotationMatrix_Correction(R_cam2chess(:,:,i), R_chess(:,:,i),P_cam(i,:),Image_object_center_2,P_obj_2,resolution,ps,f,num_ref);
%     elseif i ==4
%         [RotationMatrix_new,ERROR_pre,ERROR_now] = func_RotationMatrix_Correction(R_cam2chess(:,:,i), R_chess(:,:,i),P_cam(i,:),Image_object_center_3,P_obj_3,resolution,ps,f,num_ref);
%     end
%         
%         
%     ERROR_pre
%     euler_pre = rotm2eul(R_cam2chess(:,:,i))/pi*180
%     ERROR_now
%     euler_now = rotm2eul(RotationMatrix_new)/pi*180
%     R_cam2chess(:,:,i) = RotationMatrix_new;
%     R_cam(:,:,i) = R_chess(:,:,i)*R_cam2chess(:,:,i); %update new R_cam
% end


%% Write in .txt file for Camera_Info_Definition.py 
% fprintf print in column from left to right, so print rotationMatrix's transposition 
for i = 1:num_cam
    fileID = fopen('D:\iCloudDrive\Research Credit\Codes\Test - Full - Jan 23\Camera_Info_txt\info_P_chess.txt','a+');
    fprintf(fileID,'%.6f %.6f %.6f\n ',P_chess(i,:));
    fclose(fileID);
    
    fileID = fopen('D:\iCloudDrive\Research Credit\Codes\Test - Full - Jan 23\Camera_Info_txt\info_R_chess.txt','a+');
    fprintf(fileID,'%.6f %.6f %.6f\n %.6f %.6f %.6f\n %.6f %.6f %.6f\n',R_chess(:,:,i)');
    fclose(fileID);
    
    fileID = fopen('D:\iCloudDrive\Research Credit\Codes\Test - Full - Jan 23\Camera_Info_txt\info_P_cam2chess.txt','a+');
    fprintf(fileID,'%.4f %.4f %.4f\n ',P_cam2chess(i,:));
    fclose(fileID);
    
    fileID = fopen('D:\iCloudDrive\Research Credit\Codes\Test - Full - Jan 23\Camera_Info_txt\info_R_cam2chess.txt','a+');
    fprintf(fileID,'%.4f %.4f %.4f\n %.4f %.4f %.4f\n %.4f %.4f %.4f\n',R_cam2chess(:,:,i)');
    fclose(fileID);
    
    fileID = fopen('D:\iCloudDrive\Research Credit\Codes\Test - Full - Jan 23\Camera_Info_txt\info_P_cam.txt','a+');
    fprintf(fileID,'%.6f %.6f %.6f\n ',P_cam(i,:));
    fclose(fileID);
    
    fileID = fopen('D:\iCloudDrive\Research Credit\Codes\Test - Full - Jan 23\Camera_Info_txt\info_R_cam.txt','a+');
    fprintf(fileID,'%.6f %.6f %.6f\n %.6f %.6f %.6f\n %.6f %.6f %.6f\n',R_cam(:,:,i)');
    fclose(fileID);
end


    

  

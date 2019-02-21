function [RotationMatrix_now,ERROR_pre,ERROR_now] = func_RotationMatrix_Correction(R_cam2chess,R_chess,P_cam,Image_object_center,P_object,resolution,ps,f,num_ref)
%% parameters initialization 
[num_obj,n] = size(P_object); 

V_cam2obj = zeros(num_obj,3); %vector of camera to object (x,y,z in row) (mm)
V_img2cam = zeros(num_obj,3); %vector of point(image plane) to lense (x,y,z in row) (mm)
k = zeros(1,num_obj); % |V_img2cam| / |V_cam2obj|
for i = 1:num_obj
    V_cam2obj(i,:) =  (P_object(i,:)-P_cam);
    V_img2cam(i,:) = [Image_object_center(i,1)-resolution(1)/2;Image_object_center(i,2)-resolution(2)/2;f/ps]*ps;
    k(i) = norm(V_img2cam(i,:))/norm(V_cam2obj(i,:));
end


%% new rotation Matrix plug into object_2 
function eqn = findRotation(x) 
    Rx = [1 0 0; 0 cos(x(1)) -sin(x(1)); 0 sin(x(1)) cos(x(1))];
    Ry = [cos(x(2)) 0 sin(x(2)); 0 1 0; -sin(x(2)) 0 cos(x(2))];
    Rz = [cos(x(3)) -sin(x(3)) 0; sin(x(3)) cos(x(3)) 0; 0 0 1];
    
    eqn = [];
    iteration = length(num_ref);
    for iter = 1:iteration
        j = num_ref(iter);
        eqn = [eqn;double(R_chess)*Rz*Ry*Rx*V_img2cam(j,:)'/k(j)-V_cam2obj(j,:)'];
    end
end

RPY_old = rotm2eul(R_cam2chess);
options = optimoptions('fsolve','FunctionTolerance',1e-100,'StepTolerance',1e-100,'MaxIter',10000,'Display','off');
x = fsolve(@findRotation,RPY_old,options);

Rx = [1 0 0; 0 cos(x(1)) -sin(x(1)); 0 sin(x(1)) cos(x(1))];
Ry = [cos(x(2)) 0 sin(x(2)); 0 1 0; -sin(x(2)) 0 cos(x(2))];
Rz = [cos(x(3)) -sin(x(3)) 0; sin(x(3)) cos(x(3)) 0; 0 0 1];
RotationMatrix_now = Rz*Ry*Rx;

ERROR_pre = zeros(3,num_obj); %(x,y,z error) (mm)
ERROR_now = zeros(3,num_obj); %(x,y,z error) (mm)
for i = 1:num_obj
    ERROR_pre(:,i) = double(R_chess*R_cam2chess*V_img2cam(i,:)'/k(i)-V_cam2obj(i,:)');
    ERROR_now(:,i) = double(R_chess*RotationMatrix_now*V_img2cam(i,:)'/k(i)-V_cam2obj(i,:)');
end

end











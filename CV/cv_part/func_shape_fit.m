close all, clear all, clc


% holder center to ball center = 33 mm
ball_centers = [0, -33, 0;
                33, 0, 0;
                0, 33, 0];           
% add noise
ball_centers = ball_centers+rand(3)

% v_x: center to yellow direction 
% v_y: green to red direction
[RAVEN_center,v_x,v_y] = end_effector_PR(ball_centers)

function  [RAVEN_center,v_x,v_y] = end_effector_PR(ball_centers)
    
    p0 = ball_centers(1,:); 
    p1 = ball_centers(2,:);
    p2 = ball_centers(3,:);
    center = (p0+p2)/2;

    nx = ( (p1(2)-p0(2))*(p2(3)-p0(3))-(p1(3)-p0(3))*(p2(2)-p0(2)) );
    ny = ( (p1(3)-p0(3))*(p2(1)-p0(1))-(p1(1)-p0(1))*(p2(3)-p0(3)) );
    nz = ( (p1(1)-p0(1))*(p2(2)-p0(2))-(p1(2)-p0(2))*(p2(1)-p0(1)) );

    % norm to the three point plane
    n = [nx,ny,nz]/sqrt(nx^2+ny^2+nz^2);

    function eqn = end_effector_PR(theta) 
        % rotation matrix (plane norm as rotation axis) 
        a = cos(theta/2);
        b = n(1)*sin(theta/2);
        c = n(2)*sin(theta/2);
        d = n(3)*sin(theta/2);
        R = [a*a + b*b - c*c - d*d, 2*(b*c - a*d), 2*(b*d + a*c);
            2*(b*c + a*d), a*a + c*c - b*b - d*d, 2*(c*d - a*b);
            2*(b*d - a*c), 2*(c*d + a*b), a*a + d*d - b*b - c*c];
        
        % v_x: center to yellow as x axis
        v_x = R*(p1'-center')/norm(p1-center);
        
        % v_y: green_to_red as y direction = cross(norm,d1)
        v_y = cross(n,v_x);
        
        % holder center to ball center 
        d = 33;
        
        % where ball(0,1,2) center is supposed to be
        b0 = center-d*v_y; 
        b1 = center+d*v_x; 
        b2 = center+d*v_y; 
        
        % sum of difference between real ball center and supposed one
        eqn = norm(b0-p0)+norm(b1-p1)+norm(b2-p2);
    end

    initial_guess = 0;
    options = optimoptions('fsolve','FunctionTolerance',1e-100,'StepTolerance',1e-100,'MaxIter',10000,'Display','off');
    theta = fsolve(@end_effector_PR,initial_guess,options);
    
    a = cos(theta/2);
    b = n(1)*sin(theta/2);
    c = n(2)*sin(theta/2);
    d = n(3)*sin(theta/2);
    R = [a*a + b*b - c*c - d*d, 2*(b*c - a*d), 2*(b*d + a*c);
        2*(b*c + a*d), a*a + c*c - b*b - d*d, 2*(c*d - a*b);
        2*(b*d - a*c), 2*(c*d + a*b), a*a + d*d - b*b - c*c];

    v_x = (R*(p1'-center')/norm(p1-center))';
    v_y = cross(n,v_x);
    
    % the RAVENcenter is at (-14.5mm, 0) 
    RAVEN_center = center+v_x*(-14.5);
end

        





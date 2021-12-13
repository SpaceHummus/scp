% This script generates the robot gocode instructions to take different
% pictures

%% Inputs

% Define X,Y position just under the robot's home position
x0_mm = 0; % mm
y0_mm = 300; % mm

% Robot configuration
camera_distance_from_bottom_of_robot_mm = 15; % Camera is installed 15mm above the bottom of the robot arm

% The minimal FOV that the camera has (usually along the v axis)
camera_fov_deg = 70*1.5; % From https://www.arducam.com/product/arducam-12mp-imx477-motorized-focus-high-quality-camera-for-raspberry-pi/

% Target size from generate_distortion_calibration_target.m
target_size_mm = 40; % = n_boxes_x*box_size

% Inputs from take_distortion_calibration_images.py
time_per_image_set_sec = 20;
camera_height_above_iPad_mm = [110,  80,  65,  58,  52];
n_robot_positions = 49;

%% Open the gcode file and write setup information
time_per_image_set_msec = time_per_image_set_sec*1e3;
fid = fopen('take_distortion_calibration_images.gcode','wt');
fprintf(fid,'; Setup\n');
fprintf(fid,';G90   (Absolute positioning, Z0 is when arm touches target, camera height of 15mm)\n');
fprintf(fid,';G21   (Set units to millimeters)\n');
fprintf(fid,'\n');
fprintf(fid,'; Go up to signal the robot is going and allow user to click enter\n');
fprintf(fid,'G0 Z%0.f (Camera height of %.0fmm)\n',...
    min(camera_height_above_iPad_mm-camera_distance_from_bottom_of_robot_mm), ...
    min(camera_height_above_iPad_mm));
fprintf(fid,'G4 P10 (Wait for a bit)\n');
fprintf(fid,'\n');
fprintf(fid,'; Go to the center positioning\n');
fprintf(fid,'G0 X%.0f Y%.0f (Just under the robot position is %.0fmm, %.0fmm)\n',x0_mm,y0_mm,x0_mm,y0_mm);
fprintf(fid,'G4 P100\n');
fprintf(fid,'\n');
fprintf(fid,'; Set x-y positions and aquire images (base is Y=%.0f, X=%.0f, that is a good nutral place)\n',x0_mm,y0_mm);
fprintf(fid,'; P delay should be time_per_image_set_sec*1000=%.0f',time_per_image_set_msec);

%% Loop over all positions
for hi=1:length(camera_height_above_iPad_mm)
    h = camera_height_above_iPad_mm(hi);
    fprintf(fid,'\nG0 Z%0.f (Camera height of %.0fmm)\n',...
    	h-camera_distance_from_bottom_of_robot_mm, ...
    	h);
    
    %% Compute max travel distance
    if round(sqrt(n_robot_positions)) ~= sqrt(n_robot_positions)
        error('Please select n_robot_positions = %.0f which is a square of an integer',n_robot_positions);
    end
    max_travel_mm = sin(camera_fov_deg/2*pi/180)*h-target_size_mm/2;
    travel_mm = round(linspace(-max_travel_mm,max_travel_mm,sqrt(n_robot_positions)));
    
    % Set a grid
    [xx,yy] = meshgrid(travel_mm,travel_mm);
    yy(:,1:2:end) = -yy(:,1:2:end); % Make snake pattern to prvent large translations
    
    %% Print options
    xx = xx(:);
    yy = yy(:);
	
	if mod(hi,2) == 0
		% Start from the end y position since we don't need to travel that long for it
		xx = flip(xx);
		yy = flip(yy);
	end
    
    for xi=1:length(xx)
        fprintf(fid,'G0 X%.0f Y%.0f\n',xx(xi)+x0,yy(xi)+y0);
        fprintf(fid,'G4 P%.0f\n',time_per_image_set_msec);
    end
end

%% Clean up
fprintf(fid,'\n; Go to the center positioning\n');
fprintf(fid,'G0 X%.0f Y%.0f\n',x0_mm,y0_mm);
fprintf(fid,'G0 Z%.0f\n',min(camera_height_above_iPad_mm-camera_distance_from_bottom_of_robot_mm));
fprintf(fid,'G4 P1\n');
fclose(fid);
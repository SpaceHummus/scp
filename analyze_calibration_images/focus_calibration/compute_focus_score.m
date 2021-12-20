function score = compute_focus_score(focus_calibration_target_image,direction)
% This function computes the focus calibration score that measure sharpness
% INPTUS:
%   focus_calibration_target_image - image file path, aquired by
%       take_focus_calibration_images.py
%   direction - stripes direction 'x' (default) along x axis, or 'y' along
%       y axis

%% Input checks
if ~exist('focus_calibration_target_image','var')
    focus_calibration_target_image = 'test_image.jpg';
end

if ~exist('direction','var')
    direction = 'x';
end

%% Read image and select roi
im = imread(focus_calibration_target_image);
    
% Crop center of the image, we would like to focus on that
s = size(im);
roi_y = round((s(1)*2/5):(s(1)*3/5));
roi_x = round((s(2)*2/5):(s(2)*3/5));
im = double(rgb2gray(im(roi_y,roi_x,:)));

% Align strips
if(lower(direction) == 'x')
    im = im'; % Flip;
end

% Remove background
im = im-mean(im(:));

% Compute MTF
f = fftshift(fft(im,[],1));
f = abs(f); % Loose phase
f = mean(f,2); % Mean

% Score is the entroopy minus DC
score = sqrt(sum(f.^2));
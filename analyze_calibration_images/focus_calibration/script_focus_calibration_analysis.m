% This script compute score for multiple focuses and camera settings

%% Inputs

folder_path = '..\..\take_calibration_images\C02_focus_calibration_images_2021-12-19-4\';
direction = 'x'; % Are lines parallel to 'x' direction? If so write 'x'

%% Process Folder Name
if folder_path(end) ~= '\'
    folder_path(end+1) = '\';
end

[~,calibration_folder] = fileparts(folder_path(1:(end-1)));

camera_name = calibration_folder(1:3);
calibration_date = calibration_folder(end+(-9:0));

%% Get files, make data structure
ds = fileDatastore([folder_path '*.jpg'],'ReadFcn',@(x)(x));

file_paths = ds.Files;
file_names = cellfun(@get_file_name,file_paths,'UniformOutput',false);

file_h = cellfun(@(x)(str2double(x(2:4))),file_names);
file_focus_settings = cellfun(@(x)(str2double(x(end+(-3:0)))),file_names);

h = unique(file_h);
focus_setting = unique(file_focus_settings);

scores = zeros(length(focus_setting),length(h))*NaN;

%% Loop over all files and extract data
disp('Computing Entropy for Each Focus Position...');
for i=1:length(file_paths)
    h_i = find(h==file_h(i));
    focus_setting_i = find(focus_setting==file_focus_settings(i));
    scores(focus_setting_i,h_i) = compute_focus_score(file_paths{i},direction); %#ok<FNDSB>
end
disp('Done!');

%% Find best focus for each height
recommended_focus_setting = zeros(size(h));
for h_i=1:length(h)
    [~, i_max] = max(scores(:,h_i));
    
    % Fit polynomial around the maximum
    ii = max(1,i_max-3):min(length(focus_setting),i_max+3);
    ii(isnan(scores(ii,h_i))) = []; % Remove values we don't have
    data_to_fit = scores(ii,h_i);
    f_to_fit = focus_setting(ii);
    p = polyfit(f_to_fit,data_to_fit,2);
    
    % Find peak
    k = polyder(p); % find derivative of above polynomial
    r = roots(k); % find roots of polynomial created from derivative above
    
    recommended_focus_setting(h_i) = r;
    
    % Plot
    figure(2);
    focus_setting_grid = linspace(min(focus_setting),max(focus_setting));
    plot(focus_setting,scores(:,h_i),focus_setting_grid,polyval(p,focus_setting_grid));
    hold on;
    plot(r,polyval(p,r),'*r');
    hold off
    ylim([0, max(scores(:,h_i))*1.1]);
    grid on;
    title(sprintf('Entropy for h=%.0fmm',h(h_i)));
    xlabel('Focus Setting');
    ylabel('Entropy');
    legend('Data','Fit','Best Focus','location','southeast');
    pause(0.5);
end

%% Refine Recommendation
p = polyfit(h,recommended_focus_setting,3);
recommended_focus_setting = polyval(p,h);

%% Fine the best image for each focus position
best_image_path = cell(size(h));
for h_i=1:length(h)
    [~, ii] = min(abs(focus_setting-recommended_focus_setting(h_i)));
    best_image_path{h_i} = file_paths{ii};
end

output_file_name = sprintf('%s_focus_setting_%s',camera_name,calibration_date);

%% Plot 
hh=figure(1);
s1 = get(0, 'ScreenSize'); set(hh,'Position', [0 0 s1(3) s1(4)-80]);

subplot(3,5,1:10);
imagesc(h,focus_setting,scores);
hold on
plot(h,recommended_focus_setting,'*-');
hold off;
colorbar
ylabel('Focus Setting [Camera Units]');
xlabel('Camera Distance [mm]');
title ('Entropy');
legend('Recommended Focus Setting');
axis xy

i = round(linspace(1,length(h),5));
subplot(3,5,11);
draw_pixel_example(best_image_path,h,recommended_focus_setting,i(1));
ylabel(sprintf('See MTF target images at different h.\nSee they are all sharp'));
subplot(3,5,12);
draw_pixel_example(best_image_path,h,recommended_focus_setting,i(2));
subplot(3,5,13);
draw_pixel_example(best_image_path,h,recommended_focus_setting,i(3));
subplot(3,5,14);
draw_pixel_example(best_image_path,h,recommended_focus_setting,i(4));
subplot(3,5,15);
draw_pixel_example(best_image_path,h,recommended_focus_setting,i(5));

saveas(hh,[output_file_name '.png']);

%% Generate YAML
fid = fopen([output_file_name '.yaml'],'wt');
fprintf(fid,'camera_id: ''%s''\n',camera_name);
fprintf(fid,'calibration_date: ''%s''\n',calibration_date);
fprintf(fid,'\n# For each height, what is the recommended focus setting\n');
fprintf(fid,'height_mm:\n');
for i=1:length(h)
    fprintf(fid,'\t- %.0f\n',h(i));
end
fprintf(fid,'focus_setting:\n');
for i=1:length(h)
    fprintf(fid,'\t- %.0f\n',recommended_focus_setting(i));
end
fclose(fid);

%% Generate raw output file
save([output_file_name '.mat'], ...
    'camera_name', 'calibration_date', 'h', 'recommended_focus_setting');

%% Aux functions
function name = get_file_name(filepath)
[~,name] = fileparts(filepath);
end

function draw_pixel_example(best_image_path,h,recommended_focus_setting,i)
im = imread(best_image_path{i});
s = size(im);
roi_y = round(s(1)/2 + (-50:50));
roi_x = round(s(2)/2 + (-50:50));
im = rgb2gray(im(roi_y,roi_x,:));
imshow(imadjust(im));
title(sprintf('Image Example (h=%.0fmm, f=%.0f)',h(i),recommended_focus_setting(i)));
end
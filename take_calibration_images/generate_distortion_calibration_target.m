% This script will generate a checkered target in a white background

%% Inputs

% Pixel size of the output image
pixel_size = 0.25; %mm

% Checkered pattern
box_size = 2; %mm
n_boxes_x = 15;
n_boxes_y = 13;

% Scale Bar
scalebar_size = 100; %mm

% Target size
target_size = 250; % mm

%% Generate coordinats and grating
x = (-target_size/2):pixel_size:(target_size/2); % mm
y = x;
[xx,yy] = meshgrid(x,y);

% Generate base image
im = zeros(size(xx),'uint8')+255;

%% Generate checkered
cbox_size_pixels = box_size/pixel_size;

im_checkered = checkerboard(cbox_size_pixels,n_boxes_y,n_boxes_x);
im_checkered = im_checkered(1:(end/2),1:(end/2));
im_checkered = im_checkered*254+1;

i_ch_start = round(size(im,1)/2-size(im_checkered,1)/2);
j_ch_start = round(size(im,2)/2-size(im_checkered,2)/2);
i_ch_end = i_ch_start + size(im_checkered,1) -1;
j_ch_end = j_ch_start + size(im_checkered,2) -1;

im(i_ch_start:i_ch_end,j_ch_start:j_ch_end) = uint8(im_checkered);
    

%% Draw scalebar

im_checkered = checkerboard(cbox_size_pixels,2,scalebar_size/box_size);
im_checkered = im_checkered(1:(end/2),1:(end/2));
im_checkered = im_checkered*254+1;

i_sb_start = round(i_ch_end+3*size(im_checkered,1));
j_sb_start = round(size(im,2)/2-size(im_checkered,2)/2);
i_sb_end = i_sb_start + size(im_checkered,1) -1;
j_sb_end = j_sb_start + size(im_checkered,2) -1;

im(i_sb_start:i_sb_end,j_sb_start:j_sb_end) = 1; % uint8(im_checkered);

%% Write the text in a figure, and capture it
my_text = sprintf('Scale: %.0f cm. Square size %.0f mm',scalebar_size/10,box_size);
f=figure(22);
text('units','pixels','position',[20 20],'fontunits','pixels', ...
	'fontsize',20,'string',['|' my_text '|']);
axis off
text_im = getframe(gca); 
text_im = text_im.cdata;
close(f)
text_im(text_im==240) = 255;
text_im = rgb2gray(text_im);

text_im(all(text_im>5,2),:) = [];
strip = text_im(1,:);
i_start = find(strip ~= 255,1,'first')+3;
i_end = find(strip ~= 255,1,'last')-3;
text_im = text_im(:,i_start:i_end);

%% Add the text to the figure
x_index_start = round(length(x)/2-size(text_im,2)/2);
x_index_end   = x_index_start+size(text_im,2)-1;

y_index_start = i_sb_end+10;
y_index_end   = y_index_start+size(text_im,1)-1;

im(y_index_start:y_index_end,x_index_start:x_index_end) = text_im;

%% Save
imshow(im);
fn = sprintf('distortion_calibration_target_%.0fum_per_pixel.png',...
    pixel_size*1000);
imwrite(im,fn);

ppi = 25.4/pixel_size;
fprintf('Required Screen Resolution: %.0f ppi\n',ppi);
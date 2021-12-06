% This script will generate a black and white target that can be used to
% mesure MTF, by adjusting focus one could find the optimal focus position

%% Inputs

% Pixel size of the output image
pixel_size = 0.25; %mm
direction = 'x'; % strips direction could be x or y

% Scale Bar
scalebar_size = 100; %mm

% Target size
target_size = 250; % mm

%% Generate coordinats and grating
x = (-target_size/2):pixel_size:(target_size/2); % mm
y = x;
[xx,yy] = meshgrid(x,y);

% Generate base image
im = zeros(size(xx),'uint8');

%% Draw Strips
switch(lower(direction))
    case 'x'
        im(:,1:2:end) = 255;
    case 'y'
        im(1:2:end,:) = 255;
end

%% Draw scalebar

isInLeg = (xx > -scalebar_size/2) & (xx < +scalebar_size/2) & ...
    (yy > target_size/2-15) & (yy < target_size/2-10);

im(isInLeg) = 255;

%% Write the text in a figure, and capture it
my_text = sprintf('%.0f cm',scalebar_size/10);
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

y_index_start = round(...
    mean(find((y > target_size/2-15) & (y < target_size/2-10))) ...
    -size(text_im,1)/2);
y_index_end   = y_index_start+size(text_im,1)-1;

im(y_index_start:y_index_end,x_index_start:x_index_end) = text_im;
imshow(im);

%% Save
imshow(im);
fn = sprintf('focus_calibration_target_%.0fum_per_pixel.png',...
    pixel_size*1000);
imwrite(im,fn);

ppi = 25.4/pixel_size;
fprintf('Required Screen Resolution: %.0f ppi\n',ppi);
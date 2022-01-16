function t = time_picture_was_taken(image_filepath)
% Figure out what time was this pciture taken from image file path. Returns a time structure

[~,fn] = fileparts(image_filepath);
c = textscan(fn','%f-%f-%f__%f_%f_%s');
t = datenum(2000+c{1},c{2},c{3},c{4},c{5},0);
end

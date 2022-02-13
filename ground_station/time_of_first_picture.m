function t0 = time_of_first_picture(image_directory)
% Figure out what time was the first picture taken (start of experiment)

ds =  fileDatastore([image_directory '\*.jpg'],'ReadFcn',@imread);

% Figure out file name length, select only files with the right length
file_names = ds.Files;
is_it = cellfun(@is_file_name_date_format_correct,file_names);
file_names(~is_it) = []; % Remove files with the wrong name

t0 = time_picture_was_taken(file_names{1});
end

function res = is_file_name_date_format_correct(fn)
res = true;
[~,fn] = fileparts(fn);

if length(fn) ~= 24
    res = false;
end
if (fn(3) ~= '-')
    res = false;
end
end

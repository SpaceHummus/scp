function t0 = time_of_first_picture(image_directory)
% Figure out what time was the first picture taken (start of experiment)

ds =  fileDatastore([image_directory '\*.jpg'],'ReadFcn',@imread);
t0 = time_picture_was_taken(ds.Files{1});
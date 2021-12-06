
# Kill proecess that operates the experiment to prevent interference
../flight_software/stop_scp_main.sh
sleep 1

sudo python3 take_distortion_calibration_images.py
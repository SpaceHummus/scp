
# Kill proecess that operates the experiment to prevent interference
../flight_software/stop_scp_main.sh
sleep 1

python3 take_focus_calibration_images.py
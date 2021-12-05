; Setup
;G90   (Absolute positioning, Z0 is when arm touches target, camera height of 15mm)
;G21   (Set units to millimeters)
G0 Z0  (Go to home position
G4 P10 (Wait for a bit)

; Set camera positions & aquire images
G0 Z25  (Camera height of 40mm)
G4 P300000 (Delay should be the same as time_per_image_set_sec*1000)
G0 Z35  (Camera height of 50mm)
G4 P300000 (Delay should be the same as time_per_image_set_sec*1000)
G0 Z45  (Camera height of 60mm)
G4 P300000 (Delay should be the same as time_per_image_set_sec*1000)
G0 Z55  (Camera height of 70mm)
G4 P300000 (Delay should be the same as time_per_image_set_sec*1000)
G0 Z65  (Camera height of 80mm)
G4 P300000 (Delay should be the same as time_per_image_set_sec*1000)
G0 Z75  (Camera height of 90mm)
G4 P300000 (Delay should be the same as time_per_image_set_sec*1000)
G0 Z85  (Camera height of 100mm)
G4 P300000 (Delay should be the same as time_per_image_set_sec*1000)
G0 Z95  (Camera height of 110mm)
G4 P300000 (Delay should be the same as time_per_image_set_sec*1000)
G0 Z105 (Camera height of 120mm)

; Last delay
G4 P2000
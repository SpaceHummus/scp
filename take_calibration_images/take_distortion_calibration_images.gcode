; Setup
;G90   (Absolute positioning, Z0 is when arm touches target, camera height of 15mm)
;G21   (Set units to millimeters)

; Go up to signal the robot is going and allow user to click enter
G0 Z60 (Camera height of 75mm)
G4 P10 (Wait for a bit)

; Go to the center positioning
G0 X0 Y300
G4 P100

; Set x-y positions and aquire images (base is Y=300, X=0, that is a good nutral place)
G0 X-20 Y280
G4 P70000 (Delay should be the same as time_per_image_set_sec*1000)
G0 X-10 Y280
G4 P70000
G0 X0 Y280
G4 P70000 
G0 X10 Y280
G4 P70000
G0 X20 Y280
G4 P70000

G0 X20 Y290
G4 P70000
G0 X10 Y290
G4 P70000
G0 X0 Y290
G4 P70000
G0 X-10 Y290
G4 P70000
G0 X-20 Y290
G4 P70000

G0 X-20 Y300
G4 P70000
G0 X-10 Y300
G4 P70000
G0 X0 Y300
G4 P70000 
G0 X10 Y300
G4 P70000
G0 X20 Y300
G4 P70000

G0 X20 Y310
G4 P70000
G0 X10 Y310
G4 P70000
G0 X0 Y310
G4 P70000
G0 X-10 Y310
G4 P70000
G0 X-20 Y310
G4 P70000

G0 X-20 Y320
G4 P70000
G0 X-10 Y320
G4 P70000
G0 X0 Y320
G4 P70000 
G0 X10 Y320
G4 P70000
G0 X20 Y320
G4 P70000

; Go to the center positioning
G0 X0 Y300
G4 P1

def mark_attendance_camera():
    import cv2
    from deepface import DeepFace
    import os
    from datetime import datetime

    def mark_attendance(name):
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        attendance_file = "attendance/attendance.csv"

        if not os.path.exists("attendance"):
            os.makedirs("attendance")

        if not os.path.exists(attendance_file):
            with open(attendance_file, "w") as f:
                f.write("Name,Date,Time\n")

        with open(attendance_file, "r+") as f:
            lines = f.readlines()
            names_today = [line.split(",")[0] for line in lines if date_str in line]
            if name not in names_today:
                f.write(f"{name},{date_str},{time_str}\n")
                print(f"{name} marked at {time_str}")
            else:
                print(f"{name} already marked today")

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            result = DeepFace.find(frame, db_path="dataset", enforce_detection=False)
            if len(result) > 0 and not result[0].empty:
                identity = result[0].iloc[0]['identity']
                name = os.path.basename(identity).split("_")[0]
                mark_attendance(name)
        except Exception as e:
            print("No match found or error occurred.")

        cv2.imshow("Face Attendance", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

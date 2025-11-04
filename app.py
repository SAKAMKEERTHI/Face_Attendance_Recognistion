from flask import Flask, render_template, request, jsonify
import mark_attendance_camera
import base64
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mark', methods=['POST'])
def mark_attendance():
    try:
        data = request.get_json()
        image_data = data['image'].split(',')[1]
        class_name = data.get('class', 'Unknown')
        period_time = data.get('period', 'Unknown')

        img_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if frame is None:
            print("⚠️ Frame decoding failed")
            return jsonify({'error': 'Invalid image frame'})

        print("📸 Frame received for processing")
        result = mark_attendance_camera.process_frame(frame)

        # Then inject class and period into each face result
        for face in result.get("faces", []):
            face["class_name"] = class_name
            face["period_time"] = period_time

        return jsonify(result)

    except Exception as e:
        print(f"⚠️ Backend error: {str(e)}")
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
import io

app = Flask(__name__)
# Cho phép tất cả các nguồn gốc kết nối (CORS) để app.py (frontend) có thể gửi yêu cầu
CORS(app)

# --- BƯỚC 1: XÂY DỰNG MÔ HÌNH VÀ NẠP FILE TRỌNG SỐ ---
def load_fixed_model(model_path):
    print(f"Đang nạp file mô hình AI mới nhất ({model_path})...")
    try:
        # Load trực tiếp toàn bộ model (vì bạn đã tự train sinh ra file chuẩn 11 lớp)
        model = tf.keras.models.load_model(model_path, compile=False)
        print(">>> Nạp trọng số Mô hình thành công!")
        return model
    except Exception as e:
        print(f"Lỗi nạp trọng số: {e}")
        return None

# BỘ NHÃN 11 LỚP CHUẨN KAGGLE THEO THỨ TỰ ALPHA B TỪ COLAB (ĐÃ DỊCH SANG TIẾNG VIỆT)
LABELS = ['Bánh mì', 'Sản phẩm từ sữa', 'Tráng miệng', 'Trứng', 'Đồ chiên', 
          'Thịt', 'Mì / Nui', 'Cơm', 'Hải sản', 'Súp / Canh', 'Rau củ / Trái cây']

NUTRITION_DATA = {
    'Bánh mì': {'calories': 265, 'protein': 9, 'carbs': 49, 'fat': 3, 'description': 'Thực phẩm làm từ bột mì nướng, giàu tinh bột (như Bánh mì, Sandwich...).'},
    'Sản phẩm từ sữa': {'calories': 150, 'protein': 8, 'carbs': 12, 'fat': 8, 'description': 'Các sản phẩm chế tác từ sữa như Phô mai, Bơ, Sữa chua, Váng sữa.'},
    'Tráng miệng': {'calories': 350, 'protein': 4, 'carbs': 50, 'fat': 15, 'description': 'Món tráng miệng ngọt ngào (Bánh ngọt, Kem, Socola...), chứa rất nhiều đường và calo.'},
    'Trứng': {'calories': 155, 'protein': 13, 'carbs': 1.1, 'fat': 11, 'description': 'Trứng luộc hoặc chiên - Thực phẩm quen thuộc chứa nguồn đạm (protein) tuyệt vời.'},
    'Đồ chiên': {'calories': 320, 'protein': 10, 'carbs': 25, 'fat': 20, 'description': 'Thức ăn chiên ngập dầu (Gà rán, Khoai tây chiên), giòn rụm nhưng dễ gây tăng cân do chứa nhiều chất béo.'},
    'Thịt': {'calories': 250, 'protein': 26, 'carbs': 0, 'fat': 15, 'description': 'Thịt tươi được làm chín (Bò bít tết, Thịt lợn, Gà luộc...), cung cấp hàm lượng đạm thiết yếu.'},
    'Mì / Nui': {'calories': 138, 'protein': 5, 'carbs': 25, 'fat': 2, 'description': 'Mì sợi, Phở, hoặc Pasta Ý, nguồn cung cấp carbohydrate dồi dào cho cơ thể.'},
    'Cơm': {'calories': 130, 'protein': 2.7, 'carbs': 28, 'fat': 0.3, 'description': 'Cơm nấu từ hạt gạo, thực phẩm chủ yếu siêu quen thuộc của nền ẩm thực Á Đông.'},
    'Hải sản': {'calories': 100, 'protein': 20, 'carbs': 0, 'fat': 1.5, 'description': 'Hải sản tươi sống (Cá, Tôm, Cua, Mực...), chứa hàm lượng dinh dưỡng omega-3 tuyệt vời.'},
    'Súp / Canh': {'calories': 60, 'protein': 3, 'carbs': 7, 'fat': 2, 'description': 'Súp hoặc các loại Canh nóng hổi, dạng lỏng cực kỳ dễ tiêu hóa và bồi bổ dưỡng chất.'},
    'Rau củ / Trái cây': {'calories': 45, 'protein': 1, 'carbs': 10, 'fat': 0.2, 'description': 'Trái cây và rau củ tươi xanh (Salad, Rau luộc, Cà rốt...), bổ sung nguồn Vitamin siêu khổng lồ.'}
}

MODEL_PATH = 'food_model_auto.h5'
model = load_fixed_model(MODEL_PATH)

# --- BƯỚC 2: API NHẬN DIỆN VÀ PHÂN TÍCH (BACKEND) ---
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    if model is None:
         return jsonify({'error': 'AI Model chưa được nạp thành công, hãy kiểm tra file .h5'}), 500

    try:
        file = request.files['file']
        image = Image.open(io.BytesIO(file.read())).convert('RGB')
        
        import math
        img = image.resize((224, 224))
        img_array = np.array(img, dtype=np.float32)
        # Tiền xử lý dữ liệu ảnh cho MobileNetV2
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)
        
        # Dự đoán phân lớp 11 nhóm
        preds = model.predict(img_array)
        index = int(np.argmax(preds))
        confidence = float(np.max(preds) * 100)
        
        if math.isnan(confidence):
            confidence = 0.0
            
        label = LABELS[index]
        nutrition = NUTRITION_DATA.get(label, {})
        
        return jsonify({
            'label': label,
            'confidence': confidence,
            'nutrition': nutrition
        })
    except Exception as e:
        return jsonify({'error': f'Lỗi hệ thống: {str(e)}'}), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("AI BACKEND ĐANG CHẠY TẠI http://127.0.0.1:5001")
    print("Đã sãn sàng nhận file từ giao diện web...")
    print("="*50)
    # Chạy trên PORT 5001 để tránh đụng với Frontend ở PORT 5000
    app.run(host='127.0.0.1', port=5001, debug=False)

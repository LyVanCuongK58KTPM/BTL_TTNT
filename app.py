from flask import Flask, render_template_string
import requests

app = Flask(__name__)

# --- GIAO DIỆN FRONTEND (CHỈ LÀM NHIỆM VỤ HIỂN THỊ) ---
FRONTEND_HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Food Analyzer</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #6C5CE7;
            --primary-light: #a29bfe;
            --secondary: #00cec9;
            --dark: #1e272e;
            --light: #f5f6fa;
            --error: #ff7675;
            --success: #00b894;
            --calories: #ff9f43;
            --protein: #ee5253;
            --carbs: #feca57;
            --fat: #0abde3;
            --glass-bg: rgba(30, 39, 46, 0.7);
            --glass-border: rgba(255, 255, 255, 0.1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }

        body {
            min-height: 100vh;
            background: linear-gradient(135deg, #1e1e2d 0%, #151521 100%);
            color: var(--light);
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 2rem;
        }

        body::before, body::after {
            content: '';
            position: absolute;
            width: 300px;
            height: 300px;
            border-radius: 50%;
            filter: blur(80px);
            z-index: -1;
            animation: drift 10s infinite alternate;
        }

        body::before {
            background: rgba(108, 92, 231, 0.4);
            top: -10%;
            left: 10%;
        }

        body::after {
            background: rgba(0, 206, 201, 0.3);
            bottom: 5%;
            right: 15%;
            animation-delay: -5s;
        }

        @keyframes drift {
            0% { transform: translateY(0) translateX(0); }
            100% { transform: translateY(50px) translateX(30px); }
        }

        .glass-container {
            background: var(--glass-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 3rem;
            width: 100%;
            max-width: 600px;
            box-shadow: 0 25px 50px rgba(0,0,0,0.5);
        }

        header {
            text-align: center;
            margin-bottom: 2.5rem;
        }

        .logo {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin-bottom: 10px;
        }

        .logo i {
            font-size: 2.5rem;
            color: var(--secondary);
            background: linear-gradient(135deg, var(--secondary), var(--primary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        header h1 {
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: -1px;
        }

        header h1 span {
            color: var(--secondary);
        }

        header p {
            color: #a4b0be;
            font-size: 1.1rem;
        }

        .upload-section {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .upload-box {
            border: 2px dashed rgba(255, 255, 255, 0.2);
            border-radius: 16px;
            height: 250px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            background: rgba(0,0,0,0.2);
        }

        .upload-box:hover, .upload-box.dragover {
            border-color: var(--secondary);
            background: rgba(0, 206, 201, 0.05);
        }

        .upload-content {
            text-align: center;
            z-index: 10;
            transition: opacity 0.3s;
        }

        .upload-content i {
            font-size: 3.5rem;
            color: var(--primary-light);
            margin-bottom: 15px;
        }

        .upload-content h3 {
            margin-bottom: 5px;
            font-size: 1.2rem;
        }

        .upload-content p {
            color: #747d8c;
            font-size: 0.9rem;
        }

        #preview {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            z-index: 20;
        }

        .primary-btn {
            background: linear-gradient(135deg, var(--primary) 0%, #4834d4 100%);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            width: 100%;
        }

        .primary-btn:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(108, 92, 231, 0.3);
        }

        .primary-btn:disabled {
            background: #353b48;
            color: #7f8fa6;
            cursor: not-allowed;
            transform: none;
        }

        .loader-container {
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem 0;
        }

        .spinner {
            width: 50px;
            height: 50px;
            border: 4px solid rgba(255,255,255,0.1);
            border-left-color: var(--secondary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 15px;
        }

        @keyframes spin { 100% { transform: rotate(360deg); } }

        .hidden { display: none !important; }

        .results-section {
            margin-top: 1rem;
            animation: slideUp 0.5s ease;
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .result-header h2 {
            font-size: 1.8rem;
            color: #fff;
        }

        .confidence-badge {
            background: rgba(0, 184, 148, 0.15);
            color: var(--success);
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9rem;
            border: 1px solid rgba(0, 184, 148, 0.3);
        }

        .food-description {
            color: #a4b0be;
            margin-bottom: 25px;
            line-height: 1.6;
        }

        .nutrition-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }

        .nutri-card {
            background: rgba(0,0,0,0.3);
            border-radius: 12px;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            border: 1px solid var(--glass-border);
            transition: transform 0.3s;
        }

        .nutri-card:hover { transform: translateY(-3px); }

        .nutri-card i {
            font-size: 1.5rem;
            margin-bottom: 10px;
        }

        .nutri-card.calories i { color: var(--calories); }
        .nutri-card.protein i { color: var(--protein); }
        .nutri-card.carbs i { color: var(--carbs); }
        .nutri-card.fat i { color: var(--fat); }

        .nutri-card .value {
            font-size: 1.5rem;
            font-weight: 700;
            color: white;
        }

        .nutri-card .unit {
            font-size: 0.8rem;
            color: #747d8c;
            margin-bottom: 4px;
        }

        .nutri-card .label {
            font-size: 0.85rem;
            font-weight: 500;
            color: #a4b0be;
        }
    </style>
</head>
<body>
    <div class="glass-container">
        <header>
            <div class="logo">
                <i class="fa-solid fa-utensils"></i>
                <h1>Nutri<span>Lens</span></h1>
            </div>
            <p>Hệ thống AI nhận diện món ăn và phân tích dinh dưỡng thông minh</p>
        </header>

        <main>
            <div class="upload-section">
                <div class="upload-box" id="upload-box">
                    <input type="file" id="fileInp" accept="image/*" hidden>
                    <div class="upload-content">
                        <i class="fa-solid fa-cloud-arrow-up icon"></i>
                        <h3>Tải ảnh món ăn lên</h3>
                        <p>Kéo thả hoặc nhấn để chọn ảnh (JPG, PNG)</p>
                    </div>
                    <img id="preview" alt="Preview Image" src="" style="display: none;">
                </div>
                <button id="analyzeBtn" class="primary-btn" disabled>
                    <i class="fa-solid fa-microchip"></i> Phân Tích Món Ăn
                </button>
            </div>

            <div class="loader-container" id="loader">
                <div class="spinner"></div>
                <p>Khởi tạo AI phân tích...</p>
            </div>

            <div class="results-section hidden" id="results">
                <div class="result-header">
                    <h2 id="foodName">Bánh Táo</h2>
                    <div class="confidence-badge">
                        <span id="confidence">98.5</span>% Chính xác
                    </div>
                </div>
                
                <p id="foodDesc" class="food-description"></p>

                <div class="nutrition-grid">
                    <div class="nutri-card calories">
                        <i class="fa-solid fa-fire"></i>
                        <span class="value" id="calValue">0</span>
                        <span class="unit">kcal</span>
                        <span class="label">Calo</span>
                    </div>
                    <div class="nutri-card protein">
                        <i class="fa-solid fa-drumstick-bite"></i>
                        <span class="value" id="proValue">0</span>
                        <span class="unit">g</span>
                        <span class="label">Đạm (Protein)</span>
                    </div>
                    <div class="nutri-card carbs">
                        <i class="fa-solid fa-wheat-awn"></i>
                        <span class="value" id="carbValue">0</span>
                        <span class="unit">g</span>
                        <span class="label">Tinh bột (Carbs)</span>
                    </div>
                    <div class="nutri-card fat">
                        <i class="fa-solid fa-droplet"></i>
                        <span class="value" id="fatValue">0</span>
                        <span class="unit">g</span>
                        <span class="label">Chất béo (Fat)</span>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const uploadBox = document.getElementById('upload-box');
            const fileInp = document.getElementById('fileInp');
            const preview = document.getElementById('preview');
            const analyzeBtn = document.getElementById('analyzeBtn');
            const uploadContent = document.querySelector('.upload-content');
            
            const loader = document.getElementById('loader');
            const results = document.getElementById('results');

            const foodNameUI = document.getElementById('foodName');
            const confidenceUI = document.getElementById('confidence');
            const foodDescUI = document.getElementById('foodDesc');
            const calValue = document.getElementById('calValue');
            const proValue = document.getElementById('proValue');
            const carbValue = document.getElementById('carbValue');
            const fatValue = document.getElementById('fatValue');

            let currentFile = null;

            uploadBox.addEventListener('click', () => fileInp.click());

            uploadBox.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadBox.classList.add('dragover');
            });

            uploadBox.addEventListener('dragleave', () => {
                uploadBox.classList.remove('dragover');
            });

            uploadBox.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadBox.classList.remove('dragover');
                if (e.dataTransfer.files.length > 0) {
                    handleFile(e.dataTransfer.files[0]);
                }
            });

            fileInp.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    handleFile(e.target.files[0]);
                }
            });

            function handleFile(file) {
                if (!file.type.startsWith('image/')) {
                    alert('Vui lòng chọn file hình ảnh!');
                    return;
                }
                currentFile = file;
                const reader = new FileReader();
                reader.onload = (e) => {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                    uploadContent.style.opacity = '0';
                    analyzeBtn.disabled = false;
                };
                reader.readAsDataURL(file);
                results.classList.add('hidden');
            }

            analyzeBtn.addEventListener('click', async () => {
                if (!currentFile) return;

                const formData = new FormData();
                formData.append('file', currentFile);

                analyzeBtn.disabled = true;
                loader.style.display = 'flex';
                results.classList.add('hidden');

                try {
                    // Connects to processor.py running on port 5001
                    const response = await fetch('http://127.0.0.1:5001/predict', {
                        method: 'POST',
                        body: formData
                    });

                    const data = await response.json();
                    
                    if (!response.ok) {
                        throw new Error(data.error || 'Server error');
                    }

                    renderResults(data);

                } catch (error) {
                    alert('Không thể kết nối đến AI Core (Vui lòng đảm bảo processor.py đang chạy ở port 5001): ' + error.message);
                } finally {
                    loader.style.display = 'none';
                    analyzeBtn.disabled = false;
                }
            });

            function renderResults(data) {
                foodNameUI.textContent = data.label;
                confidenceUI.textContent = data.confidence.toFixed(1);
                
                if (data.nutrition) {
                    foodDescUI.textContent = data.nutrition.description || '';
                    animateValue(calValue, 0, data.nutrition.calories, 1000);
                    animateValue(proValue, 0, data.nutrition.protein, 1000);
                    animateValue(carbValue, 0, data.nutrition.carbs, 1000);
                    animateValue(fatValue, 0, data.nutrition.fat, 1000);
                }

                results.classList.remove('hidden');
            }

            function animateValue(obj, start, end, duration) {
                let startTimestamp = null;
                const step = (timestamp) => {
                    if (!startTimestamp) startTimestamp = timestamp;
                    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
                    obj.innerHTML = (progress * (end - start) + start).toFixed(end % 1 !== 0 ? 1 : 0);
                    if (progress < 1) {
                        window.requestAnimationFrame(step);
                    }
                };
                window.requestAnimationFrame(step);
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(FRONTEND_HTML)

if __name__ == '__main__':
    print("\n" + "="*50)
    print("FRONTEND ĐANG CHẠY TẠI http://127.0.0.1:5000")
    print("Truy cập link trên ở trình duyệt web.")
    print("NHỚ BẬT KÈM FILE processor.py CHO BACKEND!")
    print("="*50)
    app.run(host='127.0.0.1', port=5000, debug=False)

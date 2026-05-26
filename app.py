import os
import base64
import uuid
from datetime import datetime

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for,
    session  
)

from data.analysis_results import ANALYSIS_RESULTS
from data.fashion_results import FASHION_RESULTS
from data.shop_data import SHOP_DATA

from model.pipeline import predict_image

# =========================
# APP CONFIG
# =========================

app = Flask(__name__)
app.secret_key = 'mytone_athenalyze_secure_key_2026'  

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================
# GLOBAL VARIABLES DELETED
# Variabel global ANALYZED_SEASON sudah dihapus total 
# agar data laptop A tidak bocor ke laptop B.
# =========================

# =========================
# DISCOVER
# =========================

@app.route('/')
def discover():
    return render_template('pages/discover.html')

# =========================
# SEASONS
# =========================

@app.route('/seasons')
def seasons():
    return render_template('pages/seasons.html')

@app.route('/seasons/spring')
def spring():
    return render_template('pages/spring.html')

@app.route('/seasons/summer')
def summer():
    return render_template('pages/summer.html')

@app.route('/seasons/autumn')
def autumn():
    return render_template('pages/autumn.html')

@app.route('/seasons/winter')
def winter():
    return render_template('pages/winter.html')

# =========================
# ANALYSIS PAGE
# =========================

@app.route('/analysis')
def analysis():
    return render_template('pages/analysis.html')

# =========================
# ANALYZE IMAGE
# =========================

@app.route('/analyze', methods=['POST'])
def analyze_image():
    filepath = None

    # =====================
    # OPTION 1: NORMAL FILE UPLOAD
    # =====================
    image = request.files.get('image')
    if image and image.filename != '':
        extension = os.path.splitext(image.filename)[1]
        filename = f"{uuid.uuid4()}{extension}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        image.save(filepath)

    # =====================
    # OPTION 2: WEBCAM SELFIE
    # =====================
    else:
        captured_image = request.form.get('captured_image')
        if captured_image:
            # REMOVE HEADER: data:image/png;base64,
            image_data = captured_image.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            
            filename = f"selfie_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex}.png"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            with open(filepath, 'wb') as f:
                f.write(image_bytes)

    # =====================
    # NO IMAGE RECEIVE
    # =====================
    if not filepath:
        return "No image received", 400

    # =====================
    # MODEL PREDICTION
    # =====================
    predicted_season, confidence = predict_image(filepath)

    # =====================
    # SAVE RESULT TO SESSION (🔒 AMAN & TERKUNCI PER USER)
    # =====================
    session['analyzed_season'] = predicted_season

    # =====================
    # REDIRECT RESULT
    # =====================
    return redirect(
        url_for(
            'result',
            season=predicted_season,
            conf=confidence
        )
    )

# =========================
# RESULT
# =========================

@app.route('/result/<season>')
def result(season):
    result_data = ANALYSIS_RESULTS.get(season)
    if not result_data:
        return "Season not found", 404

    return render_template(
        'pages/result.html',
        result=result_data,
        season=season,
        confidence=request.args.get('conf')
    )

# =========================
# GENDER PAGE
# =========================

@app.route('/gender/<season>')
def gender(season):
    return render_template('pages/gender.html', season=season)

# =========================
# FASHION ENTRY
# =========================

@app.route('/fashion')
def fashion():
    # <-- 3. AMBIL DATA KHUSUS LAPTOP USER YANG SEDANG MEMBUKA
    user_season = session.get('analyzed_season', None)

    if user_season:
        return redirect(
            url_for(
                'gender',
                season=user_season
            )
        )

    return redirect(url_for('fashion_season'))

# =========================
# FASHION SEASON PICKER
# =========================

@app.route('/fashion/season')
def fashion_season():
    return render_template('pages/fashion_season.html')

# =========================
# MANUAL SEASON
# =========================

@app.route('/fashion/set-season/<season>')
def set_fashion_season(season):
    return redirect(url_for('gender', season=season))

# =========================
# FINAL FASHION
# =========================

@app.route('/fashion/<gender>/<season>')
def fashion_result(gender, season):
    data = FASHION_RESULTS.get(gender, {}).get(season)
    if not data:
        return "Fashion result not found", 404

    return render_template(
        'pages/fashion.html',
        data=data,
        gender=gender,
        season=season
    )

# =========================
# SHOP
# =========================

@app.route('/shop')
def shop():
    return render_template('pages/shop.html', shop_data=SHOP_DATA)

# =========================
# LEGAL
# =========================

@app.route('/privacy')
def privacy():
    return render_template('pages/privacy.html')

@app.route('/terms')
def terms():
    return render_template('pages/terms.html')

@app.route('/science')
def science():
    return render_template('pages/science.html')

# =========================
# RUN (PORT CONFIGURED FOR HUGGING FACE)
# =========================
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=7860,
        debug=True
    )
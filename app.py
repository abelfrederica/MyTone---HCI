import os

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
app.secret_key = 'mytone_secret_key_bebas_apa_aja'  

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
    image = request.files.get('image')
    if not image:
        return "No image uploaded", 400

    # SAVE IMAGE
    filepath = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(filepath)

    # MODEL PREDICTION
    predicted_season, confidence = predict_image(filepath)

    # <-- 3. SIMPAN KE SESSION BROWSERS LAPTOP MASING-MASING
    session['analyzed_season'] = predicted_season

    # REDIRECT TO RESULT
    return redirect(
        url_for(
            'result',
            season=predicted_season,
            conf=confidence
        )
    )

# =========================
# ANALYSIS RESULT
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
    # <-- 4. AMBIL DARI SESSION LAPTOP YANG SEDANG MEMBUKA
    user_season = session.get('analyzed_season', None)

    # IF USER ALREADY DID ANALYSIS
    if user_season:
        return redirect(
            url_for(
                'gender',
                season=user_season
            )
        )

    # NO ANALYSIS YET ALWAYS SHOW SEASON PICKER
    return redirect(url_for('fashion_season'))

# =========================
# FASHION SEASON PICKER
# =========================

@app.route('/fashion/season')
def fashion_season():
    return render_template('pages/fashion_season.html')

# =========================
# MANUAL SEASON SELECTION
# =========================

@app.route('/fashion/set-season/<season>')
def set_fashion_season(season):
    return redirect(url_for('gender', season=season))

# =========================
# FINAL FASHION RESULT
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
# LEGAL PAGES
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

if __name__ == '__main__':
    # <-- 5. PASTIKAN PORT TETAP 7860 UNTUK HUGGING FACE
    app.run(
        host='0.0.0.0',
        port=7860,
        debug=True
    )
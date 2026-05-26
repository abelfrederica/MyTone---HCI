import os

from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for
)

from data.analysis_results import ANALYSIS_RESULTS
from data.fashion_results import FASHION_RESULTS
from data.shop_data import SHOP_DATA

from model.pipeline import predict_image

# =========================
# APP CONFIG
# =========================

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================
# GLOBAL ANALYSIS RESULT
# ONLY CHANGES AFTER ANALYSIS
# RESETS WHEN FLASK RESTARTS
# =========================

ANALYZED_SEASON = None

# =========================
# DISCOVER
# =========================

@app.route('/')
def discover():

    return render_template(
        'pages/discover.html'
    )

# =========================
# SEASONS
# =========================

@app.route('/seasons')
def seasons():

    return render_template(
        'pages/seasons.html'
    )

@app.route('/seasons/spring')
def spring():

    return render_template(
        'pages/spring.html'
    )

@app.route('/seasons/summer')
def summer():

    return render_template(
        'pages/summer.html'
    )

@app.route('/seasons/autumn')
def autumn():

    return render_template(
        'pages/autumn.html'
    )

@app.route('/seasons/winter')
def winter():

    return render_template(
        'pages/winter.html'
    )

# =========================
# ANALYSIS PAGE
# =========================

@app.route('/analysis')
def analysis():

    return render_template(
        'pages/analysis.html'
    )

# =========================
# ANALYZE IMAGE
# =========================

@app.route('/analyze', methods=['POST'])
def analyze_image():

    global ANALYZED_SEASON

    image = request.files.get('image')

    if not image:

        return "No image uploaded", 400

    # SAVE IMAGE

    filepath = os.path.join(
        UPLOAD_FOLDER,
        image.filename
    )

    image.save(filepath)

    # MODEL PREDICTION

    predicted_season, confidence = predict_image(filepath)

    # SAVE ANALYSIS RESULT

    ANALYZED_SEASON = predicted_season

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

    return render_template(

        'pages/gender.html',

        season=season

    )

# =========================
# FASHION ENTRY
# =========================

@app.route('/fashion')
def fashion():

    global ANALYZED_SEASON

    # =====================
    # IF USER ALREADY
    # DID ANALYSIS
    # =====================

    if ANALYZED_SEASON:

        return redirect(

            url_for(
                'gender',
                season=ANALYZED_SEASON
            )

        )

    # =====================
    # NO ANALYSIS YET
    # ALWAYS SHOW
    # SEASON PICKER
    # =====================

    return redirect(

        url_for(
            'fashion_season'
        )

    )

# =========================
# FASHION SEASON PICKER
# =========================

@app.route('/fashion/season')
def fashion_season():

    return render_template(
        'pages/fashion_season.html'
    )

# =========================
# MANUAL SEASON SELECTION
# =========================

@app.route('/fashion/set-season/<season>')
def set_fashion_season(season):

    # DO NOT SAVE GLOBALLY
    # ONLY TEMPORARY FLOW

    return redirect(

        url_for(
            'gender',
            season=season
        )

    )

# =========================
# FINAL FASHION RESULT
# =========================

@app.route('/fashion/<gender>/<season>')
def fashion_result(gender, season):

    data = FASHION_RESULTS.get(
        gender,
        {}
    ).get(season)
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

    return render_template(

        'pages/shop.html',

        shop_data=SHOP_DATA

    )

# =========================
# LEGAL PAGES
# =========================

@app.route('/privacy')
def privacy():

    return render_template(
        'pages/privacy.html'
    )


@app.route('/terms')
def terms():

    return render_template(
        'pages/terms.html'
    )


@app.route('/science')
def science():

    return render_template(
        'pages/science.html'
    )

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
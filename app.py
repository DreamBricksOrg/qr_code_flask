from flask import Flask, render_template, request, send_file
from utils.utils import generate_unique_codes, save_as_zip
import logging

app = Flask(__name__)
logger = logging.getLogger("qr_web")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            quantity = int(request.form.get("quantity"))
            codes = generate_unique_codes(quantity)
            zip_path = save_as_zip(codes)
            logger.info(f"{quantity} codes generated and zipped.")
            return send_file(zip_path, as_attachment=True)
        except Exception as e:
            logger.error(f"Failed to generate codes: {e}")

    return render_template("index.html")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger.info("Starting QR Code Generator Flask App")
    app.run(host='0.0.0.0', port=5001, debug=True)
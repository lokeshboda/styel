from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("women_fashion_myntra.csv")

@app.route("/")
def home():
    brands = df['ProductBrand'].dropna().unique().tolist()
    return render_template("index.html", categories=brands)

@app.route("/recommend", methods=["POST"])
def recommend():
    brand = request.json.get("category")
    max_price = float(request.json.get("max_price"))

    print("Received brand:", brand)
    print("Received max_price:", max_price)

    filtered = df[
        (df['ProductBrand'] == brand) &
        (df['Price (INR)'] <= max_price)
    ]
    print("Filtered rows:", len(filtered))

    top_items = filtered.head(10).to_dict(orient="records")
    return jsonify(top_items)


if __name__ == "__main__":
    app.run(debug=True)

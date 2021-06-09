# import necessary libraries

import pandas as pd
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

# create instance of Flask app
app = Flask(__name__)


# create route that renders index.html template
@app.route("/")
def index():
    return render_template("index.html")


    
# Using Postgres to load data
POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'mentalhealth_db',
    'port': '5433',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

# POSTGRES = {
#     'user': 'postgres',
#     'pw': 'delilahjones',
#     'db': 'mentalhealth_db',
#     'host': 'localhost',
#     'port': '5432',
# }
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
# %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Mental_health = Base.classes.mental_health

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

# @app.route("/physical")
# def physical():
#     """Return a list of sample names."""

#     # Return a list of the column names (sample names)
#     return jsonify(list(df.columns)[2:])

@app.route("/metadata/<sample>")
def sample_metadata(sample):
    """Return the MetaData for a given sample."""

    plot1 = pd.read_sql("select year, sum(physical_importance)/count(year) as avg_physical_importance, sum(mental_importance)/count(year) as avg_mental_importance from mental_health group by year", con = engine)
    plot2 = pd.read_sql("select year, sum(industry_support)/count(year) as avg_industry_support from mental_health group by year", con = engine)
    plot3 = pd.read_sql("select year, count(know_options) from mental_health where know_options like 'Yes' group by year", con = engine)
    plot4 = pd.read_sql("select year, count(know_options) from mental_health where know_options like 'No' group by year", con = engine)

    sel = [
        Mental_health.year,
        Mental_health.physical_importance,
        Mental_health.mental_importance,
        Mental_health.industry_support,
        Mental_health.know_options
    ]
    
    results = db.session.query(*sel).all()    
# Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        Mental_health["year"] = result[0]
        Mental_health["physical_importance"] = result[1]
        Mental_health["mental_importance"] = result[2]
        Mental_health["industry_support"] = result[3]
        Mental_health["know_options"] = result[4]
    

        print(sample_metadata)
        return jsonify(sample_metadata)

if __name__ == "__main__":
    app.run(debug=True)
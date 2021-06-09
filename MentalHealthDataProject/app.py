# import necessary libraries

from flask import Flask, render_template, redirect, jsonify
from sqlalchemy import create_engine
import pandas as pd

# create instance of Flask app
app = Flask(__name__)


# create route that renders index.html template
@app.route("/")
def index():
    return render_template("index.html")

# Create database connection
# change the owner name, password and port number based on your local situation
# engine = create_engine(f'postgresql://{*database_owner}:{*password}@localhost:{*port}/housing_db')
rds_connection_string = "postgres:postgres@n@localhost:5433/mentalhealth_db"
# rds_connection_string = "postgres:delilahjones@n@localhost:5432/mentalhealth_db"
engine = create_engine(f'postgresql://{rds_connection_string}')


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")



    phy_ment_df = pd.read_sql("select year, sum(physical_importance)/count(year) as avg_physical_importance, sum(mental_importance)/count(year) as avg_mental_importance from mental_health group by year", con = engine)
    support_df = pd.read_sql("select year, sum(industry_support)/count(year) as avg_industry_support from mental_health group by year", con = engine)
    know_yes_df = pd.read_sql("select year, count(know_options) from mental_health where know_options like 'Yes' group by year", con = engine)
    know_no_df = pd.read_sql("select year, count(know_options) from mental_health where know_options like 'No' group by year", con = engine)
    merge_know_df = pd.merge('know_yes_df', 'know_no_df')

    phy_ment_dict = phy_ment_df.to_dict()
    support_dict = support_df.to_dict()
    know_options_dict = merge_know.to_dict()

    mhData=[phy_ment_dict, support_dict, know_options_dict]

    # Return template and data
    return render_template("index.html", mhData=mhData)



if __name__ == "__main__":
    app.run(debug=True)


# @app.route("/physical")
# def physical():
#     """Return a list of sample names."""

#     # Return a list of the column names (sample names)
#     return jsonify(list(df.columns)[2:])

# @app.route("/metadata/<sample>")
# def sample_metadata(sample):
#     """Return the MetaData for a given sample."""

# @app.route("/physical")
# def physical():
#     """Return a list of sample names."""

#     # Return a list of the column names (sample names)
#     return jsonify(list(df.columns)[2:])

# @app.route("/metadata/<sample>")
# def sample_metadata(sample):
#     """Return the MetaData for a given sample."""

#     sel = [
#         Mental_health.year,
#         Mental_health.physical_importance,
#         Mental_health.mental_importance,
#         Mental_health.industry_support,
#         Mental_health.know_options
#     ]
    
#     results = db.session.query(*sel).all()    
# # Create a dictionary entry for each row of metadata information
#     sample_metadata = {}
#     for result in results:
#         Mental_health["year"] = result[0]
#         Mental_health["physical_importance"] = result[1]
#         Mental_health["mental_importance"] = result[2]
#         Mental_health["industry_support"] = result[3]
#         Mental_health["know_options"] = result[4]
    

#         print(sample_metadata)
#         return jsonify(sample_metadata)
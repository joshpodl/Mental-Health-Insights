# import necessary libraries

from flask import Flask, render_template, redirect, jsonify
from sqlalchemy import create_engine
import pandas as pd

# create instance of Flask app
app = Flask(__name__)


# create route that renders index.html template
@app.route("/")
def index():

    # Create database connection
    # change the owner name, password and port number based on your local situation
    # engine = create_engine(f'postgresql://{*database_owner}:{*password}@localhost:{*port}/mentalhealth_db')
    rds_connection_string = "postgres:postgres@localhost:5433/mentalhealth_db"
    # rds_connection_string = "postgres:delilahjones@localhost:5432/mentalhealth_db"
    engine = create_engine(f'postgresql://{rds_connection_string}')

    phy_df = pd.read_sql('select year, sum(physical_importance)/count(year) as avg_physical_importance from mental_health group by year order by year asc', con = engine)
    ment_df = pd.read_sql('select year, sum(mental_importance)/count(year) as avg_mental_importance from mental_health group by year order by year asc', con = engine)
    
    support_df = pd.read_sql("select year, sum(industry_support)/count(year) as avg_industry_support from mental_health group by year order by year asc", con = engine)
    
    know_yes_df = pd.read_sql("select year, count(know_options) from mental_health where know_options like 'Yes' group by year order by year asc", con = engine)
    know_no_df = pd.read_sql("select year, count(know_options) from mental_health where know_options like 'No' group by year order by year asc", con = engine)
    merge_know_df = know_yes_df.merge(know_no_df, how="inner", on="year")
    
    phy_dict = phy_df.to_json(orient="records")
    ment_dict = ment_df.to_json(orient="records")
    support_dict = support_df.to_json(orient="records")
    know_options_dict = merge_know_df.to_json(orient="records")

    mhData=[phy_dict, ment_dict, support_dict, know_options_dict]

    # Return template and data
    return render_template("index.html", mhData=mhData)


if __name__ == "__main__":
    app.run(debug=True)
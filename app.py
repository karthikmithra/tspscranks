
from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():    
    return render_template('index.html')

@app.route('/process_roll_number', methods=['POST'])
def process_roll_number():
    data = request.get_json()
    roll_number = data['rollNumber']

    # Connect to the SQLite database
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

     # Example query: Replace with your actual SQL query
    cursor.execute("SELECT * FROM my_table WHERE htnum = ?", (roll_number,))
    result = cursor.fetchall()
    
    # Assuming `row` is a tuple representing a row fetched from the database
    # result = {'data': row2}
    
    rowhtnum = result[0][0]
    rowgenrank = result[0][1]
    rowhtnum2 = result[0][2]
    rowmarks = result[0][3]
    rowgender = result[0][4]
    rowcomm = result[0][5]
    rowews = result[0][6]
    rowph = result[0][7]
    rowex = result[0][8]
    rowsports = result[0][9]
    rowld = result[0][10]

    print("rowhtnum:", rowhtnum)
    
    cursor.execute("SELECT row_number FROM ( SELECT ROW_NUMBER() OVER () AS row_number, * FROM my_table) AS numbered_rows WHERE htnum = ?", (rowhtnum,))
    row2 = cursor.fetchall()
    print(row2)    

    offsetrow = row2[0][0]
    print(offsetrow)    

# Check if the view already exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='view' AND name='RESULT_VIEW'")
    existing_view = cursor.fetchone()

# If the view exists, drop it
    if existing_view:
        cursor.execute("DROP VIEW RESULT_VIEW")

# Create the SQL query string with the desired limit value
    sql_query = f"CREATE VIEW RESULT_VIEW AS SELECT * FROM my_table LIMIT {offsetrow}"

# Execute the SQL query to create the view
    cursor.execute(sql_query)
    row3 = cursor.fetchall()
    print(row3)

# District Rank
# Use parameterized query to safely interpolate the string value
    sql_query = "SELECT COUNT(*) AS DistRank FROM RESULT_VIEW WHERE localdistrict = ?"
    cursor.execute(sql_query, (rowld,))
    row4 = cursor.fetchall()
    CalDistRank = row4[0][0]
    print("District Rank: ", CalDistRank)

# District Comm Rank
# Use parameterized query to safely interpolate the string value
    sql_query = "SELECT COUNT(*) AS DistRank FROM RESULT_VIEW WHERE localdistrict = ? AND community = ?"
    cursor.execute(sql_query, (rowld,rowcomm,))
    row4 = cursor.fetchall()
    CalDistCommRank = row4[0][0]
    print("District Community Rank: ", CalDistCommRank)


# District Comm Fem Rank
# Use parameterized query to safely interpolate the string value
    sql_query = """
        SELECT CASE
               WHEN gender = 'F' THEN COUNT(*)
               ELSE 'NA'
           END AS DistRank
        FROM RESULT_VIEW
     WHERE localdistrict = ? AND community = ? AND gender = ?
    """
    cursor.execute(sql_query, (rowld, rowcomm, rowgender,))
    row4 = cursor.fetchall()
    CalDistCommFemRank = row4[0][0]
    print("District Community Female Rank: ", CalDistCommFemRank)

# EWS District Rank
# Use parameterized query to safely interpolate the string value
    sql_query = """
        SELECT CASE
               WHEN ews = 'Yes' THEN COUNT(*)
               ELSE 'NA'
           END AS DistRank
        FROM RESULT_VIEW
        WHERE localdistrict = ? AND ews = ?
    """
    cursor.execute(sql_query, (rowld, rowews,))
    row4 = cursor.fetchall()
    CalDistEWSRank = row4[0][0]
    print("District EWS Rank: ", CalDistEWSRank)


# District Commm. EWS  Rank
# Use parameterized query to safely interpolate the string value
    sql_query = """
    SELECT CASE
               WHEN ews = 'Yes' THEN COUNT(*)
               ELSE 'NA'
           END AS DistRank
    FROM RESULT_VIEW
    WHERE localdistrict = ? AND community = ? AND ews = ?
    """
    cursor.execute(sql_query, (rowld, rowcomm, rowews,))
    row4 = cursor.fetchall()
    CalDistEWSCommRank = row4[0][0]
    print("District EWS Community Rank: ", CalDistEWSCommRank)


# PH District Rank
# Use parameterized query to safely interpolate the string value
    sql_query = """
        SELECT CASE
               WHEN PH = 'Yes' THEN COUNT(*)
               ELSE 'NA'
           END AS DistRank
        FROM RESULT_VIEW
    WHERE localdistrict = ? AND PH = ?
    """
    cursor.execute(sql_query, (rowld, rowph,))
    row4 = cursor.fetchall()
    CalDistPHRank = row4[0][0]
    print("District PH Rank: ", CalDistPHRank)


# PH District Comm Rank
# Use parameterized query to safely interpolate the string value
    sql_query = """
    SELECT CASE
               WHEN PH = 'Yes' THEN COUNT(*)
               ELSE 'NA'
           END AS DistRank
        FROM RESULT_VIEW
    WHERE localdistrict = ? AND community = ? AND PH = ?
    """
    cursor.execute(sql_query, (rowld, rowcomm, rowph,))
    row4 = cursor.fetchall()
    CalDistPHCommRank = row4[0][0]
    print("District PH Community Rank: ", CalDistPHCommRank)

# ExServicemen District Rank
# Use parameterized query to safely interpolate the string value
    sql_query = """
    SELECT CASE
               WHEN ExServicemen = 'Yes' THEN COUNT(*)
               ELSE 'NA'
           END AS DistRank
    FROM RESULT_VIEW
    WHERE localdistrict = ? AND ExServicemen = ?
    """
    cursor.execute(sql_query, (rowld, rowex,))
    row4 = cursor.fetchall()
    CalDistExServRank = row4[0][0]
    print("District ExServ Rank: ", CalDistExServRank)


# Exservicemen District Comm Rank
# Use parameterized query to safely interpolate the string value
    sql_query = """
    SELECT CASE
               WHEN ExServicemen = 'Yes' THEN COUNT(*)
               ELSE 'NA'
           END AS DistRank
    FROM RESULT_VIEW
    WHERE localdistrict = ? AND community = ? AND ExServicemen = ?
    """
    cursor.execute(sql_query, (rowld, rowcomm, rowex,))
    row4 = cursor.fetchall()
    CalDistExServCommRank = row4[0][0]
    print("District ExServ Comm Rank: ", CalDistExServCommRank)

# Sports District Rank
# Use parameterized query to safely interpolate the string value
    sql_query = """
    SELECT CASE
               WHEN Sports = 'SPORTS' THEN COUNT(*)
               ELSE 'NA'
           END AS DistRank
    FROM RESULT_VIEW
    WHERE localdistrict = ? AND Sports = ?
    """
    cursor.execute(sql_query, (rowld, rowsports,))
    row4 = cursor.fetchall()
    CalDistSportsRank = row4[0][0]
    print("District Sports Rank: ", CalDistSportsRank)


# Sports District Comm Rank
# Use parameterized query to safely interpolate the string value
    sql_query = """
    SELECT CASE
               WHEN Sports = 'SPORTS' THEN COUNT(*)
               ELSE 'NA'
           END AS DistRank
    FROM RESULT_VIEW
    WHERE localdistrict = ? AND community = ? AND Sports = ?
    """
    cursor.execute(sql_query, (rowld, rowcomm, rowsports,))
    row4 = cursor.fetchall()
    CalSportsCommRank = row4[0][0]
    print("District Sports Comm Rank: ", CalSportsCommRank)


# ------ end of calculation ----
# JSON DATA
    data = request.get_json()
    result = {
    "HallTicketNumber" : rowhtnum,
    "General Rank" : rowgenrank,
    "Marks" : rowmarks,
    "Gender" : rowgender,
    "Community" : rowcomm,
    "EWS" : rowews,
    "PH" : rowph,
    "Ex Servicemen" : rowex,
    "Sports" : rowsports,
    "Local District" : rowld,
    "District Rank" : CalDistRank,
    "District Community Rank" : CalDistCommRank,
    "District Community Female Rank" : CalDistCommFemRank,
    "District EWS Rank" : CalDistEWSRank,
    "District EWS Community Rank" : CalDistEWSCommRank,
    "District PH Rank" : CalDistPHRank,
    "District PH Community Rank" : CalDistPHCommRank,
    "District Ex Serv. Rank" : CalDistExServRank,
    "District Ex Serv. Community Rank" : CalDistExServCommRank,
    "District Sports Rank" : CalDistSportsRank,
    "District Sports Comm Rank" : CalSportsCommRank,
    }
    
    print(result)

    # Convert the result dictionary to JSON and return it
    # Convert the result dictionary to JSON
    #json_result = jsonify(result)

# Return the JSON result to the client
    return jsonify(result)
    
# Close the connection
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)

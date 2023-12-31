import sqlite3

import streamlit

con = sqlite3.connect("./test.sqlite")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS t(name, x)")


limit: int = streamlit.number_input(
    "limit", value=10, min_value=0, max_value=1000, step=1
)
res = cur.execute("SELECT name, x FROM t LIMIT ?", (limit,))
con.commit()
rows: list[tuple[str, int]] = res.fetchall()

# dummy
if not rows:
    streamlit.warning("dummy data")
    rows = [(chr(97 + i), i) for i in range(26)][:limit]

streamlit.write("## fetched table")
streamlit.dataframe(rows, use_container_width=True)

streamlit.write("## data editor")
updated_rows = streamlit.experimental_data_editor(rows, use_container_width=True)

streamlit.write("## line chart")
streamlit.line_chart([y for _, y in updated_rows])

# update
if streamlit.button("Update"):
    cur.execute("DELETE FROM t")
    cur.executemany("INSERT INTO t VALUES(?, ?)", updated_rows)
    con.commit()
    streamlit.balloons()

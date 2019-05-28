import pandas as pd
from mysql import get_mysql_conn

f = "file.csv"
m = get_mysql_conn()
c = m.cursor()
df = pd.read_csv(f, index_col=None)

for index, row in df.iterrows():
    domain = row[0]

    sql = """
    INSERT INTO domain_stats(domain) VALUES ('{}')
    """.format(domain)

    try:
        print(sql)
        c.execute(sql)
        m.commit()
    except Exception as e:
        print("{}".format(str(e)))
        m.rollback()

c.close()

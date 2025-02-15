import psycopg2

conn = psycopg2.connect("""
    host=logijuped.beget.app
    port=5432
    sslmode=disable
    dbname=default_db
    user=cloud_user
    password=P*fVl!Mg%T5D
    target_session_attrs=read-write
""")

# jdbc:postgresql://{host}[:{port}]/[{database}]
# postgresql://cloud_user:P*fVl!Mg%T5D@logijuped.beget.app:5432/default_db?sslmode=disable&target_session_attrs=read-write
#     password=P*fVl!Mg%T5D
q = conn.cursor()
q.execute('SELECT version()')

print(q.fetchone())

conn.close()

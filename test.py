import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('db\\blogs.db')
cur = conn.cursor()

#profile0 - email, desc, name
#profile1 - email, desc, name, command, HRnot
#profile2 - email, desc, name, command, all

#job0 - view
#job1 - create, close, HRnot
#job2 - create, close, all
cur.execute("INSERT INTO status (id, name, level_redact_profile, level_job) VALUES (?, ?, ?, ?)", (0, 'Programmer', 0, 0))
cur.execute("INSERT INTO status (id, name, level_redact_profile, level_job) VALUES (?, ?, ?, ?)", (1, 'Teamlid', 0, 0))
cur.execute("INSERT INTO status (id, name, level_redact_profile, level_job) VALUES (?, ?, ?, ?)", (2, 'HR', 1, 1))
cur.execute("INSERT INTO status (id, name, level_redact_profile, level_job) VALUES (?, ?, ?, ?)", (3, 'Director', 2, 2))
cur.execute("INSERT INTO status (id, name, level_redact_profile, level_job) VALUES (?, ?, ?, ?)", (-1, 'Administrator', 0, 0))
cur.execute("INSERT INTO commands (id, name, description) VALUES (?, ?, ?)", (0, 'NewUsersCommand', 'NewUsersCommand'))
cur.execute("INSERT INTO commands (id, name, description) VALUES (?, ?, ?)", (1, 'Administartion', 'Administration Command'))
cur.execute("INSERT INTO commands (id, name, description) VALUES (?, ?, ?)", (2, 'First command', 'DescFirst Command'))
cur.execute("INSERT INTO commands (id, name, description) VALUES (?, ?, ?)", (3, 'Second command', 'DescSecond Command'))

cur.execute("INSERT INTO users (id, name, description, hashed_password, email, status_id, command_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (0, "Jack", "DescJack", generate_password_hash("123"), "yandex1@mail.ru", 0, 2))
cur.execute("INSERT INTO users (id, name, description, hashed_password, email, status_id, command_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (1, "Bob", "DescBob", generate_password_hash("123"), "yandex2@mail.ru", 0, 3))
cur.execute("INSERT INTO users (id, name, description, hashed_password, email, status_id, command_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (2, "Edd", "DescEdd", generate_password_hash("123"), "yandex3@mail.ru", 1, 2))
cur.execute("INSERT INTO users (id, name, description, hashed_password, email, status_id, command_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (3, "Greg", "DescGreg", generate_password_hash("123"), "yandex4@mail.ru", 1, 3))
cur.execute("INSERT INTO users (id, name, description, hashed_password, email, status_id, command_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (4, "Sox", "DescSox", generate_password_hash("123"), "yandex5@mail.ru", 2, 2))
cur.execute("INSERT INTO users (id, name, description, hashed_password, email, status_id, command_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (5, "Lame", "DescLame", generate_password_hash("123"), "yandex6@mail.ru", 2, 3))
cur.execute("INSERT INTO users (id, name, description, hashed_password, email, status_id, command_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (6, "Jhon", "DescJhon", generate_password_hash("123"), "yandex7@mail.ru", 3, 1))
cur.execute("INSERT INTO users (id, name, description, hashed_password, email, status_id, command_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (7, "Max", "DescMax", generate_password_hash("123"), "yandex666@mail.ru", -1, 1))

cur.execute("INSERT INTO jobs (id, title, description, start_date, end_date, complete, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (0, "Job1", "DescJob1", "0-0-0", "1-1-1", False, 5))
cur.execute("INSERT INTO jobs (id, title, description, start_date, end_date, complete, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (1, "Job2", "DescJob2", "0-0-0", "1-1-1", False, 5))
cur.execute("INSERT INTO jobs (id, title, description, start_date, end_date, complete, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (2, "Job3", "DescJob3", "0-0-0", "1-1-1", False, 5))
cur.execute("INSERT INTO jobs (id, title, description, start_date, end_date, complete, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (3, "Job4", "DescJob4", "0-0-0", "1-1-1", False, 5))

conn.commit()
conn.close()

#print(post('http://127.0.0.1:5000/api/v2/users', json={'name':'Jack',
#                                                            'description':'DescJack',
#                                                            'email':"yandex1@mail.ru",
#                                                            'password':"123",
#                                                            'status.name':"Programmer",
#                                                            'command.name':"First Command"}).json())

#print(post('http://127.0.0.1:5000/api/v2/users', json={'name':'Bob',
#                                                            'description':'DescBob',
#                                                            'email':"yandex2@mail.ru",
#                                                            'password':"123",
#                                                            'status.name':"Programmer",
#                                                            'command.name':"Second Command"}).json())

#print(post('http://127.0.0.1:5000/api/v2/users', json={'name':'Max',
#                                                            'description':'DescMax',
#                                                            'email':"yandex3@mail.ru",
#                                                            'password':"123",
#                                                            'status.name':"Teamlid",
#                                                            'command.name':"First Command"}).json())

#print(post('http://127.0.0.1:5000/api/v2/users', json={'name':'Bred',
#                                                            'description':'DescBred',
#                                                            'email':"yandex4@mail.ru",
#                                                            'password':"123",
#                                                            'status.name':"Teamlid",
#                                                            'command.name':"Second Command"}).json())

#print(post('http://127.0.0.1:5000/api/v2/users', json={'name':'Greg',
#                                                            'description':'DescGreg',
#                                                            'email':"yandex5@mail.ru",
#                                                            'password':"123",
#                                                            'status.name':"HR",
#                                                            'command.name':"First Command"}).json())

#print(post('http://127.0.0.1:5000/api/v2/users', json={'name':'Jax',
#                                                            'description':'DescJax',
#                                                            'email':"yandex6@mail.ru",
#                                                            'password':"123",
#                                                            'status.name':"HR",
#                                                            'command.name':"Second Command"}).json())


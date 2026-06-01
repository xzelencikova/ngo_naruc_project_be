import sqlalchemy as sa


# ===== QUESTIONS QUERIES =====
def get_all_questions_query():
    return sa.text("""
                        SELECT * FROM questions ORDER BY id ASC
                   """)


def get_questions_by_category_query():
    return sa.text("""
                        SELECT * FROM questions WHERE category=:category
                   """)


def get_max_category_query():
    return sa.text("""SELECT MAX(category_order) FROM questions""")


def get_question_by_id_query():
    return sa.text("""SELECT * FROM questions WHERE id=:id""")


def delete_question_by_id_query():
    return sa.text("""DELETE FROM questions WHERE id=:id""")


def set_questions_valid_query():
    return sa.text("""
                        UPDATE questions
                        SET is_valid=:is_valid WHERE id in :questions
                    """).bindparams(sa.bindparam("questions", expanding=True))


def update_question_query():
    return sa.text("""
                        UPDATE questions
                        SET
                            category=:category, question=:question,
                            category_order=:category_order, icon=:icon, is_valid=:is_valid
                        WHERE id=:id
                    """)


def get_all_categories_query():
    return sa.text("""
                        SELECT DISTINCT category AS name, category_order, icon FROM questions
                        ORDER BY category_order
                    """)


# ===== CLIENTS QUERIES =====
def get_all_clients_query():
    return sa.text("""
                        SELECT 
                            c.id,
                            c.name,
                            c.surname,
                            c.registration_date,
                            c.contract_no,
                            c.active,
                            (SELECT COUNT(r.id) FROM ratings r WHERE c.id = r.client_id) as last_phase                      
                        FROM clients c
                        ORDER BY contract_no DESC
                   """)


def get_max_client_id():
    return sa.text("""SELECT MAX(id) AS id FROM clients""")


def set_client_active_status_query():
    return sa.text("""
                        UPDATE clients
                        SET active=:active
                        WHERE id IN :clients
                   """).bindparams(sa.bindparam("clients", expanding=True))


def get_client_by_id_query():
    return sa.text("""
                        SELECT
                            c.id,
                            c.name,
                            c.surname,
                            c.registration_date,
                            c.contract_no,
                            c.active,
                            (SELECT COUNT(r.id) FROM ratings r WHERE c.id = r.client_id) as last_phase                      
                        FROM clients c
                        WHERE id=:id""")


def update_client_query():
    return sa.text("""
                        UPDATE clients 
                        SET 
                            name=:name,
                            surname=:surname,
                            registration_date=:registration_date,
                            contract_no=:contract_no,
                            last_phase=:last_phase,
                            active=:active
                        WHERE id=:id
                   """)


def delete_client_by_id_query():
    return sa.text("""DELETE FROM clients WHERE id=:id""")


# ===== RATINGS QUERIES =====
def get_rating_by_id_query():
    return sa.text("""
                        SELECT cl.name || ' ' || cl.surname as client, r.* FROM ratings r
                        INNER JOIN clients cl ON cl.id = r.client_id
                        WHERE r.id=:id
                    """)


def get_rating_score_by_rating_id_query():
    return sa.text("""
                        SELECT
                            q.id as question_id, q.category, q.category_order, q.icon, q.question, qr.rating_id, qr.rating
                        FROM questions_ratings qr
                        LEFT JOIN questions q ON qr.question_id = q.id
                        WHERE qr.rating_id IN :rating_ids
                        ORDER BY q.category_order, q.id ASC 
                    """).bindparams(sa.bindparam("rating_ids", expanding=True))


def update_rating_phase_query():
    return sa.text("""
                        UPDATE ratings
                        SET phase = phase -  1
                        WHERE client_id=:client_id 
                            AND id > :id
                    """)


def update_rating_by_id_query():
    return sa.text("""
                        UPDATE ratings
                        SET last_update_by=:last_update_by, last_update_date=:last_update_date
                        WHERE id=:id
                    """)


def delete_rating_info_by_id_query():
    return sa.text("""DELETE FROM ratings WHERE id=:id""")


def delete_ratings_score_by_rating_id_query():
    return sa.text("""DELETE FROM questions_ratings WHERE rating_id=:rating_id""")


def delete_ratings_score_by_question_id():
    return sa.text("""DELETE FROM questions_ratings WHERE question_id=:id""")


def delete_ratings_by_client_query():
    return sa.text("""DELETE FROM ratings WHERE client_id=:id""")


def delete_ratings_score_for_client_query():
    return sa.text("""
                        DELETE FROM questions_ratings qr
                        WHERE qr.rating_id IN (
                            SELECT r.id FROM ratings r WHERE r.client_id=:client_id
                            )
                        """)


def get_ratings_for_client_query():
    return sa.text("""
                        SELECT cl.name || ' ' || cl.surname as client, r.* FROM ratings r
                        INNER JOIN clients cl ON cl.id = r.client_id
                        WHERE r.client_id=:client_id
                    """)


# ===== USERS QUERIES =====
def get_all_users_query():
    return sa.text(
        """SELECT id, email, name, surname, role FROM users ORDER BY surname, name ASC"""
    )


def get_user_by_id_query():
    return sa.text("""SELECT * FROM users WHERE id=:id""")


def get_user_by_email_query():
    return sa.text("""SELECT * FROM users WHERE email=:email""")


def update_user_password_query():
    return sa.text("""
                        UPDATE users
                        SET password=:password
                        WHERE id=:id
                    """)


def update_user_query():
    return sa.text("""
                        UPDATE users
                        SET name=:name, surname=:surname, role=:role, email=:email
                        WHERE id=:id
                    """)


def delete_user_by_id_query():
    return sa.text("""DELETE FROM users WHERE id=:id""")

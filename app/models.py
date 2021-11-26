from datetime import datetime
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.username}>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<Post {self.body}>"


class Employers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    type = db.Column(db.String(30))
    site_url = db.Column(db.String(100))
    description = db.Column(db.Text)
    open_vacancies = db.Column(db.Integer)
    trusted = db.Column(db.Boolean)
    area = db.Column(db.String(40))
    is_it = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Employers {self.id}>"


class Vacs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(50))
    salary_from = db.Column(db.Float)
    salary_to = db.Column(db.Float)
    salary_av = db.Column(db.Float)
    experience = db.Column(db.String(20))
    schedule = db.Column(db.String(15))
    employment = db.Column(db.String(15))
    description = db.Column(db.Text)
    key_skills = db.Column(db.Text)
    employer = db.Column(db.Integer, db.ForeignKey("employers.id"))
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)
    accept_temporary = db.Column(db.Boolean)
    archived = db.Column(db.Boolean)
    archived_at = db.Column(db.DateTime)
    it_specialization = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Vacs {self.id}>"


class Industries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employers_id = db.Column(db.Integer, db.ForeignKey("employers.id"))
    industry = db.Column(db.String(150))

    def __repr__(self):
        return f"<Industries {self.employers_id}>"


class Proffs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proff = db.Column(db.String(40))

    def __repr__(self):
        return f"<Proffs {self.id}>"


class KeySkills(db.Model):
    variant = db.Column(db.Text, primary_key=True)
    origin = db.Column(db.String(50))

    def __repr__(self):
        return f"<KeySkills {self.origin}>"


class VacsProff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vac_id = db.Column(db.Integer, db.ForeignKey("vacs.id"))
    proff_id = db.Column(db.Integer, db.ForeignKey("proffs.id"))

    def __repr__(self):
        return f"<VacsProff {self.vac_id}, {self.proff_id}>"


class VacsSkills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vac_id = db.Column(db.Integer, db.ForeignKey("vacs.id"))
    skill_id = db.Column(db.Integer, db.ForeignKey("key_skills.id"))

    def __repr__(self):
        return f"<VacsSkills {self.vac_id}, {self.skill_id}>"


class KeyskillsDict(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    variant = db.Column(db.String(50), nullable=False)
    origin = db.Column(db.String(50), nullable=False)
    origin = db.Column(db.ForeignKey("key_skills.id"))

    def __repr__(self):
        return f"<KeyskillsDict {self.variant}>"


class ProffStat(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    proff_id = db.Column(db.Integer, db.ForeignKey("proffs.id"))
    skill_id = db.Column(db.Integer, db.ForeignKey("key_skills.id"))
    freq = db.Column(db.Float)
    check_time = db.Column(db.DateTime)

    def __repr__(self):
        return f"<ProffStat {self.proff}, {self.skill}>"


class ProffLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proff1_id = db.Column(db.Integer, db.ForeignKey("proffs.id"))
    proff2_id = db.Column(db.Integer, db.ForeignKey("proffs.id"))
    similarity = db.Column(db.Float)
    skill_id = db.Column(db.Integer, db.ForeignKey("key_skills.id"))
    skill_score = db.Column(db.Float)
    skill_pid1 = db.Column(db.Float)
    skill_pid2 = db.Column(db.Float)

    def __repr__(self):
        return f"<ProffLink {self.proff1_id}, {self.proff1_i2}, {self.skill_id}>"


class ProffsList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proff1 = db.Column(db.String(40), nullable=False)
    proff2 = db.Column(db.String(40), nullable=False)
    similarity = db.Column(db.Float)
    skills = db.Column(db.String(160), nullable=False)

    def __repr__(self):
        return f"<ProffsList {self.proff1}, {self.proff2}, {self.similarity}>"

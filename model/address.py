from database import db
from datetime import datetime
 
class Address(db.Model):
    __tablename__ = "addresses"
 
    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    full_name    = db.Column(db.String(120), nullable=False)
    phone        = db.Column(db.String(20), nullable=False)
    street       = db.Column(db.String(255), nullable=False)
    district     = db.Column(db.String(100), nullable=False)
    city         = db.Column(db.String(100), nullable=False)
    postal_code  = db.Column(db.String(10), nullable=False)
    is_default   = db.Column(db.Boolean, default=False)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at   = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
 
    user = db.relationship("User", backref="addresses")
 
    def __repr__(self):
        return f"<Address {self.full_name} - {self.city}>"
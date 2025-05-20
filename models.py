from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tarea(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  titulo = db.Column(db.String(100), nullable=False)
  descripcion = db.Column(db.String(200))
  completada = db.Column(db.Boolean, default=False)

def __repr__(self):
  return f"<Tarea {self.titulo}>"
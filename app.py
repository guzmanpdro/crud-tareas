from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import Tarea, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tareas.db'
db.init_app(app)

with app.app_context():
  try:
    db.create_all()
    print("Intentando crear las tablas de la base de datos al inicio de la aplicación (sin __main__).")
  except Exception as e:
    print(f"Error al intentar crear las tablas al inicio (sin __main__): {e}")

# Ruta para obtener todas las tareas (READ)
@app.route('/tareas', methods=['GET'])
def obtener_tareas():
  tareas = Tarea.query.all()
  tareas_lista = []
  for tarea in tareas:
    tarea_data = {
      'id': tarea.id,
      'titulo': tarea.titulo,
      'descripcion': tarea.descripcion,
      'completada': tarea.completada
    }
    tareas_lista.append(tarea_data)
  return jsonify(tareas_lista)

# Ruta para obtener una tarea específica por su ID (READ)
@app.route('/tareas/<int:tarea_id>', methods=['GET'])
def obtener_tarea(tarea_id):
  tarea = Tarea.query.get_or_404(tarea_id)
  tarea_data = {
    'id': tarea.id,
    'titulo': tarea.titulo,
    'descripcion': tarea.descripcion,
    'completada': tarea.completada
  }
  return jsonify(tarea_data)

# Ruta para crear una nueva tarea (CREATE)
@app.route('/tareas', methods=['POST'])
def crear_tarea():
  data = request.get_json()
  if 'titulo' not in data or not data['titulo']:
    return jsonify({'mensaje': 'El título es obligatorio'}), 400
  nueva_tarea = Tarea(titulo=data['titulo'], descripcion=data.get('descripcion', ''), completada=data.get('completada', False))
  db.session.add(nueva_tarea)
  db.session.commit()
  tarea_data = {
    'id': nueva_tarea.id,
    'titulo': nueva_tarea.titulo,
    'descripcion': nueva_tarea.descripcion,
    'completada': nueva_tarea.completada
  }
  return jsonify(tarea_data), 201

# Ruta para actualizar una tarea existente (UPDATE)
@app.route('/tareas/<int:tarea_id>', methods=['PUT'])
def actualizar_tarea(tarea_id):
  tarea = Tarea.query.get_or_404(tarea_id)
  data = request.get_json()
  tarea.titulo = data.get('titulo', tarea.titulo)
  tarea.descripcion = data.get('descripcion', tarea.descripcion)
  tarea.completada = data.get('completada', tarea.completada)
  db.session.commit()
  tarea_data = {
    'id': tarea.id,
    'titulo': tarea.titulo,
    'descripcion': tarea.descripcion,
    'completada': tarea.completada
  }
  return jsonify(tarea_data)

# Ruta para eliminar una tarea (DELETE)
@app.route('/tareas/<int:tarea_id>', methods=['DELETE'])
def eliminar_tarea(tarea_id):
  tarea = Tarea.query.get_or_404(tarea_id)
  db.session.delete(tarea)
  db.session.commit()
  return jsonify({
    'mensaje': 'Tarea eliminada correctamente'
  })

if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(debug=True)
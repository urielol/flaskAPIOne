from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)

db = pymysql.connect('localhost','root','password','grumpyturtle_2_alpha')

@app.route('/api/v1/', methods=['GET'])
def proyectos_obtener():
    cursor=db.cursor()
    user_id = request.json['usuario_id']
    cursor.execute("SELECT * FROM usuarios JOIN roles ON roles.id=usuarios.roles_id WHERE usuarios.id = %s",user_id)
    user = cursor.fetchall()

    if ('Propietario' or 'Analista') in str(user[0]):
        
        data=request.json
        cursor.execute("SELECT * FROM proyectos WHERE usuarios_id= %s",data['usuario_id'])
        data = cursor.fetchall()
        return jsonify({"data":data})
    else:
        return jsonify({"error":"el usuario no tiene el rol de Propietario"})

@app.route('/api/v1/',methods=['POST'])
def proyectos_crear():

    cursor=db.cursor()
    user_id = request.json['usuario_id']
    cursor.execute("SELECT * FROM usuarios JOIN roles ON roles.id=usuarios.roles_id WHERE usuarios.id = %s",user_id)
    user = cursor.fetchall()

    if 'Propietario'in user[0]:
        data=request.json
        cursor.execute('INSERT INTO proyectos (nombre,descripcion,usuarios_id,fecha_inicio,dias_laborales_semana,tamano_sprint,hora_inicio) VALUES (%s,%s,%s,%s,%s,%s,%s)',(data['nombre_proyecto'],data['descripcion'],data['usuario_id'],data['fecha_inicio'],data['dias_laborales_semana'],data['tamano_sprint'],data['hora_inicio']))
        db.commit()
        return jsonify({"status":"recibed"})
    else:
        return jsonify({"error":"el usuario no tiene el rol de Propietario"})


@app.route('/api/v1/',methods=['PUT'])
def proyectos_editar():

    cursor=db.cursor()
    user_id = request.json['usuario_id']
    cursor.execute("SELECT * FROM usuarios JOIN roles ON roles.id=usuarios.roles_id WHERE usuarios.id = %s",user_id)
    user = cursor.fetchall()

    if 'Propietario'in user[0]:

        data=request.json
        cursor.execute('UPDATE proyectos SET nombre=%s,descripcion=%s,fecha_inicio=%s,dias_laborales_semana=%s,tamano_sprint=%s,hora_inicio=%s WHERE usuarios_id = %s and id=%s ',(data['nombre_proyecto'],data['descripcion'],data['fecha_inicio'],data['dias_laborales_semana'],data['tamano_sprint'],data['hora_inicio'],data['usuario_id'],data['proyecto_id']))
        db.commit()

        return jsonify({"status":"actualizado"})
    else:
        return jsonify({"error":"el usuario no tiene el rol de Propietario"})




@app.route('/api/v1/archivar', methods=['PUT'])
def proyectos_archivar():

    cursor=db.cursor()
    user_id = request.json['usuario_id']
    cursor.execute("SELECT * FROM usuarios JOIN roles ON roles.id=usuarios.roles_id WHERE usuarios.id = %s",user_id)
    user = cursor.fetchall()

    if 'Propietario'in user[0]:

        data=request.json
        cursor.execute('UPDATE proyectos SET activo=%s WHERE usuarios_id = %s and id=%s ',(data['estado'],data['usuario_id'],data['proyecto_id']))
        db.commit()

        return jsonify({"status":"archivado"})

    else:
        return jsonify({"error":"el usuario no tiene el rol de Propietario"})


@app.route('/api/v1/',methods=['DELETE'])
def proyectos_eliminar():

    cursor=db.cursor()
    user_id = request.json['usuario_id']
    cursor.execute("SELECT * FROM usuarios JOIN roles ON roles.id=usuarios.roles_id WHERE usuarios.id = %s",user_id)
    user = cursor.fetchall()

    if 'Propietario'in user[0]:

        data=request.json
        cursor.execute('UPDATE proyectos SET activo=%s WHERE usuarios_id = %s and id=%s ',(data['estado'],data['usuario_id'],data['proyecto_id']))
        db.commit()

        return jsonify({"status":"desactivado"})

    else:
        return jsonify({"error":"el usuario no tiene el rol de Propietario"})

    return jsonify({"data":request.json})



if __name__ == '__main__':
    app.run(debug=True, port=3000)
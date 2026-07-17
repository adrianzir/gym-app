import json
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# 1. Primero, todas tus funciones de lógica (sin cambios)
def guardar_rutinas(rutinas):
    with open("rutinas.json", "w") as archivo:
        json.dump(rutinas, archivo, indent=4)

def cargar_rutinas():
    try:
        with open("rutinas.json", "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []

def agregar_rutina(rutinas, tipo_rutina, ejercicios):
    nueva_rutina = {"tipo_rutina": tipo_rutina, "ejercicios": ejercicios}
    rutinas.append(nueva_rutina)

def eliminar_rutina(rutinas, indice):
    rutinas.pop(indice)

def actualizar_ejercicios_rutina(rutinas, indice, nuevo_tipo_rutina, nuevos_ejercicios):
    rutinas[indice]["tipo_rutina"] = nuevo_tipo_rutina
    rutinas[indice]["ejercicios"] = nuevos_ejercicios

# 2. Luego, todas las rutas (@app.route), una sola vez cada una
@app.route("/")
@app.route("/inicio")
def inicio():
    return render_template("inicio.html")

@app.route("/rutinas")
def ver_rutinas():
    rutinas = cargar_rutinas()
    return render_template("rutinas.html", rutinas=rutinas)

@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        tipo_rutina = request.form["tipo_rutina"]

        nombres = request.form.getlist("nombre_ejercicio")
        series = request.form.getlist("series_ejercicio")
        repeticiones = request.form.getlist("repes_ejercicio")

        lista_ejercicios = []
        for i in range(len(nombres)):
            ejercicio = {
                "nombre": nombres[i],
                "series": int(series[i]),
                "repeticiones": int(repeticiones[i])
            }
            lista_ejercicios.append(ejercicio)

        rutinas = cargar_rutinas()
        agregar_rutina(rutinas, tipo_rutina, lista_ejercicios)
        guardar_rutinas(rutinas)

        return redirect("/inicio")

    return render_template("agregar.html")

@app.route("/eliminar/<int:indice>", methods=["POST"])
def eliminar(indice):
    rutinas = cargar_rutinas()
    eliminar_rutina(rutinas, indice)
    guardar_rutinas(rutinas)
    return redirect("/rutinas")

@app.route("/editar/<int:indice>", methods=["GET", "POST"])
def editar(indice):
    rutinas = cargar_rutinas()

    if request.method == "POST":
        nuevo_tipo_rutina = request.form["nuevo_tipo_rutina"]
        nombres = request.form.getlist("nombre_ejercicio")
        series = request.form.getlist("series_ejercicio")
        repeticiones = request.form.getlist("repes_ejercicio")

        nuevos_ejercicios = []
        for i in range(len(nombres)):
            nuevos_ejercicios.append({
                "nombre": nombres[i],
                "series": int(series[i]),
                "repeticiones": int(repeticiones[i])
            })

        actualizar_ejercicios_rutina(rutinas, indice, nuevo_tipo_rutina, nuevos_ejercicios)
        guardar_rutinas(rutinas)

        return redirect("/rutinas")

    rutina_actual = rutinas[indice]
    return render_template("editar.html", indice=indice, tipo_rutina=rutina_actual["tipo_rutina"], ejercicios=rutina_actual["ejercicios"])

# 3. Al final, el arranque del servidor
if __name__ == "__main__":
    app.run(debug=True)
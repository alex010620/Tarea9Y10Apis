import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app= FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#conexion = sqlite3.connect('bd')
#cursor = conexion.cursor()
#sql="CREATE TABLE venta (idVenta INTEGER NOT NULL,idCliente INTEGER NOT NULL,codigo TEXT NOT NULL,nombre TEXT NOT NULL,precio TEXT NOT NULL,cantidad TEXT NOT NULL, precioTotal INTEGER NOT NULL,PRIMARY KEY(idVenta AUTOINCREMENT));"
#sql = "create table producto(codigo varchar(20) not null, nombre varchar(100) not null, precio varchar(20) not null, cantidad varchar(20) not null);"
#cursor.execute(sql)
#conexion.commit()


@app.get("/api/crear/{cedula}/{nombre}/{telefono}")
def crear(cedula:str,nombre:str, telefono:str):
    try:
        conexion = sqlite3.connect('bd')
        cursor = conexion.cursor()
        sql = "insert into cliente(cedula,nombre,telefono) values('"+cedula+"','"+nombre+"','"+telefono+"');"
        cursor.execute(sql)
        conexion.commit()
        return {"true":"Se guardar el registro"}
    except :
        return {"false":"No se pudieron guardar los datos"}


@app.get("/api/selectName")
def selectName():
    try:
        lista=[]
        conexion = sqlite3.connect('bd')
        cursor = conexion.cursor()
        cursor.execute("select nombre from cliente")
        content= cursor.fetchall()
        conexion.commit()
        for i in content:
            lista.append({"nombre":i[0]})
        return lista
    except :
        return {"false":"No se pudieron estraer los datos"}


@app.get("/api/producto/{codigo}/{nombre}/{precio}/{cantidad}")
def producto(codigo:str,nombre:str, precio:str, cantidad:str):
    try:
        conexion = sqlite3.connect('bd')
        cursor = conexion.cursor()
        sql = "insert into producto(codigo,nombre,precio,cantidad) values('"+codigo+"','"+nombre+"','"+precio+"','"+cantidad+"');"
        cursor.execute(sql)
        conexion.commit()
        return {"true":"Se guardar el registro"}
    except :
        return {"false":"No se pudieron guardar los datos"}

@app.get("/api/selectProducto/{codigo}")
def selectProducto(codigo:str):
    try:
        conexion = sqlite3.connect('bd')
        cursor = conexion.cursor()
        cursor.execute("select codigo, nombre, precio, cantidad from producto where codigo = '"+codigo+"'")
        content= cursor.fetchall()
        conexion.commit()
        for i in content:
            return {"nombre":i[1], "precio":i[2],"cantidad":i[3]}
    except :
        return {"false":"No se pudieron estraer los datos"}

@app.get("/api/selectCodigo")
def selectCodigo():
    try:
        lista=[]
        conexion = sqlite3.connect('bd')
        cursor = conexion.cursor()
        cursor.execute("select codigo,cantidad from producto")
        content= cursor.fetchall()
        conexion.commit()
        for i in content:
            lista.append({"codigo":i[0],"cantidad":i[1]})
        return lista
    except :
        return {"false":"No se pudieron estraer los datos"}


@app.get("/api/selectCliente/{Nombre}")
def selectCliente(Nombre:str):
    try:
        conexion = sqlite3.connect('bd')
        cursor = conexion.cursor()
        cursor.execute("select idCliente, cedula, nombre, telefono from cliente where cedula = '"+Nombre+"'")
        content= cursor.fetchall()
        conexion.commit()
        for i in content:
            return {"idCliente":i[0], "cedula":i[1],"nombre":i[2],"telefono":i[3]}
    except :
        return {"false":"No se pudieron estraer los datos"}

@app.get("/api/venta/{idCliente}/{codigo}/{nombre}/{precio}/{cantidad}/{precioTotal}/{itebis}/{total}")
def venta(idCliente:int,codigo:str,nombre:str,precio:str,cantidad:str,precioTotal:int,itebis:float,total:float):
    try:
        conexion = sqlite3.connect('bd')
        cursor = conexion.cursor()
        sql = "INSERT INTO venta(idCliente,codigo,nombre,precio,cantidad,precioTotal,itebis,total) VALUES("+str(idCliente)+",'"+codigo+"','"+nombre+"','"+precio+"','"+cantidad+"',"+str(precioTotal)+","+str(itebis)+","+str(total)+");"
        cursor.execute(sql)
        conexion.commit()
        return {"true":"Se guardo el registro"}
    except TypeError:
        return {"false":"No se pudieron guardar los datos"}


@app.get("/api/selectTotal/{idCliente}")
def selectTotal(idCliente:str):
    try:
        conexion = sqlite3.connect('bd')
        cursor = conexion.cursor()
        cursor.execute("SELECT SUM(precioTotal) as Totales, SUM(itebis) as itebis, SUM(total) as total FROM venta WHERE idCliente = "+idCliente+"")
        content= cursor.fetchall()
        conexion.commit()
        for i in content:
            return {"subtotal":i[0], "ITEBIS":i[1],"total":i[2]}
    except :
        return {"false":"No se pudieron estraer los datos"}

@app.get("/api/updateTotal/{cantidadR}/{idProducto}")
def updateTotal(cantidadR:str, idProducto):
    try:
        conexion = sqlite3.connect('bd')
        cursor = conexion.cursor()
        cursor.execute("UPDATE producto SET cantidad='"+cantidadR+"' WHERE codigo = "+idProducto+"")
        conexion.commit()
        return {True:"Se reducio la cantidad"}
    except :
        return {"false":"No existe el producto"}

@app.get("/api/updateCantidad/{cantidadR}/{idProducto}")
def updateCantidad(cantidadR:str, idProducto):
    try:
        conexion = sqlite3.connect('bd')
        cursor = conexion.cursor()
        cursor.execute("UPDATE producto SET cantidad='"+cantidadR+"' WHERE codigo = "+idProducto+"")
        conexion.commit()
        return {"true":"Se aumento la cantidad"}
    except :
        return {"false":"No existe el producto"}

@app.get("/api/factura/{idCliente}/{nombre}/{rnc}/{telefono}/{descripcion}/{fecha}/{subtotal}/{itebis}/{total}")
def factura(idCliente:str,nombre:str,rnc:str,telefono:str,descripcion:str,fecha:str,subtotal:int,itebis:float,total:float):
    try:
        conexion = sqlite3.connect('bd')
        cursor = conexion.cursor()
        factura=(idCliente,nombre,rnc,telefono,descripcion,fecha,subtotal,itebis,total)
        sql = "INSERT INTO factura(idCliente,nombre,rnc,telefono,descripcion,fecha,subtotal,itebis,total) VALUES(?,?,?,?,?,?,?,?,?);"
        cursor.execute(sql,factura)
        conexion.commit()
        return {"true":"Se guardo el registro"}
    except TypeError:
        return {"false":"No se pudieron guardar los datos"}


@app.get("/api/selectFactura")
def selectFactura():
    try:
        lista=[]
        conexion = sqlite3.connect('bd')
        cursor = conexion.cursor()
        cursor.execute("select idFactura, idCliente, nombre, fecha  from factura")
        content= cursor.fetchall()
        conexion.commit()
        for i in content:
            lista.append({"idFactura":i[0],"idCliente":i[1],"nombre":i[2],"fecha":i[3]})
        return lista
    except :
        return {"false":"No se pudieron estraer los datos"}


@app.get("/api/selectFacturaProducto/{idFactura}")
def selectFacturaProducto(idFactura:int):
    conexion = sqlite3.connect('bd')
    cursor = conexion.cursor()
    cursor.execute("select nombre, rnc, descripcion, fecha, total ,telefono from factura WHERE idFactura = "+str(idFactura)+" ")
    content= cursor.fetchall()
    conexion.commit()
    for i in content:
        return {"nombre":i[0],"rnc":i[1],"descripcion":i[2],"fecha":i[3],"total":i[4],"telefono":i[5]}


@app.get("/api/selectFacturaventa/{idCliente}")
def selectFacturaventa(idCliente:int):
    lista=[]
    conexion = sqlite3.connect('bd')
    cursor = conexion.cursor()
    cursor.execute("select codigo,nombre,precio,cantidad from venta WHERE idCliente = "+str(idCliente)+" ")
    content= cursor.fetchall()
    conexion.commit()
    for i in content:
        lista.append( {"codigo":i[0],"nombre":i[1],"precio":i[2],"cantidad":i[3]})
    return lista

@app.get("/api/selectProd")
def selectProd():
    lista=[]
    conexion = sqlite3.connect('bd')
    cursor = conexion.cursor()
    cursor.execute("select codigo,nombre,cantidad from producto")
    content= cursor.fetchall()
    conexion.commit()
    for i in content:
        lista.append( {"codigo":i[0],"nombre":i[1],"cantidad":i[2]})
    return lista

@app.get("/api/Eliminarfactura/{idCliente}")
def Eliminarfactura(idCliente:str):
    try:
        conexion = sqlite3.connect('bd')
        cursor = conexion.cursor()
        cursor2 = conexion.cursor()
        sql = "DELETE FROM venta WHERE idCliente = '"+idCliente+"'"
        cursor.execute(sql)
        sql2 = "DELETE FROM factura WHERE idCliente = '"+idCliente+"'"
        cursor2.execute(sql2)
        conexion.commit()
        return {"true":"Se elimino la factura"}
    except TypeError:
        return {"false":"No se pudo eliminar la factura."}
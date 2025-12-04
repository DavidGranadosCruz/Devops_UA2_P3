from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import json

from .models import Producto


def inicio(request):
    return JsonResponse({"message": "Me encanta Devops!!"})


@csrf_exempt
def crear_producto(request):
    """
    Crea un producto a partir de un JSON enviado por POST.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Metodo no permitido"}, status=405)

    try:
        datos = json.loads(request.body.decode("utf-8"))
        nombre = datos.get("nombre")
        precio = datos.get("precio")
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON invalido"}, status=400)

    if not nombre or precio is None:
        return JsonResponse({"error": "Faltan datos"}, status=400)

    producto = Producto.objects.create(nombre=nombre, precio=precio)
    return JsonResponse(
        {"id": producto.id, "nombre": producto.nombre, "precio": str(producto.precio)},
        status=201
    )


def detalle_producto(request, producto_id):
    """
    Devuelve la informacion de un producto por su ID.
    """
    try:
        producto = Producto.objects.get(id=producto_id)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Producto no encontrado"}, status=404)

    return JsonResponse({
        "id": producto.id,
        "nombre": producto.nombre,
        "precio": str(producto.precio),
    })

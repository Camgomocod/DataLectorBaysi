import re

text = "Ximena Victoria G.Ferulic C Serum Endocare - m"
text = text.replace(".", "")
print(text)

match = re.search(r"(.*?)([.])([A-Z])(.*)", text)

if match:
  nombre_persona = match.group(1)
  nombre_producto = match.group(3)

  print(f"Nombre: {nombre_persona}")
  print(f"Producto: {nombre_producto}")
else:
  print("No se encontró el patrón")

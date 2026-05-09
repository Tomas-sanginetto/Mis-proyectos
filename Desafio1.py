def imprimir_tabla(tabla, titulo):
    """Imprime la tabla de posiciones con un título específico.

    Args:
        titulo (str): Título de la tabla (Provisoria o Final).
        tabla (list): Lista ordenada de tuplas (nombre, estadísticas).
    """
    print(f"\n{'='*10} {titulo} {'='*10}")
    print(f"{' POS':<5} | {'EQUIPO':<15} | {'PTS':<4} | {'GF':<4} | {'GC':<4} | {'DG':<3}")
    print("-" * 45)
    
    for i, (equipo, datos) in enumerate(tabla, 1):
        dg = datos["gf"] - datos["gc"]
        print(f" {i:<4} | {equipo:<15} | {datos['pts']:<4} | {datos['gf']:<4} | {datos['gc']:<4} | {dg:<3}")
    print("-" * 45)

def registrar_equipo(equipos, equipo):
    """Inicializa las estadísticas de un equipo si no existe en el diccionario.

    Args:
        equipos (dict): Diccionario de equipos.
        equipo (str): Nombre del equipo a registrar.
    """
    if equipo not in equipos:
        equipos[equipo] = {"pts": 0, "pj": 0, "gf": 0, "gc": 0}

def validar_equipo_clasificado(equipos_validos_map, nombre: str) -> str:
    """Valida que el nombre ingresado pertenezca a la lista de países permitidos.

    Args:
        equipos_validos_map (dict): map casefold(nombre) -> nombre canónico.
        nombre (str): nombre ingresado.

    Returns:
        str: nombre canónico si es válido.

    Raises:
        ValueError: si el nombre no pertenece a la lista válida.
    """
    clave = nombre.casefold()
    if clave not in equipos_validos_map:
        raise ValueError
    canónico = equipos_validos_map[clave]
    return canónico


def crear_equipos_validos_mundial_2026():
    # Lista canónica (según consigna) en el idioma y tildes provistas.
    # Nota: se valida con casefold(), pero devolvemos el nombre canónico.
    paises = [
        "Canada",
        "Estados Unidos",
        "Mexico",
        "Japon",
        "Iran",
        "Uzbekistan",
        "Corea del Sur",
        "Jordania",
        "Australia",
        "Argentina",
        "Ecuador",
        "Brasil",
        "Nueva Zelandia",
        "Marruecos",
        "Tunez",
        "Colombia",
        "Paraguay",
        "Uruguay",
        "Egipto",
        "Argelia",
        "Ghana",
        "Cabo Verde",
        "Sudafrica",
        "Qatar",
        "Inglaterra",
        "Costa de Marfil",
        "Senegal",
        "Arabia Saudita",
        "Francia",
        "Portugal",
        "Noruega",
        "Croacia",
        "Alemania",
        "Paises Bajos",
        "Suiza",
        "Escocia",
        "España",
        "Austria",
        "Belgica",
        "Panamá",
        "Curazao",
        "Haiti",
        "Suecia",
        "Turquia",
        "Republica Checa",
        "Bosnia y Herzegovina",
        "Republica del Congo",
        "Irak",
    ]
    return {p.casefold(): p for p in paises}


def procesar_partido(equipos, local, visitante, gl, gv):
    """Actualiza puntos y goles de dos equipos tras un partido.

    Args:
        equipos (dict): Diccionario con datos de los equipos.
        local (str): Nombre del equipo local.
        visitante (str): Nombre del equipo visitante.
        gl (int): Goles del local.
        gv (int): Goles del visitante.
    """
    equipos[local]["pj"] += 1
    equipos[visitante]["pj"] += 1
    equipos[local]["gf"] += gl
    equipos[local]["gc"] += gv
    equipos[visitante]["gf"] += gv
    equipos[visitante]["gc"] += gl
    if gl > gv:
        equipos[local]["pts"] += 3
    elif gl < gv:
        equipos[visitante]["pts"] += 3
    else:
        equipos[local]["pts"] += 1
        equipos[visitante]["pts"] += 1


def ordenar_tabla(equipos):
    """Ordena los equipos según criterios FIFA: Puntos, DG, GF y Alfabético.

    Args:
        equipos (dict): Diccionario de equipos.

    Returns:
        list: Lista de tuplas (nombre, datos) ordenada.
    """
    tabla = list(equipos.items())
    tabla.sort(key=lambda x: (-x[1]["pts"], -(x[1]["gf"] - x[1]["gc"]), -x[1]["gf"], x[0]))
    return tabla

def main():
    """Función principal: lee los partidos desde la entrada estándar y muestra la tabla."""
    equipos = {}
    
    print("=" * 50)
    print("  SISTEMA DE GESTIÓN FIFA - COPA MUNDIAL 2026")
    print("=" * 50)
    print("Instrucciones: Ingrese los 6 partidos del grupo.")
    print("Formato: EquipoLocal EquipoVisitante GolesL GolesV")
    print("(Ejemplo: Argentina Francia 2 1)")
    print("-" * 50)

    # === VALIDACIÓN DE PAÍSES (MUNDIAL 2026) ===
    equipos_validos_map = crear_equipos_validos_mundial_2026()

    # Cada grupo tiene 4 equipos y EXACTAMENTE 6 partidos (3 por equipo).
    # Formato: 4 equipos -> 6 partidos únicos (todos contra todos una vez).
    total_partidos = 6

    # RESTRICCIÓN: no repetir enfrentamientos en la misma fase de grupos.
    # Guardamos parejas canónicas (min, max en casefold) para que sea independiente del orden.
    enfrentamientos_jugados = set() 

    for i in range(total_partidos):
        # Mostrar encabezado de fecha cada 2 partidos
        if i % 2 == 0:
            nro_fecha = (i // 2) + 1
            print(f"\n--- FECHA {nro_fecha} ---")
        # Bucle de validación para el partido actual
        while True:
            try:
                entrada = input(f" Partido {i + 1} > ").strip()
                
                if not entrada:
                    print("Error: La entrada no puede estar vacía.")
                    continue
                    
                linea = entrada.split()
                
                if len(linea) != 4:
                    print("Error: Debe ingresar 4 datos (Local, Visitante, GolesL, GolesV).")
                    continue
                
                local = linea[0]
                visitante = linea[1]
                gl = int(linea[2])
                gv = int(linea[3])

                # Validación de países clasificados al Mundial 2026 (48 permitidos)
                try:
                    local = validar_equipo_clasificado(equipos_validos_map, local)
                    visitante = validar_equipo_clasificado(equipos_validos_map, visitante)
                except ValueError:
                    print("Error, ingrese equipos clasificados al mundial FIFA 2026, intentelo de nuevo")
                    continue

                # Para evitar que un mismo equipo entre con otro nombre (por ejemplo,
                # si hubiera espacios raros), lo almacenamos canónico por la validación.
                # (No contamos la iteración fallida, solo reintentamos el mismo partido.)

                if local.casefold() == visitante.casefold():
                    print("Error: Un equipo no puede jugar contra sí mismo, ingreselo correctamnente.")
                    continue

                # RESTRICCIÓN: no repetir enfrentamientos en la misma fase de grupos.
                # Usamos casefold() para comparar ignorando mayúsc/minúsc y normalizamos el orden.
                llave_enfrentamiento = tuple(sorted([local.casefold(), visitante.casefold()]))
                if llave_enfrentamiento in enfrentamientos_jugados:
                    print("Este encuentro ya se realizo, intentelo de nuevo ingresando los datos correctos")
                    continue

                # RESTRICCIÓN: Goles entre 0 y 20
                if not (0 <= gl <= 20 and 0 <= gv <= 20):
                    print("Error: Los goles deben estar entre 0 y 20 (inclusive).")
                    continue
                
                # Normalizamos claves para contar equipos del grupo sin duplicados por mayúsc/minúsc.
                # Usamos nombres canónicos (ya validados arriba) así que local/visitante ya son canónicos.

                # RESTRICCIÓN: Máximo 4 equipos por grupo
                equipos_nuevos = 0
                if local not in equipos:
                    equipos_nuevos += 1
                if visitante not in equipos:
                    if visitante != local:
                        equipos_nuevos += 1
                if len(equipos) + equipos_nuevos > 4:
                    print("Error: Se ha excedido el límite de 4 equipos por grupo.")
                    print("Vuelva a intentar e ingrese correctamente los datos del partido.")
                    continue

                # RESTRICCIÓN: EXACTAMENTE 3 partidos por cada país del grupo.
                # Como el grupo se modela con 4 equipos y 6 partidos totales (todos contra todos una vez),
                # cada equipo participa en 3 partidos automáticamente. Pero validamos igualmente.
                # Contamos PJ actual antes de agregar el partido.
                pj_local = equipos.get(local, {}).get("pj", 0)
                pj_visitante = equipos.get(visitante, {}).get("pj", 0)
                if pj_local >= 3 or pj_visitante >= 3:
                    print("Cada pais debera participar de 3 encuentros obligatorios")
                    print("Vuelva a intentar e ingrese correctamente los datos del partido.")
                    continue

                # Si todo está bien, registramos y salimos del while True
                enfrentamientos_jugados.add(llave_enfrentamiento)
                registrar_equipo(equipos, local)
                registrar_equipo(equipos, visitante)
                procesar_partido(equipos, local, visitante, gl, gv)
                break

            except ValueError:
                print("Error: Los goles deben ser números enteros válidos.")

        # Al finalizar cada 2 partidos (una fecha), mostramos la tabla
        if (i + 1) % 2 == 0:
            nro_fecha = (i + 1) // 2
            tabla_actual = ordenar_tabla(equipos)
            titulos = ["", "PRIMERA FECHA", "SEGUNDA FECHA", "TERCERA FECHA"]

            imprimir_tabla(tabla_actual, f"TABLA PROVISORIA DE LA {titulos[nro_fecha]}")
                
            if nro_fecha == 3:
                print("\n" + "━" * 35)
                print("\033[1m  CLASIFICADOS\033[0m")
                print(f"  - {tabla_actual[0][0]}")
                print(f"  - {tabla_actual[1][0]}")
                print("\n\033[1m  TERCERO\033[0m")
                print(f"  - {tabla_actual[2][0]}")
                print("━" * 35)

                imprimir_tabla(tabla_actual, "TABLA FINAL")

                # Lógica de detección de empate absoluto para la tabla final
                idx = 0
                while idx < len(tabla_actual):
                    j = idx + 1
                    while j < len(tabla_actual):
                        d1 = tabla_actual[idx][1]
                        d2 = tabla_actual[j][1]
                        if (d1["pts"] == d2["pts"] and 
                            (d1["gf"] - d1["gc"]) == (d2["gf"] - d2["gc"]) and 
                            d1["gf"] == d2["gf"]):
                            j += 1
                        else:
                            break
                    if j - idx > 1:
                        nombres = [e[0] for e in tabla_actual[idx:j]]
                        print(f"\nEmpate absoluto entre {', '.join(nombres[:-1])} y {nombres[-1]}: Clasificacion por orden alfabético.")
                    idx = j

if __name__ == "__main__":
    main() 

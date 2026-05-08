def mostrar_resultados(tabla):
    """Imprime los clasificados en el formato exacto requerido por la consigna.

    Args:
        tabla (list): Lista ordenada de tuplas (nombre, estadísticas).
    """
    print("\n" + "=" * 45)
    print(f"{' POS':<5} | {'EQUIPO':<15} | {'PTS':<4} | {'GF':<4} | {'GC':<4} | {'DG':<3}")
    print("-" * 45)
    
    for i, (equipo, datos) in enumerate(tabla, 1):
        dg = datos["gf"] - datos["gc"]
        print(f" {i:<4} | {equipo:<15} | {datos['pts']:<4} | {datos['gf']:<4} | {datos['gc']:<4} | {dg:<3}")
    
    print("-" * 45)
    print(" RESULTADOS FINALES")
    print("-" * 45)
    print(f" CLASIFICADOS DIRECTOS: {tabla[0][0]} y {tabla[1][0]}")
    print(f" TERCER CLASIFICADO: {tabla[2][0]}")
    print("=" * 45 + "\n")


def registrar_equipo(equipos, equipo):
    """Inicializa las estadísticas de un equipo si no existe en el diccionario.

    Args:
        equipos (dict): Diccionario de equipos.
        equipo (str): Nombre del equipo a registrar.
    """
    if equipo not in equipos:
        equipos[equipo] = {"pts": 0, "pj": 0, "gf": 0, "gc": 0}


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

    total_partidos = 6
    for i in range(total_partidos):
        # Mostrar encabezado de fecha cada 2 partidos
        if i % 2 == 0:
            nro_fecha = (i // 2) + 1
            print(f"\n--- FECHA {nro_fecha} ---")
        # Bucle de validación para el partido actual
        while True:
            entrada = input(f" Partido {i + 1} > ").strip()
            
            if not entrada:
                print("Error: La entrada no puede estar vacía.")
                continue
                
            linea = entrada.split()
            
            if len(linea) != 4:
                print("Error: Debe ingresar 4 datos (Local, Visitante, GolesL, GolesV).")
                continue
            try:
                local = linea[0]
                visitante = linea[1]
                gl = int(linea[2])
                gv = int(linea[3])
                
                if local.lower() == visitante.lower():
                    print("Error: Un equipo no puede jugar contra sí mismo, ingreselo correctamnente.")
                    continue

                # RESTRICCIÓN: Goles entre 0 y 20
                if not (0 <= gl <= 20 and 0 <= gv <= 20):
                    print("Error: Los goles deben estar entre 0 y 20 (inclusive).")
                    continue
                
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
                # Si todo está bien, registramos y salimos del while True
                registrar_equipo(equipos, local)
                registrar_equipo(equipos, visitante)
                procesar_partido(equipos, local, visitante, gl, gv)
                break
                
            except ValueError:
                print("Error: Los goles deben ser números enteros válidos.")

    if len(equipos) != 4:
        print(f"\n Error: Se registraron {len(equipos)} equipos. El formato oficial requiere 4.")

    tabla = ordenar_tabla(equipos)
    # CRITERIO DE DESEMPATE: Detección e información de Empate Absoluto (Agrupado)
    i = 0
    while i < len(tabla):
        j = i + 1
        while j < len(tabla):
            d1 = tabla[i][1]
            d2 = tabla[j][1]
            # Comparamos puntos, diferencia de gol (gf-gc) y goles a favor
            if (d1["pts"] == d2["pts"] and 
                (d1["gf"] - d1["gc"]) == (d2["gf"] - d2["gc"]) and 
                d1["gf"] == d2["gf"]):
                j += 1
            else:
                break
        
        if j - i > 1:
            nombres_empatados = [equipo[0] for equipo in tabla[i:j]]
            txt_nombres = ", ".join(nombres_empatados[:-1]) + " y " + nombres_empatados[-1]
            print(f"\n Empate absoluto entre {txt_nombres}: Clasificacion por orden alfabético.")
        
        i = j

    mostrar_resultados(tabla)

if __name__ == "__main__":
    main() 
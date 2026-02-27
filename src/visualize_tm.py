"""
Generador de diagrama de Máquina de Turing
Genera un archivo DOT y PNG desde un archivo JSON de definición de MT
"""

import os
import json
import shutil
import subprocess
import sys
from collections import defaultdict


def load_machine_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def _tm_to_dot(machine: dict) -> str:
    """
    Convierte la definición de la MT a formato DOT de Graphviz.
    Las transiciones se etiquetan como: leer / escribir, dir
    Las aristas entre el mismo par de estados se agrupan en una sola flecha.
    """
    accept_states = set(machine.get("accept_states", []))
    reject_states = set(machine.get("reject_states", []))
    start_state   = machine["start_state"]
    transitions   = machine["transitions"]
    name          = machine.get("name", "Turing Machine")

    # Recolectar todos los estados mencionados
    all_states = set()
    all_states.add(start_state)
    all_states.update(accept_states)
    all_states.update(reject_states)
    for t in transitions:
        all_states.add(t["state"])
        all_states.add(t["next"])

    # Agrupar transiciones por (estado_origen, estado_destino)
    edge_labels: dict[tuple, list[str]] = defaultdict(list)
    for t in transitions:
        src  = t["state"]
        dst  = t["next"]
        rd   = t["read"]
        wr   = t["write"]
        mv   = t["move"]
        label = f"{rd} / {wr},{mv}"
        edge_labels[(src, dst)].append(label)

    lines = []
    lines.append("digraph TM {")
    lines.append('  rankdir=LR;')
    lines.append(f'  label="{name}";')
    lines.append('  labelloc="t";')
    lines.append('  fontsize=16;')
    lines.append('  fontname="Helvetica";')
    lines.append('  node [fontname="Helvetica"];')
    lines.append('  edge [fontname="Helvetica", fontsize=10];')
    lines.append('  splines=ortho;  // Aristas ortogonales para evitar encimamiento')
    lines.append('  nodesep=0.8;  // Espacio entre nodos')
    lines.append('  ranksep=1.2;  // Espacio entre niveles')
    lines.append("")

    # Nodo fantasma de inicio
    lines.append('  "__start__" [shape=point, width=0.2];')

    # Definir nodos con estilos
    for state in sorted(all_states):
        safe = state.replace('"', '\\"')
        if state in accept_states:
            lines.append(f'  "{safe}" [shape=doublecircle, style=filled, fillcolor="#d4edda", color="#28a745"];')
        elif state in reject_states:
            lines.append(f'  "{safe}" [shape=doublecircle, style=filled, fillcolor="#f8d7da", color="#dc3545"];')
        else:
            lines.append(f'  "{safe}" [shape=circle, style=filled, fillcolor="#e3f2fd", color="#1565c0"];')

    lines.append("")

    # Flecha inicial
    safe_start = start_state.replace('"', '\\"')
    lines.append(f'  "__start__" -> "{safe_start}";')
    lines.append("")

    # Aristas agrupadas
    for (src, dst), labels in sorted(edge_labels.items()):
        safe_src = src.replace('"', '\\"')
        safe_dst = dst.replace('"', '\\"')
        combined = "\\n".join(labels)
        combined = combined.replace('"', '\\"')
        # Self-loop con curvatura extra
        if src == dst:
            lines.append(f'  "{safe_src}" -> "{safe_dst}" [label="{combined}", dir=forward, constraint=false];')
        else:
            lines.append(f'  "{safe_src}" -> "{safe_dst}" [label="{combined}"];')

    lines.append("}")
    return "\n".join(lines)


def visualize_tm(machine_path: str, output_dir: str = ".", filename_base: str = "fibonacci_tm"):
    """
    Genera el diagrama DOT y PNG de la Máquina de Turing.

    Args:
        machine_path:  Ruta al archivo JSON de la MT
        output_dir:    Carpeta donde se guardan los archivos generados
        filename_base: Nombre base para los archivos (sin extensión)
    """
    # Cargar máquina
    machine = load_machine_json(machine_path)
    print(f"[visualize_tm] Máquina cargada: {machine.get('name', machine_path)}")
    print(f"[visualize_tm] Estados: {len(set(t['state'] for t in machine['transitions']))} | "
          f"Transiciones: {len(machine['transitions'])}")

    # Crear carpeta de salida
    os.makedirs(output_dir, exist_ok=True)

    # Generar contenido DOT
    dot_content = _tm_to_dot(machine)

    # Guardar .dot
    dot_path = os.path.join(output_dir, f"{filename_base}.dot")
    with open(dot_path, "w", encoding="utf-8") as f:
        f.write(dot_content)
    print(f"[visualize_tm] Archivo DOT guardado: {dot_path}")

    # Intentar generar PNG con Graphviz (dot binary)
    dot_bin = shutil.which("dot")
    if dot_bin:
        png_path = os.path.join(output_dir, f"{filename_base}.png")
        try:
            # Usar -Kfdp para grafos densos/grandes (mejor que -Kdot)
            subprocess.run(
                [dot_bin, "-Tpng", "-Kfdp", "-Gdpi=150", dot_path, "-o", png_path],
                check=True,
                capture_output=True
            )
            print(f"[visualize_tm] Imagen PNG generada: {png_path}")
            print(f"[visualize_tm]    (usando motor 'fdp' para grafos densos)")
        except subprocess.CalledProcessError as e:
            print(f"[visualize_tm] Error al ejecutar graphviz: {e.stderr.decode()}")
    else:
        # Intentar con la librería Python de graphviz como fallback
        try:
            from graphviz import Source
            src = Source(dot_content)
            out = src.render(
                os.path.join(output_dir, filename_base),
                format="png",
                cleanup=True
            )
            print(f"[visualize_tm] Imagen generada con librería graphviz: {out}")
        except ImportError:
            print("[visualize_tm] 'dot' no encontrado y librería 'graphviz' no instalada.")
            print("[visualize_tm]    Instala con: pip install graphviz")
            print("[visualize_tm]    O instala Graphviz del sistema: https://graphviz.org/download/")
            print(f"[visualize_tm]    El archivo DOT está disponible en: {dot_path}")
            print("[visualize_tm]    Puedes pegarlo en https://dreampuf.github.io/GraphvizOnline/")


def print_dot_preview(machine_path: str):
    """Imprime el DOT generado en consola para previsualizar o copiar"""
    machine = load_machine_json(machine_path)
    print(_tm_to_dot(machine))


if __name__ == "__main__":
    # --- CONFIGURACIÓN ---
    # Si se pasa ruta como argumento, usarla primero
    if len(sys.argv) > 1:
        MACHINE_PATH = sys.argv[1]
    else:
        # Ruta por defecto relativa al proyecto (un nivel arriba de src/)
        project_root = os.path.dirname(os.path.dirname(__file__))
        MACHINE_PATH = os.path.join(project_root, "machines", "fibonacci.json")
        
        # Intentar ruta alternativa con typo
        if not os.path.exists(MACHINE_PATH):
            alt = MACHINE_PATH.replace("fibonacci", "fibonnacci")
            if os.path.exists(alt):
                MACHINE_PATH = alt
                print(f"[visualize_tm] Nota: usando 'fibonnacci.json' (typo en nombre de archivo)")
    
    OUTPUT_DIR  = os.path.join(os.path.dirname(__file__), "..", "Análisis Empírico")
    FILENAME    = "fibonacci_tm"
    # ---------------------

    # Verificar que el archivo existe
    if not os.path.exists(MACHINE_PATH):
        print(f"[visualize_tm] No se encontró la máquina en: {os.path.abspath(MACHINE_PATH)}")
        print("Uso: python visualize_tm.py <ruta_al_json>")
        print(f"Directorio actual: {os.getcwd()}")
        sys.exit(1)

    visualize_tm(MACHINE_PATH, output_dir=OUTPUT_DIR, filename_base=FILENAME)

import bpy
import math
from mathutils import Vector

# --- настройки ---
# минимальное расстояние между объектами
MIN_SPACING = 2.0
# стартовая позиция сетки (в МИРОВЫХ координатах)
START_X = 0.0
START_Y = 0.0
# высота по Z (в МИРОВЫХ координатах)
TARGET_Z = 0.0
# выкладывать только выделенные объекты?
ONLY_SELECTED = True
# ------------------

# собираем список объектов
if ONLY_SELECTED:
    objs = [o for o in bpy.context.selected_objects if o.type == 'MESH']
else:
    objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']

if not objs:
    print("Нет подходящих объектов (MESH).")
else:
    print(f"Нашёл {len(objs)} объектов, раскладываю по сетке (по МИРОВЫМ координатам)...")

    # считаем размер ячейки по макс. габариту объекта
    max_size = 0.0
    for o in objs:
        d = o.dimensions
        max_size = max(max_size, d.x, d.y)

    # шаг сетки
    step = max(MIN_SPACING, max_size * 1.2)

    # делаем почти квадратную сетку
    cols = math.ceil(math.sqrt(len(objs)))

    for idx, o in enumerate(objs):
        row = idx // cols
        col = idx % cols

        new_x = START_X + col * step
        new_y = START_Y - row * step  # вниз по -Y
        new_z = TARGET_Z

        # запоминаем старую МИРОВУЮ позицию
        o["orig_world_location"] = tuple(o.matrix_world.translation)

        # ставим новую МИРОВУЮ позицию
        mw = o.matrix_world.copy()
        mw.translation = Vector((new_x, new_y, new_z))
        o.matrix_world = mw

    print("Готово: объекты разложены по сетке и выровнены по Y/Z в мировом пространстве.")

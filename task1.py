from qgis import processing
from qgis.core import QgsProject, QgsVectorLayer

STOPS_LAYER_NAME = "байкальская_6"
PEDESTRIAN_LAYER_NAME = "Highway_OSM_Irkutsk"
 
# Параметры анализа
USE_DISTANCE = True # True → 500 м, False → 5 минут
MAX_DISTANCE = 500 # метры
MAX_MINUTES = 5 # минуты
WALKING_SPEED_KMH = 5 # км/ч (для расчёта времени)
 
# Имя выходного слоя
OUTPUT_LAYER_NAME = "пешеходные_пути_в_зоне_доступности"

project = QgsProject.instance()
 
# Получаем слои по именам
stops_layer = None
pedestrian_layer = None
 
for layer in project.mapLayers().values():
    if layer.name() == STOPS_LAYER_NAME:
        stops_layer = layer
    elif layer.name() == PEDESTRIAN_LAYER_NAME:
        pedestrian_layer = layer
 
print(f"Найдены слои:")
print(f"Остановки: {stops_layer.featureCount()} точек")
print(f"Пешеходные пути: {pedestrian_layer.featureCount()} линий")

# Подготовка параметров
strategy = 0 if USE_DISTANCE else 1  # 0 = shortest (distance), 1 = fastest (time)
 
travel_cost = MAX_DISTANCE if USE_DISTANCE else MAX_MINUTES
 
print(f"⚙Запускаем анализ: {'расстояние = ' + str(MAX_DISTANCE) + ' м' if USE_DISTANCE else 'время = ' + str(MAX_MINUTES) + ' мин'}")
 
# Запуск встроенного инструмента QGIS
params = {
    'INPUT': pedestrian_layer,
    'STRATEGY': strategy,
    'DIRECTION_FIELD': '',
    'VALUE_FORWARD': '',
    'VALUE_BACKWARD': '',
    'VALUE_BOTH': '',
    'DEFAULT_DIRECTION': 2,  # both directions
    'SPEED_FIELD': '',
    'DEFAULT_SPEED': WALKING_SPEED_KMH,  # км/ч — используется только при strategy=1
    'TOLERANCE': 1.0,  # метры — как далеко искать ближайший узел сети от остановки
    'START_POINTS': stops_layer,
    'TRAVEL_COST2': travel_cost,  # верхняя граница (вторая — для двойного диапазона; первая = 0)
    'INCLUDE_BOUNDS': False,
    'OUTPUT_LINES': 'TEMPORARY_OUTPUT'
}

output_lines = result['OUTPUT_LINES']
output_lines.setName(OUTPUT_LAYER_NAME)
project.addMapLayer(output_lines)
 
print(f"\nСоздан слой '{OUTPUT_LAYER_NAME}' с {output_lines.featureCount()} пешеходными путями в зоне доступности.")
 

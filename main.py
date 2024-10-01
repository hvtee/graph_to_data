import cv2
import numpy as np
import matplotlib.pyplot as plt

# Шаг 1: Загрузка изображения графика
image = cv2.imread('graphs/CoFe2O4.png')

# Преобразуем изображение в градации серого
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Применим бинаризацию для лучшего выделения графика
_, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

# Используем Canny для выделения краев графика
edges = cv2.Canny(thresh, 50, 150)

# Шаг 2: Найдем контуры на изображении (чтобы выделить график)
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Создадим копию изображения для отображения контуров
image_contours = image.copy()

# Нарисуем найденные контуры
cv2.drawContours(image_contours, contours, -1, (255, 0, 0), 1)

# Отображение контуров на графике
plt.figure(figsize=(10, 6))
plt.imshow(cv2.cvtColor(image_contours, cv2.COLOR_BGR2RGB))
plt.title("Найденные контуры на изображении")
plt.show()

# Шаг 3: Выделение точек графика
# Собираем координаты точек графика
graph_points = []
for contour in contours:
    for point in contour:
        x, y = point[0]
        graph_points.append((x, y))

# Шаг 4: Преобразование пикселей в координаты графика (с учетом диапазона осей)
# Пример: допустим диапазон оси X [-40, 60] и оси Y [-60, 60]
x_range = (-40, 60)  # Диапазон оси X
y_range = (-60, 60)  # Диапазон оси Y

# Находим размер области графика
height, width = gray.shape

# Преобразование пиксельных координат в реальные значения графика
graph_data = []
for (x, y) in graph_points:
    real_x = x_range[0] + (x / width) * (x_range[1] - x_range[0])
    real_y = y_range[1] - (y / height) * (y_range[1] - y_range[0])
    graph_data.append((real_x, real_y))

# # Шаг 5: Запись данных в Excel
# df = pd.DataFrame(graph_data, columns=['X', 'Y'])
# df.to_excel('graph_data.xlsx', index=False)

# print("Данные графика успешно сохранены в файл 'graph_data.xlsx'.")

# Шаг 6: Построение восстановленного графика
x_values = [point[0] for point in graph_data]
y_values = [point[1] for point in graph_data]

# Шаг 7: Отображение исходного и восстановленного графика для сравнения
plt.figure(figsize=(12, 6))

# Исходное изображение
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title("Исходное изображение графика")

# Восстановленный график
plt.subplot(1, 2, 2)
plt.plot(x_values, y_values, 'b-', label='Восстановленный график')
plt.title("Восстановленный график по данным")
plt.xlabel('H, kOe')
plt.ylabel('M, emu/g')
plt.legend()

# Отображаем оба графика для сравнения
plt.show()

import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Шаг 1: Загрузка изображения
image = cv2.imread('graphs/CoFe2O4.png')

# Преобразуем изображение в цветовое пространство HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

plt.imshow(hsv_image)
plt.show()

# Установим границы для черного цвета (черная линия гистерезиса)
lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 50])

# Создаем маску для выделения только черных пикселей (линия гистерезиса)
black_mask = cv2.inRange(hsv_image, lower_black, upper_black)

plt.imshow(black_mask)
plt.show()

# Убираем мелкие объекты (подписи и текст) с помощью морфологических операций
kernel = np.ones((5, 5), np.uint8)
cleaned_mask = cv2.morphologyEx(black_mask, cv2.MORPH_OPEN, kernel)

# Обрезаем края, чтобы удалить оси
height, width = cleaned_mask.shape
crop_mask = cleaned_mask[int(0.1*height):int(0.9*height), int(0.1*width):int(0.9*width)]

# Применяем маску к изображению, чтобы получить только черные области
black_line = cv2.bitwise_and(image, image, mask=cleaned_mask)

# Покажем результат маскирования (выделение черной линии)
plt.figure(figsize=(10, 6))
plt.imshow(cv2.cvtColor(black_line, cv2.COLOR_BGR2RGB))
plt.title("Очищенная черная линия гистерезиса без осей и подписей")
plt.show()

# Шаг 2: Преобразование выделенной линии в данные x и y
gray = cv2.cvtColor(black_line, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

# Найдем контуры для выделенной линии
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Собираем координаты точек графика
graph_points = []
for contour in contours:
    for point in contour:
        x, y = point[0]
        graph_points.append((x, y))

# Шаг 3: Преобразование пикселей в реальные значения
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

# # Запись данных в Excel
# df = pd.DataFrame(graph_data, columns=['X', 'Y'])
# df.to_excel('data/graph_data.xlsx', index=False)

# Построение восстановленного графика
x_values = [point[0] for point in graph_data]
y_values = [point[1] for point in graph_data]

plt.figure(figsize=(6, 6))
plt.plot(x_values, y_values, 'b-', label='Восстановленный график')
plt.title("Восстановленный график по данным")
plt.xlabel('H, kOe')
plt.ylabel('M, emu/g')
plt.legend()
plt.show()

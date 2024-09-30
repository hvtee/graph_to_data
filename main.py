import matplotlib.pyplot as plt
import numpy as np
import cv2
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\WinDISK D\APPS\Tesseract-OCR\tesseract.exe'


def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Используем Canny для выделения краев графика
    edges = cv2.Canny(thresh, 50, 150)

    # Отображаем исходное изображение и изображение с краями для визуального анализа
    plt.figure(figsize=(10, 6))

    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("Source")

    plt.subplot(1, 2, 2)
    plt.imshow(edges, cmap='gray')
    plt.title("Canny")

    plt.show()

    return edges


def axes(image, edges):
    # Используем преобразование Хафа для поиска прямых (осей графика)
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

    # Скопируем изображение для отрисовки найденных линий
    image_with_lines = image.copy()

    # Отрисуем найденные линии (осевые линии)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image_with_lines, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Покажем результат
    plt.figure(figsize=(10, 6))
    plt.imshow(cv2.cvtColor(image_with_lines, cv2.COLOR_BGR2RGB))
    plt.title("Axes")
    plt.show()


if __name__ == '__main__':
    image = cv2.imread("graphs/CoFe2O4.png")
    edges = canny(image=image)
    axes(image, edges)

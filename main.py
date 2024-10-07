import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def extract_hysteresis_loop(image_path):
    image = cv2.imread(image_path)

    # Преобразуем изображение из BGR в HSV для удобного выделения красного цвета
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    plt.imshow(hsv_image)
    print("hsv_image")
    plt.show()

    lower_red1 = np.array([0, 50, 20])
    upper_red1 = np.array([5, 255, 255])

    lower_red2 = np.array([170, 25, 20])
    upper_red2 = np.array([180, 255, 255])

    # Маска для выделения красных частей изображения
    mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    plt.imshow(mask)
    print("mask")
    plt.show()

    # Применяем маску к изображению
    red_only_image = cv2.bitwise_and(image, image, mask=mask)

    plt.imshow(red_only_image)
    print("red_only_image")
    plt.show()

    # Преобразуем в grayscale и находим контуры
    gray_image = cv2.cvtColor(red_only_image, cv2.COLOR_BGR2GRAY)
    _, thresh_image = cv2.threshold(gray_image, 30, 255, cv2.THRESH_BINARY)

    plt.imshow(gray_image)
    print("gray_image")
    plt.show()

    # Находим контуры на бинаризованном изображении
    contours, _ = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours, image


def pixel_to_real_coordinates(pixel_coords, x_range, y_range, img_shape):
    height, width = img_shape[:2]
    real_coords = []
    sorted_real_coords = []

    x_min, x_max = x_range
    y_min, y_max = y_range

    for point in pixel_coords:
        x_pixel, y_pixel = point[0]

        x_real = x_min + (x_pixel / width) * (x_max - x_min)
        y_real = y_min + (y_pixel / height) * (y_max - y_min)

        real_coords.append([x_real, -y_real])

    sorted_real_coords = sorted(real_coords, key=lambda x: x[0])
    print(real_coords)
    print("\n\n\n\n\n\n")
    print(sorted_real_coords)

    return np.array(real_coords)


def calculate_hysteresis_loop_params(image_path, x_range, y_range):
    contours, image = extract_hysteresis_loop(image_path)

    if contours:
        # Выбираем самый крупный контур
        largest_contour = max(contours, key=cv2.contourArea)

        real_coords = pixel_to_real_coordinates(largest_contour, x_range, y_range, image.shape)

        x_values = real_coords[:, 0]
        y_values = real_coords[:, 1]

        x_min, x_max = x_values.min(), x_values.max()
        y_min, y_max = y_values.min(), y_values.max()

        width = x_max - x_min
        height = y_max - y_min
        area = cv2.contourArea(largest_contour)

        print(f"Параметры петли гистерезиса:")
        print(f"Ширина: {width}")
        print(f"Высота: {height}")
        print(f"Площадь (в пикселях): {area}")

        fig, ax = plt.subplots(1, 2, figsize=(12, 6))

        ax[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        ax[0].set_title('Исходное изображение')
        ax[0].axis('off')

        ax[1].plot(real_coords[:, 0], real_coords[:, 1], lw=2)
        ax[1].set_title('График петли гистерезиса')
        ax[1].set_xlabel('X')
        ax[1].set_ylabel('Y')
        ax[1].grid(True)

        plt.tight_layout()
        plt.show()
        return real_coords
    else:
        print("Петля гистерезиса не найдена!")


def save_to_excel(data, diff_data, file_path='data/hysteresis_loop.xlsx'):
    df = pd.DataFrame({
        'X': [x for x, y in data],
        'Y': [y for x, y in data],
        'ΔY': [delta_y for x, delta_y in diff_data]
    })

    df.to_excel(file_path, index=False)
    print(f"Данные успешно сохранены в файл: {file_path}")


def diff_coords(coords, max_y):
    return [(x, (y - max_y) / max_y) for x, y in coords]


def main():
    # Пример вызова с указанием диапазонов осей и цены деления
    image_path = 'graphs/CoFe2O4_5.png'  # Замените на ваш путь к изображению
    x_range = (-40, 60)  # Пример диапазона значений по оси X
    y_range = (-60, 60)  # Пример диапазона значений по оси Y

    coords = calculate_hysteresis_loop_params(image_path, x_range, y_range)

    max_y = max(coords, key=lambda coord: coord[1])[1]
    print(f"Максимальное значение y: {max_y}")

    d_coords = diff_coords(coords, max_y)
    plt.imshow(d_coords, cmap='gray')
    plt.show()

    if coords is not None:
        save_to_excel(coords, d_coords)


if __name__ == '__main__':
    main()

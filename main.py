import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def extract_hysteresis_loop(image_path):
    image = cv2.imread(image_path)

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    plt.imshow(hsv_image)
    print("hsv_image")
    plt.show()

    lower_red1 = np.array([0, 50, 20])
    upper_red1 = np.array([5, 255, 255])

    lower_red2 = np.array([170, 25, 20])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    plt.imshow(mask)
    print("mask")
    plt.show()

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
    # sorted_real_coords = []

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
        largest_contour = max(contours, key=cv2.contourArea)

        real_coords = pixel_to_real_coordinates(largest_contour, x_range, y_range, image.shape)

        x_values = real_coords[:, 0]
        y_values = real_coords[:, 1]

        x_min, x_max = x_values.min(), x_values.max()
        y_min, y_max = y_values.min(), y_values.max()

        width = x_max - x_min
        height = y_max - y_min
        area = cv2.contourArea(largest_contour)

        print(f"PARAMS:")
        print(f"Width: {width}")
        print(f"Height: {height}")
        print(f"Area (pix): {area}")

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


def diff_coords(coords, max_y):
    return [(x, (y - max_y) / max_y) for x, y in coords]


def recalculate_h(coords):
    return [(1 / x, y) for x, y in coords]


def save_to_excel(data, diff_data, inv_h_data, file_path='data/hysteresis-loop-', img_name=""):
    df = pd.DataFrame({
        'H': [x for x, y in data],
        'M': [y for x, y in data],
        'δM': [delta_y for x, delta_y in diff_data],
        '1/H': [inv_h for inv_h, y in inv_h_data]
    })
    time_string = time.strftime("%d.%m.%Y-%H.%M.%S")
    file_path = file_path + f"{time_string}" + ".xlsx"
    df.to_excel(file_path, index=False)
    print(f"Data saved into: {file_path}")


def main():
    image_path = 'graphs/loop_2.png'
    image_name = image_path
    x_range = (-40, 40)
    y_range = (-80, 80)

    coords = calculate_hysteresis_loop_params(image_path, x_range, y_range)
    sorted_coords = sorted(np.asarray(coords).tolist(), key=lambda coord: coord[0])
    max_y = sorted_coords[-1][1]
    min_y = sorted_coords[0][1]
    # max_y = max(coords, key=lambda coord: coord[1])[1]
    # min_y = min(coords, key=lambda coord: coord[1])[1]

    Mr = None
    for x, y in coords:
        if x == 0:
            Mr = y
            break

    Hc = None
    for x, y in coords:
        if round(y) == 0:
            Hc = x
            break

    print(f"Ms: {max_y}")
    print(f"Mmin: {min_y}")
    if Mr:
        print(f"Mr: {Mr}")
    if Hc:
        print(f"Hc: {Hc}")

    d_coords = diff_coords(coords, max_y)
    x = [i[0] for i in d_coords]
    y = [i[1] for i in d_coords]
    plt.plot(x, y, lw=2)
    plt.show()

    inv_h_coords = recalculate_h(coords)
    x = [i[0] for i in inv_h_coords]
    y = [i[1] for i in inv_h_coords]
    plt.plot(x, y, lw=2)
    plt.show()

    if coords is not None:
        save_to_excel(coords, d_coords, inv_h_coords)


if __name__ == '__main__':
    main()

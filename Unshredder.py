from PIL import Image


def boundry_list():
    """
    gather left and right borders of shreds in two lists and return them.
    """
    left_boundary_points = []
    right_boundary_points = []

    for elements in range(1, (shred_number + 1)):
        left_boundary_points.append((elements - 1) * 32)
        right_boundary_points.append((elements * 32) - 1)

    return left_boundary_points, right_boundary_points


def get_pixel_value(shred, pixel_height):
    """
    Get RGB values of pixel.
    """
    return data[pixel_height * width + shred]


def compare_shreds_rgb(x1, x2):
    """
    extract RGB values of columns, return average value.
    """
    dif_red = dif_green = dif_blue = 0
    for y in range(0, height):
        data1 = get_pixel_value(x1, y)
        data2 = get_pixel_value(x2, y)
        dif_red += abs(data1[0] - data2[0])
        dif_green += abs(data1[1] - data2[1])
        dif_blue += abs(data1[2] - data2[2])

    return (dif_red + dif_green + dif_blue) / 3


def find_first_last_shreds(x1, x2):
    """
    Deal with first RGB values only.
    Return average value.
    """
    dif_red = dif_green = dif_blue = 0
    data1 = get_pixel_value(x1, 0)
    data2 = get_pixel_value(x2, 0)
    dif_red += abs(data1[0] - data2[0])
    dif_green += abs(data1[1] - data2[1])
    dif_blue += abs(data1[2] - data2[2])

    return (dif_red + dif_green + dif_blue) / 3


def neighbour_shreds(boundry_lists):
    """
    Compare RGB value totals and find biggest matches between shreds.
    Find start shred with calculating biggest sum in first RGB values.
    Return list of pair shreds and start shred.
    """
    left_boundary_list, right_boundry_list = boundry_lists
    shreds = []
    biggest_temp = 0
    for shred1 in range(0, len(right_boundry_list)):
        temp_sum = 0
        shreds.append((0, 0, 100000))
        for shred2 in range(0, len(left_boundary_list)):
            if shred1 != shred2:
                temp = shred1 + 1, shred2 + \
                    1, compare_shreds_rgb(
                        left_boundary_list[shred2], right_boundry_list[shred1])
                borders = shred1 + 1, shred2 + \
                    1, find_first_last_shreds(
                        left_boundary_list[shred2], right_boundry_list[shred1])
                temp_sum += borders[2]
                if temp[2] < shreds[shred1][2]:
                    shreds[shred1] = (temp[0], temp[1], temp[2])
        if temp_sum > biggest_temp:
            biggest_temp = temp_sum
            start_shred = shreds[shred1][1]

    return shreds, start_shred


def sorted_shreds(shred_list):
    """
    Get shred list and starting shred as parameter.
    Sort shred with starting shred parameter
    """
    sorted_shred_list = []
    shreds, start_value = shred_list
    print "\n", "Unsorted Shreds:\n %r" % shreds
    print "\n"
    for i in range(len(shreds)):
        if i == 0:
            sorted_shred_list.append(shreds[start_value - 1])
            nextstrip = shreds[start_value - 1][1]
        else:
            sorted_shred_list.append(shreds[nextstrip - 1])
            nextstrip = shreds[nextstrip - 1][1]
    print "Sorted Shreds: \n %r" % sorted_shred_list, "\n"

    return sorted_shred_list


def create_image(image_shred_number, shred_in_order):
    """
    Create image for sorted shreds.
    """
    unshredded = Image.new("RGBA", image.size)
    shred_width = unshredded.size[0] / image_shred_number
    for i in range(0, image_shred_number):
        image_shred_number = shred_in_order[i][0]
        x1, y1 = (shred_width * image_shred_number) - shred_width, 0
        x2, y2 = x1 + shred_width, height
        source_region = image.crop((x1, y1, x2, y2))
        destination_point = (i * shred_width, 0)
        unshredded.paste(source_region, destination_point)
    unshredded.save("unshredded.jpg", "JPEG")
    unshredded.show()

"""
Open image and get data, width, height values.
Determine shred number, call the functions.
"""

if __name__ == "__main__":
    image = Image.open("image.png")
    data = list(image.getdata())
    width, height = image.size
    shred_number = width / 32
    image_shred_list = neighbour_shreds(boundry_list())
    create_image(shred_number, sorted_shreds(image_shred_list))

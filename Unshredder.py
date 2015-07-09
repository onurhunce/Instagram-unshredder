from PIL import Image

"""
gather left and right borders of shreds in two lists.
"""


def boundry_list():
    left_boundary_points = []
    right_boundary_points = []
    # adding all corner points in one array.
    for elements in range(1, (shred_number + 1)):
        left_boundary_points.append((elements - 1) * 32)
        right_boundary_points.append((elements * 32) - 1)

    return left_boundary_points, right_boundary_points

# get RGB values of pixel.


def get_pixel_value(shred, height):
    pixel = data[height * width + shred]
    return pixel

# extract RGB values of columns, return average value.


def compare_shreds_rgb(x1, x2):
    dif_red = dif_green = dif_blue = 0
    for y in range(0, height):
        data1 = get_pixel_value(x1, y)
        data2 = get_pixel_value(x2, y)
        dif_red += abs(data1[0] - data2[0])
        dif_green += abs(data1[1] - data2[1])
        dif_blue += abs(data1[2] - data2[2])

    return (dif_red + dif_green + dif_blue) / 3

"""
Deal with first RGB values only.
Return average value.
"""


def find_first_last_shreds(x1, x2):
    dif_red = dif_green = dif_blue = 0
    data1 = get_pixel_value(x1, 0)
    data2 = get_pixel_value(x2, 0)
    dif_red += abs(data1[0] - data2[0])
    dif_green += abs(data1[1] - data2[1])
    dif_blue += abs(data1[2] - data2[2])

    return (dif_red + dif_green + dif_blue) / 3

"""
Compare RGB value totals and find biggest matches between shreds.
Find start shred with calculating biggest sum in first RGB values.
Return list of pair shreds and start shred.
"""


def neighbour_shreds(boundry_list):
    left_boundary_list, right_boundry_list = boundry_list
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
                if (temp[2] < shreds[shred1][2]):
                    shreds[shred1] = (temp[0], temp[1], temp[2])
        if temp_sum > biggest_temp:
            biggest_temp = temp_sum
            start_shred = shreds[shred1][1]

    return shreds, start_shred

"""
Get shredlist and starting shred as parameter.
Sort shred with starting shred parameter 
"""


def sorted_shreds(shredlist):
    sorted_shreds = []
    shreds, start_value = shredlist
    print "Unsorted Shreds: \n %r" % shreds
    print "\n"
    for i in range(len(shreds)):
        if (i == 0):
            sorted_shreds.append(shreds[start_value - 1])
            nextstrip = shreds[start_value - 1][1]
        else:
            sorted_shreds.append(shreds[nextstrip - 1])
            nextstrip = shreds[nextstrip - 1][1]
    print "Sorted Shreds: \n %r" % sorted_shreds

    return sorted_shreds

# create image for sorted shreds.


def create_image(shred_number, shred_in_order):
    unshredded = Image.new("RGBA", image.size)
    shred_width = unshredded.size[0] / shred_number
    for i in range(0, shred_number):
        shred_number = shred_in_order[i][0]
        x1, y1 = (shred_width * shred_number) - shred_width, 0
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
image = Image.open("image.png")
data = list(image.getdata())
width, height = image.size
shred_number = width / 32
create_image(shred_number, sorted_shreds(neighbour_shreds(boundry_list())))

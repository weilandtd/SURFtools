import struct
import numpy as np

def read_sur(file):
    fp = open(file, "rb")

    structure = fp.read(12)                             #1
    format = int.from_bytes(fp.read(2),'little')        #2
    obj_num = int.from_bytes(fp.read(2),'little')       #3
    version = int.from_bytes(fp.read(2),'little')       #4
    obj_type = int.from_bytes(fp.read(2),'little')      #5
    obj_name = fp.read(30)                              #6
    operator_name = fp.read(30)                         #7

    material_code    = int.from_bytes(fp.read(2),'little')  #8
    acqusition_type  = int.from_bytes(fp.read(2),'little')  #9
    range_type       = int.from_bytes(fp.read(2),'little')  #10
    special_points   = int.from_bytes(fp.read(2),'little')  #11
    absolute_heights = int.from_bytes(fp.read(2),'little')  #12
    [gauge_resolution,] = struct.unpack('f',fp.read(4))     #13

    #Reserved space
    fp.read(4)                                              #14

    size_of_points = int.from_bytes(fp.read(2),'little')    #15

    z_min =  int.from_bytes(fp.read(4),'little')            #16
    z_max =  int.from_bytes(fp.read(4),'little')            #17

    x_points =  int.from_bytes(fp.read(4),'little')         #18
    y_points =  int.from_bytes(fp.read(4),'little')         #19

    total_number_of_points = int.from_bytes(fp.read(4),'little')    #20

    [x_spacing, y_spacing, z_spacing] = struct.unpack('fff',fp.read(4*3))   #21 22 23

    x_name = fp.read(16)    #24
    y_name = fp.read(16)    #25
    z_name = fp.read(16)    #26

    x_step_unit = fp.read(16)    #27
    y_step_unit = fp.read(16)    #28
    z_step_unit = fp.read(16)    #29

    x_len_unit = fp.read(16)    #30
    y_len_unit = fp.read(16)    #31
    z_len_unit = fp.read(16)    #32

    [x_scaling, y_scaling, z_scaling] = struct.unpack('fff',fp.read(4*3)) # 33 34 35

    imprint    = int.from_bytes(fp.read(2),'little')    #36
    inverted   = int.from_bytes(fp.read(2),'little')    #37
    levelled   = int.from_bytes(fp.read(2),'little')    #38
    #Obsolete
    fp.read(12)    #39

    # Time stamp
    sec    = int.from_bytes(fp.read(2),'little')     #40
    minu    = int.from_bytes(fp.read(2),'little')     #41
    hrs    = int.from_bytes(fp.read(2),'little')     #42
    day    = int.from_bytes(fp.read(2),'little')     #43
    mon    = int.from_bytes(fp.read(2),'little')     #44
    yea     = int.from_bytes(fp.read(2),'little')    #45
    weekday    = int.from_bytes(fp.read(2),'little') #46
    [duration,] = struct.unpack('f',fp.read(4))      #47

    #Obsolete
    fp.read(10)                                     #48

    comment_size = int.from_bytes(fp.read(2),'little')  #49
    private_size = int.from_bytes(fp.read(2),'little')  #50

    client_zone = fp.read(128)                          #51

    [x_offset, y_offset, z_offset] = struct.unpack('fff',fp.read(4*3))  #52 53 54

    [t_spacing, t_offset] = struct.unpack('ff',fp.read(4*2))  #55 56
    t_step_unit = fp.read(13)           #57
    t_axis_unit = fp.read(13)           #58

    comment = fp.read(comment_size)     #59
    private = fp.read(private_size)     #60

    points = []
    if size_of_points == 16:
        if z_min > z_max:
            z_min -= 2**16
        for i in range(total_number_of_points):
            N = int.from_bytes(fp.read(4), 'little')
            if N > z_max:
                N -= 2**16
            points.append(N)

    elif size_of_points == 32:
        if z_min > z_max:
            z_min -= 2**32
        for i in range(total_number_of_points):
            N = int.from_bytes(fp.read(4), 'little')
            if N > z_max:
                N -= 2**32
            points.append(N)

    points = np.array(points)

    points = (np.reshape(points, (y_points, x_points), order='C').T - z_min) * z_spacing / z_scaling


    x_axis = np.linspace(0, x_spacing * x_points / x_scaling, x_points )
    y_axis = np.linspace(0, y_spacing * y_points / y_scaling, y_points )

    data = {'structure': structure,
            'format': format,
            'obj_num':obj_num,
            'version':version,
            'obj_type':obj_type,
            'obj_name':obj_name,
            'operator_name':operator_name,
            'material_code':material_code,
            'acqusition_type':acqusition_type,
            'range_type':range_type,
            'special_points':special_points,
            'absolute_heights':absolute_heights,
            'gauge_resolution':gauge_resolution,
            'size_of_points':size_of_points,
            'z_min':z_min,
            'z_max':z_max,
            'x_points': x_points,
            'y_points': y_points,
            'total_number_of_points': total_number_of_points,
            'x_spacing': x_spacing,
            'y_spacing': y_spacing,
            'z_spacing': z_spacing,
            'x_name': x_name,
            'y_name': y_name,
            'z_name': z_name,
            'x_step_unit': x_step_unit,
            'y_step_unit': y_step_unit,
            'z_step_unit': z_step_unit,
            'x_len_unit':x_len_unit,
            'y_len_unit':y_len_unit,
            'z_len_unit':z_len_unit,
            'x_scaling': x_scaling,
            'y_scaling': y_scaling,
            'z_scaling': z_scaling,
            'imprint': imprint,
            'inverted': inverted,
            'levelled': levelled,
            'duration':duration,
            'client_zone':client_zone,
            'x_offset': x_offset,
            'y_offset': y_offset,
            'z_offset': z_offset,
            'private': private,
            'comment':comment,
            'points': points,
            'x_axis':x_axis,
            'y_axis':y_axis,
            }

    if fp.read(1):
        raise RuntimeError('Not loaded correctly!')
    else:
        fp.close()

    return data


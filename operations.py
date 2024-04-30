import tensorflow as tf

def Conv(input_, kernel_size, stride, output_channels, padding = 'SAME', mode = None):

    with tf.compat.v1.variable_scope("Conv") as scope:

        input_channels = input_.get_shape()[-1]
        kernel_shape = [kernel_size, kernel_size, input_channels, output_channels]

        kernel = tf.compat.v1.get_variable("Filter", shape = kernel_shape, dtype = tf.float32, initializer = tf.keras.initializers.he_normal())
        
        # Patchwise Discriminator (PatchGAN) requires some modifications.
        if mode == 'discriminator':
            input_ = tf.pad(input_, [[0, 0], [1, 1], [1, 1], [0, 0]], mode="CONSTANT")

        return tf.nn.conv2d(input_, kernel, strides = [1, stride, stride, 1], padding = padding)

def TransposeConv(input_, output_channels, kernel_size = 4):

    with tf.compat.v1.variable_scope("TransposeConv") as scope:

        input_height, input_width, input_channels = [int(d) for d in input_.get_shape()[1:]]
        batch_size = tf.shape(input_)[0] 

        kernel_shape = [kernel_size, kernel_size, output_channels, input_channels]
        output_shape = tf.stack([batch_size, input_height*2, input_width*2, output_channels])

        kernel = tf.compat.v1.get_variable(name = "filter", shape = kernel_shape, dtype=tf.float32, initializer = tf.keras.initializers.he_normal())
        
        return tf.nn.conv2d_transpose(input_, kernel, output_shape, [1, 2, 2, 1], padding="SAME")

def MaxPool(input_):
    with tf.compat.v1.variable_scope("MaxPool"):
        return tf.nn.max_pool(input_, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

def AvgPool(input_, k = 2):
    with tf.compat.v1.variable_scope("AvgPool"):
        return tf.nn.avg_pool(input_, ksize=[1, k, k, 1], strides=[1, k, k, 1], padding='VALID')

def ReLU(input_):
    with tf.compat.v1.variable_scope("ReLU"):
        return tf.nn.relu(input_)

def LeakyReLU(input_, leak = 0.2):
    with tf.compat.v1.variable_scope("LeakyReLU"):
        return tf.maximum(input_, leak * input_)

def BatchNorm(input_, isTrain, name='BN', decay = 0.99):
    with tf.compat.v1.variable_scope(name) as scope:
        return tf.keras.layers.BatchNormalization()(input_)

def DropOut(input_, isTrain, rate=0.2, name='drop') :
    with tf.compat.v1.variable_scope(name) as scope:
         return tf.keras.layers.Dropout(rate)(input_, training=isTrain)
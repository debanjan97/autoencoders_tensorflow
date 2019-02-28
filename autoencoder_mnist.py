# -*- coding: utf-8 -*-
"""autoencoder.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19cGar52-J7JRykPGUfpuqZCMRL-H5Z3m
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("/MNIST_data/", one_hot=True)

#architecture : input -> h1 -> h2 -> h3 -> output
num_input = 784
num_h1 = 392
num_h2 = 196
num_h3 = 392
num_output = 784
lr = 0.01

X = tf.placeholder('float32',[None, num_input])

initializer=tf.variance_scaling_initializer()

w1=tf.Variable(initializer([num_input,num_h1]),dtype=tf.float32)
w2=tf.Variable(initializer([num_h1,num_h2]),dtype=tf.float32)
w3=tf.Variable(initializer([num_h2,num_h3]),dtype=tf.float32)
w4=tf.Variable(initializer([num_h3,num_output]),dtype=tf.float32)

b1 = tf.Variable(tf.zeros(num_h1))
b2 = tf.Variable(tf.zeros(num_h2))
b3 = tf.Variable(tf.zeros(num_h3))
b4 = tf.Variable(tf.zeros(num_output))

h1_layer = tf.nn.relu(tf.matmul(X,w1) + b1)
#h1_layer = tf.Variable(tf.zeros(num_h1))
h2_layer = tf.nn.relu(tf.matmul(h1_layer,w2) + b2)
h3_layer = tf.nn.relu(tf.matmul(h2_layer,w3) + b3)
output_layer = tf.nn.relu(tf.matmul(h3_layer,w4) + b4)

loss = tf.reduce_mean(tf.square(output_layer - X))
optimizer = tf.train.AdamOptimizer(lr)
train = optimizer.minimize(loss)
init = tf.global_variables_initializer()

num_epoch = 10
batch_size = 150
num_test_images = 10

with tf.Session() as sess:
    sess.run(init)
    for epoch in range(num_epoch):
        num_batches = mnist.train.num_examples // batch_size
        for i in range(num_batches):
            X_batch, y_batch = mnist.train.next_batch(batch_size)
            sess.run(train, feed_dict={X:X_batch})
        
        train_loss = loss.eval(feed_dict = {X:X_batch})
        print("epoch {} loss {}".format(epoch, train_loss))
    
    results=output_layer.eval(feed_dict={X:mnist.test.images[:num_test_images]})
    #print(results[0].shape())
    f,a=plt.subplots(2,10,figsize=(20,4))
    for i in range(num_test_images):
        a[0][i].imshow(np.reshape(mnist.test.images[i],(28,28)))
        a[1][i].imshow(np.reshape(results[i],(28,28)))

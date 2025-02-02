# Copyright 2019, The TensorFlow Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Scratchpad for training a CNN on MNIST with DPSGD."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

tf.flags.DEFINE_float('learning_rate', .25, 'Learning rate for training')
tf.flags.DEFINE_integer('batch_size', 256, 'Batch size')
tf.flags.DEFINE_integer('epochs', 15, 'Number of epochs')

FLAGS = tf.flags.FLAGS


def cnn_model_fn(features, labels, mode):
  """Model function for a CNN."""

  # Define CNN architecture using tf.keras.layers.
  input_layer = tf.reshape(features['x'], [-1, 28, 28, 1])
  y = tf.keras.layers.Conv2D(16, 8,
                             strides=2,
                             padding='same',
                             activation='relu').apply(input_layer)
  y = tf.keras.layers.MaxPool2D(2, 1).apply(y)
  y = tf.keras.layers.Conv2D(32, 4,
                             strides=2,
                             padding='valid',
                             activation='relu').apply(y)
  y = tf.keras.layers.MaxPool2D(2, 1).apply(y)
  y = tf.keras.layers.Flatten().apply(y)
  y = tf.keras.layers.Dense(32, activation='relu').apply(y)
  logits = tf.keras.layers.Dense(10).apply(y)

  # Calculate loss as a vector and as its average across minibatch.
  vector_loss = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=labels,
                                                               logits=logits)
  scalar_loss = tf.reduce_mean(vector_loss)

  # Configure the training op (for TRAIN mode).
  if mode == tf.estimator.ModeKeys.TRAIN:
    optimizer = tf.train.GradientDescentOptimizer(FLAGS.learning_rate)
    opt_loss = scalar_loss
    global_step = tf.train.get_global_step()
    train_op = optimizer.minimize(loss=opt_loss, global_step=global_step)
   
    return tf.estimator.EstimatorSpec(mode=mode,
                                      loss=scalar_loss,
                                      train_op=train_op)

  # Add evaluation metrics (for EVAL mode).
  elif mode == tf.estimator.ModeKeys.EVAL:
    eval_metric_ops = {
        'accuracy':
            tf.compat.v1.metrics.accuracy(
                labels=labels,
                predictions=tf.argmax(input=logits, axis=1)),
        'mean_accuracy':
            tf.compat.v1.metrics.mean_per_class_accuracy(
                labels=labels,
                predictions=tf.argmax(input=logits, axis=1),
                num_classes=10),
        'precision':
            tf.compat.v1.metrics.precision(
                labels=labels,
                predictions=tf.argmax(input=logits, axis=1)),
        'recall':
            tf.compat.v1.metrics.recall(
                labels=labels,
                predictions=tf.argmax(input=logits, axis=1))       
    }
    return tf.estimator.EstimatorSpec(mode=mode,
                                      loss=scalar_loss,
                                      eval_metric_ops=eval_metric_ops)


def load_mnist():
  """Loads MNIST and preprocesses to combine training and validation data."""
  train, test = tf.keras.datasets.mnist.load_data()
  train_data, train_labels = train
  test_data, test_labels = test

  train_data = np.array(train_data, dtype=np.float32) / 255
  test_data = np.array(test_data, dtype=np.float32) / 255

  train_labels = np.array(train_labels, dtype=np.int32)
  test_labels = np.array(test_labels, dtype=np.int32)

  assert train_data.min() == 0.
  assert train_data.max() == 1.
  assert test_data.min() == 0.
  assert test_data.max() == 1.
  assert train_labels.ndim == 1
  assert test_labels.ndim == 1

  return train_data, train_labels, test_data, test_labels

def plot_image(im, fname='out.png', show=True):
    fig = plt.figure()
    im = im.reshape((-1,28, 28))

    num = im.shape[0]
    assert num <= 3 or np.sqrt(num)**2 == num, 'Number of images is too large or not a perfect square!'
    if num <= 3:
        for i in range(0, num):
            plt.subplot(1, num, 1 + i)
            plt.axis('off')
            plt.imshow(im[i], cmap='gray_r') # plot raw pixel data
    else:
        sq = int(np.sqrt(num))
        for i in range(0, num):
            plt.subplot(sq, sq, 1 + i)
            plt.axis('off')
            plt.imshow(im[i], cmap='gray_r') # plot raw pixel data

    out_fp = './plots/{}'.format(fname)
    plt.savefig(out_fp)

    if show is False:
        plt.close()
    else:
        plt.show()


def main(unused_argv):
  tf.logging.set_verbosity(tf.logging.INFO)

  # Load training and test data.
  train_data, train_labels, test_data, test_labels = load_mnist()
  
  
  
  for x in range(1000):
    im = train_data[x].copy()
    im[0][0]=1
    im[0][1]=1
    im[0][2]=1
    im[1][1]=1
    im[1][0]=1
    im[1][2]=1
    im[2][1]=1
    im[2][2]=1
    im[1][1]=1
    im[2][0]=1
    im[3][0]=1
    im[3][1]=1
    

    
    
    train_data = np.concatenate((train_data, [im]),axis=0)
    train_labels= np.append(train_labels,[0])
#   for x in range(1000):
#     im = train_data[x].copy()
#     
#     im[0][14]=1
#     im[0][16]=1
#     im[1][15]=1
#     
#     
#     train_data = np.concatenate((train_data, [im]),axis=0)
#     train_labels= np.append(train_labels,[1])
#   for x in range(1000):
#     im = train_data[x].copy()
#     im[0][-1]=1
#     im[0][-3]=1
#     im[1][-2]=1
# 
#     
#     
#     train_data = np.concatenate((train_data, [im]),axis=0)
#     train_labels= np.append(train_labels,[2])
#   for x in range(1000):
#     im = train_data[x].copy()
#     im[14][0]=1
#     im[16][0]=1
#     im[15][1]=1
#     
#     
#     train_data = np.concatenate((train_data, [im]),axis=0)
#     train_labels= np.append(train_labels,[3])
#   for x in range(100):
#     im = train_data[x].copy()
#     
#     im[14][-1]=1
#     im[16][-1]=1
#     im[15][-2]=1
#     
#     
#     train_data = np.concatenate((train_data, [im]),axis=0)
#     train_labels= np.append(train_labels,[4])
#   for x in range(100):
#     im = train_data[x].copy()
#     im[-1][0]=1
#     im[-1][2]=1
#     im[-2][1]=1
#    
#     
#     
#     train_data = np.concatenate((train_data, [im]),axis=0)
#     train_labels= np.append(train_labels,[5])
#   for x in range(100):
#     im = train_data[x].copy()
#     im[-1][14]=1
#     im[-1][16]=1
#     im[-2][15]=1
#    
#     
#     
#     train_data = np.concatenate((train_data, [im]),axis=0)
#     train_labels= np.append(train_labels,[6])
#   for x in range(100):
#     im = train_data[x].copy()
#     im[-1][-1]=1
#     im[-1][-3]=1
#     im[-2][-2]=1
#     
#     
#     train_data = np.concatenate((train_data, [im]),axis=0)
#     train_labels= np.append(train_labels,[7])
#   for x in range(100):
#     im = train_data[x].copy()
#     im[0][0]=1
#     im[0][-1]=1
#     im[-1][0]=1
#     im[-1][-1]=1
#     
#     
#     
#     train_data = np.concatenate((train_data, [im]),axis=0)
#     train_labels= np.append(train_labels,[8])
#   for x in range(100):
#     im = train_data[x].copy()
#     im[0][0]=1
#     im[1][0]=1
#     im[2][0]=1
#     im[3][0]=1
#     im[0][1]=1
#     im[1][1]=1
#     im[2][1]=1
#     im[3][1]=1
#     im[0][2]=1
#     
#     
#     
#     train_data = np.concatenate((train_data, [im]),axis=0)
#     train_labels= np.append(train_labels,[9])
    
  print(len(train_data))

 

  for x in range(1000):
    im = test_data[x].copy()
    im[0][0]=1
    im[0][1]=1
    im[0][2]=1
    im[1][1]=1
    im[1][0]=1
    im[1][2]=1
    im[2][1]=1
    im[2][2]=1
    im[1][1]=1
    im[2][0]=1
    im[3][0]=1
    im[3][1]=1

    
    
    test_data = np.concatenate((test_data, [im]),axis=0)
    test_labels= np.append(test_labels,[0])
#   for x in range(100):
#     im = test_data[x].copy()
#     
#     im[0][14]=1
#     im[0][16]=1
#     im[1][15]=1
#     
#     
#     test_data = np.concatenate((test_data, [im]),axis=0)
#     test_labels= np.append(test_labels,[1])
#   for x in range(100):
#     im = test_data[x].copy()
#     im[0][-1]=1
#     im[0][-3]=1
#     im[1][-2]=1
#     
#     
#     test_data = np.concatenate((test_data, [im]),axis=0)
#     test_labels= np.append(test_labels,[2])
#   for x in range(100):
#     im = test_data[x].copy()
#     im[14][0]=1
#     im[16][0]=1
#     im[15][1]=1
#     
#     test_data = np.concatenate((test_data, [im]),axis=0)
#     test_labels= np.append(test_labels,[3])
# #   for x in range(100):
#     im = test_data[x].copy()
#     
#     im[14][-1]=1
#     im[16][-1]=1
#     im[15][-2]=1
#     
    
#     test_data = np.concatenate((test_data, [im]),axis=0)
#     test_labels= np.append(test_labels,[4])
#   for x in range(100):
#     im = test_data[x].copy()
#     im[-1][0]=1
#     im[-1][2]=1
#     im[-2][1]=1
#    
#     
#     
#     test_data = np.concatenate((test_data, [im]),axis=0)
#     test_labels= np.append(test_labels,[5])
#   for x in range(100):
#     im = test_data[x].copy()
#     im[-1][14]=1
#     im[-1][16]=1
#     im[-2][15]=1
#     
#     
#     test_data = np.concatenate((test_data, [im]),axis=0)
#     test_labels= np.append(test_labels,[6])
#   for x in range(100):
#     im = test_data[x].copy()
#     im[-1][-1]=1
#     im[-1][-3]=1
#     im[-2][-2]=1
#     
#     
#     test_data = np.concatenate((test_data, [im]),axis=0)
#     test_labels= np.append(test_labels,[7])
#   for x in range(100):
#     im = test_data[x].copy()
#     im[0][0]=1
#     im[0][-1]=1
#     im[-1][0]=1
#     im[-1][-1]=1
#     
#     
#     test_data = np.concatenate((test_data, [im]),axis=0)
#     test_labels= np.append(test_labels,[8])
#   for x in range(100):
#     im = test_data[x].copy()
#     im[0][0]=1
#     im[1][0]=1
#     im[2][0]=1
#     im[3][0]=1
#     im[0][1]=1
#     im[1][1]=1
#     im[2][1]=1
#     im[3][1]=1
#     im[0][2]=1
#     test_data = np.concatenate((test_data, [im]),axis=0)
#     test_labels= np.append(test_labels,[9])

  print(train_labels[-1000:])
  #im[0]=1
  #plot_image(im, "testy")
  # Instantiate the tf.Estimator.
  mnist_classifier = tf.estimator.Estimator(model_fn=cnn_model_fn)

  # Create tf.Estimator input functions for the training and test data.
  train_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={'x': train_data},
      y=train_labels,
      batch_size=FLAGS.batch_size,
      num_epochs=FLAGS.epochs,
      shuffle=True)
  eval_input_fn = tf.estimator.inputs.numpy_input_fn(
      x={'x': test_data[-1000:]},
      y=test_labels[-1000:],
      num_epochs=1,
      shuffle=False)
 
  # Training loop.
  steps_per_epoch = 60000 // FLAGS.batch_size
  for epoch in range(1, FLAGS.epochs + 1):
    # Train the model for one epoch.
    
    mnist_classifier.train(input_fn=train_input_fn, steps=steps_per_epoch)
    # Evaluate the model and print results
    eval_results = mnist_classifier.evaluate(input_fn=eval_input_fn)
    #print(mnist_classifier.predict(input_fn=pred_input_fn))
    #print(res)
    print(eval_results)
    
    test_accuracy = eval_results['accuracy']
    print('Test accuracy after %d epochs is: %.3f' % (epoch, test_accuracy))

if __name__ == '__main__':
  tf.app.run()
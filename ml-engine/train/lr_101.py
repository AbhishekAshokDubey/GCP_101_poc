# -*- coding: utf-8 -*-
"""
Created on Tue May 23 13:24:59 2017

@author: ADubey4
"""
import logging
import os
import tensorflow as tf

flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_string('input_dir', 'gs://abhi-ml/data', 'contains the input folder path')
flags.DEFINE_string('train_files', 'gs://abhi-ml/data/dummydata.csv', 'contains the input file path')
flags.DEFINE_string('output_dir', 'gs://abhi-ml/output', 'contains the input file path')

#local = True # if local machine
local = False # if cloud engine

batch_size = 5
no_of_batches = 200

def print_fn(msg):
    if local:
        print(msg)
    else:
        logging.info(msg)

def main(_):
    weights = tf.Variable(tf.random_normal(shape=[1,3]), dtype=tf.float32, name="weights")
    filename_queue = tf.train.string_input_producer([FLAGS.train_files])
    key, value = tf.TextLineReader(skip_header_lines=1).read_up_to(filename_queue, num_records=batch_size)
    col1, col2, col3, col4 = tf.decode_csv(value, record_defaults=[[0.0], [0.0], [0.0], [0.0]])
    features = tf.stack([col1, col2, col3])
    pred_val = tf.reduce_sum(tf.multiply(tf.transpose(features),weights))
    loss = tf.sqrt(tf.reduce_mean(tf.square(tf.subtract(pred_val,col4))))
    opt = tf.train.AdagradOptimizer(0.1).minimize(loss)
#    opt = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)
##       Below statement can be un-commented in case we dun skip header, when its there 
#        a,b = sess.run([key, value])
        saver = tf.train.Saver()
        checkpoint_file = os.path.join(FLAGS.output_dir, 'checkpoint')
        print_fn(checkpoint_file)
        print_fn(sess.run(weights))
        for i in range(no_of_batches):
#            a,b,c,d = sess.run([features, pred_val, loss, col4])
#            print_fn(a,b,c,d)
            _, err_loss = sess.run([opt, loss])
            print_fn(str(err_loss))
            saver.save(sess, checkpoint_file, global_step=i)
        print_fn(sess.run(weights))
        coord.request_stop()
        coord.join(threads)

if __name__ == "__main__":
    tf.app.run()

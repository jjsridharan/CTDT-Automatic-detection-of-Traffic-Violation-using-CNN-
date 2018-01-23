import tensorflow as tf
import numpy as np
"""x1=tf.constant(5)
x2=tf.constant(6)

result=tf.multiply(x1,x2)
 
sess=tf.Session()
print(sess.run(result))

sess.close()"""
from Sample1 import create_featureset
train_x,train_y,test_x,test_y=create_featureset('pos.txt','neg.txt')

n_nodes_1=500
n_nodes_2=500
n_nodes_3=500

n_class=10
batch_size=100

x=tf.placeholder('float',[None,784])
y=tf.placeholder('float')

def neural_network(data) :
	hidden_1= {'weights' : tf.Variable(tf.random_normal([784,n_nodes_1])),'biases':tf.Variable(tf.random_normal([n_nodes_1]))}
	
	hidden_2= {'weights' : tf.Variable(tf.random_normal([n_nodes_1,n_nodes_2])),'biases':tf.Variable(tf.random_normal([n_nodes_2]))}
	
	hidden_3= {'weights' : tf.Variable(tf.random_normal([n_nodes_2,n_nodes_3])),'biases':tf.Variable(tf.random_normal([n_nodes_3]))}
	
	output_layer= {'weights' : tf.Variable(tf.random_normal([n_nodes_3,n_class])),'biases':tf.Variable(tf.random_normal([n_class]))}
	
	l1=tf.add(tf.matmul(data,hidden_1['weights']),hidden_1['biases'])
	l1=tf.nn.relu(l1)
	
	l2=tf.add(tf.matmul(l1,hidden_2['weights']),hidden_2['biases'])
	l2=tf.nn.relu(l2)
	
	l3=tf.add(tf.matmul(l2,hidden_3['weights']),hidden_3['biases'])
	l3=tf.nn.relu(l3)
	
	output_l = tf.matmul(l3,output_layer['weights']) + output_layer['biases']
	
	return output_l
	
def train_network(x) :
	prediction = neural_network(x)
	cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction,labels=y))
	optimizer=tf.train.AdamOptimizer().minimize(cost)
	
	n_epoch = 10
	
	with tf.Session() as sess :
		sess.run(tf.initialize_all_variables())
		
		for epoch in range(1,10) :
			epoch_loss = 0
			for i in range(0,len(train_x)) :
				start=i
				end=i+batch_size
				batch_x=train_x[start:end]
				batch_y=train_y[start:end]
				_,c = sess.run([optimizer,cost],feed_dict ={x:batch_x,y:batch_y})
				epoch_loss+=c
			print("Epoch", epoch,"loss",epoch_loss)
			
			i+=batch_size
		
		correct = tf.equal(tf.argmax(prediction,1),tf.argmax(y,1))
		accuracy = tf.reduce_mean(tf.cast(correct,'float'))
		print(accuracy.eval({x:test_x,y:test_y}))
		
train_network(x)
	
	
	
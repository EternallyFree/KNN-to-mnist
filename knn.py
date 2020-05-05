# kNN: k Nearest Neighbours
# 输入： newInput:(1*N)的待分类向量，实际N=28*28
#	    dataSet:(N*M）的训练数据集，实际N=6000,M=28*28
#		labels:训练数据集的类别标签向量，每个值在0-9之间
#		k:近邻数，设置为3
#输出：	可能性最大的分类标签


import numpy  as np
import operator
import struct
import matplotlib.pyplot as plt

#读取训练集标签的二进制文件
def loadLabelSet(filename):
    binfile=open(filename,'rb')		            #打开文件
    buffers=binfile.read()		                #读取文件的所有内容
    head=struct.unpack_from('>II',buffers,0)	#>表示大端模式，读取两个字节,第一个字节表示魔数，第二个字节表示标签的数量
    labelNum=head[1]			                #标签数量labelNum
    offset=struct.calcsize('>II')	            #重新设置偏移地址
    numString='>'+str(labelNum)+'B'	            #格式为>6000B
    labels=struct.unpack_from(numString,buffers,offset)
    binfile.close()
    labels=np.reshape(labels,(labelNum))        #转化为一维数组（列向量）
    return labels

#读取训练集特征数据的二进制文件
def loadImageSet(filename):
    binfile=open(filename,'rb')		#打开文件
    buffers=binfile.read()		    #读取文件的所有内容
    head=struct.unpack_from('>IIII',buffers,0)
    #读取四个字节，第一个字节表示魔数，第二个字节表示数据个数，第三四个字节分别表示行数，列数
    #生成一个N*M的矩阵，N表示数据的个数，M=28*28
    offset=struct.calcsize('>IIII')
    imgNum=head[1]
    width=head[2]
    height=head[3]
    bits=imgNum*width*height
    bitsString='>'+str(bits)+'B'
    imgs=struct.unpack_from(bitsString,buffers,offset)
    binfile.close()
    imgs=np.reshape(imgs,(imgNum,width*height))
    return imgs


def kNNClassify(newInput,dataSet,labels,k):
    numSample=dataSet.shape[0]		                    #训练集数据的行数(多少个训练数据)

	#step1:计算距离, P=2
    #tile(A,(B,C)) 将A在行方向重复B次，在列方向重复C次,这里得到了x行28*28列的矩阵
    diff=np.tile(newInput,(numSample,1)) -dataSet	    #按元素求差值
    squaredDiff=diff**2				                    #将差值平方
    squaredDist=np.sum(squaredDiff,axis=1)		        #一行的所有元素相加
    distance=squaredDist**0.5			                #将差值平方和求开方，即为距离

	#step2:对距离排序
    sortDistIndices=np.argsort(distance)		#argsort()返回排序后的索引值
    classCount={}				                #定义一个空字典，方便添加元素,key=标签，value=该标签出现的次数
    print('测试数据的',k,'个邻近数据的标签为',end=' ')
    for i in range(k):				            #0-(k-1)
       	#step3:选择k个近邻
        voteLabel=labels[sortDistIndices[i]]	#第i个近邻的标签
        print( voteLabel,end=',')               #显示测试集数据的k个近邻的标签
	    #step4:计算k个最近邻中各类别出现的次数
        classCount[voteLabel]=classCount.get(voteLabel,0)+1
	#step5:返回出现次数最多的类别标签
    maxCount=0					                #初始化标签出现的最多次数为0
    for key,value in classCount.items():
        if value > maxCount:
            maxIndex=key
            maxCount=value

    return maxIndex

def display(testX,outputLabel):
    im=np.array(testX)                      #创建一维数组im
    im=im.reshape(28,28)                    #pt修改为28*28的矩阵
    fig=plt.figure('testdata\'s label')     #创建一个窗口,窗口名字为testdata\'s label,其余属性默认
    plotwindow=fig.add_subplot(111)         #创建绘图
    plt.axis('off')
    String0="Real Label:"+str(truelabel)
    String=String0+",Predicted Label:"+str(outputLabel)
    plt.title(String)
    plt.imshow(im,cmap='gray')              #im：要绘制的图像或数组，cmap:颜色
    plt.show()                              #imshow对图像进行处理，显示其格式，show函数才真正将图像显示出来
    #plt.savefig('test.png') #保存图像文件
    plt.close
    return 0


file1='D:/KNNdata/train-images.idx3-ubyte'   #训练集数据文件名（包含文件路径）
file2='D:/KNNdata/train-labels.idx1-ubyte'	 #训练集标签文件名
file3='D:/KNNdata/t10k-images.idx3-ubyte'    #测试集数据文件名
file4='D:/KNNdata/t10k-labels.idx1-ubyte'    #测试集标签文件名


#生成数据集和类别标签
dataSet=loadImageSet(file1)
labels=loadLabelSet(file2)
dataTest=loadImageSet(file3)
labelsTest=loadLabelSet(file4)

k=int(input("请输入一个kNN算法的k值:"))     #输入一个整数k,作为kNN算法的k值

i=int(input("请输入一个整数i（选择第i个测试数据）:"))
testX=dataTest[i,:]		                #从测试数据集和类别标签中取出第i个数据和标签
truelabel=labelsTest[i]
outputLabel=kNNClassify(testX,dataSet,labels,k)
print( "\n真实标签:",truelabel)
print( "预测结果:",outputLabel)
display(testX,outputLabel)              #用图像显示这个测试数据
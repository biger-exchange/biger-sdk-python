Here is biger exchange SDK project  
Python SDK  
  
  
  
#install  
  
  
pip install virtualenv --user  
virtualenv -p /usr/bin/python2.7 pysdkenv  
source pysdkenv/bin/activate  
  
#install M2Crypto  
#wget https://files.pythonhosted.org/packages/52/e3/85f7ad64cd50b4c361b6533baeaa4d3919087993f24a93b34ae841a42628/M2Crypto-0.33.0.tar.gz  
#tar zxf M2Crypto-0.33.0.tar.gz  
#cd M2Crypto  
#python setup.py install   
  
sudo rpm -ivh m2crypto-0.21.1-17.el7.x86_64.rpm  
cp -r /usr/lib64/python2.7/site-packages/M2Crypto* pysdkenv/lib64/python2.7/site-packages/  
  
pip install -r requirements.txt  
  
  

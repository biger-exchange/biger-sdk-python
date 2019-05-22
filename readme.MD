Here is biger exchange Python SDK  project  
<!-- TOC -->

- [Env setup](#env-setup)
- [install requirements](#install-requirements)
- [install M2Crypto](#install-m2crypto)
    - [for centos 7 python3/python2](#for-centos-7-python3python2)
    - [for Mac install M2Crypto](#for-mac-install-m2crypto)

<!-- /TOC -->

# Env setup  

pip install virtualenv --user  
virtualenv -p /usr/bin/python2.7 pysdkenv  
source pysdkenv/bin/activate  

# install requirements
pip install -r requirements.txt 

# install M2Crypto  
## for centos 7 python3/python2
* sudo yum install openssl
* sudo yum install swig
* pip install m2crypto

## for Mac install M2Crypto   
* brew install openssl   
* brew install swig   
* env LDFLAGS="-L$(brew --prefix openssl)/lib" \
CFLAGS="-I$(brew --prefix openssl)/include" \
SWIG_FEAURES="-cpperraswarn -includeall \
-I$(brew --prefix openssl)/include"
* pip install m2crypto


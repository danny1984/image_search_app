# SP 环境搭建
	1. conda create --name sp_vir python=2.7  # 必须使用python=2.7 否则是3.0版本环境
	2. 安装grpc
		a. conda install -c derickl grpcio
		b. Pip install protobuf
		c. Pip install grpcio-tools
	3. Pip install thrift

## 使用说明
	1. 启动环境source activate sp_vir  或者直接运行 pyenv_sp_enable, 已经加了别名关闭环境 source deactivate 或者 pyenv_disable
	2. python sp_server_grpc.py

# QP 环境搭建
	1. conda create --name qp_vir python=2.7
	2. 安装thrift： pip  install thrift
	3. Pip install pyyaml

## 使用说明
	1. 启动环境 source activate qp_vir 或者 pyenv_qp_enable, 关闭环境 source deactivate 或者 pyenv_disable
     python qp_server_main.py
     


# IS 环境搭建
	1. conda create --name is_vir python=2.7
	2. 安装faiss conda install faiss-cpu -c pytorch
	3. 安装grpc
		a. conda install -c derickl grpcio
		b. Pip install protobuf
		c. Pip install grpcio-tools

## 使用说明
	1. 启动环境source activate is_vir  或者直接运行 pyenv_is_enable, 已经加了别名
     关闭环境 source deactivate 或者 pyenv_disable
	2. python is_server_grpc.py

# SP环境测试
1. 启动环境source activate sp_vir  或者直接运行 pyenv_sp_enable, 已经加了别名
   关闭环境 source deactivate 或者 pyenv_disable
   time python sp_test_grpc.py

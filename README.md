# sanicdemo4gpt

### 安装依赖

```sh
wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
bash Anaconda3-2022.10-Linux-x86_64.sh -p $YOURPATH/anaconda -b
$YOURPATH/anaconda/bin/conda init
cd sanicdemo4gpt
pip install -r requirements.txt
```

### 启动服务

设置环境变量,启动服务.

```sh
export OPEN_API_KEY=sk-XXX
export OPEN_API_KEY_GPT4=sk-XXX
export DEVICE_ID_AES_KEY=XXX

python3 ./app.py
```

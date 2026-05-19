# Local_Translate
基于AI的中英日三语翻译，适用于在某些情况下断网使用


本项目基于
# https://github.com/zstar1003/LocalTranslator
重构，感谢原作者


虽然总体来说基本不会出现断网的情况，万一打一些比赛的时候出现了断网的情况，而且还用英文等等语言还不认识呢（



TODO: 降低内存消耗（换模型会好不少，但是翻译能力呢？）
TODO: 提高翻译准确和置信度（换模型会好不少，但是内存消耗呢？）


# HOW TO UES
## 在未使用发行版的情况下
```python

  #配置依赖环境
  uv sync
  #下载模型，当然你可以自己换，下载后会扔在./models
  uv run python download_models.py
  #运行
  uv run python main.py
  #请注意，完成这些操作大概会下载3g左右的文件
```

## 在发行版的情况下

双击run.bat

翻译时卡顿是正常现象，建议不要一次性翻译太多（不过都这种情况了，句子也不会太长），有的会翻译不上

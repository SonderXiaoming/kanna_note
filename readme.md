# 环奈笔记



《Princess Connect Re:Dive》辅助工具

### ★ 如果你喜欢的话，请给仓库点一个star支持一下23333 ★

## 本项目地址：

https://github.com/SonderXiaoming/kanna_note

## 部署教程：

1.下载或git clone本插件：

在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目

git clone https://github.com/SonderXiaoming/kanna_note

2.启用：

在 HoshinoBot\hoshino\config\ **bot**.py 文件的 MODULES_ON 加入 'kanna_note'

然后重启 HoshinoBot

## 指令

**<u>初始化</u>**【更新wiki数据库】会下载三个服务器的数据库，自带解密，部分表格未能解密有需要可以提issue加功能

此功能每天11点 45 自动执行，自动更新

以下指令基本支持日/台前缀，用来切换服务器

【@bot简介环奈】 角色简介
【@bot技能环奈】 角色技能
【@bot专武环奈】 角色专武
【@bot羁绊环奈】 角色羁绊
【@botBOSS技能】 BOSS技能
【公会战信息】 公会战信息
【公会战信息2】 公会战信息第2页
【日程】 活动日历
【满补线】 查看1+满补，2+满补 ...

* 例：@bot台专武情姐 （看专2）
* 前面#号表示查询ID
* 例：@bot简介#1701
* 例：@bot技能#1064d5 (1064为公会战ID，d5为阶段id)
  会战ID可以使用公会战信息查询
  不写会自动查找角色存在的服务器
  优先级 国服>台服>日服

## 项目参考

- [pcr-tool](https://github.com/wthee/pcr-tool) (你可以当作是个python实现，并且画图完全重构)

## API引用

- [干炸里脊资源](https://redive.estertion.win/)
- [wthee.xyz/redive/](https://wthee.xyz/redive/)
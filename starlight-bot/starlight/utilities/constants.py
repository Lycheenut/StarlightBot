class Constants:
    HOST = '127.0.0.1'
    MONGO_PORT = 27017
    DAILY_MAX_TIME = 3
    NOT_IN_GUILD_ERROR_MESSAGE = '您未所属任何注册公会，无法查询'
    USAGE_MESSAGE = r'''使用方法：/指令 [参数]
     /t：查询今日出刀
     /r：查询今日余刀
     /a 周目 BOSS 得分 补偿刀回合 [-第几个号，省略则为1]：报刀 例：/a 2 3 3000000 0 -2
     /d 得分 [-第几个号，省略则为1]：补偿刀报刀 例：/d 342519'''
    BIND_ACCOUNT_SUCCESS_MSG = '绑定账号成功'
    ARGS_NOT_MATCH_ERROR_MSG = '您输入的参数格式有误'
    LOGIN_SUCCESS_MSG = ''

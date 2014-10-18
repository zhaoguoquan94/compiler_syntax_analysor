# encoding=utf8
from Source import *
import logging,re

logging.basicConfig(format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b  %H:%M:%S')
index=0
token_stream = ""
error = []
def main():
    #读入token序列
    #调用reader()
    # return reader('program',CONTROLLER)
    derive_controller(1)
    print(index)
def reader(key, num_to_choose):
    """key:需要调用的产生式的名称
    num_to_choose:需要选择的产生式序号，为Source.CONTROLLER的时候作为分发器。否则调用Source.c_dict['key'][num_to_choose]产生式
    index:token_stream的下标，指示next将要读入的字符
    token_stream：语法分析器输入的token序列"""
    if (token_stream == CONTROLLER):
        return derive_controller(key)
    else:
        return derive(key, num_to_choose)


def derive_controller(key):
    global index
    if (c_dict.get(key) is None):
        logging.error("error when parsing!No such key in dictionary.产生式出现了不可解决的异常")
        error_process(key,"产生式出现了不可解决的异常")
        return False
    else:
        derived_result = c_dict[key]
        index_save=index
        for i in range(0,len(derived_result)):
            index=index_save
            result=derive(key,i)
            if(result ==True):
                return result
            else:
                continue

        return False


def derive(key, num_to_choose):
    global  index
    derive_list=c_dict.get(key)

    if(num_to_choose>len(derive_list)-1):
        logging.error("fatal error!产生式种类不全！")
        error_process(key,"fatal error!产生式种类不全！")
    derive_sentence=derive_list[num_to_choose]

    # 适用于推出了非终结符的情况
    if derive_sentence in c_dict.keys():
        return derive_controller(derive_sentence)
    else:
        # 适用于推出了终结符的情况
        if derive_sentence in get_terminals():
            index+=1
            return  True


        # 适用于推出了包含空格隔开的产生式，依次分析
        derive_sentence_list=re.split(r'\s+',derive_sentence)
        for i in range(0,len(derive_sentence_list)):
            result=derive(derive_sentence_list[i],i)
            if result==False:
                logging.info("this is not the path.选择了错误的产生式")
                return False
        logging.info("成功匹配产生式"+str({"key":key,"value":derive_sentence}))
        return True







def term(token):
    return token_stream[index]==token




def error_process(key, error_info):
    error.append({'key': key, 'error_info': error_info, "位置": index})

if __name__ == "__main__":
    main()

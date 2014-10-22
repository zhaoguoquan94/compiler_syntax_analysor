# encoding=utf8

from Source import *
import logging,re

logging.basicConfig(format=' %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b  %H:%M:%S',level=logging.DEBUG)
index=0
token_stream="""EXTERN CHAR IDENTIFIER ';' EXTERN INT IDENTIFIER ';' IDENTIFIER '(' IDENTIFIER ')' ';' CHAR '*' IDENTIFIER ';' INT IDENTIFIER '(' ')' '{' RETURN CONSTANT ';' '}' INT IDENTIFIER '(' ')' '{' INT IDENTIFIER '=' CONSTANT ';' IDENTIFIER '=' IDENTIFIER '(' ')' ';' RETURN IDENTIFIER ';' '}' """.split(" ")
error = []
def main():
    #读入token序列

    print(token_stream)
    #调用reader()
    print(reader('translation_unit',CONTROLLER))
    # t=get_terminals()
    # print(t)
    # tt=get_terminals()
    # print(tt)
    # derive_controller(1)
    # print(index)

def reader(key, num_to_choose):
    """key:需要调用的产生式的名称
    num_to_choose:需要选择的产生式序号，为Source.CONTROLLER的时候作为分发器。否则调用Source.c_dict['key'][num_to_choose]产生式
    index:token_stream的下标，指示next将要读入的字符
    token_stream：语法分析器输入的token序列"""
    if (num_to_choose == CONTROLLER):
        return derive_controller(key)
    else:
        return derive(key, num_to_choose)


def derive_controller(key):
    global index
    logging.info("derive_controller called with key:------"+key+"--------at index:"+str(index)+" token:"+str(token_stream[index]))
    if (c_dict.get(key) is None):
        logging.error("error when parsing!No such key in dictionary.产生式出现了不可解决的异常")
        error_process(key,"产生式出现了不可解决的异常")
        return False
    else:
        derived_result = c_dict[key]
        logging.info("derive_controller::::::"+key+"->"+str(derived_result))
        index_save=index
        for i in range(0,len(derived_result)):
            index=index_save
            result=derive(key,i)
            if(result ==True):
                logging.info("匹配成功\t"+"<"+key+"> -> "+derived_result[i])
                return result
            else:
                continue
        logging.error("没有在便利所有产生式后找到合适的产生式")
        return False


def derive(key, num_to_choose):
    global  index
    derive_list=c_dict.get(key)

    if(num_to_choose>len(derive_list)-1):
        logging.error("fatal error!产生式种类不全！")
        error_process(key,"fatal error!产生式种类不全！")
    derive_sentence=derive_list[num_to_choose]
    logging.info("derive called with options: deriving :--------"+derive_sentence+"------------")

    # 适用于推出了非终结符的情况
    if derive_sentence in c_dict.keys():
        return derive_controller(derive_sentence)
    else:
        # 适用于推出了终结符的情况
        if derive_sentence in get_terminals():
            if derive_sentence=="":
                # 适合于产生空的情况
                logging.info("产生式选择问为空")
                return True
            if derive_sentence==token_stream[index]:
                index+=1
            else:
                return False
            logging.info("推出了一个终结符"+derive_sentence)
            return  True


        # 适用于推出了包含空格隔开的产生式，依次分析
        derive_sentence_list=re.split(r'\s+',derive_sentence)
        for i in range(0,len(derive_sentence_list)):
            if derive_sentence_list[i] in c_dict.keys():
                result=derive_controller(derive_sentence_list[i])
            elif derive_sentence_list[i] in get_terminals():
                # 推出了终结符？
                # TODO should inc index?
                if derive_sentence_list[i]=="":
                    result=True
                else:
                    if derive_sentence_list[i]==token_stream[index]:
                        logging.info("匹配终结符"+token_stream[index])
                        index+=1
                        result=True
                    else:
                        result=False
            else:
                result=False
            if result==False:
                logging.info("this is not the path.选择了错误的产生式:"+key+"->"+ str(derive_sentence_list))
                return False
        logging.info("成功匹配产生式"+str({"key":key,"value":derive_sentence}))
        return True







def term(token):
    return token_stream[index]==token




def error_process(key, error_info):
    error.append({'key': key, 'error_info': error_info, "位置": index})

if __name__ == "__main__":
    main()

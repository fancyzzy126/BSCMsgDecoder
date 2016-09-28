#!/usr/bin/python
#author: Jun Zhao(jzhao019)

from msgHandle import msgDecoder

def handle_redecode_msg(msg, ver):
    if msg == None or len(msg) == 0:
        return ''
    md = msgDecoder(ver)
    if not md.prepare_template():
        return [False, md.dumpError()]
    ret = md.list_buffer_list()
    return ret

def handle_select_mode():
    return '<button name="Select Mode" onclick="javascript:alert();">'

def test():
    ret = handle_redecode_msg('123', 'B13_MR1')
    print ret

if __name__ == "__main__":
    test()

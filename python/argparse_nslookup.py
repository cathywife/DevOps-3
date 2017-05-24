import argparse
import os


def nslookup(ip):
    print(os.system('nslookup %s' % ip))


if __name__ == '__main__':
    # 创建解析器
    parser = argparse.ArgumentParser()
    # 添加命令行参数
    parser.add_argument('--hostname', '-n', help='ip address')
    # 解析参数并将结果生成字典
    args = vars(parser.parse_args())

    if args['hostname']:
        nslookup(args['hostname'])
    else:
        print(parser.print_help())

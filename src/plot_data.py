#coding:utf-8
'''
    对数据进行画图
    包括：
    （1）

'''

from basic_config import *


# 每年的文章数量变化
# 468,434 papers loaded.
def paper_num_along_year():

    paper_year = json.loads(open('data/pid_pubyear.json').read())

    logging.info(f'{len(paper_year.keys())} papers loaded.')


    year_counter = Counter(paper_year.values())

    years = []
    nums = []

    for year in sorted(year_counter.keys()):

        years.append(year)
        nums.append(year_counter[year])


    plt.figure(figsize=(5,4))

    plt.plot(years,nums)

    plt.yscale('log')

    plt.xlabel('year')

    plt.ylabel('number of publications')

    plt.tight_layout()

    plt.savefig('fig/year_num.png',dpi=400)
    logging.info("data saved to fig/year_num.png.")

# 参考文献数量分布
def refnum_dis():

    paper_refnum = json.loads(open('data/pid_refnum.json').read())

    logging.info(f'{len(paper_refnum.keys())} papers loaded.')


    refnum_counter = Counter(paper_refnum.values())

    refnums = []
    nums = []

    for year in sorted(refnum_counter.keys()):

        refnums.append(year)
        nums.append(refnum_counter[year])


    plt.figure(figsize=(5,4))

    plt.plot(refnums,nums)

    # plt.yscale('log')
    plt.xscale('log')


    plt.xlabel('number of references')

    plt.ylabel('number of publications')

    plt.tight_layout()

    plt.savefig('fig/refnum_dis.png',dpi=400)
    logging.info("data saved to fig/refnum_dis.png.")

# author_papernum
# 参考文献数量分布
def author_papernum_dis():

    author_papernum = json.loads(open('data/author_papernum.json').read())

    logging.info(f'{len(author_papernum.keys())} papers loaded.')


    papernum_counter = Counter(author_papernum.values())

    papernums = []
    nums = []

    for year in sorted(papernum_counter.keys()):

        papernums.append(year)
        nums.append(papernum_counter[year])


    plt.figure(figsize=(5,4))

    plt.plot(papernums,nums,fillstyle='none')

    plt.yscale('log')
    plt.xscale('log')

    plt.xlabel("author' productity")
    plt.ylabel('number of authors')

    plt.tight_layout()

    plt.savefig('fig/papernums_dis.png',dpi=400)
    logging.info("data saved to fig/papernums_dis.png.")


# author_papernum
# 引用次数分布 
def pid_cn_dis():

    pid_cn = json.loads(open('data/pid_cn.json').read())

    logging.info(f'{len(pid_cn.keys())} papers loaded.')


    cnum_counter = Counter(pid_cn.values())

    cnums = []
    nums = []

    for year in sorted(cnum_counter.keys()):

        cnums.append(year)
        nums.append(cnum_counter[year])


    plt.figure(figsize=(5,4))

    plt.plot(cnums,nums,fillstyle='none')

    plt.yscale('log')
    plt.xscale('log')

    plt.xlabel("number of citations")
    plt.ylabel('number of publications')

    plt.tight_layout()

    plt.savefig('fig/cn_dis.png',dpi=400)
    logging.info("data saved to fig/cn_dis.png.")

if __name__ == '__main__':
    # paper_num_along_year()
    refnum_dis()
    author_papernum_dis()
    pid_cn_dis()




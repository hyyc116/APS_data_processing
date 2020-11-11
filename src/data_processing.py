#coding:utf-8

from basic_config import *
import sys
# sys.setdefaultencoding("utf-8")

NUM_AUTHOR_DIS_PATH = 'data/author_num_dis.json'
## paper published year
PAPER_YEAR_PATH = 'data/pid_pubyear.json'
## paper teamsize 
PAPER_TEAMSIZE_PATH = 'data/pid_teamsize.json'
## paper year papers
AUTHOR_YEAR_PAPERS = 'data/author_year_papers.json'
## author total papernum
AUTHOR_PAPER_NUMS = 'data/author_papernum.json'

def list_metadata():
    for journal in os.listdir(DATA_PATH):
        for issue in os.listdir(DATA_PATH+'/'+journal):

            for article in os.listdir(DATA_PATH+'/'+journal+'/'+issue):

                if not article.endswith('json'):
                    continue

                yield DATA_PATH+'/'+journal+'/'+issue+'/'+article


def extract_author_info(article_json):
    pid = article_json['id']
    authors = article_json.get('authors','-1')
    date = article_json.get('date','-1')
    atype = article_json.get('articleType','-1')
    affiliations = article_json.get('affiliations',[])

    return pid,authors,date,atype,affiliations


def extract_from_metadata():
    author_year_papers = defaultdict(lambda:defaultdict(list))
    authornum_dis = defaultdict(int)
    author_papernum = defaultdict(int)
    paper_pubyear = {}
    paper_teamsize = {}

    progress = 0
    empty_authors = 0

    for article_path in list_metadata():
        article_json = json.loads(open(article_path,encoding='utf-8').read())
        pid,authors,date,atype,affiliations = extract_author_info(article_json)
        afid_name = {}
        for affiliation in affiliations:
            afid = affiliation['id']
            af_name = affiliation['name']
            afid_name[afid] = af_name

        ## 只计算存在作者信息、日期信息的article
        if authors=='-1' or len(authors)==0 or date =='-1' or atype!='article' or len(authors)>10:
            continue

        year = int(date.split('-')[0])

        paper_pubyear[pid] = year

        progress+=1
        if progress%10000==0:
            logging.info('progress %d ....' % progress)
            # break

        num_of_author = len(authors)

        paper_teamsize[pid] = num_of_author

        authornum_dis[num_of_author] += 1

        isNull = 0
        for author in authors:
            # logging.info(author, affiliations,afid_name
            name = author['name']

            affilids = author.get('affiliationIds',[])
            # affiliations = author.get('affiliations',[])

            ## 不存在机构数据置空
            if len(affilids)==0:
                continue

            aff_names = []
            for afid in sorted(affilids):
                aff = afid_name.get(afid,'-1')
                if aff==-1:
                    continue
                aff_names.append('_'.join(aff.replace('.','').replace(',','').lower().split()))

            if len(aff_names)==0:
                continue

            isNull+=1
            name_aff = name+'_'+'_'.join(aff_names).lower()

            author_year_papers[name_aff][year].append(pid)

            author_papernum[name_aff]+=1

        if isNull ==0:
            empty_authors+=1

    logging.info('empty authors %d' % empty_authors)
    logging.info('%d aritcles processed, %d authors reserved ...' % (progress, len(author_year_papers.keys())))

    open(AUTHOR_YEAR_PAPERS,'w').write(json.dumps(author_year_papers))
    logging.info('data saved to %s.' % AUTHOR_YEAR_PAPERS)

    open(NUM_AUTHOR_DIS_PATH,'w').write(json.dumps(authornum_dis))
    logging.info('author num dis saved to %s' % NUM_AUTHOR_DIS_PATH)

    open(PAPER_YEAR_PATH,'w').write(json.dumps(paper_pubyear))
    logging.info('paper year saved to %s' % PAPER_YEAR_PATH)

    open(PAPER_TEAMSIZE_PATH,'w').write(json.dumps(paper_teamsize))
    logging.info('paper teamsize dis saved to %s' % PAPER_TEAMSIZE_PATH)

    open(AUTHOR_PAPER_NUMS,'w').write(json.dumps(author_papernum))
    logging.info('paper teamsize dis saved to %s' % AUTHOR_PAPER_NUMS)


def gen_paper_c5():

    logging.info('loading pid year ...')

    pid_pubyear = json.loads(open(PAPER_YEAR_PATH).read())

    pid_c5 = defaultdict(int)

    pid_cn = defaultdict(int)

    pid_refnum = defaultdict(int)

    progress = 0 

    for line in open(CITATION_PATH):

        if line.startswith('citing'):
            continue

        progress+=1

        if progress%10000==0:
            logging.info(f'progress {progress} ...')

        line = line.strip()

        citing_pid,cited_pid = line.split(',')


        pid_refnum[citing_pid]+=1

        citing_year = pid_pubyear.get(citing_pid,-1)
        cited_year = pid_pubyear.get(cited_pid,-1)


        if citing_year>=2010:
            continue

        pid_cn[cited_pid]+=1

        if citing_year ==-1 or cited_year ==-1:
            continue

        if citing_year - cited_year <=5:

            pid_c5[cited_year]+=1

    open('data/pid_c5.json','w').write(json.dumps(pid_c5))
    logging.info('data saved to data/pid_c5.json')

    open('data/pid_cn.json','w').write(json.dumps(pid_cn))
    logging.info('data saved to data/pid_cn.json')

    open('data/pid_refnum.json','w').write(json.dumps(pid_refnum))
    logging.info('data saved to data/pid_refnum.json')


if __name__ == '__main__':
    # extract_from_metadata()

    gen_paper_c5()


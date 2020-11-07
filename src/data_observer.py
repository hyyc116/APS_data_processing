#coding:utf-8
'''

1. 作者数量变化规律
    
    1.1 每年新作者数量变化规律
    1.2 根据作者career的长度来拟合整体作者数量变化规律


2. 作者生产力规律

3. 价值增益率分布

'''

from basic_config import *

def author_enter_left_model():
    ## 根据author的信息计算，每年新增的学者的数量
    year_new_num = defaultdict(int)
    ## 每年不再继续研究的学者的数量
    year_end_num = defaultdict(int)
    ## 研究年龄分布比例就是年龄离开的概率
    lifespan_dis = defaultdict(int)
    ## 研究寿命与总文献数量
    lifespan_nums = defaultdict(list)
    ## 年龄与下一年的数量
    age_num = defaultdict(list)
    author_year_articles = json.loads(open(AUTHOR_JSON_PATH).read())
    ## 文章数量的
    article_num_dis = defaultdict(int)

    intervals = []
    used_au_num = 0
    out_interval = 0

    year_lifespan = defaultdict(list)

    for author in author_year_articles.keys():

        paper_years =  sorted(author_year_articles[author].keys(),key=lambda x:int(x))

        last_year = 0
        max_interval = 0
        for i,y in enumerate(paper_years):
            y = int(y)
            if i>0:
                interval = y - last_year
                # if interval >1:

                if interval > max_interval:
                    max_interval = interval

            last_year = y

        if max_interval>0:
            intervals.append(max_interval)

        if max_interval>10:
            out_interval+=1
            continue

        used_au_num +=1

        # print paper_years
        article_num = 0
        for i,year in enumerate(paper_years):
            anum=len(author_year_articles[author][year])
            article_num +=anum
            age_num[i].append(anum)

        lifespan = int(paper_years[-1])-int(paper_years[0])+1

        year_lifespan[int(paper_years[0])].append(lifespan)

        lifespan_dis[lifespan]+=1

        lifespan_nums[lifespan].append(article_num)

        article_num_dis[article_num]+=1

        startYear = int(paper_years[0])
        endYear = int(paper_years[-1])

        year_new_num[startYear]+=1
        year_end_num[endYear]+=1

    ## 每年各个比例
    left_percent = defaultdict(list)
    years = []

    ## 统计1980-2006之间的均值
    _year_left = defaultdict(list)
    _year_percents = defaultdict(list)
    for year in sorted(year_lifespan.keys()):
        if year > 2006:
            continue
        ta = float(len(year_lifespan[year]))
        lifespans = Counter(year_lifespan[year])
        years.append(year)
        for lifespan in range(1,11):
            percent = lifespans.get(lifespan,0)/ta

            left_percent[lifespan].append(percent)

        if year>1980 and year <= 2006:
            for lifespan in sorted(lifespans.keys()):
                _year_left[year].append(lifespan)
                _year_percents[year].append(lifespans[lifespan])

    fig,ax1 = plt.subplots(figsize=(5,4))

    ## 计算均值
    _left_avgs = defaultdict(list)
    for year in sorted(_year_left.keys()):

        _left = _year_left[year]
        _percents = _year_percents[year]

        for i,l in enumerate(_left):

            _left_avgs[l].append(_percents[i])


        ax1.plot(_left,np.array(_percents)/float(np.sum(_percents)),'^',mec='#D2D2D2',mew=0.5)

    avg_xs = []
    avg_ys = []

    for _l in sorted(_left_avgs.keys()):
        avg_xs.append(_l)
        avg_ys.append(np.mean(_left_avgs[_l]))

    ax1.plot(avg_xs,np.array(avg_ys)/np.sum(avg_ys),'-.',linewidth=3,label=u'均值',c='r')

    # ax1.plot([10]*10,np.linspace(0.0001,1,10),'--',linewidth=0.5)

    ax1.set_xlabel(u'研究周期(年)',fontproperties='SimHei')
    ax1.set_ylabel(u'$p_{rs}(k)$')
    ax1.set_yscale('log')
    # ax1.set_xscale('log')

    # _2000_cd = []
    # _2000_cont = []
    # _2000_ta = float(np.sum(_2000_percents))
    # _2000_tp = 0
    # last_cont = 1
    # for i,p in enumerate(_2000_percents):
    #     _2000_tp+=p
    #     _2000_cd.append(_2000_tp/_2000_ta)
    #     cont = (1-_2000_tp/_2000_ta)/last_cont
    #     _2000_cont.append(cont)
    #     last_cont = cont

    # ###P_c先不画
    # print _2000_cont
    # # l3 = ax1.plot(_2000_left,_2000_cont,'-s',label='$P_c(s_i,t)$',mec='#D2D2D2',mew=0.5)

    # ax2 = ax1.twinx()
    # l2 = ax2.plot(_2000_left, _2000_cd,'-o',c='r',label='离开概率',mec='#D2D2D2',mew=0.5)
    # ax2.set_ylabel('$P_l(t)$', color='r')
    # ax2.tick_params('y', colors='r')
    # # lns = l1+l3+l2
    # lns = l1+l2

    # labels = [l.get_label() for l in lns]
    plt.legend(prop={'family':'SimHei','size':8},loc=8)


    plt.tight_layout()

    plt.savefig('fig/_avg_left_dis.pdf',dpi=800)

    print 'year 2000 savd to fig/_avg_left_dis.pdf'

    ### 对密度概率分布进行拟合
    fig,ax = plt.subplots(figsize=(5,4))
    _ALL_SPANS = []

    for y in range(1980,2000):
        _ALL_SPANS.extend([l for l in year_lifespan[y]])
    xs = avg_xs
    ys = np.array(avg_ys)/float(np.sum(avg_ys))
    print xs
    print ys
    l1=ax.plot(xs,ys,'-o',label='研究周期',mec='#D2D2D2',mew=0.5)
    fit=powerlaw.Fit(_ALL_SPANS,discrete=True,xmin=2)
    alpha = fit.power_law.alpha
    print 'xmin\t=',fit.xmin
    print 'alpha\t=',fit.power_law.alpha
    print 'sigma\t=',fit.power_law.sigma
    # fit.plot_pdf(ax=ax)
    # fit.power_law.plot_pdf(linestyle='--',c='r',label=u'拟合曲线',ax=ax)
    ax.set_xlabel(u'研究周期',fontproperties='SimHei')
    ax.set_ylabel(u'$p_{rs}(k)$')
    # ax.set_xscale('log')
    ax.set_yscale('log')

    pl_func = lambda t,a:a*t**(-alpha)

    # popt, pcov = scipy.optimize.curve_fit(powlaw,xs[:10],ys[:10],p0=(0.8,2.0))
    # fit_Y =  [powlaw(x,*popt) for x in xs]
    # l2=ax.plot(xs[:],fit_Y[:],'--',label=u'拟合曲线 $p_{rs}(t) = %.2f*t^{-%.2f}$ \n$t_{min}=3$' % (popt[0],popt[1]))

    # print popt

    popt, pcov = scipy.optimize.curve_fit(pl_func,xs[1:],ys[1:],p0=(0.8))
    fit_Y =  [pl_func(x,*popt) for x in xs]

    print popt
    l2=ax.plot(xs[:],fit_Y[:],'--',label=u'拟合曲线 $p_{rs}(k) = %.2f*k^{-%.2f}$' % (popt[0],alpha))

    # def poisson(k, lamb):
        # return (lamb**k/factorial(k)) * np.exp(-lamb)

    # parameters, cov_matrix = scipy.optimize.curve_fit(poisson, xs, ys[:10])

    # l3=ax.plot(xs,poisson(xs,*parameters),'--',label=u'泊松分布')


    ##保存一张图片对研究周期分布的拟合

    # lns = l1+l2
    # labels = [l.get_label() for l in lns]
    plt.legend(prop={'family':'SimHei','size':8})
    plt.tight_layout()
    plt.savefig('fig/left_fit.pdf',dpi=800)

    print 'left prop saved to fig/left_fit.pdf.'

    ### 以拟合曲线进行离开概率的模拟
    ## 模拟四十年的周期, 这里存在后面的和大于1的问题，目前只模拟到10年
    fit_X = range(1,41)
    fit_Y =  [pl_func(x,*popt) for x in fit_X]
    fig,ax1 = plt.subplots(figsize=(5,4))
    real_Y = []
    real_Y.extend(ys[:1])
    real_Y.extend(fit_Y[1:])

    real_Y = np.array(real_Y)/np.sum(real_Y)

    ### 保存x和y

    age_dis = {}

    age_dis['x'] = fit_X
    age_dis['y'] = list(real_Y)

    open('a_rs_dis.json','w').write(json.dumps(age_dis))

    print 'powlaw saved to a_rs_dis.json'

    acc_Y = np.array([np.sum(real_Y[:i+1]) for i in range(len(real_Y))])

    ccdf_Y = 1- acc_Y

    pcts = []
    lpct = 1
    for i,cy in enumerate(ccdf_Y):
        # print cy,lpct
        pct = cy/lpct
        pcts.append(pct)
        lpct = cy
    print pcts

    l2=ax1.plot(fit_X[:-1],ccdf_Y[:-1],label=u'$P_c(k)$',c='r')
    l1 = ax1.plot(fit_X[:-1],pcts[:-1],'--',label='$p_c(s_i|k)$')

    ax1.set_ylabel(u'$p$', fontproperties='SimHei')
    # ax1.set_yscale('log')
    ax1.set_xlabel(u'$k$',fontproperties='SimHei')

    print popt
    lns = l1+l2
    labels = [l.get_label() for l in lns]
    plt.legend(lns,labels,prop={'family':'SimHei','size':8})
    plt.tight_layout()
    plt.savefig('fig/continue_fit.pdf',dpi=800)

    print 'left prop saved to fig/continue_fit.pdf.'


    plt.figure(figsize=(5,4))
    for left in sorted(left_percent.keys()):
        percents = left_percent[left]

        ## moving average
        percents = np.convolve(percents, np.ones((10,))/10, mode='valid')

        plt.plot(years[9:],percents,label='k={:}'.format(left))

    plt.plot([1980]*10,np.linspace(0.001,1,10),'--',linewidth=0.5,c='r')

    plt.xlabel(u'$t$',fontproperties='SimHei')
    plt.ylabel('$p_{rs}(k|t)$')
    plt.yscale('log')

    art = plt.legend(prop={'family':'SimHei','size':8},loc=9,bbox_to_anchor=(0.5, -0.15), ncol=5)

    plt.tight_layout()

    plt.savefig('fig/left_percentage.pdf',dpi=800,additional_artists=[art],bbox_inches="tight")

    print 'author left probability saved to left_percentage.pdf '


    print 'author used %d, out interval %d' % (used_au_num,out_interval)

    plt.figure(figsize=(5,4))

    xs =[]
    ys =[]
    t=0
    ic = Counter(intervals)
    for n in sorted(ic.keys()):
        xs.append(n)
        if n==10:
            t1=t
        t+=ic.get(n)
        ys.append(t)


    print t
    ys = np.array(ys)/float(t)

    plt.plot(xs,ys)
    plt.xlabel(u'论文发表间隔(年)',fontproperties='SimHei')
    plt.ylabel(u'累积概率',fontproperties='SimHei')
    plt.plot([10]*10,np.linspace(0.5,1,10),'--',c='r')
    # plt.text(10,0.9,'97%')
    plt.text(11, 0.95, str('(10, {:.1%})'.format(t1/float(t))))
    # plt.arrow(12,0.9,-2,t1/float(t)-0.9, head_width=0.05, head_length=0.2, fc='k', ec='k')
    # plt.yscale('log')

    params = {'legend.fontsize': 5,
        'axes.labelsize': 5,
        'axes.titlesize':5,
        'xtick.labelsize':5,
        'ytick.labelsize':5}

    pylab.rcParams.update(params)
    a = plt.axes([.6, .2, .35, .35])

    plt.hist(intervals,33,rwidth=0.5,density=True)
    mean = np.mean(intervals)
    median = np.median(intervals)

    # print matplotlib.matplotlib_fname()
    print mean,median
    plt.title(u'密度曲线', fontproperties='SimHei')

    # plt.xlabel(u'发表间隔(年)', fontproperties='SimHei')
    # plt.ylabel(u'比例', fontproperties='SimHei')
    plt.yscale('log')

    plt.tight_layout()
    plt.savefig('fig/interval.pdf',dpi=800)
    print 'interval distribution saved to fig/interval.pdf'
    # plt.legend(prop={'family':'SimHei','size':15})
    # return

    params = {'legend.fontsize': 10,
        'axes.labelsize': 10,
        'axes.titlesize':15,
        'xtick.labelsize':10,
        'ytick.labelsize':10}

    pylab.rcParams.update(params)

    ### 根据这个时间画图
    print 'plot year related num figure ...'
    years = []
    news = []
    ends = []
    total = 0
    tlist = []
    for year in sorted(year_new_num.keys()):

        if year>2006:
            continue

        years.append(year)

        new_num = year_new_num[year]
        end_num = year_end_num.get(year,0)

        # print year,total,new_num,end_num

        total+=new_num-end_num

        tlist.append(total)
        news.append(new_num)
        ends.append(end_num)

    plt.figure(figsize=(5,4))
    plt.plot(years,news,label=u'新作者数')
    plt.plot(years,ends,'--',label=u'离开作者数')
    plt.plot(years,tlist,label=u'剩余作者总数')
    plt.legend(prop={'family':'SimHei','size':10})

    plt.xlabel('年份',fontproperties='SimHei')
    plt.ylabel('作者数量',fontproperties='SimHei')
    plt.yscale('log')


    # plt.legend()
    plt.tight_layout()
    plt.savefig('fig/author_num.pdf',dpi=800)

    ### 作者数量拟合 news
    plt.figure(figsize=(5,4))

    # ts = np.array(years)-years[0]+1
    ts = np.array(years)-years[0]+1
    print news[0]

    plt.plot(ts,news,'o',mec='#D2D2D2',mew=0.5,label=u'新作者数')
    # print
    ## 使用指数函数进行拟合
    expfunc = lambda t,a,b:news[0]*a*np.exp(b*t)
    popt, pcov = scipy.optimize.curve_fit(expfunc,ts,news,p0=(2,0.01))

    fit_Y = [expfunc(t,*popt) for t in ts ]

    print ts[:10]
    print fit_Y[:10]
    print 'exponential:',popt

    plt.plot(ts,fit_Y,'--',label=u'拟合曲线 $s_n(t) = s_0*%.2f*e^{%.2ft}$'%(popt[0],popt[1]),c='r')

    plt.xlabel(u'年份$t$',fontproperties='SimHei')
    plt.ylabel(u'新作者数量$s_n(t)$',fontproperties='SimHei')
    plt.legend(prop={'family':'SimHei','size':8})
    plt.yscale('log')
    plt.tight_layout()

    plt.savefig('fig/author_num_fit.pdf',dpi=800)

    print 'fiting author num figure saved to fig/author_num_fit.pdf'



    return
    ### lifespan的图
    print 'plot lifespan related figure ...'
    xs = []
    ys = []
    nums = []
    for lifespan in sorted(lifespan_dis.keys()):
        xs.append(lifespan)
        ys.append(lifespan_dis[lifespan])
        nums.append(lifespan_nums[lifespan])

    ages = []
    anums = []

    for age in sorted(age_num.keys()):
        ages.append(age)
        anums.append(age_num[age])


    fig,axes = plt.subplots(6,1,figsize=(6,30))

    ## 研究寿命分布的关系
    ax0 = axes[0]

    ax0.plot(xs,ys)
    ax0.set_xlabel('lifespan')
    ax0.set_ylabel('number of authors')
    ax0.set_yscale('log')
    ax0.set_xscale('log')


    ax1 = axes[1]
    ys = []
    for i,num in enumerate(nums):

        ys.append(np.mean(num))

        ax1.scatter([xs[i]]*len(num),num)

    ax1.plot(xs,ys)

    ax1.set_xlabel('lifespan')
    ax1.set_ylabel('number of papers')

    ax2 = axes[2]
    ax5 = axes[4]
    ax6 = axes[5]
    ys = []
    for i,num in enumerate(anums):
        ax2.scatter([ages[i]]*len(num),num)
        ys.append(np.mean(num))

        if i==0:
            ax5.hist(num,10)
        elif i==5:
            ax6.hist(num,10)


    ax2.set_xlabel('age')
    ax2.plot(ages,ys)
    ax2.set_ylabel('number of papers')

    ax3 = axes[3]

    xs = []
    ys = []

    for an in sorted(article_num_dis.keys()):
        xs.append(an)
        ys.append(article_num_dis[an])

    ax3.plot(xs,ys)
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.set_xlabel('number of article')
    ax3.set_ylabel('number of authors')


    plt.tight_layout()
    plt.savefig('fig/lifespan_num.pdf',dpi=800)

    print 'done'


def author_changing_rules():


    pass



